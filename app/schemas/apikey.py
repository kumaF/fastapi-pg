from datetime import datetime

from pydantic import (
    Field,
    field_validator,
)

from app.core.security import generate_api_key
from app.schemas.base import BaseSchema
from app.utils.helpers import clean_text


ALLOWED_SERVICES: list[str] = [
    'frontend-svc',
    'backend-svc',
]


class BaseApiKeySchema(BaseSchema):
    service_name: str = Field(...)

    @field_validator('service_name')
    @classmethod
    def validate_service_name(cls, v: str):
        err_msg: str = ''

        if v.strip() == '':
            err_msg = 'Category service_name cannot be empty.'
            raise ValueError(err_msg)

        if not v.endswith('-svc'):
            err_msg = 'service_name must end with "-svc"'
            raise ValueError(err_msg)

        if v not in ALLOWED_SERVICES:
            err_msg = f'service_name must be one of: {ALLOWED_SERVICES}'
            raise ValueError(err_msg)

        return clean_text(v)


class RequestApiKeySchema(BaseApiKeySchema):
    api_key: str = Field(default_factory=generate_api_key)


class ResponseApiKeySchema(RequestApiKeySchema):
    id: str = Field(...)
    is_active: bool = Field(...)
    scopes: list[str] = Field(...)
    last_used_at: datetime | None = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
