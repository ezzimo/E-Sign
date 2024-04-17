from sqlmodel import Session, select

from app.models.audit_log_model import AuditLog
from app.schemas.audit_log_schema import AuditLogCreate


def create_audit_log(db: Session, audit_log: AuditLogCreate) -> AuditLog:
    db_audit_log = AuditLog(**audit_log.model_dump())
    db.add(db_audit_log)
    db.commit()
    db.refresh(db_audit_log)
    return db_audit_log


def get_audit_logs_by_document(db: Session, document_id: int):
    return db.exec(select(AuditLog).where(AuditLog.document_id == document_id)).all()
