from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.document_model import Document, DocumentSignatoryLink

if TYPE_CHECKING:
    from .signature_request_model import SignatureRequest
    from .user_model import User


class Signatory(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    signer_id: int | None = Field(default=None, foreign_key="user.id", nullable=True)
    creator_id: int = Field(default=None, foreign_key="user.id", nullable=False)
    signing_order: int
    signed_at: datetime | None = None
    signature_image: str | None = None
    first_name: str
    last_name: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    documents: list["Document"] = Relationship(
        back_populates="signatories",
        link_model=DocumentSignatoryLink,
    )
    requests: list["SignatureRequest"] = Relationship(back_populates="signatory")
    signer: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Signatory.signer_id"}
    )
    creator: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Signatory.creator_id"}
    )
