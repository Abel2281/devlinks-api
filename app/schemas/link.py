import re
from datetime import datetime

from pydantic import BaseModel, field_validator


class LinkCreate(BaseModel):
    title: str
    url: str
    order: int = 0
    is_active: bool = True

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if len(v.strip()) < 1 or len(v) > 100:
            raise ValueError("Title must be between 1 and 100 characters")
        return v.strip()

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if re.match(r"^javascript:", v, re.IGNORECASE):
            raise ValueError("URL cannot use javascript: protocol")
        if not re.match(r"^https?://", v):
            raise ValueError("URL must start with http:// or https://")
        if len(v) > 500:
            raise ValueError("URL must not exceed 500 characters")
        return v.strip()


class LinkUpdate(BaseModel):
    title: str | None = None
    url: str | None = None
    order: int | None = None
    is_active: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str | None) -> str | None:
        if v is not None:
            if len(v.strip()) < 1 or len(v) > 100:
                raise ValueError("Title must be between 1 and 100 characters")
            return v.strip()
        return v

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str | None) -> str | None:
        if v is not None:
            if re.match(r"^javascript:", v, re.IGNORECASE):
                raise ValueError("URL cannot use javascript: protocol")
            if not re.match(r"^https?://", v):
                raise ValueError("URL must start with http:// or https://")
            if len(v) > 500:
                raise ValueError("URL must not exceed 500 characters")
            return v.strip()
        return v


class LinkResponse(BaseModel):
    id: str
    title: str
    url: str
    order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}