from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class AuditLogAction(str, Enum):
    DOCUMENT_UPLOADED = "document uploaded"
    SIGNATURE_REQUESTED = "signature requested"
    DOCUMENT_SIGNED = "document signed"
    DOCUMENT_VIEWED = "document viewed"


class AuditLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    document_id: int | None = Field(default=None, foreign_key="document.id")
    user_id: int | None = Field(default=None, foreign_key="user.id")
    action: AuditLogAction
    timestamp: datetime = Field(default_factory=datetime.now)
