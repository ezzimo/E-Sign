import logging
import sys
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from app.api.deps import get_current_user, get_db
from app.crud import audit_log_crud
from app.crud.signature_request_crud import (
    create_signature_request,
    delete_signature_request,
    get_all_signature_requests,
    get_signatories_by_signature_request,
    get_signature_request,
    get_signature_requests_by_document,
    update_signature_request,
)
from app.models.models import (
    AuditLogAction,
    Document,
    DocumentStatus,
    Signatory,
    SignatureRequestStatus,
    User,
)
from app.schemas.schemas import (
    AuditLogCreate,
    DocumentOut,
    ReminderSettingsSchema,
    SignatoryOut,
    SignatureRequestCreate,
    SignatureRequestRead,
    SignatureRequestUpdate,
)
from app.services.file_service import (
    generate_secure_link,
    handle_multiple_signatories,
    handle_single_signatory,
)
from app.utils import send_signature_request_email

# Create a logger for your application
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

router = APIRouter()
STATIC_FILES_DIR = Path("/app/static/document_files")


@router.get("/", response_model=list[SignatureRequestRead])
def list_signature_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all signature requests for the admin or the current user.
    """
    signature_requests = get_all_signature_requests(db=db, current_user=current_user)
    return signature_requests


@router.post(
    "/", response_model=SignatureRequestRead, status_code=status.HTTP_201_CREATED
)
def initiate_signature_request(
    request: Request,
    signature_request: SignatureRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Initiate a new signature request.
    """
    if len(signature_request.signatories) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one signatory is required.",
        )

    signature_request_data = create_signature_request(
        db=db, request_data=signature_request, sender_id=current_user.id
    )

    if len(signature_request.signatories) == 1:
        handle_single_signatory(signature_request_data, db, request)
    else:
        handle_multiple_signatories(signature_request_data, db, request)

    # When loading documents, include necessary joins or subqueries:
    documents = db.exec(
        select(Document).where(
            Document.id.in_([doc.id for doc in signature_request_data.documents])
        )
    ).all()

    # Do similar for signatories:
    signatories = db.exec(
        select(Signatory).where(
            Signatory.id.in_([sig.id for sig in signature_request_data.signatories])
        )
    ).all()

    # Create a response object with the appropriate structure
    response_data = SignatureRequestRead(
        id=signature_request_data.id,
        sender_id=signature_request_data.sender_id,
        created_at=signature_request_data.created_at,
        updated_at=signature_request_data.updated_at,
        status=signature_request_data.status,
        name=signature_request_data.name,
        delivery_mode=signature_request_data.delivery_mode,
        ordered_signers=signature_request_data.ordered_signers,
        reminder_settings=(
            ReminderSettingsSchema.model_validate(
                signature_request_data.reminder_settings
            )
            if signature_request_data.reminder_settings
            else None
        ),
        expiry_date=signature_request_data.expiry_date,
        message=signature_request_data.message,
        token=signature_request_data.token,
        documents=[DocumentOut.model_validate(doc) for doc in documents],
        signatories=[SignatoryOut.model_validate(sig) for sig in signatories],
    )

    return response_data


