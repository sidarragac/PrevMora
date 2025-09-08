from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Service Template"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    
    # WhatsApp settings
    WA_PHONE_ID: str = "800388773155876"
    WA_LANG: str = "es_MX"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"  # Ignorar campos extra en lugar de rechazarlos
    )


settings = Settings()

