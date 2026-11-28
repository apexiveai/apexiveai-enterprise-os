
from pathlib import Path

from pydantic import field_validator
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "ApexiveAI Enterprise OS"
    app_version: str = "1.0.0"
    environment: str = Field(
        default="development",
        validation_alias=AliasChoices("ENVIRONMENT", "APP_ENV"),
    )
    auto_create_tables: bool = False
    temporal_address: str = "localhost:7233"
    temporal_task_queue: str = "apexive.enterprise.processes"

    database_url: str = "sqlite:///./apexiveai.db"
    redis_url: str | None = None
    cors_origins: str = Field(
        default="",
        validation_alias=AliasChoices("CORS_ORIGINS", "BACKEND_CORS_ORIGINS"),
    )
    model_gateway_url: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MODEL_GATEWAY_URL", "OPENAI_BASE_URL"),
    )
    model_gateway_api_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("MODEL_GATEWAY_API_KEY", "OPENAI_API_KEY"),
    )
    model_gateway_default_model: str = Field(
        default="gpt-4o-mini",
        validation_alias=AliasChoices("MODEL_GATEWAY_DEFAULT_MODEL", "AI_MODEL"),
    )
    model_gateway_timeout_seconds: float = 30.0
    model_gateway_fallback_urls: str | None = None
    object_storage_path: Path = PROJECT_ROOT / "data" / "objects"

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

    @field_validator("model_gateway_url", mode="before")
    @classmethod
    def normalize_model_gateway_url(cls, value):
        if value is None or not str(value).strip():
            return None
        return str(value).strip().rstrip("/")

    @field_validator("model_gateway_api_key", mode="before")
    @classmethod
    def normalize_model_gateway_api_key(cls, value):
        if value is None or not str(value).strip():
            return None
        return str(value).strip()

    @field_validator("model_gateway_fallback_urls", mode="before")
    @classmethod
    def normalize_model_gateway_fallback_urls(cls, value):
        if value is None or not str(value).strip():
            return None
        urls = [item.strip().rstrip("/") for item in str(value).split(",") if item.strip()]
        return ",".join(urls) or None

    @field_validator("object_storage_path", mode="before")
    @classmethod
    def normalize_object_storage_path(cls, value):
        if value is None or not str(value).strip():
            return PROJECT_ROOT / "data" / "objects"
        return Path(value).expanduser()


settings = Settings()
