from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.modules.agents.catalog import AGENT_CATALOG
from app.modules.agents.models import (
    AgentAuditLog,
    AgentDefinition,
    AgentExecution,
    AgentMemory,
    AgentPerformanceReview,
)
from app.modules.agents.schemas import (
    AgentReviewCreate,
    AgentCatalogInstallRequest,
    AgentCreate,
    AgentPolicyUpdate,
    AgentStatusUpdate,
    MemoryCreate,
)
from app.modules.agents.tool_registry import (
    TOOL_REGISTRY,
    ToolNotFoundError,
    execute_tool,
    validate_tool_keys,
)
from app.modules.agents.policy import validate_tool_access


class AgentNotFoundError(Exception):
    pass


class AgentConflictError(Exception):
    pass


def write_audit(
    db: Session,
    tenant_id: str,
    actor_id: str,
    action: str,
    resource_type: str,
    resource_id: str | None = None,
    agent_id: str | None = None,
    details: dict | None = None,
) -> None:
    db.add(AgentAuditLog(
        tenant_id=tenant_id,
        agent_id=agent_id,
        actor_id=actor_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details or {},
    ))


def get_agent(db: Session, tenant_id: str, agent_id: str) -> AgentDefinition:
    agent = db.scalar(select(AgentDefinition).where(
        AgentDefinition.id == agent_id,
        AgentDefinition.tenant_id == tenant_id,
    ))
    if agent is None:
        raise AgentNotFoundError(agent_id)
    return agent


def create_agent(db: Session, data: AgentCreate) -> AgentDefinition:
    validate_tool_keys(data.allowed_tools)
    agent = AgentDefinition(
        tenant_id=data.tenant_id,
        slug=data.slug,
        name=data.name,
        description=data.description,
        model=data.model or settings.model_gateway_default_model,
        system_prompt=data.system_prompt,
        allowed_tools=sorted(set(data.allowed_tools)),
        status="active",
        created_by=data.created_by,
    )
    db.add(agent)
    try:
        db.flush()
        write_audit(
            db, data.tenant_id, data.created_by, "agent.created",
            "agent", agent.id, agent.id, {"slug": agent.slug},
        )
        db.commit()
        db.refresh(agent)
        return agent
    except IntegrityError as exc:
        db.rollback()
        raise AgentConflictError("An agent with this slug already exists for the tenant.") from exc


def list_agents(db: Session, tenant_id: str) -> list[AgentDefinition]:
    return list(db.scalars(
        select(AgentDefinition)
        .where(AgentDefinition.tenant_id == tenant_id)
        .order_by(AgentDefinition.created_at.desc())
    ).all())


def update_agent_policy(
    db: Session,
    tenant_id: str,
    agent_id: str,
    data: AgentPolicyUpdate,
) -> AgentDefinition:
    agent = get_agent(db, tenant_id, agent_id)
    validate_tool_keys(data.allowed_tools)
    agent.allowed_tools = sorted(set(data.allowed_tools))
    write_audit(
        db,
        tenant_id,
        data.actor_id,
        "agent.policy_updated",
        "agent",
        agent.id,
        agent.id,
        {"allowed_tools": agent.allowed_tools},
    )
    db.commit()
    db.refresh(agent)
    return agent


def update_agent_status(
    db: Session,
    tenant_id: str,
    agent_id: str,
    data: AgentStatusUpdate,
) -> AgentDefinition:
    agent = get_agent(db, tenant_id, agent_id)
    agent.status = data.status
    write_audit(
        db,
        tenant_id,
        data.actor_id,
        f"agent.{data.status}",
        "agent",
        agent.id,
        agent.id,
        {"status": data.status},
    )
    db.commit()
    db.refresh(agent)
    return agent


def list_catalog() -> list[dict[str, object]]:
    return [template.as_dict() for template in AGENT_CATALOG]


