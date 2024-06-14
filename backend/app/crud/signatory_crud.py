import logging

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.models import (
    DocField,
    Signatory,
    User,
)
from app.schemas.schemas import FieldCreate, SignatoryCreate, SignatoryUpdate

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def create_signatory(
    db: Session, *, obj_in: SignatoryCreate, creator_id: int
) -> Signatory:
    # Validate that signing_order is greater than zero
    if obj_in.signing_order <= 0:
        raise ValueError("Signing order must be greater than zero")

    # Find a user by email to link as the signer
    user: User | None = db.exec(select(User).where(User.email == obj_in.email)).first()

    # If found, link as the signer
    signer_id = user.id if user else None
    signer = user if user else None

    # Create the new signatory
    signatory = Signatory(
        first_name=obj_in.first_name,
        last_name=obj_in.last_name,
        email=obj_in.email,
        phone_number=obj_in.phone_number,
        role=obj_in.role,
        signing_order=obj_in.signing_order,
        user_id=signer_id,
        creator_id=creator_id,
        user=signer,
        creator=db.get(User, creator_id),
    )

    # Persist the new signatory in the database
    db.add(signatory)
    db.commit()
    db.refresh(signatory)

    # Create fields for the signatory
    for field in obj_in.fields:
        db_field = DocField(
            type=field.type,
            page=field.page,
            document_id=field.document_id,
            signer_id=signatory.id,
            optional=field.optional,
            mention=field.mention,
            text=field.text,
            # Only include coordinates if valid
            x=field.x if field.x else None,
            y=field.y if field.y else None,
            height=field.height if field.height else None,
            width=field.width if field.width else None,
        )
        signatory.fields.append(db_field)

    db.commit()
    db.refresh(signatory)
    logger.info(f"Created signatory {signatory.id} by user {creator_id}")
    return signatory


def get_signatory(db: Session, signatory_id: int) -> Signatory | None:
    return db.get(Signatory, signatory_id)


def get_signatories_by_document(db: Session, document_id: int) -> list[Signatory]:
    return db.exec(select(Signatory).where(Signatory.document_id == document_id)).all()


def update_signatory(
    db: Session, signatory_id: int, update_data: SignatoryUpdate
) -> Signatory:
    # Fetch the existing signatory to update
    signatory = db.get(Signatory, signatory_id)
    if not signatory:
        logger.error(f"Signatory with ID {signatory_id} not found.")
        raise ValueError(f"Signatory with ID {signatory_id} not found.")

    # Apply the updates, excluding unset values
    for var, value in update_data.model_dump(exclude_unset=True).items():
        setattr(signatory, var, value)

    db.commit()
    db.refresh(signatory)
    logger.info(f"Updated signatory {signatory_id}")
    return signatory


def delete_signatory(db: Session, signatory_id: int):
    # Fetch the existing signatory to delete
    db_signatory = db.get(Signatory, signatory_id)
    if not db_signatory:
        logger.error(f"Signatory with ID {signatory_id} not found.")
        raise ValueError(f"Signatory with ID {signatory_id} not found.")

    db.delete(db_signatory)
    db.commit()
    logger.info(f"Deleted signatory {signatory_id}")


def create_field_signatory(
    db: Session, field_data: FieldCreate, signatory_id: int
) -> DocField:
    # Validate the field data
    try:
        field_data.validate_fields()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Create the DocField explicitly
    db_field = DocField(
        **field_data.model_dump(exclude_unset=True),
        signer_id=signatory_id,
    )

    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field
