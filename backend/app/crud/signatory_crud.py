import logging

from sqlmodel import Session, select

from app.models.signatory_model import Signatory
from app.models.user_model import User
from app.schemas.signatory_schema import SignatoryCreate, SignatoryUpdate

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
        **obj_in.model_dump(exclude_unset=True),
        signer_id=signer_id,
        creator_id=creator_id,
        user=signer,
        creator=db.get(User, creator_id),
    )

    # Persist the new signatory in the database
    db.add(signatory)
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
