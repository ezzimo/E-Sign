from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel

# from .field_model import DocField
# from .requests_documents_link_model import RequestDocumentLink

if TYPE_CHECKING:
    # from .signature_request_model import SignatureRequest
    from .user_model import User

import enum


class DocumentStatus(enum.Enum):
    DRAFT = "draft"
    SENT_FOR_SIGNATURE = "sent for signature"
    SIGNED = "signed"
    REJECTED = "rejected"


class DocumentBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    title: str
    file: str
    status: DocumentStatus = Field(sa_column=SAEnum(DocumentStatus))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Document(DocumentBase, table=True):
    owner_id: int = Field(foreign_key="user.id")

    # doc_requests: list["SignatureRequest"] = Relationship(
    # back_populates="documents",
    # link_model=RequestDocumentLink,
    # )
    owner: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Document.owner_id]"},
        back_populates="documents"
    )
    # signature_fields: list["DocField"] = Relationship(back_populates="document")
