from datetime import datetime

from pydantic import BaseModel, Field, ValidationError

from app.models.field_model import FieldType


class FieldBase(BaseModel):
    type: FieldType
    page: int


class RadioCreate(BaseModel):
    name: str
    x: int
    y: int
    size: int | None = Field(default=24)


class FieldCreate(FieldBase):
    signer_id: int | None = None
    document_id: str | None = None
    x: int | None = None
    y: int | None = None
    height: int | None = None
    width: int | None = None
    optional: bool | None = None
    mention: str | None = None
    name: str | None = None
    checked: bool | None = None
    max_length: int | None = None
    question: str | None = None
    instruction: str | None = None
    text: str | None = None
    radios: list[RadioCreate] | None = None

    def validate_fields(self):
        # Check if the field type is either 'checkbox' or 'radio_group'
        if self.type in {"checkbox", "radio_group"}:
            # Ensure x, y, height, and width aren't set
            if self.x or self.y or self.height or self.width:
                raise ValidationError(
                    f"Fields 'x', 'y', 'height', and 'width' are not allowed for type '{self.type}'."
                )

        # Ensure all radios are valid ORM objects
        if self.type == FieldType.RADIO_GROUP and self.radios:
            for radio in self.radios:
                if not isinstance(radio, RadioCreate):
                    raise ValueError("Radio fields must be valid Radio ORM objects.")

    class Config:
        from_attributes = True


class FieldOut(FieldBase):
    id: int
    signer_id: int | None = None
    document_id: int | None = None
    signature_request_id: int | None = None
    created_at: datetime
    updated_at: datetime

    radios: list[RadioCreate] | None = None

    class Config:
        from_attributes = True


class FieldUpdate(FieldCreate):
    pass
