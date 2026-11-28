from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DeviceCreate(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=150)
    device_type: str = Field(min_length=1, max_length=80)
    protocol: str = Field(min_length=1, max_length=40)
    manufacturer: str | None = Field(default=None, max_length=120)
    model: str | None = Field(default=None, max_length=120)
    endpoint: str | None = Field(default=None, max_length=500)
    description: str | None = None
    metadata_json: dict[str, Any] = Field(default_factory=dict)


class DeviceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    manufacturer: str | None = None
    model: str | None = None
    endpoint: str | None = None
    description: str | None = None
    metadata_json: dict[str, Any] | None = None


class DeviceStatusUpdate(BaseModel):
    status: str = Field(
        pattern="^(online|offline|degraded|maintenance|fault|disabled)$"
    )


class DeviceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    device_type: str
    manufacturer: str | None
    model: str | None
    protocol: str
    endpoint: str | None
    status: str
    description: str | None
    metadata_json: dict[str, Any]
    created_at: datetime
    updated_at: datetime
