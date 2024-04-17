from datetime import datetime

from pydantic import BaseModel


class SignatoryBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    signer_id: int
    creator_id: int
    signing_order: int
    signature_image: str | None = None

    class Config:
        from_attributes = True


class SignatorySchema(SignatoryBase):
    # Remove the direct document reference
    pass


class SignatoryCreate(SignatorySchema):
    pass


class SignatoryUpdate(SignatorySchema):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    signing_order: int | None = None
    signature_image: str | None = None
    signed_at: datetime | None = None


class SignatoryOut(SignatorySchema):
    id: int
    signed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
