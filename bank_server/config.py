from pydantic_settings import BaseSettings
from pydantic import SecretStr


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


config = Settings()