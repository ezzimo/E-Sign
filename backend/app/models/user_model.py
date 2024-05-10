from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship
from .document_model import Document


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

    documents: Document = Relationship(back_populates="owner")
