# signature_request_schema.py
from datetime import datetime

from pydantic import BaseModel

from app.schemas.field_schema import FieldCreate
from app.schemas.signatory_schema import SignatoryBase


class ReminderSettingsSchema(BaseModel):
    interval_in_days: int
    max_occurrences: int
    timezone: str | None = None


class SignatureRequestBase(BaseModel):
    name: str
    delivery_mode: str
    ordered_signers: bool
    reminder_settings: ReminderSettingsSchema | None = None
    expiration_date: datetime | None = None
    message: str | None = None
    expiry_date: datetime | None = None


class SignatureRequestCreate(SignatureRequestBase):
    signatories: list["SignatoryData"]
    documents: list[int]


class SignatureRequestRead(SignatureRequestBase):
    id: int
    sender_id: int
    created_at: datetime
    updated_at: datetime


class SignatureRequestUpdate(BaseModel):
    pass


class SignatoryData(BaseModel):
    info: SignatoryBase
    fields: list["FieldCreate"]

    class Config:
        from_attributes = True
