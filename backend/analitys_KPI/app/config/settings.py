import logging  # para manejar los logs o mensajes de error

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(
    level=logging.INFO,  # nivel mínimo que quieres mostrar (DEBUG, INFO, WARNING, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Stats2Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = Field(default="AnalyticsKPIService", env="APP_NAME")
    APP_VERSION: str = Field(default="0.1.0", env="APP_VERSION")
    TIMEZONE: str = Field(default="UTC-05", env="TIMEZONE")
    DESCRIPTION: str = Field(
        default="Stats2 microservice for PrevMora", env="DESCRIPTION"
    )
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="local", env="ENVIRONMENT")
    LOG_LEVEL: str = Field(default="DEBUG", env="LOG_LEVEL")

    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    # Database
    DB_DRIVER: str = Field(default="mssql+aioodbc", env="DB_DRIVER")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")
    DB_PORT: int = Field(default=1433, env="DB_PORT")
    DB_NAME: str = Field(..., env="DB_NAME")

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=yes"

    @property
    def fast_kwargs(self) -> dict:
        return {
            "title": self.APP_NAME,
            "version": self.APP_VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL if self.DEBUG else None,
            "openapi_url": self.OPENAPI_URL if self.DEBUG else None,
            "redoc_url": self.REDOC_URL if self.DEBUG else None,
        }


settings = Stats2Settings()
