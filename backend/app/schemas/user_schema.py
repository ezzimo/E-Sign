from datetime import datetime

from pydantic import BaseModel, EmailStr, validator
from sqlmodel import SQLModel


# Base user schema reflects shared attributes between different user operations
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool | None = True
    is_superuser: bool | None = False
    full_name: str | None = None
    first_name: str
    last_name: str
    company: str | None = None
    role: str | None = None  # Consider using Enum for predefined roles


# Schema for user creation requests includes password
class UserCreate(UserBase):
    password: str

    @validator("password")
    def validate_password(cls, v):
        # Implement password validation logic here
        return v


# Schema for updating user data; all fields are optional
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    company: str | None = None
    role: str | None = None


# Output schema for returning user data; includes fields not modifiable by the user
class UserOut(UserBase):
    id: int | None = None
    created_at: datetime
    updated_at: datetime


# Schema for returning lists of users; includes count for pagination or metadata purposes
class UsersOut(SQLModel):
    data: list[UserOut]
    count: int


# Schema for public user registration without authentication
class UserCreateOpen(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    first_name: str
    last_name: str
    company: str | None = None
    role: str  # This could be set to a default or omitted based on your app logic

    @validator("password")
    def validate_password(cls, v):
        # Implement password validation logic here
        return v


# Schema for updating the current user's own information, omitting sensitive fields
class UserUpdateMe(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    company: str | None = None
    # Not including 'role' or 'is_superuser' as those shouldn't be self-updated


# Schema for updating a user's password
class UpdatePassword(BaseModel):
    current_password: str
    new_password: str

    @validator("new_password")
    def validate_new_password(cls, v, values, **kwargs):
        # Implement password validation logic here
        # You might want to ensure that new_password is different from current_password
        return v
