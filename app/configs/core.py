from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', '.env.local'),
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=True,
    )

    token_algorithm: str = Field(default='ES256')
    password_regex: str = Field(
        default=r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
    )

    logger_name: str = Field(
        validation_alias='LOGGER_NAME',
        default='uvicorn',
    )
    request_id_ctx_key: str = Field(
        validation_alias='REQUEST_ID_CTX_KEY',
        default='request_id',
    )
    access_token_exp_delta: int = Field(
        validation_alias='ACCESS_TOKEN_EXP_DELTA',
        default=60 * 24,  # in minutes
    )
    refresh_token_exp_delta: int = Field(
        validation_alias='REFRESH_TOKEN_EXP_DELTA',
        default=60 * 24 * 30,  # in minutes
    )
    cursor_exp_delta: int = Field(
        validation_alias='CURSOR_EXP_DELTA',
        default=60 * 24,  # in minutes
    )
    token_issuer: str = Field(
        validation_alias='TOKEN_ISSUER',
        default='auth:appname',
    )
    token_audience: str = Field(
        validation_alias='TOKEN_ISSUER',
        default='api:appname',
    )
    apikey_name: str = Field(
        validation_alias='API_KEY_NAME',
        default='X-API-KEY'
    )

    public_key: str = Field(validation_alias='PUBLIC_KEY')
    private_key: str = Field(validation_alias='PRIVATE_KEY')
    secret_key: str = Field(validation_alias='SECRET_KEY')


settings = Settings()  # type: ignore[missing-arguments]
