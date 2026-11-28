
import asyncio
from datetime import datetime, timezone

from sqlalchemy import select
from temporalio import activity

from app.db.session import SessionLocal
from app.modules.process_automation.models import (
    ProcessExecution,
    ProcessApproval,
    ProcessAuditLog,
)

from .contracts import ProcessStep
from .policy import evaluate_step
from .actions import execute_action


def utc_now():
    return datetime.now(timezone.utc)


def write_audit(
    db,
    execution,
    actor_id: str,
    action: str,
    details: dict | None = None,
):
    db.add(
        ProcessAuditLog(
            tenant_id=execution.tenant_id,
            definition_id=execution.definition_id,
            execution_id=execution.id,
            actor_id=actor_id,
            action=action,
            details=details or {},
        )
    )


@activity.defn
async def mark_execution_started(payload: dict) -> dict:
    with SessionLocal() as db:
        execution = db.get(
            ProcessExecution,
            payload["execution_id"],
        )

        if execution is None:
            raise ValueError("Execution not found")

        if execution.status in ("completed", "rejected", "failed"):
            return {"status": execution.status}

        execution.status = "running"

        if execution.started_at is None:
            execution.started_at = utc_now()

        write_audit(
            db,
            execution,
            "system",
            "execution.started",
        )

        db.commit()

        return {"status": execution.status}


@activity.defn
async def authorize_step(payload: dict) -> dict:
    step = ProcessStep.model_validate(payload["step"])
    decision = evaluate_step(step)

    return {
        "allowed": decision.allowed,
        "requires_approval": decision.requires_approval,
        "reason": decision.reason,
    }


@activity.defn
async def request_step_approval(payload: dict) -> dict:
    with SessionLocal() as db:
        execution = db.get(
            ProcessExecution,
            payload["execution_id"],
        )

        if execution is None:
            raise ValueError("Execution not found")

        if execution.status in ("completed", "rejected", "failed"):
            raise ValueError("Execution is no longer active")

        step_id = payload["step_id"]

        approval = db.scalar(
            select(ProcessApproval).where(
                ProcessApproval.execution_id == execution.id,
                ProcessApproval.step_id == step_id,
            )
        )

        if approval is None:
            approval = ProcessApproval(
                execution_id=execution.id,
                step_id=step_id,
                status="pending",
            )
            db.add(approval)

            write_audit(
                db,
                execution,
                "system",
                "approval.requested",
                {"step_id": step_id},
            )

        execution.status = "waiting_approval"
        db.commit()

        return {
            "approval_id": approval.id,
            "step_id": approval.step_id,
            "status": approval.status,
        }


@activity.defn
async def execute_step(payload: dict) -> dict:
    step = ProcessStep.model_validate(payload["step"])

    decision = evaluate_step(step)

    if not decision.allowed:
        raise PermissionError(decision.reason)

    # Avoid repeating an already persisted step.
    with SessionLocal() as db:
        execution = db.get(
            ProcessExecution,
            payload["execution_id"],
        )

        if execution is None:
            raise ValueError("Execution not found")

        if step.step_id in (execution.completed_steps or []):
            return {
                "step_id": step.step_id,
                "action": step.action_key,
                "status": "completed",
                "result": (execution.outputs or {}).get(step.step_id),
                "already_completed": True,
            }

    # Run potentially blocking action outside the activity event loop.
    result = await asyncio.to_thread(
        execute_action,
        step.action_key,
        step.parameters,
    )

    with SessionLocal() as db:
        execution = db.get(
            ProcessExecution,
            payload["execution_id"],
        )

        if execution is None:
            raise ValueError("Execution not found")

        # Protect against a concurrent duplicate completion.
        if step.step_id not in (execution.completed_steps or []):
            outputs = dict(execution.outputs or {})
            outputs[step.step_id] = result
            execution.outputs = outputs

            completed = list(execution.completed_steps or [])
            completed.append(step.step_id)
            execution.completed_steps = completed

            write_audit(
                db,
                execution,
                "system",
                "step.completed",
                {
                    "step_id": step.step_id,
                    "action": step.action_key,
                },
            )

            db.commit()

        return {
            "step_id": step.step_id,
            "action": step.action_key,
            "status": "completed",
            "result": result,
        }


@activity.defn
async def finalize_execution(payload: dict) -> dict:
    with SessionLocal() as db:
        execution = db.get(
            ProcessExecution,
            payload["execution_id"],
        )

        if execution is None:
            raise ValueError("Execution not found")

        status = payload["status"]

        if status not in (
            "completed",
            "rejected",
            "failed",
            "approval_timeout",
        ):
            raise ValueError("Invalid final execution status")

        execution.status = status
        execution.error = payload.get("error")
        execution.completed_at = utc_now()

        write_audit(
            db,
            execution,
            "system",
            f"execution.{status}",
            {
                "completed_steps": execution.completed_steps or [],
                "error": execution.error,
            },
        )

        db.commit()

        return {
            "execution_id": execution.id,
            "status": execution.status,
        }
