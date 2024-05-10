import enum
from datetime import datetime
# from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, Relationship, SQLModel

# if TYPE_CHECKING:
# from .document_model import Document
# from .signature_request_model import SignatureRequest


class FieldType(enum.Enum):
    SIGNATURE = "signature"
    MENTION = "mention"
    TEXT = "text"
    CHECKBOX = "checkbox"
    RADIO_GROUP = "radio_group"
    READ_ONLY_TEXT = "read_only_text"


class DocFieldBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    type: FieldType = Field(sa_column=SAEnum(FieldType))
    page: int
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    x: int | None = None
    y: int | None = None
    height: int | None = None
    width: int | None = None


class DocField(DocFieldBase, table=True):
    document_id: int = Field(foreign_key="document.id")
    signature_request_id: int = Field(foreign_key="signaturerequest.id")
    signer_id: int | None = Field(default=None, foreign_key="signatory.id")

    # document: "Document" = Relationship(back_populates="signature_fields")
    # signature_request: "SignatureRequest" = Relationship(back_populates="fields")

    optional: bool | None = Field(default=None)
    checked: bool | None = Field(default=None)
    mention: str | None = Field(default=None)
    name: str | None = Field(default=None)
    max_length: int | None = Field(default=None)
    question: str | None = Field(default=None)
    instruction: str | None = Field(default=None)
    text: str | None = Field(default=None)

    radios: list["Radio"] = Relationship(back_populates="doc_field")


class Radio(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    field_id: int = Field(foreign_key="docfield.id")
    name: str
    x: int
    y: int
    size: int | None = Field(default=24)

    doc_field: DocField = Relationship(back_populates="radios")
