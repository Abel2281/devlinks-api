import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    display_name: str
    password: str
    bio: str | None = None
    profile_image_url: str | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]{3,50}$", v):
            raise ValueError(
                "Username must be 3-50 characters, alphanumeric and underscores only"
            )
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, v: str) -> str:
        if len(v.strip()) < 1 or len(v) > 100:
            raise ValueError("Display name must be between 1 and 100 characters")
        return v.strip()


class UserUpdate(BaseModel):
    display_name: str | None = None
    bio: str | None = None
    profile_image_url: str | None = None


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    display_name: str
    bio: str | None = None
    profile_image_url: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserPublic(BaseModel):
    username: str
    display_name: str
    bio: str | None = None
    profile_image_url: str | None = None

    model_config = {"from_attributes": True}