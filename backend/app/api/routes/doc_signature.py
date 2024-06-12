import logging
import random
import base64
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from app.api.deps import SessionDep
from app.crud import audit_log_crud, signed_document_crud, signatory_crud
from app.models.models import (
    AuditLogAction,
    Document,
    DocumentStatus,
    Signatory,
    SignatureRequest,
    SignatureRequestStatus,
)
from app.schemas.schemas import AuditLogCreate, DocumentSignatureDetailsCreate, SignatoryUpdate
from app.services.file_service import (
    add_fields_to_pdf,
    apply_pdf_security,
    generate_pdf_hash,
    send_otp_code,
    verify_secure_link_token,
)
from app.services.file_utils import convert_pdf_to_images
from app.utils import send_signature_request_notification_email

templates = Jinja2Templates(directory="signature-templates")
logger = logging.getLogger(__name__)
router = APIRouter()

SIGNATURES_DIR = Path("/app/static/signatures")
SIGNATURES_DIR.mkdir(parents=True, exist_ok=True)

otp_store = {}
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
    require_otp = payload.get("require_otp")

    if document_ids is None:
        raise HTTPException(status_code=400, detail="No document id in the payload")
    if email is None:
        raise HTTPException(status_code=400, detail="No email in the payload")
    if signatory_id is None:
        raise HTTPException(status_code=400, detail="No signatory id in the payload")
    if signature_request_id is None:
        raise HTTPException(
            status_code=400, detail="No signature_request id in the payload"
        )
    if require_otp is None:
        raise HTTPException(status_code=400, detail="No require_otp id in the payload")

    signature_request_statement = select(SignatureRequest).where(
        SignatureRequest.id == int(signature_request_id)
    )
    signature_request = session.exec(signature_request_statement).first()
    if not signature_request:
        raise HTTPException(
            status_code=404, detail="Signature request not found"
        )
    if signature_request.status in [SignatureRequestStatus.COMPLETED, SignatureRequestStatus.CANCELED]:
        if signature_request.status == SignatureRequestStatus.COMPLETED:
            return RedirectResponse(url="/api/v1/signe/signature_completed")
        elif signature_request.status == SignatureRequestStatus.CANCELED:
            return RedirectResponse(url="/api/v1/signe/signature_canceled")

    document_urls = []
    for document_id in document_ids:
        document_statement = select(Document).where(Document.id == int(document_id))
        document = session.exec(document_statement).first()
        if document is None:
            raise HTTPException(
                status_code=404,
                detail="No Document corresponding to the payload document id",
            )
        folder_name = f"{document.owner_id}_{document.title}"
        image_folder = STATIC_FILES_DIR / folder_name

        if not image_folder.exists():
            convert_pdf_to_images(
                STATIC_FILES_DIR / f"{document.file}", image_folder
            )

        # Ensure the images are already converted and available

        image_urls = [
            f"/api/v1/static/document_files/{document.owner_id}_{document.title}/page_{i}.png"
            for i in range(1, len(list(image_folder.glob("*.png"))) + 1)
        ]
        document_urls.append(image_urls)

        if document.status != DocumentStatus.VIEWED:
            document.status = DocumentStatus.VIEWED
            session.add(document)
            session.commit()
            session.refresh(document)

        audit_log_crud.create_audit_log(
            session,
            AuditLogCreate(
                description="Document viewed",
                ip_address=request.client.host,
                action=AuditLogAction.DOCUMENT_VIEWED,
                signature_request_id=signature_request_id,
            ),
        )

        send_signature_request_notification_email(
            signature_request.sender.email,
            signature_request.name,
            signature_request.id,
            signature_request.status.value,
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
            "require_otp": require_otp,
        },
    )


