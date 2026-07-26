"""FastAPI application configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or defaults."""

    app_name: str = "HumanOS API Server"
    app_version: str = "0.1.0"
    debug: bool = False

    api_prefix: str = "/v1"
    secret_key: str = "humanos_secret_key_change_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(env_prefix="HUMANOS_")


settings = Settings()