@router.get("/{request_id}", response_model=SignatureRequestRead)
def read_request(request_id: int, db: Session = Depends(get_db)):
    """
    Get a signature request by ID.
    """
    db_request = get_signature_request(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Signature request not found")
    return db_request


@router.get("/document/{document_id}", response_model=list[SignatureRequestRead])
def read_requests_by_document(document_id: int, db: Session = Depends(get_db)):
    """
    Get all signature requests for a specific document.
    """
    requests = get_signature_requests_by_document(db=db, document_id=document_id)
    return requests


@router.put("/{request_id}", response_model=SignatureRequestRead)
def update_request(
    request_id: int,
    signature_request: SignatureRequestUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a signature request.
    """
    db_request = get_signature_request(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Signature request not found")
    updated_request = update_signature_request(
        db=db, db_obj=db_request, obj_in=signature_request
    )
    return updated_request


@router.delete("/{request_id}", response_model=dict)
def delete_request(request_id: int, db: Session = Depends(get_db)):
    """
    Delete a signature request.
    """
    db_request = get_signature_request(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Signature request not found")
    delete_signature_request(db=db, request_id=request_id)
    return {"message": "Signature request deleted successfully"}


@router.get(
    "/signature-request/{request_id}/signers", response_model=list[SignatoryOut]
)
def list_signature_request_signers(request_id: int, db: Session = Depends(get_db)):
    """
    List all signatories for a specific signature request.
    """
    signatories = get_signatories_by_signature_request(db, request_id)
    if not signatories:
        raise HTTPException(
            status_code=404, detail="No signatories found for this signature request."
        )
    return signatories


@router.get(
    "/{signature_request_id}/documents/{document_id}/download",
    response_class=FileResponse,
)
async def download_signed_document(
    signature_request_id: int, document_id: int, db: Session = Depends(get_db)
):
    # Verify if the document is associated with the signature request and is signed
    document = db.exec(
        select(Document).where(
            Document.id == document_id,
            Document.signature_requests.any(id=signature_request_id),
            Document.status == DocumentStatus.SIGNED,
        )
    ).first()

    if not document:
        raise HTTPException(
            status_code=404, detail="Document not found or not signed yet"
        )

    pdf_path = (
        STATIC_FILES_DIR / "signed_documents" / f"{document.owner_id}_{document.file}"
    )

    # Assuming document.file_url is the path to the file on disk
    return FileResponse(
        path=pdf_path, filename=document.title, media_type="application/pdf"
    )


@router.put("/{request_id}/cancel", response_model=SignatureRequestRead)
def cancel_signature_request(
    request: Request,
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Cancel a signature request.
    """
    db_request = get_signature_request(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Signature request not found")
    if db_request.status in [
        SignatureRequestStatus.COMPLETED,
        SignatureRequestStatus.EXPIRED,
    ]:
        raise HTTPException(
            status_code=400, detail="Completed or expired requests cannot be canceled"
        )

    db_request.status = SignatureRequestStatus.CANCELED
    db.commit()
    db.refresh(db_request)

    # Create an audit log for the cancellation
    audit_log_crud.create_audit_log(
        db,
        AuditLogCreate(
            description="Signature request canceled",
            ip_address=request.client.host,
            action=AuditLogAction.SIGNATURE_REQUEST_CANCELED,
            signature_request_id=db_request.id,
        ),
    )

    return db_request


@router.put("/{request_id}/activate", response_model=SignatureRequestRead)
def activate_signature_request(
    request_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Activate a canceled signature request.
    """
    db_request = get_signature_request(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Signature request not found")
    if db_request.status in [
        SignatureRequestStatus.COMPLETED,
        SignatureRequestStatus.EXPIRED,
    ]:
        raise HTTPException(
            status_code=400, detail="Completed or expired requests cannot be activated"
        )
    if db_request.status != SignatureRequestStatus.CANCELED:
        raise HTTPException(
            status_code=400, detail="Only canceled requests can be activated"
        )

    # Update the status to SENT
    db_request.status = SignatureRequestStatus.SENT
    db.commit()
    db.refresh(db_request)

    # Send a new email as in the initiation of the signature request
    first_signatory = db_request.signatories[0]
    secure_link, token = generate_secure_link(
        db_request.expiry_date,
        db_request.id,
        first_signatory.email,
        [document.id for document in db_request.documents],
        first_signatory.id,
        db_request.require_otp,
    )
    email_response = send_signature_request_email(
        email_to=first_signatory.email,
        document_title="signature request",
        link=secure_link,
        message=db_request.message,
    )

    if email_response and email_response.status_code == 250:
        # Email sent successfully, create an audit log
        audit_log_crud.create_audit_log(
            db,
            AuditLogCreate(
                description="Signature request reactivated",
                ip_address=request.client.host,
                action=AuditLogAction.SIGNATURE_REQUEST_REACTIVATED,
                signature_request_id=db_request.id,
            ),
        )
    else:
        # Email sending failed, raise an error
        error_message = f"""
            Failed to send email: {email_response.status_text if email_response else 'No response'}
        """
        logging.error(error_message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message
        )

    return db_request
