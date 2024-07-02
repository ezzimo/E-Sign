import logging
from typing import List

from fastapi import HTTPException
from sqlalchemy import and_
from sqlmodel import Session, select

from app.models.models import (
    DocField,
    Document,
    RequestDocumentLink,
    RequestSignatoryLink,
    ReminderSettings,
    Signatory,
    SignatureRequest,
    SignatureRequestStatus,
    User,
)
from app.schemas.schemas import SignatureRequestCreate, SignatureRequestUpdate

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_signature_request(
    db: Session, request_data: SignatureRequestCreate, sender_id: int
) -> SignatureRequest:
    # Create the signature request
    signature_request = SignatureRequest(
        name=request_data.name,
        delivery_mode=request_data.delivery_mode,
        ordered_signers=request_data.ordered_signers,
        message=request_data.message,
        expiry_date=request_data.expiry_date,
        sender_id=sender_id,
        require_otp=request_data.require_otp,
    )
    db.add(signature_request)
    db.commit()
    db.refresh(signature_request)

    # Associate documents with the signature request
    for document_id in request_data.documents:
        document = db.exec(select(Document).where(Document.id == document_id)).first()

        if document is None:
            raise HTTPException(
                status_code=404, detail=f"Document with ID {document_id} not found"
            )
        signature_request.documents.append(document)

    # Create and associate signatories
    for signer_data in request_data.signatories:
        signatory_info = signer_data.info

        # Find a user by email to link as the signer
        user: User | None = db.exec(
            select(User).where(User.email == signatory_info.email)
        ).first()

        # If found, link as the signer
        signer_id = user.id if user else None
        signer = user if user else None

        new_signer = Signatory(
            first_name=signatory_info.first_name,
            last_name=signatory_info.last_name,
            email=signatory_info.email,
            phone_number=signatory_info.phone_number,
            role=signatory_info.role,
            signing_order=signatory_info.signing_order,
            creator_id=sender_id,
            user_id=signer_id,
            user=signer,
        )

        db.add(new_signer)
        db.commit()
        db.refresh(new_signer)

        signature_request.signatories.append(new_signer)

        for field_data in signer_data.fields:
            new_field = DocField(
                type=field_data.type,
                page=field_data.page,
                signature_request_id=signature_request.id,
                document_id=field_data.document_id,
                signer_id=new_signer.id,
                optional=field_data.optional,
                mention=field_data.mention,
                text=field_data.text,
                x=field_data.x,
                y=field_data.y,
                height=field_data.height,
                width=field_data.width,
            )

            db.add(new_field)
            db.commit()
            db.refresh(new_field)

    # Create reminder settings if provided
    if request_data.reminder_settings:
        reminder_settings = ReminderSettings(
            interval_in_days=request_data.reminder_settings.interval_in_days,
            max_occurrences=request_data.reminder_settings.max_occurrences,
            timezone=request_data.reminder_settings.timezone,
            request_id=signature_request.id,
        )
        db.add(reminder_settings)
        db.commit()
        db.refresh(reminder_settings)
        signature_request.reminder_settings = reminder_settings

    db.commit()
    db.refresh(signature_request)
    return signature_request


def get_signature_request(db: Session, request_id: int) -> SignatureRequest | None:
    return db.get(SignatureRequest, request_id)


def get_signature_requests_by_document(
    db: Session, document_id: int
) -> list[SignatureRequest]:
    """
    Fetch all signature requests linked to a specific document ID.

    Args:
        db (Session): The database session dependency.
        document_id (int): The ID of the document.

    Returns:
        list[SignatureRequest]: A list of signature requests linked to the document.
    """
    try:
        # Query the signature requests associated with the document
        statement = (
            select(SignatureRequest)
            .join(RequestDocumentLink)
            .where(RequestDocumentLink.document_id == document_id)
        )
        signature_requests = db.exec(statement).all()
        return signature_requests
    except Exception as exc:
        logger.error(f"Failed to fetch signature requests: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error")


def update_signature_request(
    db: Session, request_id: int, request_in: SignatureRequestUpdate
) -> SignatureRequest:
    db_request = db.get(SignatureRequest, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Signature request not found")
    for var, value in request_in.model_dump(exclude_unset=True).items():
        setattr(db_request, var, value) if value is not None else None
    db.commit()
    db.refresh(db_request)
    return db_request


def delete_signature_request(db: Session, request_id: int, current_user: User):
    db_request = db.get(SignatureRequest, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Signature request not found")

    # Ensure only owner or superuser can delete the request
    if not current_user.is_superuser and db_request.sender_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Only allow deletion of certain statuses
    if db_request.status not in [
        SignatureRequestStatus.DRAFT,
        SignatureRequestStatus.EXPIRED,
        SignatureRequestStatus.CANCELED,
    ]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete signature request with status '{db_request.status.value}'."
        )

    db_request.deleted = True
    db.commit()
    # Log the deletion attempt
    logger.info(f"User {current_user.id} marked signature request {request_id} as deleted.")


def get_signatories_by_signature_request(
    db: Session, request_id: int
) -> list[Signatory]:
    """
    Retrieve all signatories related to a specific signature request ID.

    Args:
        db (Session): The database session dependency.
        request_id (int): The ID of the Request.

    Returns:
        list[Signatory]: A list of signatory linked to the request.
    """
    try:
        statement = (
            select(Signatory)
            .join(RequestSignatoryLink)
            .where(RequestSignatoryLink.signature_request_id == request_id)
        )
        signatories = db.exec(statement).all()
        return signatories
    except Exception as exc:
        logger.error(f"Failed to fetch signatories: {exc}")
        raise HTTPException(status_code=500, detail="Internal server error")


def get_all_signature_requests(
    db: Session, current_user: User
) -> List[SignatureRequest]:
    """
    Retrieve all signature requests based on user role.

    - If the user is a superuser, fetch all requests.
    - If the user is not a superuser, fetch only the requests created by the user and not marked as deleted.

    Args:
        db (Session): The database session.
        current_user (User): The current authenticated user.

    Returns:
        List[SignatureRequest]: A list of signature requests.
    """
    try:
        if current_user.is_superuser:
            logger.info(f"Superuser {current_user.id} is fetching all signature requests.")
            return db.exec(select(SignatureRequest)).all()
        else:
            logger.info(f"User {current_user.id} is fetching their non-deleted signature requests.")
            return db.exec(
                select(SignatureRequest).where(
                    and_(
                        SignatureRequest.sender_id == current_user.id,
                        SignatureRequest.deleted.is_(False)
                    )
                )
            ).all()
    except Exception as e:
        logger.error(f"Error fetching signature requests for user {current_user.id}: {str(e)}")
        raise
