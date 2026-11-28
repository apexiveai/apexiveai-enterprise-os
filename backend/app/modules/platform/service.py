import hashlib
import math
import os
import re
import tempfile
from pathlib import Path
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import check_database, check_redis
from app.modules.agents.models import AgentAuditLog, AgentDefinition, AgentExecution
from app.modules.process_automation.models import (
    ProcessApproval,
    ProcessDefinition,
    ProcessExecution,
)
from app.modules.platform.models import (
    EvaluationRun,
    KnowledgeDocument,
    KnowledgeRelation,
    PlatformEvent,
    StoredObject,
    utc_now,
)
from app.modules.platform.schemas import (
    ControlTowerComponent,
    DashboardRead,
    EvaluationCreate,
    KnowledgeDocumentCreate,
    PlatformEventCreate,
    StoredObjectCreate,
)


VECTOR_DIMENSIONS = 384
WORD_PATTERN = re.compile(r"[a-z0-9][a-z0-9_.-]{1,}", re.IGNORECASE)


class PlatformResourceNotFoundError(Exception):
    pass


class PlatformPolicyError(Exception):
    pass


def _tokens(text: str) -> list[str]:
    return [token.lower() for token in WORD_PATTERN.findall(text)]


def _vectorize(text: str) -> list[float]:
    vector = [0.0] * VECTOR_DIMENSIONS
    for token in _tokens(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % VECTOR_DIMENSIONS
        vector[index] += 1.0
    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude:
        vector = [value / magnitude for value in vector]
    return vector


def _cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def create_document(db: Session, data: KnowledgeDocumentCreate) -> KnowledgeDocument:
    document = KnowledgeDocument(
        tenant_id=data.tenant_id,
        title=data.title,
        source=data.source,
        content=data.content,
        vector=_vectorize(f"{data.title}\n{data.content}"),
        created_by=data.actor_id,
    )
    db.add(document)
    db.flush()
    for relation in data.relations:
        db.add(KnowledgeRelation(
            tenant_id=data.tenant_id,
            document_id=document.id,
            subject=relation.subject,
            predicate=relation.predicate,
            object=relation.object,
        ))
    db.add(AgentAuditLog(
        tenant_id=data.tenant_id,
        actor_id=data.actor_id,
        action="knowledge.document_created",
        resource_type="knowledge_document",
        resource_id=document.id,
        details={"title": document.title, "relation_count": len(data.relations)},
    ))
    db.commit()
    db.refresh(document)
    return document


def search_knowledge(
    db: Session,
    tenant_id: str,
    query: str,
    limit: int,
) -> list[dict]:
    query_vector = _vectorize(query)
    documents = db.scalars(
        select(KnowledgeDocument).where(KnowledgeDocument.tenant_id == tenant_id)
    ).all()
    scored = [
        (document, _cosine(query_vector, document.vector))
        for document in documents
    ]
    scored = [(document, score) for document, score in scored if score > 0]
    scored.sort(key=lambda item: (-item[1], item[0].created_at), reverse=False)
    results = []
    for document, score in scored[:limit]:
        snippet = re.sub(r"\s+", " ", document.content).strip()
        results.append({
            "document_id": document.id,
            "title": document.title,
            "source": document.source,
            "score": round(score, 4),
            "snippet": snippet[:400] + ("..." if len(snippet) > 400 else ""),
        })
    return results


def list_knowledge_relations(db: Session, tenant_id: str, limit: int = 200) -> list[KnowledgeRelation]:
    return list(db.scalars(
        select(KnowledgeRelation)
        .where(KnowledgeRelation.tenant_id == tenant_id)
        .order_by(KnowledgeRelation.created_at.desc())
        .limit(limit)
    ).all())


def publish_event(db: Session, data: PlatformEventCreate) -> PlatformEvent:
    event = PlatformEvent(
        tenant_id=data.tenant_id,
        event_type=data.event_type,
        payload=data.payload,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def list_events(
    db: Session,
    tenant_id: str,
    status: str | None,
    limit: int,
) -> list[PlatformEvent]:
    query = select(PlatformEvent).where(PlatformEvent.tenant_id == tenant_id)
    if status:
        query = query.where(PlatformEvent.status == status)
    return list(db.scalars(query.order_by(PlatformEvent.created_at.desc()).limit(limit)).all())


def dashboard_summary(db: Session, tenant_id: str) -> dict:
    def count(model, *criteria) -> int:
        statement = select(func.count()).select_from(model)
        if criteria:
            statement = statement.where(*criteria)
        return int(db.scalar(statement) or 0)

    pending_approvals = db.scalar(
        select(func.count())
        .select_from(ProcessApproval)
        .join(ProcessExecution, ProcessApproval.execution_id == ProcessExecution.id)
        .where(
            ProcessExecution.tenant_id == tenant_id,
            ProcessApproval.status == "pending",
        )
    ) or 0

    return DashboardRead(
        tenant_id=tenant_id,
        counts={
            "agents": count(AgentDefinition, AgentDefinition.tenant_id == tenant_id),
            "active_agents": count(
                AgentDefinition,
                AgentDefinition.tenant_id == tenant_id,
                AgentDefinition.status == "active",
            ),
            "agent_runs": count(AgentExecution, AgentExecution.tenant_id == tenant_id),
            "processes": count(ProcessDefinition, ProcessDefinition.tenant_id == tenant_id),
            "process_runs": count(ProcessExecution, ProcessExecution.tenant_id == tenant_id),
            "pending_approvals": int(pending_approvals),
            "knowledge_documents": count(
                KnowledgeDocument, KnowledgeDocument.tenant_id == tenant_id
            ),
            "pending_events": count(
                PlatformEvent,
                PlatformEvent.tenant_id == tenant_id,
                PlatformEvent.status == "pending",
            ),
            "stored_objects": count(StoredObject, StoredObject.tenant_id == tenant_id),
        },
    ).model_dump()


def acknowledge_event(
    db: Session,
    tenant_id: str,
    actor_id: str,
    event_id: str,
) -> PlatformEvent:
    event = db.scalar(select(PlatformEvent).where(
        PlatformEvent.id == event_id,
        PlatformEvent.tenant_id == tenant_id,
    ))
    if event is None:
        raise PlatformResourceNotFoundError(event_id)
    if event.status == "acknowledged":
        raise PlatformPolicyError("Event has already been acknowledged.")
    event.status = "acknowledged"
    event.acknowledged_at = utc_now()
    db.add(AgentAuditLog(
        tenant_id=tenant_id,
        actor_id=actor_id,
        action="platform.event_acknowledged",
        resource_type="platform_event",
        resource_id=event.id,
        details={"event_type": event.event_type},
    ))
    db.commit()
    db.refresh(event)
    return event


def evaluate_output(db: Session, data: EvaluationCreate) -> EvaluationRun:
    if data.agent_id:
        agent = db.scalar(select(AgentDefinition).where(
            AgentDefinition.id == data.agent_id,
            AgentDefinition.tenant_id == data.tenant_id,
        ))
        if agent is None:
            raise PlatformResourceNotFoundError(data.agent_id)
    normalized_output = data.output.casefold()
    checks = {
        check: check.casefold() in normalized_output
        for check in data.required_checks
    }
    score = (
        sum(checks.values()) / len(checks)
        if checks
        else (1.0 if data.output.strip() else 0.0)
    )
    evaluation = EvaluationRun(
        tenant_id=data.tenant_id,
        agent_id=data.agent_id,
        prompt=data.prompt,
        output=data.output,
        required_checks=data.required_checks,
        result={
            "passed": all(checks.values()) if checks else bool(data.output.strip()),
            "checks": checks,
            "method": "required_phrase_match",
        },
        score=score,
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation


def list_evaluations(db: Session, tenant_id: str, limit: int) -> list[EvaluationRun]:
    return list(db.scalars(
        select(EvaluationRun)
        .where(EvaluationRun.tenant_id == tenant_id)
        .order_by(EvaluationRun.created_at.desc())
        .limit(limit)
    ).all())


def store_object(db: Session, data: StoredObjectCreate) -> StoredObject:
    object_id = str(uuid4())
    object_key = f"{object_id}.blob"
    storage_root = Path(settings.object_storage_path).resolve()
    storage_root.mkdir(parents=True, exist_ok=True)
    target_path = (storage_root / object_key).resolve()
    if target_path.parent != storage_root:
        raise ValueError("Invalid object storage key.")

    encoded_content = data.content.encode("utf-8")
    temporary_path: Path | None = None
    persisted = False
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=storage_root,
            prefix=".upload-",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            temporary_file.write(encoded_content)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.replace(temporary_path, target_path)

        stored_object = StoredObject(
            id=object_id,
            tenant_id=data.tenant_id,
            object_key=object_key,
            filename=Path(data.filename).name,
            content_type=data.content_type,
            size_bytes=len(encoded_content),
            created_by=data.actor_id,
        )
        db.add(stored_object)
        db.add(AgentAuditLog(
            tenant_id=data.tenant_id,
            actor_id=data.actor_id,
            action="object.created",
            resource_type="stored_object",
            resource_id=object_id,
            details={"filename": stored_object.filename, "size_bytes": stored_object.size_bytes},
        ))
        db.commit()
        persisted = True
        db.refresh(stored_object)
        return stored_object
    finally:
        if not persisted:
            db.rollback()
            if target_path.exists():
                target_path.unlink()
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()


def get_object(db: Session, tenant_id: str, object_id: str) -> tuple[StoredObject, str]:
    stored_object = db.scalar(select(StoredObject).where(
        StoredObject.id == object_id,
        StoredObject.tenant_id == tenant_id,
    ))
    if stored_object is None:
        raise PlatformResourceNotFoundError(object_id)

    storage_root = Path(settings.object_storage_path).resolve()
    target_path = (storage_root / stored_object.object_key).resolve()
    if target_path.parent != storage_root or not target_path.is_file():
        raise PlatformResourceNotFoundError(object_id)
    try:
        content = target_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise RuntimeError("Stored object could not be read.") from exc
    return stored_object, content


def _component(key: str, name: str, status: str, description: str) -> ControlTowerComponent:
    return ControlTowerComponent(
        key=key,
        name=name,
        status=status,
        description=description,
        configured=status == "operational",
    )


def control_tower_status() -> dict:
    database_ok = check_database()
    database_backend = make_url(settings.database_url).get_backend_name()
    redis_ok = check_redis()
    redis_status = "operational" if redis_ok else ("unavailable" if redis_ok is False else "not_configured")
    gateway_configured = bool(settings.model_gateway_url and settings.model_gateway_api_key)
    gateway_status = "operational" if gateway_configured else "not_configured"
    primary = [
        _component("control_tower", "AI Control Tower", "operational", "Central engine readiness and policy visibility; API authentication is not yet enabled."),
        _component("agent_runtime", "Agent Runtime Engine", "operational", "Tenant-scoped agent registry, memory, executions, and audit records."),
        _component("orchestration", "Orchestration Engine", "operational", "Persistent sequential agent teams and Temporal process orchestration."),
        _component("model_gateway", "Model Gateway", gateway_status, "OpenAI-compatible completion routing with configured provider fallback."),
        _component("memory", "Memory Engine", "operational", "Persistent tenant-scoped agent memory stored in the configured SQL database."),
        _component("knowledge", "Knowledge Engine", "operational", "Tenant-scoped hashed-token vector retrieval and manually supplied knowledge-graph relations; no embedding model."),
        _component("policy", "Policy Engine", "operational", "Agent status and explicit allowlisted low-risk tools; actor identities are not authenticated."),
        _component("tool_execution", "Tool Execution Engine", "operational", "Allowlisted local tools only; remote MCP calls are not enabled."),
        _component("rpa_runtime", "RPA Runtime Engine", "partial", "Temporal process automation is available; browser and desktop bot adapters are not configured."),
        _component("event_bus", "Event Bus Engine", "operational", "Durable SQL event queue; Redis is an optional additional transport."),
        _component("evaluation", "Evaluation Engine", "operational", "Persisted deterministic required-phrase checks; no LLM-as-judge or test harness integration."),
        _component("observability", "Observability Engine", "partial", "Process-local HTTP request counts and latency summaries; no distributed tracing backend."),
        _component("recovery", "Recovery Engine", "operational", "Model provider fallback and Temporal process retry/recovery support."),
    ]
    data_layer = [
        _component(
            "postgresql",
            "PostgreSQL",
            "operational" if database_ok and database_backend in {"postgres", "postgresql"}
            else "not_configured" if database_ok
            else "unavailable",
            f"Configured SQL backend: {database_backend}.",
        ),
        _component("redis", "Redis", redis_status, "Optional Redis transport and cache connection."),
        _component("object_storage", "Object Storage", "operational", "Local file-backed object storage; remote S3-compatible storage is not configured."),
        _component("vector_search", "Vector Search", "operational", "Local deterministic hashed-token cosine search; semantic embeddings are not configured."),
        _component("api_gateway", "API Gateway", "operational", "FastAPI versioned API routes and OpenAPI documentation."),
        _component("mcp", "MCP", "not_configured", "MCP server/client integration is not configured."),
        _component("connectors", "Connectors", "partial", "Industrial connector profiles are stored; live ERP/CRM/HR and OT connectors are not configured."),
    ]
    components = primary + data_layer
    overall_status = (
        "unavailable" if any(item.status == "unavailable" for item in components)
        else "partial" if any(item.status in {"partial", "not_configured"} for item in components)
        else "operational"
    )
    return {
        "overall_status": overall_status,
        "components": primary,
        "integration_layer": data_layer,
    }
