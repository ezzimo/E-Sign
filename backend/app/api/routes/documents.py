import os
import logging
from typing import Any, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from app.api.deps import get_current_user, get_db
from app.crud import document_crud
from app.models.models import Document, User
from app.schemas.schemas import DocumentCreate, DocumentOut, DocumentUpdate
from app.services.file_service import save_file

# Create a logger for your application
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=DocumentOut)
async def create_document(
    db: Session = Depends(get_db),
    title: str = Form(...),
    status: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> DocumentOut:
    file_location = save_file(file, current_user.id)
    document_in = DocumentCreate(
        title=title,
        status=status,
        file=file_location,
        owner_id=current_user.id,
        file_url=file_location,
    )
    document = document_crud.create_document(db=db, obj_in=document_in)
    return document


@router.get("/{document_id}", response_model=DocumentOut)
def read_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get document by ID and return the PDF file content.
    """
    document = document_crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = document_crud.get_document_file(db, document_id, current_user.id)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path, media_type="application/pdf", filename=document.file.split("/")[-1]
    )


@router.get("/", response_model=list[DocumentOut])
def read_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[DocumentOut]:
    """
    Retrieve documents with manual mapping, including file URLs.
    """
    documents = db.exec(select(Document).offset(skip).limit(limit)).all()
    results = []
    for doc in documents:
        file_url = document_crud.generate_document_file_url(db, doc.id, current_user.id)
        doc_out = DocumentOut(
            id=doc.id,
            title=doc.title,
            file=doc.file,
            status=doc.status.value,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
            owner=doc.owner,
            file_url=file_url,
        )
        results.append(doc_out)
    return results


@router.put("/{document_id}", response_model=DocumentOut)
async def update_document(
    document_id: int,
    title: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    new_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not current_user.is_superuser and document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if new_file:
        file_location = f"static/document_files/{current_user.id}_{new_file.filename}"
        with open(file_location, "wb") as file_object:
            file_content = await new_file.read()
            file_object.write(file_content)
        document_in = DocumentUpdate(
            title=title,
            status=status,
            file=file_location,
            file_url=f"http://localhost/static/{file_location}",
        )
    else:
        document_in = DocumentUpdate(
            title=title,
            status=status,
            file=document.file,
            file_url=document.file_url,
        )

    updated_document = document_crud.update_document(
        db=db, db_obj=document, obj_in=document_in
    )

    return updated_document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete a document. Only superusers or the owner of the document can delete it.
    """
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not current_user.is_superuser and document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(document)
    db.commit()
    return {"message": "Document deleted successfully"}


@router.get("/{document_id}/file-url", response_model=str)
def get_document_file_url(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> str:
    """
    Retrieve the file URL for a specific document, ensuring that only authorized users can access it.
    """
    try:
        file_url = document_crud.generate_document_file_url(
            db, document_id, current_user.id
        )
        return file_url
    except HTTPException as exc:
        logger.error(f"Failed to retrieve file URL: {exc.detail}")
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
