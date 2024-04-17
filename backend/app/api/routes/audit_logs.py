from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.deps import get_db
from app.crud.audit_log_crud import create_audit_log, get_audit_logs_by_document
from app.schemas.audit_log_schema import AuditLogCreate, AuditLogRead

router = APIRouter()


@router.post("/", response_model=AuditLogRead)
def create_audit_log_endpoint(audit_log: AuditLogCreate, db: Session = Depends(get_db)):
    return create_audit_log(db=db, audit_log=audit_log)


@router.get("/document/{document_id}", response_model=list[AuditLogRead])
def get_audit_logs_for_document(document_id: int, db: Session = Depends(get_db)):
    return get_audit_logs_by_document(db=db, document_id=document_id)
