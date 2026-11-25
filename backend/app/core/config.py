
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "APEXIVEAI ENTERPRISE OS"
    app_version: str = "1.0.0"
    environment: str = "development"

    database_url: str = "sqlite:///./apexiveai.db"
    redis_url: str | None = None

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value):
        if not value:
            return "sqlite:///./apexiveai.db"

        if isinstance(value, str):
            replacements = (
                ("postgres://", "postgresql+psycopg://"),
                ("postgresql://", "postgresql+psycopg://"),
                ("postgresql+psycopg2://", "postgresql+psycopg://"),
            )

            for old, new in replacements:
                if value.startswith(old):
                    return value.replace(old, new, 1)

        return value

    @field_validator("redis_url", mode="before")
    @classmethod
    def normalize_redis_url(cls, value):
        if value is None or not str(value).strip():
            return None
        return str(value).strip()


settings = Settings()
