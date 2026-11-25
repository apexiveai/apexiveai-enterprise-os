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

    app_name: str = "APEXIVEAI-ENTERPRISE-OS"
    app_version: str = "1.0.0"
    environment: str = "development"

    database_url: str
    redis_url: str

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if isinstance(value, str):
            if value.startswith("postgres://"):
                return value.replace(
                    "postgres://",
                    "postgresql+psycopg://",
                    1,
                )

            if value.startswith("postgresql://"):
                return value.replace(
                    "postgresql://",
                    "postgresql+psycopg://",
                    1,
                )

            if value.startswith("postgresql+psycopg2://"):
                return value.replace(
                    "postgresql+psycopg2://",
                    "postgresql+psycopg://",
                    1,
                )

        return value


settings = Settings()
