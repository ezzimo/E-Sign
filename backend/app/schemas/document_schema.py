from datetime import datetime

from pydantic import BaseModel, Field

from app.models.document_model import DocumentStatus

from .field_schema import FieldOut
from .signature_request_schema import SignatureRequestRead
from .user_schema import UserOut


# Base schema for documents
class DocumentBase(BaseModel):
    title: str = Field(..., description="Title of the document")
    file: str = Field(..., description="File path or identifier")
    status: DocumentStatus = Field(..., description="Current status of the document")

    class Config:
        from_attributes = True  # To support compatibility with SQLModel


# Schema for document creation
class DocumentCreate(DocumentBase):
    owner_id: int | None = Field(None, description="Owner ID of the document")


# Schema for document update
class DocumentUpdate(BaseModel):
    title: str | None = Field(None, description="New title for the document")
    file: str | None = Field(None, description="New file path or identifier")
    status: DocumentStatus | None = Field(
        None, description="New status of the document"
    )

    class Config:
        from_attributes = True  # For compatibility with SQLModel


# Schema for document output (e.g., for API responses)
class DocumentOut(DocumentBase):
    id: int = Field(..., description="Unique identifier for the document")
    created_at: datetime = Field(
        ..., description="Timestamp when the document was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the document was last updated"
    )
    owner: UserOut = Field(..., description="User information of the owner")
    doc_requests: list["SignatureRequestRead"] = Field(
        default_factory=list,
        description="List of associated signature requests",
    )
    signature_fields: list["FieldOut"] = Field(
        default_factory=list,
        description="List of associated document fields",
    )

    class Config:
        orm_mode = True
        from_attributes = True
