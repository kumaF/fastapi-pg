from pydantic import Field

from app.schemas.base import BaseSchema


class DetailedError(BaseSchema):
    status_code: int
    message: str
    errors: list = Field(default=None)


__all__ = [
    'DetailedError',
]