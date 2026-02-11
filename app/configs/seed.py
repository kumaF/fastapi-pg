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

    email: str = Field(validation_alias='SEED_USER_EMAIL')
    username: str = Field(validation_alias='SEED_USER_USERNAME')
    password: str = Field(validation_alias='SEED_USER_PASSWORD')


settings = Settings()  # type: ignore[missing-arguments]
