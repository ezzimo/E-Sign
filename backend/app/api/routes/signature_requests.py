import logging
import sys

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session

from app.api.deps import get_current_user, get_db
from app.crud.signature_request_crud import (
    create_signature_request,
    delete_signature_request,
    get_all_signature_requests,
    get_signatories_by_signature_request,
    get_signature_request,
    get_signature_requests_by_document,
    update_signature_request,
)
from app.crud import audit_log_crud, document_crud
from app.models.models import (
    User,
    DocumentStatus,
    AuditLogAction,
    SignatureRequestStatus,
)
from app.schemas.schemas import (
    ReminderSettingsSchema,
    SignatoryOut,
    SignatureRequestCreate,
    SignatureRequestRead,
    SignatureRequestUpdate,
    AuditLogCreate,
)
from app.utils import send_signature_request_email, send_signature_request_notification_email
from app.services.file_service import generate_secure_link

# Create a logger for your application
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

router = APIRouter()


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

    email_response = None
    if len(signature_request.signatories) == 1:
        signatory = signature_request_data.signatories[0]
        secure_link = generate_secure_link(
            signature_request_data.expiry_date,
            signature_request_data.id,
            signatory.email,
            [document.id for document in signature_request_data.documents],
            signatory.id,
        )
        email_response = send_signature_request_email(
            email_to=signatory.email,
            document_title="signature request",
            link=secure_link,
            message=signature_request_data.message,
        )
    else:
        signature_request_data.signatories.sort(key=lambda s: s.signing_order)
        first_signatory = signature_request_data.signatories[0]
        secure_link = generate_secure_link(
            signature_request_data.expiry_date,
            signature_request_data.id,
            first_signatory.email,
            [document.id for document in signature_request_data.documents],
            first_signatory.id,
        )
        email_response = send_signature_request_email(
            email_to=first_signatory.email,
            document_title="signature request",
            link=secure_link,
            message=signature_request_data.message,
        )

    if email_response and email_response.status_code == 250:
        # Email sent successfully, update document status
        for document_id in signature_request.documents:
            document = document_crud.get_document_by_id(db, document_id)
            if document:
                document.status = DocumentStatus.SENT_FOR_SIGNATURE
                db.add(document)

        # Update signature request status
        signature_request_data.status = SignatureRequestStatus.SENT
        db.add(signature_request_data)
        db.commit()
        db.refresh(signature_request_data)

        # Create an audit log
        audit_log_crud.create_audit_log(
            db,
            AuditLogCreate(
                description="Signature request initiated",
                ip_address=request.client.host,
                action=AuditLogAction.SIGNATURE_REQUESTED,
                signature_request_id=signature_request_data.id,
            ),
        )

        # Send notification email
        send_signature_request_notification_email(
            signature_request_data.sender.email,
            signature_request_data.name,
            signature_request_data.id,
            signature_request_data.status.value,
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

    # Extracting IDs for documents and signatories
    document_ids = [document.id for document in signature_request_data.documents]
    signatory_ids = [signatory.id for signatory in signature_request_data.signatories]

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
            ReminderSettingsSchema.model_validate(signature_request_data.reminder_settings)
            if signature_request_data.reminder_settings
            else None
        ),
        expiry_date=signature_request_data.expiry_date,
        message=signature_request_data.message,
        documents=document_ids,
        signatories=signatory_ids,
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
