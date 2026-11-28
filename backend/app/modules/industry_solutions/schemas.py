from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


IndustrySolutionKey = Literal[
    "construction",
    "manufacturing",
    "energy",
    "trading",
    "hotels",
    "agro",
    "highway",
    "logistics",
]
IndustryRecordStatus = Literal["open", "in_progress", "completed", "cancelled"]


class IndustryRecordCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=250)
    payload: dict[str, str] = Field(min_length=1, max_length=20)

    @field_validator("tenant_id", "actor_id", "title")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("This value cannot be blank.")
        return normalized

    @field_validator("payload")
    @classmethod
    def validate_payload(cls, value: dict[str, str]) -> dict[str, str]:
        normalized: dict[str, str] = {}
        for key, item in value.items():
            field_name = key.strip()
            field_value = item.strip()
            if not field_name or not field_value:
                raise ValueError("Record fields cannot be blank.")
            if len(field_name) > 80 or len(field_value) > 1000:
                raise ValueError("Record field names or values exceed the allowed length.")
            normalized[field_name] = field_value
        return normalized


class IndustryRecordStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)
    status: IndustryRecordStatus

    @field_validator("tenant_id", "actor_id")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("This value cannot be blank.")
        return normalized


class IndustryRecordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: str
    tenant_id: str
    solution_key: str
    title: str
    status: IndustryRecordStatus
    payload: dict[str, str]
    created_by: str
    created_at: datetime
    updated_at: datetime
