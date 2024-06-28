import base64
import logging
import random
from datetime import datetime, timedelta
from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from app.api.deps import SessionDep
from app.crud import audit_log_crud, signatory_crud
from app.models.models import (
    AuditLogAction,
    Document,
    DocumentStatus,
    RequestSignatoryLink,
    Signatory,
    SignatureRequest,
    SignatureRequestStatus,
)
from app.schemas.schemas import AuditLogCreate, SignatoryUpdate
from app.services.file_service import (
    all_signatories_signed,
    finalize_document,
    get_signatory,
    get_signature_request,
    log_otp_verification,
    process_signatory_signature,
    send_final_notifications,
    send_next_ordered_signatory_email,
    send_otp_code,
    send_remaining_signatories_email,
    verify_otp_code,
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
    """
    Access document with a secure token and render the signing page.

    Args:
        session (Session): Database session dependency.
        token (str): Secure token for accessing the document.
        request (Request): FastAPI request object.

    Returns:
        HTMLResponse: Renders the signing page template.

    Raises:
        HTTPException: Various cases of invalid or expired token, missing data in payload, etc.
    """
    payload = verify_secure_link_token(token)
    if payload is None:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    document_ids = payload.get("document_ids")
    email = payload.get("sub")
    signatory_id = payload.get("signatory_id")
    signature_request_id = payload.get("signature_request_id")
    require_otp = payload.get("require_otp")

    # Validate payload data
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

    # Fetch the signature request
    signature_request_statement = select(SignatureRequest).where(
        SignatureRequest.id == int(signature_request_id)
    )
    signature_request = session.exec(signature_request_statement).first()
    if not signature_request:
        raise HTTPException(status_code=404, detail="Signature request not found")
    if signature_request.status in [
        SignatureRequestStatus.COMPLETED,
        SignatureRequestStatus.CANCELED,
    ]:
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
            convert_pdf_to_images(STATIC_FILES_DIR / f"{document.file}", image_folder)

        # Ensure the images are already converted and available
        image_urls = [
            f"/api/v1/static/document_files/{document.owner_id}_{document.title}/page_{i}.png"
            for i in range(1, len(list(image_folder.glob("*.png"))) + 1)
        ]
        document_urls.append(image_urls)

        # Update document status to VIEWED if not already
        if document.status != DocumentStatus.VIEWED:
            document.status = DocumentStatus.VIEWED
            session.add(document)
            session.commit()
            session.refresh(document)

        # Log the document view
        audit_log_crud.create_audit_log(
            session,
            AuditLogCreate(
                description="Document viewed",
                ip_address=request.client.host,
                action=AuditLogAction.DOCUMENT_VIEWED,
                signature_request_id=signature_request_id,
            ),
        )

        # Send notification email
        send_signature_request_notification_email(
            signature_request.sender.email,
            signature_request.name,
            signature_request.id,
            signature_request.status.value,
        )

    # Fetch the signatory
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
    otp: int | None = Form(None),
    signature_request_id: int = Form(...),
):
    """
    Verify the OTP for a signatory and handle the signing process.
    """
    logger.info("Starting OTP verification process")

    signature_request = get_signature_request(session, signature_request_id)
    signatory = get_signatory(session, email, signature_request_id)
    static_files_dir = STATIC_FILES_DIR

    if signature_request.require_otp:
        logger.info(f"Verifying OTP for {email}")
        verify_otp_code(email, otp, otp_store)
        log_otp_verification(
            session, request.client.host, signature_request_id, signatory.id
        )

    logger.info(f"Processing signature for signatory {signatory.id}")
    process_signatory_signature(
        session, signatory, signature_request, request.client.host, static_files_dir
    )

    if all_signatories_signed(signature_request.signatories):
        logger.info("All signatories have signed. Finalizing document.")
        finalize_document(
            session, signature_request, request.client.host, static_files_dir
        )
        send_final_notifications(signature_request, static_files_dir)
    else:
        if signature_request.ordered_signers:
            logger.info("Signatories are ordered. Sending email to next signatory.")
            send_next_ordered_signatory_email(signature_request, session, request)
        else:
            logger.info(
                "Signatories are not ordered. Sending email to remaining signatories."
            )
            send_remaining_signatories_email(signature_request, session, request)

    logger.info("OTP verification and signing process completed successfully")
    return JSONResponse(content={"message": "Document successfully signed!"})


@router.get("/success", response_class=HTMLResponse)
def signature_success(request: Request):
    return templates.TemplateResponse(
        "main_pages/signature_success.html",
        {"request": request, "message": "Document successfully signed!"},
    )


@router.post("/save_signature", response_class=JSONResponse)
def save_signature(
    request: Request,
    session: SessionDep,
    signature_request_id: int = Form(...),
    email: str = Form(...),
    signature_image: str = Form(...),
):
    signatory = session.exec(
        select(Signatory)
        .where(Signatory.email == email)
        .join(RequestSignatoryLink)
        .where(RequestSignatoryLink.signature_request_id == signature_request_id)
    ).first()

    if not signatory:
        raise HTTPException(
            status_code=404,
            detail="Signatory not found or not associated with the given signature request",
        )

    # Decode the base64 image
    image_data = base64.b64decode(signature_image.split(",")[1])
    signature_path = SIGNATURES_DIR / f"{signature_request_id}_{signatory.id}.png"

    # Save the image
    with open(signature_path, "wb") as f:
        f.write(image_data)

    # Update the signatory with the path to the signature image
    signatory_update = SignatoryUpdate(signature_image=str(signature_path))
    signatory_crud.update_signatory(session, signatory.id, signatory_update)

    return JSONResponse(content={"message": "Signature saved successfully"})


@router.get("/signature_completed", response_class=HTMLResponse)
def signature_completed(request: Request):
    return templates.TemplateResponse(
        "main_pages/signature_completed.html", {"request": request}
    )


@router.get("/signature_canceled", response_class=HTMLResponse)
def signature_canceled(request: Request):
    return templates.TemplateResponse(
        "main_pages/signature_canceled.html", {"request": request}
    )
