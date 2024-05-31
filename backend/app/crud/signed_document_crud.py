from sqlmodel import Session
from app.models.models import DocumentSignatureDetails
from app.schemas.schemas import DocumentSignatureDetailsCreate


def create_document_signature_details(
    session: Session, signature_details_create: DocumentSignatureDetailsCreate
) -> DocumentSignatureDetails:
    signature_details = DocumentSignatureDetails(**signature_details_create.model_dump())
    session.add(signature_details)
    session.commit()
    session.refresh(signature_details)
    return signature_details
