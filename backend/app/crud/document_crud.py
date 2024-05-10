from sqlmodel import Session

from app.models.document_model import Document
from app.schemas.document_schema import DocumentCreate, DocumentUpdate


def create_document(db: Session, *, obj_in: DocumentCreate, owner_id: int) -> Document:
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
    db: Session,
    *,
    db_obj: Document,
    obj_in: DocumentUpdate,
) -> Document:
    if obj_in.title is not None:
        db_obj.title = obj_in.title
    if obj_in.status is not None:
        db_obj.status = obj_in.status
    if obj_in.file is not None:
        db_obj.file = obj_in.file

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_document(db: Session, *, document_id: int) -> None:
    db_obj = db.get(Document, document_id)
    db.delete(db_obj)
    db.commit()


def get_document_file(db: Session, document_id: int, user_id: int) -> str:
    # Retrieve the document by ID
    document = db.get(Document, document_id)
    if not document or document.owner_id != user_id:
        raise ValueError("No permission to access this document")

    return document.file


def generate_document_file_url(db: Session, document_id: int, user_id: int) -> str:
    try:
        file_path = get_document_file(db, document_id, user_id)
        file_url = f"{file_path}"  # Example path
        return file_url
    except ValueError:
        raise ValueError("Permission denied or document not found")
