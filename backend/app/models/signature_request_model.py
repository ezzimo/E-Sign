from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from .document_model import Document
from .signatory_model import Signatory
from .user_model import User


class SignatureRequest(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    document_id: int = Field(default=None, foreign_key="document.id", nullable=False)
    sender_id: int = Field(default=None, foreign_key="user.id", nullable=False)
    signatory_id: int = Field(default=None, foreign_key="signatory.id", nullable=False)
    message: str | None = None
    expiry_date: datetime | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    document: "Document" = Relationship(back_populates="signature_requests")
    sender: "User" = Relationship(back_populates="sent_signature_requests")
    signatory: "Signatory" = Relationship(back_populates="requests")
