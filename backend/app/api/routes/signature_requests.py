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
    SignatureRequest,
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

    This endpoint allows a user to initiate a new signature request. Only the owner
    of the documents or a superuser can use those documents for the signature request.

    Args:
        request (Request): The incoming HTTP request.
        signature_request (SignatureRequestCreate): The signature request data.
        db (Session): The database session dependency.
        current_user (User): The current authenticated user.

    Returns:
        SignatureRequestRead: The created signature request.

    Raises:
        HTTPException: If no signatories are provided, or if the user is not authorized
                       to use the specified documents.
    """
    logger.info(f"User {current_user.id} is attempting to initiate a signature request.")

    # Validate signatories
    if len(signature_request.signatories) == 0:
        logger.error("At least one signatory is required.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one signatory is required.",
        )

    # Validate documents
    if len(signature_request.documents) == 0:
        logger.error("At least one document is required.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one document is required.",
        )

    # Verify document ownership
    document_ids = [doc.id for doc in signature_request.documents]
    documents = db.exec(select(Document).where(Document.id.in_(document_ids))).all()

    for document in documents:
        if document.owner_id != current_user.id and not current_user.is_superuser:
            logger.error(f"User {current_user.id} is not authorized to use document {document.id}.")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You do not have permission to use document '{document.title}' (ID: {document.id}).",
            )

    logger.info(f"User {current_user.id} is authorized to use the specified documents.")

    # Create the signature request
    signature_request_data = create_signature_request(
        db=db, request_data=signature_request, sender_id=current_user.id
    )

    # Handle signatories based on count
    if len(signature_request.signatories) == 1:
        handle_single_signatory(signature_request_data, db, request)
    else:
        handle_multiple_signatories(signature_request_data, db, request)

    # Retrieve documents and signatories for response
    documents = db.exec(
        select(Document).where(
            Document.id.in_([doc.id for doc in signature_request_data.documents])
        )
    ).all()

    signatories = db.exec(
        select(Signatory).where(
            Signatory.id.in_([sig.id for sig in signature_request_data.signatories])
        )
    ).all()

    # Create response object
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

    logger.info(f"Signature request {response_data.id} initiated successfully by user {current_user.id}.")

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
def read_signature_requests_by_document(
    document_id: int,
    db: Session = Depends(get_db),
) -> list[SignatureRequestRead]:
    """
    Retrieve all signature requests associated with a specific document ID.

    Args:
        document_id (int): The ID of the document.
        db (Session): The database session dependency.

    Returns:
        list[SignatureRequestRead]: A list of signature requests linked to the document.

    Raises:
        HTTPException: If the document is not found.
    """
    try:
        logger.info(f"Fetching signature requests for document ID {document_id}")

        # Check if the document exists
        document = db.get(Document, document_id)
        if not document:
            logger.error(f"Document with ID {document_id} not found")
            raise HTTPException(status_code=404, detail="Document not found")

        # Get all signature requests linked to the document
        requests = get_signature_requests_by_document(db=db, document_id=document_id)

        logger.info(
            f"Successfully fetched {len(requests)} signature requests for document ID {document_id}"
        )
        return requests

    except Exception as exc:
        logger.error(f"An unexpected error occurred: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error")


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
def delete_sig_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a signature request.

    Only the owner or a superuser can delete a signature request.
    The request must be in a deletable status and will be marked as deleted instead of actual deletion.

    Args:
        request_id (int): The ID of the signature request to be deleted.
        db (Session): The database session dependency.
        current_user (User): The current authenticated user.

    Returns:
        dict: A message indicating the success of the deletion.

    Raises:
        HTTPException: If the request is not found, the user lacks permissions,
                       or the request status does not allow deletion.
    """
    try:
        db_request = get_signature_request(db=db, request_id=request_id)
        if db_request is None:
            logger.error(f"Signature request with ID {request_id} not found.")
            raise HTTPException(status_code=404, detail="Signature request not found")

        delete_signature_request(db=db, request_id=request_id, current_user=current_user)
        logger.info(f"Signature request {request_id} deleted by user {current_user.id}.")
        return {"message": "Signature request deleted successfully"}
    except HTTPException as exc:
        logger.error(f"Failed to delete signature request: {exc.detail}")
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)


@router.get(
    "/signature-request/{request_id}/signers", response_model=list[SignatoryOut]
)
def list_signature_request_signers(request_id: int, db: Session = Depends(get_db)):
    """
    List all signatories for a specific signature request ID.

    Args:
        request_id (int): The ID of the request.
        db (Session): The database session dependency.

    Returns:
        list[Signatory]: A list of signatories linked to the request.

    Raises:
        HTTPException: If the request is not found.
    """
    try:
        logger.info(f"Fetching request for request ID {request_id}")

        # Check if the request exists
        request = db.get(SignatureRequest, request_id)
        if not request:
            logger.error(f"Signature Request with ID {request_id} not found")
            raise HTTPException(status_code=404, detail="Signature Request not found")

        # Get all signatories linked to the signature request
        signatories = get_signatories_by_signature_request(db, request_id)

        logger.info(
            f"Successfully fetched {len(signatories)} signatories for signature request ID {request_id}"
        )
        return signatories

    except Exception as exc:
        logger.error(f"Failed to return signatories: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/{signature_request_id}/documents/{document_id}/download",
    response_class=FileResponse,
)
async def download_signed_document(
    signature_request_id: int,
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Download the signed document associated with a completed signature request.

    Args:
        signature_request_id (int): The ID of the signature request.
        document_id (int): The ID of the document to download.
        db (Session): The database session dependency.
        current_user (User): The current authenticated user.

    Returns:
        FileResponse: The signed document file response.

    Raises:
        HTTPException: If the document or signature request is not found,
                       or if the document is not signed,
                       or if the user does not have permission to download the document.
    """
    try:
        logger.info(
            f"Attempting to download document ID {document_id} for"
            f"signature request ID {signature_request_id}"
        )

        # Verify the document is associated with the signature request, is signed,
        # and the request is completed
        document = db.exec(
            select(Document)
            .join(SignatureRequest.documents)
            .where(
                Document.id == document_id,
                Document.status == DocumentStatus.SIGNED,
                SignatureRequest.id == signature_request_id,
                SignatureRequest.status == SignatureRequestStatus.COMPLETED,
            )
        ).first()

        if not document:
            logger.error(
                f"Document with ID {document_id} not found or not signed yet for "
                f"signature request ID {signature_request_id}"
            )
            raise HTTPException(
                status_code=404, detail="Document not found or not signed yet"
            )

        # Verify the current user is the owner or a superuser
        if not current_user.is_superuser and document.owner_id != current_user.id:
            logger.error(
                f"User {current_user.id} does not have permission to download document ID {document_id}"
            )
            raise HTTPException(status_code=403, detail="Not enough permissions")

        pdf_path = STATIC_FILES_DIR / "signed_documents" / f"{document.file}"

        if not pdf_path.exists():
            logger.error(f"File {pdf_path} does not exist")
            raise HTTPException(status_code=404, detail="File not found")

        logger.info(
            f"Successfully found and returning document ID {document_id}"
            f" for signature request ID {signature_request_id}"
        )

        return FileResponse(
            path=pdf_path, filename=document.title, media_type="application/pdf"
        )

    except HTTPException as exc:
        logger.error(f"Failed to download document: {exc.detail}")
        raise
    except Exception as exc:
        logger.error(f"An unexpected error occurred: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error")


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
