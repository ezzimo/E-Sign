from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator

from app.models.user_model import UserBase  # noqa


# Base schema for common user fields
class UserBaseSchema(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    is_active: bool = Field(default=True, description="Is user active?")
    is_superuser: bool = Field(default=False, description="Is user a superuser?")


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