def install_catalog(
    db: Session,
    data: AgentCatalogInstallRequest,
) -> list[AgentDefinition]:
    template_slugs = [template.slug for template in AGENT_CATALOG]
    existing_agents = list(db.scalars(
        select(AgentDefinition).where(
            AgentDefinition.tenant_id == data.tenant_id,
            AgentDefinition.slug.in_(template_slugs),
        )
    ).all())
    agents_by_slug = {agent.slug: agent for agent in existing_agents}
    new_agents = []

    for template in AGENT_CATALOG:
        if template.slug in agents_by_slug:
            continue
        agent = AgentDefinition(
            tenant_id=data.tenant_id,
            slug=template.slug,
            name=template.name,
            description=template.responsibility,
            model=settings.model_gateway_default_model,
            system_prompt=template.system_prompt,
            allowed_tools=[],
            status="active",
            created_by=data.actor_id,
        )
        db.add(agent)
        new_agents.append(agent)

    try:
        db.flush()
        for agent in new_agents:
            write_audit(
                db,
                data.tenant_id,
                data.actor_id,
                "agent.catalog_installed",
                "agent",
                agent.id,
                agent.id,
                {"slug": agent.slug},
            )
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise AgentConflictError(
            "Agent catalog installation conflicted with an existing agent."
        ) from exc

    agents_by_slug.update({agent.slug: agent for agent in new_agents})
    return [agents_by_slug[slug] for slug in template_slugs]


def add_memory(db: Session, agent: AgentDefinition, data: MemoryCreate) -> AgentMemory:
    memory = AgentMemory(
        tenant_id=agent.tenant_id,
        agent_id=agent.id,
        memory_key=data.memory_key,
        content=data.content,
        labels=data.labels,
    )
    db.add(memory)
    db.flush()
    write_audit(
        db, agent.tenant_id, data.actor_id, "memory.created",
        "agent_memory", memory.id, agent.id,
        {"memory_key": memory.memory_key},
    )
    db.commit()
    db.refresh(memory)
    return memory


def list_memory(
    db: Session,
    agent: AgentDefinition,
    limit: int = 50,
) -> list[AgentMemory]:
    return list(db.scalars(
        select(AgentMemory)
        .where(
            AgentMemory.tenant_id == agent.tenant_id,
            AgentMemory.agent_id == agent.id,
        )
        .order_by(AgentMemory.created_at.desc())
        .limit(limit)
    ).all())


def list_tools() -> list[dict[str, str]]:
    return [
        {
            "tool_key": tool.tool_key,
            "description": tool.description,
            "risk_level": tool.risk_level,
        }
        for tool in TOOL_REGISTRY.values()
    ]


def run_tool(
    db: Session,
    agent: AgentDefinition,
    tool_key: str,
    actor_id: str,
    parameters: dict,
) -> dict:
    validate_tool_access(agent, tool_key)
    try:
        result = execute_tool(tool_key, parameters)
    except ToolNotFoundError:
        raise
    write_audit(
        db, agent.tenant_id, actor_id, "tool.executed",
        "agent_tool", tool_key, agent.id,
        {"risk_level": TOOL_REGISTRY[tool_key].risk_level},
    )
    db.commit()
    return result


def list_audit_logs(db: Session, tenant_id: str, limit: int = 100) -> list[AgentAuditLog]:
    return list(db.scalars(
        select(AgentAuditLog)
        .where(AgentAuditLog.tenant_id == tenant_id)
        .order_by(AgentAuditLog.created_at.desc())
        .limit(limit)
    ).all())


def list_executions(
    db: Session,
    agent: AgentDefinition,
    limit: int = 50,
) -> list[AgentExecution]:
    return list(db.scalars(
        select(AgentExecution)
        .where(
            AgentExecution.tenant_id == agent.tenant_id,
            AgentExecution.agent_id == agent.id,
        )
        .order_by(AgentExecution.created_at.desc())
        .limit(limit)
    ).all())


def create_performance_review(
    db: Session,
    agent: AgentDefinition,
    data: AgentReviewCreate,
) -> AgentPerformanceReview:
    review = AgentPerformanceReview(
        tenant_id=agent.tenant_id,
        agent_id=agent.id,
        reviewer_id=data.reviewer_id,
        period_start=data.period_start,
        period_end=data.period_end,
        rating=data.rating,
        summary=data.summary,
        kpi_scores=data.kpi_scores,
    )
    db.add(review)
    db.flush()
    write_audit(
        db,
        agent.tenant_id,
        data.reviewer_id,
        "agent.performance_review_created",
        "agent_performance_review",
        review.id,
        agent.id,
        {"rating": review.rating, "kpi_scores": review.kpi_scores},
    )
    db.commit()
    db.refresh(review)
    return review


def list_performance_reviews(
    db: Session,
    agent: AgentDefinition,
    limit: int = 50,
) -> list[AgentPerformanceReview]:
    return list(db.scalars(
        select(AgentPerformanceReview)
        .where(
            AgentPerformanceReview.tenant_id == agent.tenant_id,
            AgentPerformanceReview.agent_id == agent.id,
        )
        .order_by(AgentPerformanceReview.created_at.desc())
        .limit(limit)
    ).all())
