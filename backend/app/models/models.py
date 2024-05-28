from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel
import enum


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    is_active: bool = True
    is_superuser: bool = False


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str | None = None
    hashed_password: str
    first_name: str
    last_name: str
    company: str | None = None
    role: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    documents: List["Document"] = Relationship(back_populates="owner")
    signatories: List["Signatory"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"foreign_keys": "Signatory.creator_id"}
    )
    requests: List["SignatureRequest"] = Relationship(
        back_populates="sender"
    )


# Enum definitions
class DocumentStatus(enum.Enum):
    DRAFT = "draft"
    SENT_FOR_SIGNATURE = "sent for signature"
    VIEWED = "viewed"
    SIGNED = "signed"
    REJECTED = "rejected"


class FieldType(enum.Enum):
    SIGNATURE = "signature"
    MENTION = "mention"
    TEXT = "text"
    CHECKBOX = "checkbox"
    RADIO_GROUP = "radio_group"
    READ_ONLY_TEXT = "read_only_text"


class SignatureRequestStatus(enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    COMPLETED = "completed"
    EXPIRED = "expired"
    CANCELED = "canceled"


# Base model for common attributes
class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class RequestDocumentLink(SQLModel, table=True):
    signature_request_id: Optional[int] = Field(
        default=None, foreign_key="signaturerequest.id", primary_key=True
    )
    document_id: Optional[int] = Field(
        default=None, foreign_key="document.id", primary_key=True
    )


class RequestSignatoryLink(SQLModel, table=True):
    signature_request_id: Optional[int] = Field(
        default=None, foreign_key="signaturerequest.id", primary_key=True
    )
    signatory_id: Optional[int] = Field(
        default=None, foreign_key="signatory.id", primary_key=True
    )


class Document(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    file: str
    file_url: Optional[str] = None
    status: DocumentStatus = Field(sa_column=SAEnum(DocumentStatus))
    owner_id: int = Field(foreign_key="user.id")

    owner: User = Relationship(back_populates="documents")
    signature_requests: List["SignatureRequest"] = Relationship(
        back_populates="documents",
        link_model=RequestDocumentLink
    )


class DocField(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: FieldType = Field(sa_column=SAEnum(FieldType))
    page: int
    x: Optional[int] = None
    y: Optional[int] = None
    height: Optional[int] = None
    width: Optional[int] = None
    document_id: int = Field(foreign_key="document.id")
    signature_request_id: int = Field(foreign_key="signaturerequest.id")
    signer_id: Optional[int] = Field(default=None, foreign_key="signatory.id")

    signatory: Optional["Signatory"] = Relationship(back_populates="fields")
    radios: List["Radio"] = Relationship(back_populates="doc_field")


class Radio(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    field_id: int = Field(foreign_key="docfield.id")
    name: str
    x: int
    y: int
    size: Optional[int] = Field(default=24)

    doc_field: DocField = Relationship(back_populates="radios")


class Signatory(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str = Field(
        sa_column=SAEnum("signer", "viewer", "approver", name="role_types")
    )
    signing_order: int
    signed_at: Optional[datetime] = None
    signature_image: Optional[str] = None
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = Field(
        default=None, description="Phone number in E.164 format (e.g., +123456789)"
    )
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    creator_id: int = Field(default=None, foreign_key="user.id")

    user: Optional[User] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Signatory.user_id"}
    )
    creator: User = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Signatory.creator_id"},
        back_populates="signatories"
    )
    fields: List[DocField] = Relationship(back_populates="signatory")
    signature_requests: List["SignatureRequest"] = Relationship(
        back_populates="signatories",
        link_model=RequestSignatoryLink
    )


class ReminderSettings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    interval_in_days: int
    max_occurrences: int
    timezone: Optional[str] = None
    request_id: Optional[int] = Field(foreign_key="signaturerequest.id")
    request: "SignatureRequest" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "ReminderSettings.request_id"}
    )


class SignatureRequest(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: SignatureRequestStatus = Field(
        default=SignatureRequestStatus.DRAFT, sa_column=SAEnum(SignatureRequestStatus)
    )
    name: str
    delivery_mode: str
    message: Optional[str] = None
    expiry_date: Optional[datetime] = None
    ordered_signers: bool = Field(default=False)
    sender_id: int = Field(foreign_key="user.id")

    sender: User = Relationship()
    documents: List[Document] = Relationship(
        back_populates="signature_requests",
        link_model=RequestDocumentLink
    )
    signatories: List[Signatory] = Relationship(
        back_populates="signature_requests",
        link_model=RequestSignatoryLink
    )
    audit_logs: List["AuditLog"] = Relationship(back_populates="signature_request")
    reminder_settings: Optional[ReminderSettings] = Relationship(
        back_populates="request"
    )


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


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int = Field(default=None, foreign_key="user.id", nullable=False)
    # owner: "User" = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemOut(ItemBase):
    id: int
    owner_id: int


class ItemsOut(SQLModel):
    data: list[ItemOut]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str
