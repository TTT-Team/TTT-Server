from datetime import timedelta

from pydantic_settings import BaseSettings
from pydantic import SecretStr, field_validator


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # Project
    SECRET_KEY: SecretStr

    # Database
    NAME: str
    USER: str
    PASSWORD: SecretStr
    HOST: str
    PORT: str

    # JWT
    ACCESS_TOKEN_LIFETIME: timedelta
    REFRESH_TOKEN_LIFETIME: timedelta
    ALGORITHM: str
    AUTH_HEADER_TYPE: str

    @field_validator("ACCESS_TOKEN_LIFETIME", "REFRESH_TOKEN_LIFETIME", mode='before')
    def parse_timedelta(cls, value):
        """Конвертация значения из минут в timedelta."""
        return timedelta(minutes=int(value))


config = Settings()