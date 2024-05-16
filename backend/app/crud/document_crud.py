import urllib.parse

from fastapi import HTTPException
from sqlmodel import Session

from app.models.models import Document
from app.schemas.schemas import DocumentCreate, DocumentUpdate


def create_document(db: Session, *, obj_in: DocumentCreate) -> Document:
    file_url = f"http://localhost/static/document_files/{urllib.parse.quote(obj_in.file.split('/')[-1])}"
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


def get_document(db: Session, document_id: int) -> Document:
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


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
        db_obj.file_url = f"http://localhost/static/document_files/{urllib.parse.quote(obj_in.file.split('/')[-1])}"  # noqa
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


def get_document_file(db: Session, document_id: int, user_id: int) -> str:
    document = db.get(Document, document_id)
    if not document or document.owner_id != user_id:
        raise HTTPException(
            status_code=403, detail="No permission to access this document"
        )
    return document.file


def generate_document_file_url(db: Session, document_id: int, user_id: int) -> str:
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=403, detail="Document not found")
    elif document.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return (
        f"http://localhost/api/v1/static/document_files/{document.file.split('/')[-1]}"
    )
