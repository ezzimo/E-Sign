from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ValidationError, validator

from ..models.models import (  # noqa
    AuditLogAction,
    DocumentSignatureDetails,
    DocumentStatus,
    FieldType,
    SignatureRequestStatus,
    UserBase,
)


# Base schema for common user fields
class UserBaseSchema(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    is_active: bool = Field(default=True, description="Is user active?")
    is_superuser: bool = Field(default=False, description="Is user a superuser?")

    class Config:
        from_attributes = True


# Schema for creating a new user
class UserCreate(UserBaseSchema):
    password: str = Field(..., min_length=8, description="User's password")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    role: str | None = Field(None, description="User's role")

    @validator("password")
    def validate_password_strength(cls, value):
        # Implement password strength validation logic if needed
        return value

    class Config:
        from_attributes = True


# Schema for updating an existing user
class UserUpdate(UserBaseSchema):
    full_name: str | None = Field(None, description="User's full name")
    company: str | None = Field(None, description="User's company")
    role: str | None = Field(None, description="User's role")


# Schema for returning user details
class UserOut(UserBaseSchema):
    id: int = Field(..., description="User's unique ID")
    full_name: str | None = Field(None, description="User's full name")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True  # Allows conversion from SQLModel to Pydantic


# Schema for returning lists of users with a count for pagination or metadata
class UsersOut(BaseModel):
    data: list[UserOut]
    count: int


# Schema for public user registration without authentication
class UserCreateOpen(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User's password")
    full_name: str | None = Field(None, description="User's full name")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    company: str | None = Field(None, description="User's company")
    role: str | None = Field(None, description="User's role")

    @validator("password")
    def validate_password(cls, value):
        # Validate password strength, uniqueness, or other criteria
        return value


# Schema for updating a user's own information
class UserUpdateMe(BaseModel):
    email: EmailStr | None = Field(None, description="User email")
    full_name: str | None = Field(None, description="User's full name")
    first_name: str | None = Field(None, description="User's first name")
    last_name: str | None = Field(None, description="User's last name")
    company: str | None = Field(None, description="User's company")

    class Config:
        from_attributes = True


# Schema for updating a user's password
class UpdatePassword(BaseModel):
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")

    @validator("new_password")
    def validate_new_password(cls, value, values):
        # Ensure new password is different from the current password
        if "current_password" in values and value == values["current_password"]:
            raise ValueError("New password must be different from current password.")
        return value


class DocumentBase(BaseModel):
    title: str = Field(..., description="Title of the document")
    file: str = Field(..., description="File path or identifier")
    file_url: str | None = Field(None, description="URL to view the document")
    status: DocumentStatus = Field(..., description="Current status of the document")
    deleted: bool = Field(..., description="Set to 'True' when a Document is deleted")

    class Config:
        from_attributes = True


class DocumentCreate(DocumentBase):
    owner_id: int | None = Field(None, description="Owner ID of the document")


class DocumentUpdate(BaseModel):
    title: str | None = Field(None, description="New title for the document")
    status: DocumentStatus | None = Field(
        None, description="New status of the document"
    )
    file: str | None = Field(None, description="Updated file for the document")
    file_url: str | None = Field(None, description="URL to view the document")

    class Config:
        from_attributes = True


class DocumentSignatureDetailsBase(BaseModel):
    document_id: int = Field(..., description="The document's unique identifier")
    signed_hash: str = Field(..., description="SHA-256 hash of the signed document")
    timestamp: datetime = Field(
        ..., description="The time when the document was signed"
    )
    certified_timestamp: str | None = Field(
        None, description="Certified timestamp if available"
    )
    ip_address: str | None = Field(None, description="IP address of the signer")

    class Config:
        from_attributes = True


class DocumentSignatureDetailsCreate(DocumentSignatureDetailsBase):
    pass


class DocumentSignatureDetailsOut(DocumentSignatureDetailsBase):
    id: int


class DocumentOut(DocumentBase):
    id: int = Field(..., description="Unique identifier for the document")
    created_at: datetime = Field(
        ..., description="Timestamp when the document was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the document was last updated"
    )
    owner: UserOut = Field(..., description="User information of the owner")
    signature_details: DocumentSignatureDetailsOut | None = None

    @validator("file_url")
    def validate_file_url(cls, value):
        # TODO Perform validation or sanitization
        return value

    class Config:
        from_attributes = True


class FieldBase(BaseModel):
    type: FieldType
    page: int

    class Config:
        from_attributes = True


class RadioCreate(BaseModel):
    name: str
    x: int
    y: int
    size: int | None = Field(default=24)

    class Config:
        from_attributes = True


class FieldCreate(FieldBase):
    x: int | None = None
    y: int | None = None
    height: int | None = None
    width: int | None = None
    optional: bool | None = None
    mention: str | None = None
    name: str | None = None
    checked: bool | None = None
    document_id: int | None = None
    signature_request_id: int | None = None
    signer_id: int | None = None
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


class FieldOut(FieldBase):
    id: int
    signer_id: int | None = None
    document_id: int | None = None
    signature_request_id: int | None = None
    created_at: datetime
    updated_at: datetime

    radios: list[RadioCreate] | None = None


class FieldUpdate(FieldCreate):
    pass


class SignatoryBase(BaseModel):
    first_name: str = Field(..., description="First name of the signatory")
    last_name: str = Field(..., description="Last name of the signatory")
    email: EmailStr = Field(..., description="Email of the signatory")
    phone_number: str = Field(..., description="Phone number in E.164 format")
    signing_order: int = Field(..., description="Order in which the signatory signs")
    role: str = Field(..., description="Role of the signatory")

    @validator("phone_number")
    def validate_phone_number(cls, value):
        import re

        if not re.match(r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$", value):
            raise ValueError("Phone number must be in E.164 format.")
        return value

    class Config:
        from_attributes = True


class SignatoryCreate(SignatoryBase):
    fields: list[FieldCreate] = Field(..., description="Fields for this signatory")


class SignatoryUpdate(SignatoryBase):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    role: str | None = None
    signing_order: int | None = None
    signature_image: str | None = None
    signed_at: datetime | None = None


class SignatoryOut(SignatoryBase):
    id: int = Field(..., description="Unique ID of the signatory")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: datetime = Field(..., description="Last update time")
    signed_at: datetime | None = None
    fields: list[FieldCreate] = Field(..., description="Fields for this signatory")


class ReminderSettingsSchema(BaseModel):
    interval_in_days: int
    max_occurrences: int
    timezone: str | None = None

    class Config:
        from_attributes = True


class SignatureRequestBase(BaseModel):
    name: str
    delivery_mode: str
    ordered_signers: bool
    require_otp: bool = True
    reminder_settings: ReminderSettingsSchema | None = None
    expiry_date: datetime | None = None
    message: str | None = None
    token: str | None = Field(None, description="Token to get the Iframe for Signature")
    deleted: bool = Field(..., description="Set to 'True' when a Signature request is deleted")

    class Config:
        from_attributes = True


class SignatureRequestCreate(SignatureRequestBase):
    signatories: list["SignatoryData"]
    documents: list[int]

    class Config:
        from_attributes = True


class SignatureRequestRead(SignatureRequestBase):
    id: int
    status: SignatureRequestStatus
    sender_id: int
    created_at: datetime
    updated_at: datetime
    documents: list[DocumentOut]
    signatories: list[SignatoryOut]

    class Config:
        from_attributes = True


class SignatureRequestUpdate(BaseModel):
    name: str | None = None
    delivery_mode: str | None = None
    ordered_signers: bool | None = None
    reminder_settings: ReminderSettingsSchema | None = None
    expiry_date: datetime | None = None
    message: str | None = None
    signatories: list["SignatoryData"] | None = None
    documents: list[int] | None = None

    class Config:
        from_attributes = True


class SignatoryData(BaseModel):
    info: SignatoryBase
    fields: list["FieldCreate"]

    class Config:
        from_attributes = True


class AuditLogBase(BaseModel):
    description: str | None
    ip_address: str | None
    action: AuditLogAction
    signature_request_id: int | None

    class Config:
        from_attributes = True


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogRead(AuditLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
