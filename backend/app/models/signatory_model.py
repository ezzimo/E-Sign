from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Enum
from sqlmodel import Field, Relationship, SQLModel

from .requests_signatories_link_model import RequestSignatoryLink
from .user_model import User

if TYPE_CHECKING:
    from .signature_request_model import SignatureRequest


class SignatoryBase(SQLModel):
    id: int = Field(default=None, primary_key=True)
    role: str = Field(sa_column=Enum("signer", "viewer", "approver", name="role_types"))
    signing_order: int
    signed_at: datetime | None = None
    signature_image: str | None = None
    first_name: str
    last_name: str
    email: str
    phone_number: str | None = Field(
        default=None,
        description="Phone number in E.164 format (e.g., +123456789)",
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Signatory(SignatoryBase, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id")
    creator_id: int = Field(default=None, foreign_key="user.id")
    signature_requests: list["SignatureRequest"] = Relationship(
        back_populates="signatories", link_model=RequestSignatoryLink
    )
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Signatory.user_id]"},
    )
    creator: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Signatory.creator_id]"},
    )
