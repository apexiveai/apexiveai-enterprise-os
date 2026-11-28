from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ProcessStepInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=200)
    action_key: str = Field(min_length=1, max_length=150)
    step_type: str = "action"
    risk_level: str = "low"
    parameters: dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = Field(default=60, ge=1, le=3600)


class ProcessCreate(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    company_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=2, max_length=200)
    description: str = Field(default="", max_length=5000)
    created_by: str = Field(min_length=1, max_length=100)
    steps: list[ProcessStepInput] = Field(min_length=1, max_length=100)


class ProcessVersionCreate(BaseModel):
    created_by: str = Field(min_length=1, max_length=100)
    steps: list[ProcessStepInput] = Field(min_length=1, max_length=100)


class ProcessDefinitionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    company_id: str
    name: str
    description: str
    status: str
    current_version: int
    created_by: str
    created_at: datetime
    updated_at: datetime


class ProcessVersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    definition_id: str
    version_number: int
    steps: list[dict[str, Any]]
    published: bool
    created_by: str
    created_at: datetime


class ProcessExecuteRequest(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    variables: dict[str, Any] = Field(default_factory=dict)


class ProcessExecutionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    definition_id: str
    version_id: str
    tenant_id: str
    status: str
    variables: dict[str, Any]
    outputs: dict[str, Any]
    completed_steps: list[str]
    error: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime


class ApprovalDecision(BaseModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)
    approved: bool
    reason: str = Field(default="", max_length=2000)


class ProcessApprovalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    execution_id: str
    step_id: str
    status: str
    actor_id: str | None
    reason: str
    created_at: datetime
    resolved_at: datetime | None
