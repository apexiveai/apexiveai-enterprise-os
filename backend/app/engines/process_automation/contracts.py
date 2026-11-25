
from enum import StrEnum
from typing import Any
from pydantic import BaseModel, Field, ConfigDict

class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class StepType(StrEnum):
    ACTION = "action"
    APPROVAL = "approval"

class ProcessStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_id: str
    name: str
    action_key: str
    step_type: StepType = StepType.ACTION
    risk_level: RiskLevel = RiskLevel.LOW
    parameters: dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = Field(default=60, ge=1, le=3600)

class ProcessDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    process_id: str
    process_name: str
    tenant_id: str
    company_id: str
    initiated_by: str
    steps: list[ProcessStep] = Field(min_length=1, max_length=100)

class ApprovalDecision(BaseModel):
    step_id: str
    approved: bool
    actor_id: str
    reason: str = ""

class ExecutionResult(BaseModel):
    process_id: str
    status: str
    completed_steps: list[str] = Field(default_factory=list)
    failed_step: str | None = None
    outputs: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None