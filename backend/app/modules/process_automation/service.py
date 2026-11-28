from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.engines.process_automation.launcher import (
    start_execution_workflow_sync,
    signal_execution_approval_sync,
)
from app.engines.process_automation.contracts import ProcessStep
from app.engines.process_automation.actions import execute_action
from app.engines.process_automation.policy import evaluate_step
from app.modules.process_automation.models import (
    ProcessDefinition,
    ProcessVersion,
    ProcessExecution,
    ProcessApproval,
    ProcessAuditLog,
)

class ProcessTemporalError(Exception):
    pass

class ProcessNotFoundError(Exception):
    pass

class ProcessConflictError(Exception):
    pass


def now():
    return datetime.now(timezone.utc)


def audit(
    db: Session,
    tenant_id: str,
    actor_id: str,
    action: str,
    definition_id: str | None = None,
    execution_id: str | None = None,
    details: dict | None = None,
):
    db.add(ProcessAuditLog(
        tenant_id=tenant_id,
        actor_id=actor_id,
        action=action,
        definition_id=definition_id,
        execution_id=execution_id,
        details=details or {},
    ))


def get_definition(db, tenant_id, definition_id):
    item = db.scalar(
        select(ProcessDefinition).where(
            ProcessDefinition.id == definition_id,
            ProcessDefinition.tenant_id == tenant_id,
        )
    )
    if item is None:
        raise ProcessNotFoundError(definition_id)
    return item


def validate_steps(steps):
    if not steps:
        raise ValueError("A process must contain at least one step")

    normalized_steps = []

    for step in steps:
        if hasattr(step, "model_dump"):
            step_data = step.model_dump(mode="json")
        elif isinstance(step, dict):
            step_data = step
        else:
            raise ValueError(
                "Each process step must be a valid object or dictionary"
            )

        validated = ProcessStep.model_validate(step_data)
        normalized_steps.append(validated.model_dump(mode="json"))

    ids = [step["step_id"] for step in normalized_steps]

    if len(ids) != len(set(ids)):
        raise ValueError("Step IDs must be unique")

    return normalized_steps

def create_definition(db: Session, data):
    steps = validate_steps(data.steps)

    definition = ProcessDefinition(
        tenant_id=data.tenant_id,
        company_id=data.company_id,
        name=data.name,
        description=data.description,
        created_by=data.created_by,
        status="draft",
        current_version=1,
    )
    db.add(definition)
    db.flush()

    version = ProcessVersion(
        definition_id=definition.id,
        version_number=1,
        steps=steps,
        created_by=data.created_by,
    )
    db.add(version)

    audit(
        db, data.tenant_id, data.created_by,
        "process.created", definition.id,
        details={"version": 1},
    )
    db.commit()
    db.refresh(definition)
    return definition


def list_definitions(db, tenant_id):
    return list(db.scalars(
        select(ProcessDefinition)
        .where(ProcessDefinition.tenant_id == tenant_id)
        .order_by(ProcessDefinition.created_at.desc())
    ).all())


def get_versions(db, tenant_id, definition_id):
    definition = get_definition(db, tenant_id, definition_id)
    return list(db.scalars(
        select(ProcessVersion)
        .where(ProcessVersion.definition_id == definition.id)
        .order_by(ProcessVersion.version_number.desc())
    ).all())


def create_version(db, tenant_id, definition_id, data):
    definition = get_definition(db, tenant_id, definition_id)

    if definition.status == "archived":
        raise ProcessConflictError("Archived processes cannot be modified")

    steps = validate_steps([
        step.model_dump(mode="json") for step in data.steps
    ])

    number = definition.current_version + 1

    version = ProcessVersion(
        definition_id=definition.id,
        version_number=number,
        steps=steps,
        created_by=data.created_by,
    )

    definition.current_version = number
    definition.status = "draft"

    db.add(version)
    audit(
        db, tenant_id, data.created_by,
        "process.version_created", definition.id,
        details={"version": number},
    )
    db.commit()
    db.refresh(version)
    return version


