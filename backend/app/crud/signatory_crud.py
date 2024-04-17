from sqlmodel import Session, select

from app.models.signatory_model import Signatory
from app.schemas.signatory_schema import SignatoryCreate, SignatoryUpdate


def create_signatory(db: Session, *, obj_in: SignatoryCreate) -> Signatory:
    db_obj = Signatory(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_signatory(db: Session, signatory_id: int) -> Signatory | None:
    return db.get(Signatory, signatory_id)


def get_signatories_by_document(db: Session, document_id: int) -> list[Signatory]:
    return db.exec(select(Signatory).where(Signatory.document_id == document_id)).all()


def update_signatory(
    db: Session, signatory_id: int, update_data: SignatoryUpdate
) -> Signatory:
    signatory = db.get(Signatory, signatory_id)
    for var, value in update_data.dict(exclude_unset=True).items():
        setattr(signatory, var, value) if value is not None else None
    db.commit()
    return signatory


def delete_signatory(db: Session, *, signatory_id: int) -> None:
    db_obj = db.get(Signatory, signatory_id)
    db.delete(db_obj)
    db.commit()
