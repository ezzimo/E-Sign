import enum
from datetime import datetime

from sqlalchemy import Enum
from sqlmodel import Field, Relationship, SQLModel

from .audit_log_model import AuditLog
# from .document_model import Document
# from .field_model import DocField
# from .requests_documents_link_model import RequestDocumentLink
from .requests_signatories_link_model import RequestSignatoryLink
from .signatory_model import Signatory


class SignatureRequestStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    COMPLETED = "completed"
    EXPIRED = "expired"
    CANCELED = "canceled"


class ReminderSettings(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    interval_in_days: int
    max_occurrences: int
    timezone: str | None = None
    request_id: int | None = Field(foreign_key="signaturerequest.id")
    request: "SignatureRequest" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[ReminderSettings.request_id]"}
    )


class SignatureRequestBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    status: SignatureRequestStatus = Field(
        default=SignatureRequestStatus.DRAFT, sa_column=Enum(SignatureRequestStatus)
    )
    name: str
    delivery_mode: str
    message: str | None = None
    expiry_date: datetime | None = None
    ordered_signers: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class SignatureRequest(SignatureRequestBase, table=True):
    sender_id: int = Field(foreign_key="user.id")

    # documents: list[Document] = Relationship(
    # back_populates="doc_requests",
    # link_model=RequestDocumentLink,
    # )
    signatories: list[Signatory] = Relationship(
        back_populates="signature_requests",
        link_model=RequestSignatoryLink,
    )
    # fields: list[DocField] = Relationship(back_populates="signature_request")
    audit_logs: list[AuditLog] = Relationship(back_populates="signature_request")
