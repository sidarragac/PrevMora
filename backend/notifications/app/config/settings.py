import logging
import pathlib

from decouple import Config, RepositoryEnv
from pydantic_settings import BaseSettings

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.resolve()
ENV_PATH: pathlib.Path = ROOT_DIR / ".env"

config = Config(RepositoryEnv(str(ENV_PATH)))


class NotificationsSettings(BaseSettings):
    APP_NAME: str = config("APP_NAME", default="PrevMora-Notifications")
    APP_VERSION: str = config("APP_VERSION", default="0.1.0")
    TIMEZONE: str = config("TIMEZONE", default="UTC-05")
    DESCRIPTION: str = config("DESCRIPTION", default="Notifications microservice for PrevMora")
    DEBUG: bool = config("DEBUG", cast=bool, default=False)
    ENVIRONMENT: str = config("ENVIRONMENT", default="local")
    LOG_LEVEL: str = config("LOG_LEVEL", default="DEBUG")

    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    # Database - reusing the same database as credit_management
    DB_DRIVER: str = config("DB_DRIVER", default="mssql+aioodbc")
    DB_USER: str = config("DB_USER")
    DB_PASSWORD: str = config("DB_PASSWORD")
    DB_HOST: str = config("DB_HOST")
    DB_PORT: int = config("DB_PORT", cast=int, default=1433)
    DB_NAME: str = config("DB_NAME")

    class Config:
        case_sensitive = True
        env_file = f"{ROOT_DIR}/.env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=yes"

    @property
    def fastapi_kwargs(self) -> dict:
        return {
            "title": self.APP_NAME,
            "version": self.APP_VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL if self.DEBUG else None,
            "openapi_url": self.OPENAPI_URL if self.DEBUG else None,
            "redoc_url": self.REDOC_URL if self.DEBUG else None,
        }


settings = NotificationsSettings()
