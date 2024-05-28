import logging
import random
from datetime import datetime, timedelta
from pathlib import Path

from sqlmodel import select

from fastapi import APIRouter, HTTPException, Query, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.api.deps import SessionDep
from app.models.models import (
    Document,
    DocumentStatus,
    Signatory,
    AuditLogAction,
    SignatureRequest,
    SignatureRequestStatus,
)
from app.services.file_service import (
    verify_secure_link_token,
    send_otp_code,
)
from app.crud import audit_log_crud
from app.schemas.schemas import AuditLogCreate

templates = Jinja2Templates(directory="signature-templates")
logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory store for OTPs
otp_store = {}
# Define the base directory for the static files
STATIC_FILES_DIR = Path("/app/static/document_files")


@router.get("/sign_document", response_class=HTMLResponse)
def access_document_with_token(
    *, session: SessionDep, token: str = Query(...), request: Request
):
    payload = verify_secure_link_token(token)
    if payload is None:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    document_ids = payload.get("document_ids")
    email = payload.get("sub")
    signatory_id = payload.get("signatory_id")
    signature_request_id = payload.get("signature_request_id")
    if document_ids is None:
        raise HTTPException(status_code=400, detail="No document id in the payload")
    if email is None:
        raise HTTPException(status_code=400, detail="No email in the payload")
    if signatory_id is None:
        raise HTTPException(status_code=400, detail="No signatory id in the payload")
    if signature_request_id is None:
        raise HTTPException(status_code=400, detail="No signature_request id in the payload")

    document_urls = []
    for document_id in document_ids:
        document_statement = select(Document).where(Document.id == int(document_id))
        document = session.exec(document_statement).first()
        if document is None:
            raise HTTPException(
                status_code=404,
                detail="No Document corresponding to the payload document id",
            )
        file_path = STATIC_FILES_DIR / f"{document.owner_id}_{document.file}"
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        document_urls.append(f"document_files/{document.owner_id}_{document.file}")

        # Update the document status to VIEWED
        if document.status != DocumentStatus.VIEWED:
            document.status = DocumentStatus.VIEWED
            session.add(document)
            session.commit()
            session.refresh(document)

        # Create an audit log for viewing the document
        audit_log_crud.create_audit_log(
            session,
            AuditLogCreate(
                description="Document viewed",
                ip_address=request.client.host,
                action=AuditLogAction.DOCUMENT_VIEWED,
                signature_request_id=signature_request_id,
            ),
        )

    signatory_statement = select(Signatory).where(Signatory.id == int(signatory_id))
    signatory = session.exec(signatory_statement).first()

    return templates.TemplateResponse(
        "main_pages/signature.html",
        {
            "request": request,
            "document_urls": document_urls,
            "first_name": signatory.first_name,
            "last_name": signatory.last_name,
            "email": signatory.email,
            "phone_number": signatory.phone_number,
            "signature_request_id": signature_request_id,
        },
    )


@router.post("/send_otp", response_class=JSONResponse)
def send_otp(
    request: Request, session: SessionDep, email: str = Form(...), signature_request_id: int = Form(...)
):
    otp = random.randint(100000, 999999)
    expiry_time = datetime.now() + timedelta(minutes=30)
    otp_store[email] = {"otp": otp, "expires": expiry_time}
    if not send_otp_code(email, otp):
        raise HTTPException(status_code=500, detail="Failed to send OTP")

    # Create an audit log for sending OTP
    audit_log_crud.create_audit_log(
        session,
        AuditLogCreate(
            description="OTP sent",
            ip_address=request.client.host,
            action=AuditLogAction.SIGNATURE_REQUESTED,
            signature_request_id=signature_request_id,
            document_id=None,
        ),
    )

    return JSONResponse(content={"message": "OTP sent successfully"})


@router.post("/verify_otp", response_class=JSONResponse)
def verify_otp(
    request: Request,
    session: SessionDep,
    email: str = Form(...),
    otp: int = Form(...),
    signature_request_id: int = Form(...)
):
    if email not in otp_store:
        raise HTTPException(status_code=400, detail="OTP not found")
    otp_data = otp_store[email]
    if otp_data["expires"] < datetime.now():
        del otp_store[email]
        raise HTTPException(status_code=400, detail="OTP expired")
    if otp_data["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    del otp_store[email]

    # Create an audit log for verifying OTP
    audit_log_crud.create_audit_log(
        session,
        AuditLogCreate(
            description="OTP verified",
            ip_address=request.client.host,
            action=AuditLogAction.DOCUMENT_SIGNED,
            signature_request_id=signature_request_id,
            document_id=None,
        ),
    )

    # Update the signature request status to COMPLETED
    signature_request = session.get(SignatureRequest, signature_request_id)
    if not signature_request:
        raise HTTPException(status_code=404, detail="Signature request not found")

    signature_request.status = SignatureRequestStatus.COMPLETED
    session.add(signature_request)
    session.commit()
    session.refresh(signature_request)

    # Perform signing logic here (if any)

    return JSONResponse(content={"message": "OTP verified and signature request completed successfully"})
