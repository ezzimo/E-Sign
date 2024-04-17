from datetime import datetime

from pydantic import BaseModel


class SignatureRequestBase(BaseModel):
    document_id: int
    message: str | None = None
    expiry_date: datetime | None = None


class SignatureRequestCreate(SignatureRequestBase):
    signatory_id: int


class SignatureRequestRead(SignatureRequestBase):
    id: int
    sender_id: int
    signatory_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SignatureRequestUpdate(BaseModel):
    document_id: int | None = None
    message: str | None = None
    expiry_date: datetime | None = None

    class Config:
        from_attributes = True
