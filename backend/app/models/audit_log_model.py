from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .signature_request_model import SignatureRequest


class AuditLogAction(str, Enum):
    DOCUMENT_UPLOADED = "document uploaded"
    SIGNATURE_REQUESTED = "signature requested"
    DOCUMENT_SIGNED = "document signed"
    DOCUMENT_VIEWED = "document viewed"


class AuditLogBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    description: str | None
    ip_address: str | None
    action: AuditLogAction
    timestamp: datetime = Field(default_factory=datetime.now)


class AuditLog(AuditLogBase, table=True):
    signature_request_id: int = Field(default=None, foreign_key="signaturerequest.id")

    signature_request: Optional["SignatureRequest"] = Relationship(
        back_populates="audit_logs"
    )
