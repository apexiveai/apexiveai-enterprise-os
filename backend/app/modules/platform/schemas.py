from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class KnowledgeRelationInput(StrictModel):
    subject: str = Field(min_length=1, max_length=200)
    predicate: str = Field(min_length=1, max_length=120)
    object: str = Field(min_length=1, max_length=200)


class KnowledgeDocumentCreate(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=250)
    source: str = Field(default="", max_length=500)
    content: str = Field(min_length=1, max_length=200000)
    relations: list[KnowledgeRelationInput] = Field(default_factory=list, max_length=100)


class KnowledgeDocumentRead(StrictModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: str
    tenant_id: str
    title: str
    source: str
    content: str
    created_by: str
    created_at: datetime


class KnowledgeSearchRequest(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    query: str = Field(min_length=1, max_length=4000)
    limit: int = Field(default=5, ge=1, le=20)


class KnowledgeSearchResult(StrictModel):
    document_id: str
    title: str
    source: str
    score: float
    snippet: str


class KnowledgeGraphRead(StrictModel):
    id: str
    document_id: str
    subject: str
    predicate: str
    object: str
    created_at: datetime


class PlatformEventCreate(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    event_type: str = Field(min_length=1, max_length=160, pattern=r"^[a-zA-Z0-9_.:-]+$")
    payload: dict[str, Any] = Field(default_factory=dict)


class PlatformEventRead(StrictModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: str
    tenant_id: str
    event_type: str
    payload: dict[str, Any]
    status: str
    created_at: datetime
    acknowledged_at: datetime | None


class EventAcknowledge(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)


class EvaluationCreate(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    agent_id: str | None = Field(default=None, max_length=36)
    prompt: str = Field(min_length=1, max_length=12000)
    output: str = Field(min_length=1, max_length=30000)
    required_checks: list[str] = Field(default_factory=list, max_length=50)


class EvaluationRead(StrictModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: str
    tenant_id: str
    agent_id: str | None
    prompt: str
    output: str
    required_checks: list[str]
    result: dict[str, Any]
    score: float
    created_at: datetime


class StoredObjectCreate(StrictModel):
    tenant_id: str = Field(min_length=1, max_length=100)
    actor_id: str = Field(min_length=1, max_length=100)
    filename: str = Field(min_length=1, max_length=250)
    content_type: str = Field(default="text/plain", min_length=1, max_length=120)
    content: str = Field(min_length=1, max_length=1000000)


class StoredObjectRead(StrictModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: str
    tenant_id: str
    filename: str
    content_type: str
    size_bytes: int
    created_by: str
    created_at: datetime


class StoredObjectContent(StoredObjectRead):
    content: str


class ControlTowerComponent(StrictModel):
    key: str
    name: str
    status: str
    description: str
    configured: bool


class ControlTowerRead(StrictModel):
    overall_status: str
    components: list[ControlTowerComponent]
    integration_layer: list[ControlTowerComponent]


class DashboardCounts(StrictModel):
    agents: int
    active_agents: int
    agent_runs: int
    processes: int
    process_runs: int
    pending_approvals: int
    knowledge_documents: int
    pending_events: int
    stored_objects: int


class DashboardRead(StrictModel):
    tenant_id: str
    counts: DashboardCounts


class ObservabilityRead(StrictModel):
    window_size: int
    request_count: int
    error_count: int
    average_latency_ms: float
    p95_latency_ms: float
    status_codes: dict[str, int]
    recent_traces: list[dict[str, Any]]
