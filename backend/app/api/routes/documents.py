from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlmodel import Session, select

from app.api.deps import get_current_user, get_db
from app.crud import document_crud
from app.models.document_model import Document
from app.models.user_model import User
from app.schemas.document_schema import DocumentCreate, DocumentOut, DocumentUpdate
from app.schemas.field_schema import FieldOut
from app.schemas.signature_request_schema import SignatureRequestRead

router = APIRouter()


@router.post("/", response_model=DocumentOut)
async def create_document(
    db: Session = Depends(get_db),
    title: str = Form(...),
    status: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create a new document with file upload.
    """
    # Step 1: Save the uploaded file to a secure location on the server
    file_location = f"document_files/{current_user.id}_{file.filename}"
    with open(file_location, "wb") as file_object:
        file_content = await file.read()  # Read async to avoid blocking
        file_object.write(file_content)

    # Reset file pointer if needed elsewhere
    await file.seek(0)

    # Step 2: Construct a DocumentCreate schema instance with the received data
    document_data = {
        "title": title,
        "status": status,
        "file": file_location,
        "owner_id": current_user.id,
    }
    # Ensure that `DocumentCreate` schema allows passing `owner_id` and adjusts for
    # handling `status` appropriately
    document_create = DocumentCreate(**document_data)

    # Step 3: Use CRUD utility to save document metadata to the database
    document = document_crud.create_document(
        db=db, obj_in=document_create, owner_id=current_user.id
    )

    return document


@router.get("/{document_id}", response_model=DocumentOut)
def read_document(*, db: Session = Depends(get_db), document_id: int):
    """
    Get document by ID.
    """
    document = document_crud.get_document(db=db, document_id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/", response_model=list[DocumentOut])
def read_documents(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> list[DocumentOut]:
    """
    Retrieve documents with manual mapping.
    """
    documents = db.exec(select(Document).offset(skip).limit(limit)).all()

    return [
        DocumentOut(
            id=doc.id,
            title=doc.title,
            file=doc.file,
            status=doc.status.value,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
            owner=doc.owner,
            doc_requests=[
                SignatureRequestRead(**req.__dict__) for req in doc.doc_requests
            ],
            signature_fields=[
                FieldOut(**field.__dict__) for field in doc.signature_fields
            ],
        )
        for doc in documents
    ]


@router.put("/{document_id}", response_model=DocumentOut)
def update_document(
    document_id: int,
    document_in: DocumentUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update a document. Superuser can update any document. Regular users can only update their documents.
    """
    document = session.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not current_user.is_superuser and document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    for var, value in vars(document_in).items():
        setattr(document, var, value) if value else None

    session.add(document)
    session.commit()
    session.refresh(document)
    return document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete a document. Superuser can delete any document. Regular users can only delete their documents.
    """
    document = session.get(Document, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not current_user.is_superuser and document.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    session.delete(document)
    session.commit()
    return {"message": "Document deleted successfully"}