def publish_definition(db, tenant_id, definition_id, actor_id):
    definition = get_definition(db, tenant_id, definition_id)

    if definition.status == "archived":
        raise ProcessConflictError("Archived process cannot be published")

    version = db.scalar(
        select(ProcessVersion).where(
            ProcessVersion.definition_id == definition.id,
            ProcessVersion.version_number == definition.current_version,
        )
    )

    if version is None:
        raise ProcessNotFoundError("Process version not found")

    # Verify every action exists before publishing.
    for item in version.steps:
        step = ProcessStep.model_validate(item)
        evaluate_step(step)
        if not evaluate_step(step).allowed:
            raise ValueError(
                f"Unregistered or prohibited action: {step.action_key}"
            )

    version.published = True
    definition.status = "published"

    audit(
        db, tenant_id, actor_id,
        "process.published", definition.id,
        details={"version": version.version_number},
    )
    db.commit()
    db.refresh(definition)
    return definition



def create_execution(db, definition, variables):
    if definition.status != "published":
        raise ProcessConflictError(
            "Only published processes can execute"
        )

    version = db.scalar(
        select(ProcessVersion).where(
            ProcessVersion.definition_id == definition.id,
            ProcessVersion.version_number == definition.current_version,
            ProcessVersion.published.is_(True),
        )
    )

    if version is None:
        raise ProcessConflictError("Published version not found")

    execution = ProcessExecution(
        definition_id=definition.id,
        version_id=version.id,
        tenant_id=definition.tenant_id,
        status="queued",
        variables=variables or {},
        outputs={},
        completed_steps=[],
    )

    db.add(execution)
    db.flush()

    audit(
        db,
        definition.tenant_id,
        definition.created_by,
        "execution.created",
        definition.id,
        execution.id,
        {"version": version.version_number},
    )

    # Persist the execution before starting Temporal.
    db.commit()
    db.refresh(execution)

    try:
        start_execution_workflow_sync(
            execution,
            definition,
            version,
        )

    except Exception as exc:
        execution.status = "failed"
        execution.error = (
            f"Temporal start failed: "
            f"{type(exc).__name__}: {str(exc)[:1200]}"
        )
        execution.completed_at = now()

        audit(
            db,
            execution.tenant_id,
            "system",
            "execution.temporal_start_failed",
            execution.definition_id,
            execution.id,
            {"error": execution.error},
        )

        db.commit()
        db.refresh(execution)

        raise ProcessTemporalError(
            "Unable to start Temporal workflow. "
            "Execution failure has been recorded."
        ) from exc

    db.refresh(execution)
    return execution


def run_execution(db: Session, execution: ProcessExecution):
    if execution.status in ("completed", "rejected", "failed"):
        return execution

    version = db.get(ProcessVersion, execution.version_id)
    if version is None:
        execution.status = "failed"
        execution.error = "Process version not found"
        execution.completed_at = now()
        db.commit()
        return execution

    execution.status = "running"
    if execution.started_at is None:
        execution.started_at = now()
    db.commit()

    for item in version.steps:
        step = ProcessStep.model_validate(item)

        if step.step_id in execution.completed_steps:
            continue

        decision = evaluate_step(step)
        if not decision.allowed:
            execution.status = "failed"
            execution.error = decision.reason
            execution.completed_at = now()
            audit(
                db, execution.tenant_id, "system",
                "execution.policy_rejected",
                execution.definition_id, execution.id,
                {"step_id": step.step_id},
            )
            db.commit()
            return execution

        approval = db.scalar(
            select(ProcessApproval).where(
                ProcessApproval.execution_id == execution.id,
                ProcessApproval.step_id == step.step_id,
            )
        )

        requires_approval = decision.requires_approval

        if requires_approval and (
            approval is None or approval.status == "pending"
        ):
            if approval is None:
                approval = ProcessApproval(
                    execution_id=execution.id,
                    step_id=step.step_id,
                    status="pending",
                )
                db.add(approval)

            execution.status = "waiting_approval"
            audit(
                db, execution.tenant_id, "system",
                "approval.requested",
                execution.definition_id, execution.id,
                {"step_id": step.step_id},
            )
            db.commit()
            return execution

        if requires_approval and approval.status == "rejected":
            execution.status = "rejected"
            execution.error = "Human approval rejected"
            execution.completed_at = now()
            db.commit()
            return execution

        try:
            result = execute_action(
                step.action_key,
                {
                    **step.parameters,
                    "process_variables": execution.variables,
                },
            )

            outputs = dict(execution.outputs or {})
            outputs[step.step_id] = result
            execution.outputs = outputs

            completed = list(execution.completed_steps or [])
            completed.append(step.step_id)
            execution.completed_steps = completed

            audit(
                db, execution.tenant_id, "system",
                "step.completed",
                execution.definition_id, execution.id,
                {"step_id": step.step_id, "action": step.action_key},
            )
            db.commit()

        except Exception as exc:
            execution.status = "failed"
            execution.error = f"{type(exc).__name__}: {str(exc)[:1500]}"
            execution.completed_at = now()
            audit(
                db, execution.tenant_id, "system",
                "step.failed",
                execution.definition_id, execution.id,
                {"step_id": step.step_id},
            )
            db.commit()
            return execution

    execution.status = "completed"
    execution.completed_at = now()

    audit(
        db, execution.tenant_id, "system",
        "execution.completed",
        execution.definition_id, execution.id,
    )
    db.commit()
    return execution


