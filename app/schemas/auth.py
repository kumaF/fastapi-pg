from pydantic import (
    Field,
    model_validator,
)

from app.schemas.base import BaseSchema
from app.schemas.enums import GrantType
from app.schemas.user import UserCredentialsSchema


class LoginRequestSchema(BaseSchema):
    grant_type: GrantType = Field(...)
    credentials: UserCredentialsSchema | None = Field(default=None)
    refresh_token: str | None = Field(default=None)

    @model_validator(mode='after')
    def validate_login_request(self):
        if self.grant_type == GrantType.PASSWORD and self.credentials is None:
            msg: str = "The 'credentials' object is required when 'grant_type' is 'password'."
            raise ValueError(msg)
        
        if self.grant_type == GrantType.REFRESH_TOKEN and self.refresh_token is None:
            msg: str = "The 'refresh_token' field is required when 'grant_type' is 'refresh_token'."
            raise ValueError(msg)

        return self