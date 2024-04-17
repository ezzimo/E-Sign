from datetime import datetime

from pydantic import BaseModel

from app.models.audit_log_model import AuditLogAction


class AuditLogBase(BaseModel):
    document_id: int | None
    user_id: int | None
    action: AuditLogAction


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogRead(AuditLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
