from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.process_automation import service
from app.modules.process_automation.schemas import (
    ProcessCreate,
    ProcessVersionCreate,
    ProcessDefinitionRead,
    ProcessVersionRead,
    ProcessExecuteRequest,
    ProcessExecutionRead,
    ApprovalDecision,
    ProcessApprovalRead,
)

router = APIRouter(
    prefix="/process-automation",
    tags=["Process Automation"],
)

def handle_error(exc):
    if isinstance(exc, service.ProcessNotFoundError):
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    if isinstance(exc, service.ProcessConflictError):
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

    if isinstance(exc, service.ProcessTemporalError):
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )

    if isinstance(exc, ValueError):
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    raise exc


@router.get("/health")
def health():
    return {
        "module": "process-automation",
        "status": "ready",
        "execution_mode": "database-backed-local",
    }


@router.post(
    "/definitions",
    response_model=ProcessDefinitionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_definition(
    data: ProcessCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_definition(db, data)
    except (ValueError, service.ProcessConflictError) as exc:
        handle_error(exc)


@router.get(
    "/definitions",
    response_model=list[ProcessDefinitionRead],
)
def list_definitions(
    tenant_id: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    return service.list_definitions(db, tenant_id)


@router.get(
    "/definitions/{definition_id}/versions",
    response_model=list[ProcessVersionRead],
)
def list_versions(
    definition_id: str,
    tenant_id: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    try:
        return service.get_versions(db, tenant_id, definition_id)
    except service.ProcessNotFoundError as exc:
        handle_error(exc)


@router.post(
    "/definitions/{definition_id}/versions",
    response_model=ProcessVersionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_version(
    definition_id: str,
    data: ProcessVersionCreate,
    tenant_id: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    try:
        return service.create_version(db, tenant_id, definition_id, data)
    except (
        service.ProcessNotFoundError,
        service.ProcessConflictError,
        ValueError,
    ) as exc:
        handle_error(exc)


@router.post(
    "/definitions/{definition_id}/publish",
    response_model=ProcessDefinitionRead,
)
def publish_definition(
    definition_id: str,
    tenant_id: str = Query(min_length=1),
    actor_id: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    try:
        return service.publish_definition(
            db, tenant_id, definition_id, actor_id
        )
    except (
        service.ProcessNotFoundError,
        service.ProcessConflictError,
        ValueError,
    ) as exc:
        handle_error(exc)


@router.post(
    "/definitions/{definition_id}/execute",
    response_model=ProcessExecutionRead,
    status_code=status.HTTP_201_CREATED,
)
def execute_definition(
    definition_id: str,
    data: ProcessExecuteRequest,
    db: Session = Depends(get_db),
):
    try:
        return service.start_execution(
            db, data.tenant_id, definition_id, data.variables
        )
    except (
        service.ProcessNotFoundError,
        service.ProcessConflictError,
        service.ProcessTemporalError,
        ValueError,
    ) as exc:
        handle_error(exc)


@router.get(
    "/executions",
    response_model=list[ProcessExecutionRead],
)
def list_executions(
    tenant_id: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    return service.list_executions(db, tenant_id)


@router.get(
    "/executions/{execution_id}",
    response_model=ProcessExecutionRead,
)
def get_execution(
    execution_id: str,
    tenant_id: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    try:
        return service.get_execution(db, tenant_id, execution_id)
    except service.ProcessNotFoundError as exc:
        handle_error(exc)


@router.get(
    "/approvals",
    response_model=list[ProcessApprovalRead],
)
def list_approvals(
    tenant_id: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    return service.list_approvals(db, tenant_id)


@router.post(
    "/approvals/{approval_id}/resolve",
    response_model=ProcessApprovalRead,
)
def resolve_approval(
    approval_id: str,
    data: ApprovalDecision,
    db: Session = Depends(get_db),
):
    try:
        return service.resolve_approval(
            db, data.tenant_id, approval_id, data
        )
    except (
        service.ProcessNotFoundError,
        service.ProcessConflictError,
        service.ProcessTemporalError,
    ) as exc:
        handle_error(exc)
