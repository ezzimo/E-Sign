from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator

from .field_schema import FieldCreate


# Base schema for signatories
class SignatoryBase(BaseModel):
    first_name: str = Field(..., description="First name of the signatory")
    last_name: str = Field(..., description="Last name of the signatory")
    email: EmailStr = Field(..., description="Email of the signatory")
    phone_number: str = Field(..., description="Phone number in E.164 format")
    signing_order: int = Field(..., description="Order in which the signatory signs")
    role: str = Field(..., description="Last name of the signatory")

    @validator("phone_number")
    def validate_phone_number(cls, value):
        import re

        if not re.match(r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$", value):
            raise ValueError("Phone number must be in E.164 format.")
        return value

    class Config:
        from_attributes = True


# Schema for creating a new signatory
class SignatoryCreate(SignatoryBase):
    fields: list[FieldCreate] = Field(..., description="Fields for this signatory")


# Schema for updating an existing signatory
class SignatoryUpdate(SignatoryBase):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    signing_order: int | None = None
    signature_image: str | None = None
    signed_at: datetime | None = None


# Schema for returning signatory details
class SignatoryOut(SignatoryBase):
    id: int = Field(..., description="Unique ID of the signatory")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: datetime = Field(..., description="Last update time")
    signed_at: datetime | None = None

    class Config:
        from_attributes = True  # Allows compatibility with SQLModel
