from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class AgentCreate(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=2, max_length=100, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=4000)
    model: str | None = Field(default=None, max_length=200)
    system_prompt: str = Field(default="", max_length=12000)
    allowed_tools: list[str] = Field(default_factory=list, max_length=20)
    created_by: str = Field(min_length=1, max_length=100)


class AgentRead(StrictModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: str
    tenant_id: str
    slug: str
    name: str
    description: str
    model: str
    system_prompt: str
    allowed_tools: list[str]
    status: str
    created_by: str
    created_at: datetime
    updated_at: datetime


class AgentRunRequest(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)
    prompt: str = Field(min_length=1, max_length=12000)


class AgentRunResponse(StrictModel):
    execution_id: str
    status: str
    model: str
    output: str


class MemoryCreate(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)
    memory_key: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=12000)
    labels: dict[str, Any] = Field(default_factory=dict)


class MemoryRead(StrictModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: str
    agent_id: str
    memory_key: str
    content: str
    labels: dict[str, Any]
    created_at: datetime


class ToolRead(StrictModel):
    tool_key: str
    description: str
    risk_level: str


class ToolExecuteRequest(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)
    parameters: dict[str, Any] = Field(default_factory=dict)


class ToolExecuteResponse(StrictModel):
    tool_key: str
    result: dict[str, Any]


class AuditRead(StrictModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: str
    tenant_id: str
    agent_id: str | None
    actor_id: str
    action: str
    resource_type: str
    resource_id: str | None
    details: dict[str, Any]
    created_at: datetime


class AgentTeamCreate(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=2, max_length=100, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=4000)
    member_agent_ids: list[str] = Field(min_length=2, max_length=10)
    created_by: str = Field(min_length=1, max_length=100)


class AgentTeamRead(StrictModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: str
    tenant_id: str
    slug: str
    name: str
    description: str
    member_agent_ids: list[str]
    created_by: str
    created_at: datetime


class AgentTeamRunRequest(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)
    prompt: str = Field(min_length=1, max_length=12000)


class AgentTeamRunResponse(StrictModel):
    execution_id: str
    status: str
    steps: list[dict[str, Any]]
    output: str | None


class AgentTeamExecutionRead(StrictModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: str
    team_id: str
    status: str
    prompt: str
    output: dict[str, Any]
    error: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime


class AgentTemplateRead(StrictModel):
    slug: str
    name: str
    responsibility: str
    job_description: str
    permissions: list[str]
    kpis: list[str]
    tasks: list[str]
    guardrails: list[str]


class AgentReviewCreate(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    reviewer_id: str = Field(min_length=1, max_length=100)
    period_start: date
    period_end: date
    rating: int = Field(ge=1, le=5)
    summary: str = Field(min_length=1, max_length=4000)
    kpi_scores: dict[str, int] = Field(min_length=1, max_length=20)

    @model_validator(mode="after")
    def validate_review_period_and_scores(self):
        if self.period_end < self.period_start:
            raise ValueError("Review period end must be on or after its start.")
        if any(not 0 <= score <= 100 for score in self.kpi_scores.values()):
            raise ValueError("KPI scores must be between 0 and 100.")
        if any(not name.strip() or len(name) > 200 for name in self.kpi_scores):
            raise ValueError("KPI names must contain 1 to 200 characters.")
        return self


class AgentReviewRead(StrictModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: str
    tenant_id: str
    agent_id: str
    reviewer_id: str
    period_start: date
    period_end: date
    rating: int
    summary: str
    kpi_scores: dict[str, int]
    created_at: datetime


class AgentCatalogInstallRequest(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)


class AgentPolicyUpdate(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)
    allowed_tools: list[str] = Field(max_length=20)


class AgentStatusUpdate(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)
    status: str = Field(pattern="^(active|disabled)$")