@router.post("/send_otp", response_class=JSONResponse)
def send_otp(
    request: Request,
    session: SessionDep,
    email: str = Form(...),
    signature_request_id: int = Form(...),
):
    otp = random.randint(100000, 999999)
    expiry_time = datetime.now() + timedelta(minutes=30)
    otp_store[email] = {"otp": otp, "expires": expiry_time}
    if not send_otp_code(email, otp):
        raise HTTPException(status_code=500, detail="Failed to send OTP")

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
    otp: Optional[int] = Form(None),
    signature_request_id: int = Form(...),
):
    signature_request = session.get(SignatureRequest, signature_request_id)
    if not signature_request:
        raise HTTPException(status_code=404, detail="Signature request not found")

    if signature_request.require_otp:
        if email not in otp_store:
            raise HTTPException(status_code=400, detail="OTP not found")
        otp_data = otp_store[email]
        if otp_data["expires"] < datetime.now():
            del otp_store[email]
            raise HTTPException(status_code=400, detail="OTP expired")
        if otp_data["otp"] != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        del otp_store[email]

        audit_log_crud.create_audit_log(
            session,
            AuditLogCreate(
                description="OTP verified",
                ip_address=request.client.host,
                action=AuditLogAction.DOCUMENT_SIGNED,
                signature_request_id=signature_request_id,
            ),
        )

    signature_request.status = SignatureRequestStatus.COMPLETED
    session.commit()

    for document in signature_request.documents:
        document.status = DocumentStatus.SIGNED
        session.commit()

        final_pdf_path = (
            STATIC_FILES_DIR
            / "signed_documents"
            / f"{document.file}"
        )
        for signatory in signature_request.signatories:
            for field in signatory.fields:
                if field.document_id == document.id:
                    add_fields_to_pdf(
                        document.file, field, signatory, document.owner_id
                    )
        apply_pdf_security(str(final_pdf_path))

        pdf_hash = generate_pdf_hash(str(final_pdf_path))
        logger.info(f"Generated hash for document {document.id}: {pdf_hash}")

        document_signature_details = DocumentSignatureDetailsCreate(
            document_id=document.id,
            signed_hash=pdf_hash,
            timestamp=datetime.now(),
            ip_address=request.client.host,
        )
        signed_document_crud.create_document_signature_details(
            session, document_signature_details
        )

    signed_documents = [final_pdf_path for document in signature_request.documents]
    recipients = [signature_request.sender.email] + [
        signatory.email for signatory in signature_request.signatories
    ]
    for recipient in recipients:
        send_signature_request_notification_email(
            email_to=recipient,
            signature_request_name=signature_request.name,
            signature_request_id=signature_request_id,
            status=signature_request.status.value,
            documents=signed_documents,
        )

    return JSONResponse(content={"message": "Document successfully signed!"})


@router.get("/success", response_class=HTMLResponse)
def signature_success(request: Request):
    return templates.TemplateResponse(
        "main_pages/signature_success.html",
        {"request": request, "message": "Document successfully signed!"}
    )


@router.post("/save_signature", response_class=JSONResponse)
def save_signature(
    request: Request,
    session: SessionDep,
    email: str = Form(...),
    signature_request_id: int = Form(...),
    signature_image: str = Form(...),
):
    signatory = session.exec(select(Signatory).where(Signatory.email == email)).first()
    if not signatory:
        raise HTTPException(status_code=404, detail="Signatory not found")

    # Decode the base64 image
    image_data = base64.b64decode(signature_image.split(",")[1])
    signature_path = SIGNATURES_DIR / f"{signatory.id}.png"

    # Save the image
    with open(signature_path, "wb") as f:
        f.write(image_data)

    # Update the signatory with the path to the signature image
    signatory_update = SignatoryUpdate(signature_image=str(signature_path))
    signatory_crud.update_signatory(session, signatory.id, signatory_update)

    return JSONResponse(content={"message": "Signature saved successfully"})


@router.get("/signature_completed", response_class=HTMLResponse)
def signature_completed(request: Request):
    return templates.TemplateResponse("main_pages/signature_completed.html", {"request": request})


@router.get("/signature_canceled", response_class=HTMLResponse)
def signature_canceled(request: Request):
    return templates.TemplateResponse("main_pages/signature_canceled.html", {"request": request})
