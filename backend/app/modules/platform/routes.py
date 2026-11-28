from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.platform import service
from app.modules.platform.observability import observability_snapshot
from app.modules.platform.schemas import (
    ControlTowerRead,
    DashboardRead,
    EvaluationCreate,
    EvaluationRead,
    EventAcknowledge,
    KnowledgeDocumentCreate,
    KnowledgeDocumentRead,
    KnowledgeGraphRead,
    KnowledgeSearchRequest,
    KnowledgeSearchResult,
    ObservabilityRead,
    PlatformEventCreate,
    PlatformEventRead,
    StoredObjectContent,
    StoredObjectCreate,
    StoredObjectRead,
)


router = APIRouter(prefix="/platform", tags=["Core Intelligence Infrastructure"])


@router.get("/control-tower", response_model=ControlTowerRead)
def get_control_tower():
    return service.control_tower_status()


@router.get("/dashboard", response_model=DashboardRead)
def get_dashboard(
    tenant_id: str = Query(min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    return service.dashboard_summary(db, tenant_id)


@router.get("/observability", response_model=ObservabilityRead)
def get_observability():
    return observability_snapshot()


@router.post(
    "/knowledge/documents",
    response_model=KnowledgeDocumentRead,
    status_code=status.HTTP_201_CREATED,
)
def create_knowledge_document(
    data: KnowledgeDocumentCreate,
    db: Session = Depends(get_db),
):
    return service.create_document(db, data)


@router.post("/knowledge/search", response_model=list[KnowledgeSearchResult])
def search_knowledge(
    data: KnowledgeSearchRequest,
    db: Session = Depends(get_db),
):
    return service.search_knowledge(db, data.tenant_id, data.query, data.limit)


@router.get("/knowledge/graph", response_model=list[KnowledgeGraphRead])
def get_knowledge_graph(
    tenant_id: str = Query(min_length=1, max_length=100),
    limit: int = Query(default=200, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return service.list_knowledge_relations(db, tenant_id, limit)


@router.post(
    "/events",
    response_model=PlatformEventRead,
    status_code=status.HTTP_202_ACCEPTED,
)
def publish_event(
    data: PlatformEventCreate,
    db: Session = Depends(get_db),
):
    return service.publish_event(db, data)


@router.get("/events", response_model=list[PlatformEventRead])
def get_events(
    tenant_id: str = Query(min_length=1, max_length=100),
    event_status: str | None = Query(default=None, alias="status", pattern="^(pending|acknowledged)$"),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return service.list_events(db, tenant_id, event_status, limit)


@router.post("/events/{event_id}/acknowledge", response_model=PlatformEventRead)
def acknowledge_event(
    event_id: str,
    data: EventAcknowledge,
    db: Session = Depends(get_db),
):
    try:
        return service.acknowledge_event(db, data.tenant_id, data.actor_id, event_id)
    except service.PlatformResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Event not found.") from exc
    except service.PlatformPolicyError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/evaluations", response_model=EvaluationRead, status_code=status.HTTP_201_CREATED)
def evaluate_agent_output(
    data: EvaluationCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.evaluate_output(db, data)
    except service.PlatformResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent not found for this tenant.") from exc


@router.get("/evaluations", response_model=list[EvaluationRead])
def get_evaluations(
    tenant_id: str = Query(min_length=1, max_length=100),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return service.list_evaluations(db, tenant_id, limit)


@router.post(
    "/objects",
    response_model=StoredObjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_stored_object(
    data: StoredObjectCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.store_object(db, data)
    except OSError as exc:
        raise HTTPException(status_code=503, detail="Object storage is unavailable.") from exc


@router.get("/objects/{object_id}", response_model=StoredObjectContent)
def read_stored_object(
    object_id: str,
    tenant_id: str = Query(min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    try:
        stored_object, content = service.get_object(db, tenant_id, object_id)
        return {
            "id": stored_object.id,
            "tenant_id": stored_object.tenant_id,
            "filename": stored_object.filename,
            "content_type": stored_object.content_type,
            "size_bytes": stored_object.size_bytes,
            "created_by": stored_object.created_by,
            "created_at": stored_object.created_at,
            "content": content,
        }
    except service.PlatformResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Object not found.") from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
