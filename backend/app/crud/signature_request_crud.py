import logging

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.models import Document, DocField, Signatory, SignatureRequest, User
from app.schemas.schemas import (
    SignatureRequestCreate,
    SignatureRequestUpdate,
)

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
        reminder_settings=request_data.reminder_settings,
        expiration_date=request_data.expiration_date,
        sender_id=sender_id,
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

        new_signer = Signatory(
            first_name=signatory_info.first_name,
            last_name=signatory_info.last_name,
            email=signatory_info.email,
            phone_number=signatory_info.phone_number,
            role=signatory_info.role,
            signing_order=signatory_info.signing_order,
            creator_id=sender_id,
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
                # Only include coordinates if valid
                x=field_data.x if field_data.x else None,
                y=field_data.y if field_data.y else None,
                height=field_data.height if field_data.height else None,
                width=field_data.width if field_data.width else None,
            )

            db.add(new_field)
            db.commit()
            db.refresh(new_field)

        db.commit()

    return signature_request


def get_signature_request(db: Session, request_id: int) -> SignatureRequest | None:
    return db.get(SignatureRequest, request_id)


def get_signature_requests_by_document(
    db: Session, document_id: int
) -> list[SignatureRequest]:
    return db.exec(
        select(SignatureRequest).where(SignatureRequest.document_id == document_id)
    ).all()


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


def delete_signature_request(db: Session, request_id: int):
    db_request = db.get(SignatureRequest, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Signature request not found")
    db.delete(db_request)
    db.commit()


def get_signatories_by_signature_request(
    db: Session, request_id: int
) -> list[Signatory]:
    """
    Retrieve all signatories related to a specific signature request.
    """
    return db.exec(select(Signatory).where(Signatory.signatory_id == request_id)).all()


def get_all_signature_requests(db: Session, current_user: User) -> list[SignatureRequest]:
    """
    Retrieve all signature requests. If the user is an admin, fetch all requests,
    otherwise fetch only the requests created by the user.
    """
    if current_user.is_superuser:
        return db.exec(select(SignatureRequest)).all()
    else:
        return db.exec(
            select(SignatureRequest).where(SignatureRequest.sender_id == current_user.id)
        ).all()
