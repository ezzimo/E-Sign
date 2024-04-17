from sqlmodel import Session

from app.models.document_model import Document
from app.schemas.document_schema import DocumentCreate, DocumentUpdate


def create_document(db: Session, *, obj_in: DocumentCreate, owner_id: int) -> Document:
    # Create a new Document instance
    db_obj = Document(
        title=obj_in.title, status=obj_in.status, file=obj_in.file, owner_id=owner_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_document(db: Session, document_id: int) -> Document:
    return db.get(Document, document_id)


def update_document(
    db: Session, *, db_obj: Document, obj_in: DocumentUpdate
) -> Document:
    obj_data = obj_in.model_dump(exclude_unset=True)
    for key, value in obj_data.items():
        setattr(db_obj, key, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_document(db: Session, *, document_id: int) -> None:
    db_obj = db.get(Document, document_id)
    db.delete(db_obj)
    db.commit()
