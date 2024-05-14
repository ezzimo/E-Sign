from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

from app.models.document_model import DocumentStatus
from .user_schema import UserOut


class DocumentBase(BaseModel):
    title: str = Field(..., description="Title of the document")
    file: str = Field(..., description="File path or identifier")
    file_url: Optional[str] = Field(None, description="URL to view the document")
    status: DocumentStatus = Field(..., description="Current status of the document")

    class Config:
        from_attributes = True


class DocumentCreate(DocumentBase):
    owner_id: Optional[int] = Field(None, description="Owner ID of the document")


class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, description="New title for the document")
    status: Optional[DocumentStatus] = Field(
        None, description="New status of the document"
    )
    file: Optional[str] = Field(None, description="Updated file for the document")
    file_url: Optional[str] = Field(None, description="URL to view the document")

    class Config:
        from_attributes = True


class DocumentOut(DocumentBase):
    id: int = Field(..., description="Unique identifier for the document")
    created_at: datetime = Field(
        ..., description="Timestamp when the document was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the document was last updated"
    )
    owner: UserOut = Field(..., description="User information of the owner")
