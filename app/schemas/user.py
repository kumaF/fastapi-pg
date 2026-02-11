import re

from datetime import datetime

import ulid

from pydantic import (
    EmailStr,
    Field,
    field_validator,
)

from app.configs.core import settings
from app.schemas.base import BaseSchema
    

class UserCredentialsSchema(BaseSchema):
    identifier: str = Field(...)
    password: str = Field(...)


class BaseUserSchema(BaseSchema):
    username: str = Field(...)
    email: EmailStr = Field(...)


class SignupUserSchema(BaseUserSchema):
    password: str = Field(...)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):
        if not re.match(settings.password_regex, v):
            msg: str = (
                "Password must be at least 8 characters long, include an uppercase letter, "
                "a lowercase letter, a number, and a special character."
            )
            raise ValueError(msg)
        
        return v
    

class UserSchema(BaseUserSchema):
    id: str = Field(default_factory=lambda: ulid.new().str)
    is_active: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    is_deleted: bool = Field(default=False)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)