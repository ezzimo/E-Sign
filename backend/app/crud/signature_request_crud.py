from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.signature_request_model import SignatureRequest
from app.schemas.signature_request_schema import (
    SignatureRequestCreate,
    SignatureRequestUpdate,
)


def create_signature_request(
    db: Session, request: SignatureRequestCreate, sender_id: int
) -> SignatureRequest:
    db_request = SignatureRequest(**request.model_dump(), sender_id=sender_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_signature_request(db: Session, request_id: int) -> SignatureRequest | None:
    return db.get(SignatureRequest, request_id)


def get_signature_requests_by_document(
    db: Session, document_id: int
) -> list[SignatureRequest]:
    return db.exec(
        select(SignatureRequest).where(SignatureRequest.document_id == document_id)
    ).all()


def update_signature_request(
    db: Session, request_id: int, request_in: SignatureRequestUpdate
) -> SignatureRequest:
    db_request = db.get(SignatureRequest, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Signature request not found")
    for var, value in request_in.model_dump(exclude_unset=True).items():
        setattr(db_request, var, value) if value is not None else None
    db.commit()
    db.refresh(db_request)
    return db_request


def delete_signature_request(db: Session, request_id: int):
    db_request = db.get(SignatureRequest, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Signature request not found")
    db.delete(db_request)
    db.commit()
