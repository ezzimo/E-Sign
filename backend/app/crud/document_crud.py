from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.models import Document, User
from app.schemas.schemas import DocumentCreate, DocumentUpdate
from app.services.file_utils import generate_file_url


def create_document(db: Session, *, obj_in: DocumentCreate) -> Document:
    file_url = generate_file_url(obj_in.file)
    db_obj = Document(
        title=obj_in.title,
        status=obj_in.status,
        file=obj_in.file,
        file_url=file_url,
        owner_id=obj_in.owner_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_document(db: Session, *, db_obj: Document, obj_in: DocumentUpdate) -> Document:
    if obj_in.title is not None:
        db_obj.title = obj_in.title
    if obj_in.status is not None:
        db_obj.status = obj_in.status
    if obj_in.file is not None:
        db_obj.file = obj_in.file
        db_obj.file_url = generate_file_url(obj_in.file)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_document(db: Session, *, document_id: int) -> None:
    db_obj = db.get(Document, document_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(db_obj)
    db.commit()


def get_document_by_id(db: Session, document_id: int) -> Document:
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


def get_documents_by_user(db: Session, user: User, skip: int, limit: int) -> list[Document]:
    statement = select(Document).offset(skip).limit(limit)
    if not user.is_superuser:
        statement = statement.where(Document.owner_id == user.id)
    return db.exec(statement).all()
