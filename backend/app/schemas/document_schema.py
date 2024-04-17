from datetime import datetime

from pydantic import BaseModel

from app.models.document_model import DocumentStatus

from .user_schema import UserOut


class DocumentBase(BaseModel):
    title: str
    file: str
    status: DocumentStatus

    class Config:
        from_attributes = True


class DocumentSchema(DocumentBase):
    # Lazy import to avoid circular reference
    def __init__(self, **data):
        super().__init__(**data)
        from app.schemas.signatory_schema import SignatoryBase

        self.signatories: list[SignatoryBase] = []


class DocumentCreate(DocumentSchema):
    pass


class DocumentsOut(DocumentSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    owner: UserOut


class DocumentUpdate(BaseModel):
    title: str | None = None
    file: str | None = None
    status: DocumentStatus | None = None
