import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, Enum
from sqlmodel import Field, Relationship, SQLModel

from .user_model import User

if TYPE_CHECKING:
    from .signatory_model import Signatory
    from .signature_request_model import SignatureRequest


class DocumentStatus(enum.Enum):
    DRAFT = "draft"
    SENT_FOR_SIGNATURE = "sent for signature"
    SIGNED = "signed"
    REJECTED = "rejected"


# Define the association table for many-to-many relationship
class DocumentSignatoryLink(SQLModel, table=True):
    document_id: int | None = Field(
        default=None, foreign_key="document.id", primary_key=True
    )
    signatory_id: int | None = Field(
        default=None, foreign_key="signatory.id", primary_key=True
    )


class Document(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    owner_id: int = Field(foreign_key="user.id")
    owner: "User" = Relationship(back_populates="documents")
    file: str  # Path or reference to file storage
    status: DocumentStatus = Field(sa_column=Column(Enum(DocumentStatus)))
    signatories: list["Signatory"] = Relationship(
        back_populates="documents",
        link_model=DocumentSignatoryLink,
    )
    signature_requests: list["SignatureRequest"] = Relationship(
        back_populates="document"
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