def start_execution(db, tenant_id, definition_id, variables):
    definition = get_definition(db, tenant_id, definition_id)
    return create_execution(db, definition, variables)


def list_executions(db, tenant_id):
    return list(db.scalars(
        select(ProcessExecution)
        .where(ProcessExecution.tenant_id == tenant_id)
        .order_by(ProcessExecution.created_at.desc())
    ).all())


def get_execution(db, tenant_id, execution_id):
    execution = db.scalar(
        select(ProcessExecution).where(
            ProcessExecution.id == execution_id,
            ProcessExecution.tenant_id == tenant_id,
        )
    )
    if execution is None:
        raise ProcessNotFoundError(execution_id)
    return execution


def list_approvals(db, tenant_id):
    return list(db.scalars(
        select(ProcessApproval)
        .join(
            ProcessExecution,
            ProcessExecution.id == ProcessApproval.execution_id,
        )
        .where(ProcessExecution.tenant_id == tenant_id)
        .order_by(ProcessApproval.created_at.desc())
    ).all())



def resolve_approval(db, tenant_id, approval_id, data):
    approval = db.scalar(
        select(ProcessApproval)
        .join(
            ProcessExecution,
            ProcessExecution.id == ProcessApproval.execution_id,
        )
        .where(
            ProcessApproval.id == approval_id,
            ProcessExecution.tenant_id == tenant_id,
        )
    )

    if approval is None:
        raise ProcessNotFoundError(approval_id)

    execution = get_execution(
        db,
        tenant_id,
        approval.execution_id,
    )

    requested_status = (
        "approved" if data.approved else "rejected"
    )

    if approval.status == "pending":
        approval.status = requested_status
        approval.actor_id = data.actor_id
        approval.reason = data.reason
        approval.resolved_at = now()

        audit(
            db,
            tenant_id,
            data.actor_id,
            "approval.resolved",
            execution.definition_id,
            execution.id,
            {
                "step_id": approval.step_id,
                "approved": data.approved,
            },
        )

        db.commit()
        db.refresh(approval)

    elif approval.status != requested_status:
        raise ProcessConflictError(
            "Approval has already been resolved differently"
        )

    # Re-sending the same decision is allowed.
    # This supports recovery if the database commit succeeded
    # but the Temporal signal failed.
    try:
        signal_execution_approval_sync(
            tenant_id=tenant_id,
            execution_id=execution.id,
            step_id=approval.step_id,
            approved=data.approved,
            actor_id=data.actor_id,
            reason=data.reason,
        )

    except Exception as exc:
        raise ProcessTemporalError(
            "Approval was saved, but Temporal signal delivery failed. "
            "Retry the same approval decision to resend the signal."
        ) from exc

    db.refresh(approval)
    return approval
