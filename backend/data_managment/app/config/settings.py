from pydantic_settings import BaseSettings
from decouple import Config, RepositoryEnv

import logging
import pathlib

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.resolve()
ENV_PATH: pathlib.Path = ROOT_DIR / ".env"

config = Config(RepositoryEnv(str(ENV_PATH)))

class BackendBaseSettings(BaseSettings):
    # Basic application settings
    APP_NAME: str = config("APP_NAME", default="PrevMora-Template")
    APP_VERSION: str = config("APP_VERSION", default="0.1.0")
    TIMEZONE: str = config("TIMEZONE", default="UTC-05")
    DESCRIPTION: str | None = None
    DEBUG: bool = config("DEBUG", cast=bool, default=False)
    ENVIRONMENT: str = config("ENVIRONMENT", default="local")

    # Server configuration
    SERVER_HOST: str = config("BACKEND_SERVER_HOST", cast=str)
    SERVER_PORT: int = config("BACKEND_SERVER_PORT", cast=int)
    SERVER_WORKERS: int = config("BACKEND_SERVER_WORKERS", cast=int, default=1)
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    # CORS Configuration
    IS_ALLOWED_CREDENTIALS: bool = config("IS_ALLOWED_CREDENTIALS", cast=bool)

    # Logging Configuration
    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    # JWT Configuration
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", default="change-me")
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", default="HS256")
    JWT_ACCESS_TOKEN_EXPIRATION_TIME: int = config(
        "JWT_ACCESS_TOKEN_EXPIRATION_TIME", 
        default=60, 
        cast=int
    )

    class Config:
        case_sensitive = True
        env_file = f"{ROOT_DIR}/.env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    # Begin Cors dinamic configuration
    @property
    def allowed_origins(self) -> list[str]:
        if self.ENVIRONMENT == "local" or self.ENVIRONMENT == "development":
            return ["*"]
        else:
            origins_str = config("ALLOWED_ORIGINS", default="")
            if origins_str:
                return [origin.strip() for origin in origins_str.split(",")]
            else:
                raise ValueError("ALLOWED_ORIGINS is not set properly or empty in the environment variables.")

    @property
    def allowed_methods(self) -> list[str]:
        if self.ENVIRONMENT in ["local", "development"] or self.DEBUG:
            # Allow all on development
            return ["*"]
        else:
            return ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    
    @property
    def allowed_headers(self) -> list[str]:
        if self.ENVIRONMENT in ["local", "development"] or self.DEBUG:
            # Allow all headers on development
            return ["*"]
        else:
            # Change to specific headers for production
            return [
                "Authorization",
                "Content-Type", 
                "X-Requested-With",
                "Accept",
                "Origin"
            ]
        
    @property
    def cors_config(self) -> dict:
        return {
            "allow_origins": self.allowed_origins,
            "allow_credentials": self.IS_ALLOWED_CREDENTIALS,
            "allow_methods": self.allowed_methods,
            "allow_headers": self.allowed_headers,
        }
    # End Cors dinamic configuration

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

settings = BackendBaseSettings()
