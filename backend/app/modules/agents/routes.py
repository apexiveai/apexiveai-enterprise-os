from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.agents import service
from app.modules.agents.gateway import ModelGatewayError, ModelGatewayUnavailable
from app.modules.agents.policy import AgentPolicyError
from app.modules.agents.runtime import agent_orchestrator
from app.modules.agents.schemas import (
    AgentCreate,
    AgentCatalogInstallRequest,
    AgentRead,
    AgentPolicyUpdate,
    AgentReviewCreate,
    AgentReviewRead,
    AgentRunRequest,
    AgentRunResponse,
    AgentStatusUpdate,
    AgentTeamCreate,
    AgentTeamExecutionRead,
    AgentTeamRead,
    AgentTeamRunRequest,
    AgentTeamRunResponse,
    AgentTemplateRead,
    AuditRead,
    MemoryCreate,
    MemoryRead,
    ToolExecuteRequest,
    ToolExecuteResponse,
    ToolRead,
)
from app.modules.agents import teams

router = APIRouter(prefix="/agents", tags=["Agent Runtime"])


@router.get("/health")
def health():
    return {"module": "agent-runtime", "status": "ready"}


@router.get("/tools", response_model=list[ToolRead])
def list_tools():
    return service.list_tools()


@router.get("/catalog", response_model=list[AgentTemplateRead])
def list_agent_catalog():
    return service.list_catalog()


@router.post("/catalog/install", response_model=list[AgentRead])
def install_agent_catalog(
    data: AgentCatalogInstallRequest,
    db: Session = Depends(get_db),
):
    try:
        return service.install_catalog(db, data)
    except service.AgentConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/teams", response_model=AgentTeamRead, status_code=status.HTTP_201_CREATED)
def create_agent_team(data: AgentTeamCreate, db: Session = Depends(get_db)):
    try:
        return teams.create_team(db, data)
    except teams.AgentTeamConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/teams", response_model=list[AgentTeamRead])
def list_agent_teams(
    tenant_id: str = Query(min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    return teams.list_teams(db, tenant_id)


@router.get(
    "/teams/{team_id}/executions",
    response_model=list[AgentTeamExecutionRead],
)
def list_agent_team_executions(
    team_id: str,
    tenant_id: str = Query(min_length=1, max_length=100),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    try:
        team = teams.get_team(db, tenant_id, team_id)
        return teams.list_team_executions(db, team, limit)
    except teams.AgentTeamNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent team not found.") from exc


@router.post("/teams/{team_id}/run", response_model=AgentTeamRunResponse)
def run_agent_team(
    team_id: str,
    data: AgentTeamRunRequest,
    db: Session = Depends(get_db),
):
    try:
        team = teams.get_team(db, data.tenant_id, team_id)
        result = teams.run_team(db, team, data.actor_id, data.prompt)
        return AgentTeamRunResponse(
            execution_id=result.execution_id,
            status=result.status,
            steps=result.steps,
            output=result.output,
        )
    except teams.AgentTeamNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent team not found.") from exc
    except AgentPolicyError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ModelGatewayUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ModelGatewayError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post("", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
def create_agent(data: AgentCreate, db: Session = Depends(get_db)):
    try:
        return service.create_agent(db, data)
    except service.AgentConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("", response_model=list[AgentRead])
def list_agents(
    tenant_id: str = Query(min_length=1, max_length=100),
    db: Session = Depends(get_db),
):
    return service.list_agents(db, tenant_id)


@router.put("/{agent_id}/policy", response_model=AgentRead)
def update_agent_policy(
    agent_id: str,
    data: AgentPolicyUpdate,
    db: Session = Depends(get_db),
):
    try:
        return service.update_agent_policy(db, data.tenant_id, agent_id, data)
    except service.AgentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent not found.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.put("/{agent_id}/status", response_model=AgentRead)
def update_agent_status(
    agent_id: str,
    data: AgentStatusUpdate,
    db: Session = Depends(get_db),
):
    try:
        return service.update_agent_status(db, data.tenant_id, agent_id, data)
    except service.AgentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent not found.") from exc


@router.post(
    "/{agent_id}/reviews",
    response_model=AgentReviewRead,
    status_code=status.HTTP_201_CREATED,
)
def create_agent_performance_review(
    agent_id: str,
    data: AgentReviewCreate,
    db: Session = Depends(get_db),
):
    try:
        agent = service.get_agent(db, data.tenant_id, agent_id)
        return service.create_performance_review(db, agent, data)
    except service.AgentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent not found.") from exc


@router.get("/{agent_id}/reviews", response_model=list[AgentReviewRead])
def list_agent_performance_reviews(
    agent_id: str,
    tenant_id: str = Query(min_length=1, max_length=100),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    try:
        agent = service.get_agent(db, tenant_id, agent_id)
        return service.list_performance_reviews(db, agent, limit)
    except service.AgentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent not found.") from exc


@router.post("/{agent_id}/run", response_model=AgentRunResponse)
def run_agent(
    agent_id: str,
    data: AgentRunRequest,
    db: Session = Depends(get_db),
):
    try:
        agent = service.get_agent(db, data.tenant_id, agent_id)
        execution = agent_orchestrator.run(db, agent, data.actor_id, data.prompt)
        if execution.output is None:
            raise HTTPException(
                status_code=500,
                detail="Agent execution completed without an output.",
            )
        return AgentRunResponse(
            execution_id=execution.id,
            status=execution.status,
            model=execution.model,
            output=execution.output,
        )
    except service.AgentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent not found.") from exc
    except AgentPolicyError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ModelGatewayUnavailable as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ModelGatewayError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post(
    "/{agent_id}/tools/{tool_key}/execute",
    response_model=ToolExecuteResponse,
)
def execute_agent_tool(
    agent_id: str,
    tool_key: str,
    data: ToolExecuteRequest,
    db: Session = Depends(get_db),
):
    try:
        agent = service.get_agent(db, data.tenant_id, agent_id)
        result = service.run_tool(db, agent, tool_key, data.actor_id, data.parameters)
        return ToolExecuteResponse(tool_key=tool_key, result=result)
    except service.AgentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent not found.") from exc
    except AgentPolicyError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.get("/{agent_id}/memory", response_model=list[MemoryRead])
def list_agent_memory(
    agent_id: str,
    tenant_id: str = Query(min_length=1, max_length=100),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    try:
        agent = service.get_agent(db, tenant_id, agent_id)
        return service.list_memory(db, agent, limit)
    except service.AgentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent not found.") from exc


@router.post(
    "/{agent_id}/memory",
    response_model=MemoryRead,
    status_code=status.HTTP_201_CREATED,
)
def create_agent_memory(
    agent_id: str,
    data: MemoryCreate,
    db: Session = Depends(get_db),
):
    try:
        agent = service.get_agent(db, data.tenant_id, agent_id)
        return service.add_memory(db, agent, data)
    except service.AgentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent not found.") from exc


@router.get("/{agent_id}/executions")
def list_agent_executions(
    agent_id: str,
    tenant_id: str = Query(min_length=1, max_length=100),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    try:
        agent = service.get_agent(db, tenant_id, agent_id)
        return service.list_executions(db, agent, limit)
    except service.AgentNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Agent not found.") from exc


@router.get("/audit", response_model=list[AuditRead])
def list_agent_audit(
    tenant_id: str = Query(min_length=1, max_length=100),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return service.list_audit_logs(db, tenant_id, limit)
