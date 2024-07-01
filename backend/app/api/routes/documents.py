import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import Session

from app.api.deps import get_current_user, get_db
from app.crud import document_crud
from app.models.models import Document, User, DocumentStatus
from app.schemas.schemas import DocumentCreate, DocumentOut, DocumentUpdate
from app.services.file_service import save_file

logger = logging.getLogger(__name__)
router = APIRouter()

# Define the base directory for the static files
STATIC_FILES_DIR = Path("/app/static/document_files")


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
        file=Path(file_location).name,
        owner_id=current_user.id,
        file_url=str(file_location),
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
    Get document details by ID, including download URL.
    """
    document = document_crud.get_document_by_id(db, document_id)
    if not current_user.is_superuser and document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    document_out = DocumentOut(
        id=document.id,
        title=document.title,
        file=document.file,
        status=document.status.value,
        created_at=document.created_at,
        updated_at=document.updated_at,
        owner=document.owner,
    )
    document_out.file_url = f"/api/v1/documents/{document_id}/file"
    return document_out


@router.get("/{document_id}/download", response_class=FileResponse)
def download_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Download the PDF file by document ID.
    """
    document = document_crud.get_document_by_id(db, document_id)
    if not current_user.is_superuser and document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    file_path = STATIC_FILES_DIR / f"{document.file}"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=file_path, filename=document.file, media_type="application/pdf"
    )


@router.get("/{document_id}/file", response_class=FileResponse)
def get_document_file(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FileResponse:
    document = document_crud.get_document_by_id(db, document_id)
    if not current_user.is_superuser and document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    file_path = STATIC_FILES_DIR / f"{document.file}"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path, filename=document.title, media_type="application/pdf"
    )


@router.get("/", response_model=list[DocumentOut])
def read_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> list[DocumentOut]:
    documents = document_crud.get_documents_by_user(db, current_user, skip, limit)
    results = []
    for doc in documents:
        doc_out = DocumentOut(
            id=doc.id,
            title=doc.title,
            file=doc.file,
            status=doc.status.value,
            deleted=doc.deleted,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
            owner=doc.owner,
            file_url=doc.file_url,
            signature_details=doc.signature_details,
        )
        results.append(doc_out)
    return results


@router.put("/{document_id}", response_model=DocumentOut)
async def update_document(
    document_id: int,
    title: str | None = Form(None),
    status: str | None = Form(None),
    new_file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not current_user.is_superuser and document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if new_file:
        file_location = save_file(new_file, current_user.id)
        document_in = DocumentUpdate(
            title=title,
            status=status,
            file=Path(file_location).name,
            file_url=str(file_location),
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
    document = db.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if not current_user.is_superuser and document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if document.status in [
        DocumentStatus.SENT_FOR_SIGNATURE,
        DocumentStatus.VIEWED,
        DocumentStatus.PARTIALLY_SIGNED,
        DocumentStatus.SIGNED,
    ]:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Cannot delete document with status '{document.status.value}'. "
                "Deletion is only allowed for documents in 'draft' or 'rejected' status."
            )
        )

    document.deleted = True
    db.commit()

    # Log the deletion attempt
    logger.info(
        f"User {current_user.id} attempted to delete document {document_id}"
        f"with status {document.status.value}"
    )

    return {"message": "Document deleted successfully"}


@router.get("/{document_id}/file-url", response_model=str)
def get_document_file_url(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> str:
    try:
        file_url = document_crud.generate_document_file_url(
            db, document_id, current_user.id
        )
        return file_url
    except HTTPException as exc:
        logger.error(f"Failed to retrieve file URL: {exc.detail}")
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
