
import asyncio
import os
from typing import Any

from temporalio.client import Client
from app.core.config import settings
from .contracts import ProcessDefinition
from .workflows import EnterpriseProcessWorkflow


TASK_QUEUE = settings.temporal_task_queue


def execution_workflow_id(tenant_id: str, execution_id: str) -> str:
    return f"enterprise-{tenant_id}-{execution_id}"

async def get_temporal_client() -> Client:
    return await Client.connect(settings.temporal_address)

async def start_execution_workflow(
    execution: Any,
    definition: Any,
    version: Any,
) -> dict:
    client = await get_temporal_client()

    steps = []

    for item in version.steps:
        step = dict(item)

        parameters = dict(step.get("parameters") or {})
        parameters["process_variables"] = execution.variables or {}

        step["parameters"] = parameters
        steps.append(step)

    payload = {
        "process_id": execution.id,
        "process_name": definition.name,
        "tenant_id": execution.tenant_id,
        "company_id": definition.company_id,
        "initiated_by": definition.created_by,
        "steps": steps,
    }

    workflow_id = execution_workflow_id(
        execution.tenant_id,
        execution.id,
    )

    handle = await client.start_workflow(
        EnterpriseProcessWorkflow.run,
        payload,
        id=workflow_id,
        task_queue=TASK_QUEUE,
    )

    return {
        "workflow_id": handle.id,
        "run_id": handle.result_run_id,
        "status": "started",
    }


def start_execution_workflow_sync(
    execution: Any,
    definition: Any,
    version: Any,
) -> dict:
    return asyncio.run(
        start_execution_workflow(
            execution,
            definition,
            version,
        )
    )


async def signal_execution_approval(
    tenant_id: str,
    execution_id: str,
    step_id: str,
    approved: bool,
    actor_id: str,
    reason: str = "",
) -> dict:
    client = await get_temporal_client()

    workflow_id = execution_workflow_id(
        tenant_id,
        execution_id,
    )

    handle = client.get_workflow_handle(workflow_id)

    await handle.signal(
        EnterpriseProcessWorkflow.resolve_approval,
        step_id,
        approved,
        actor_id,
        reason,
    )

    return {
        "workflow_id": workflow_id,
        "step_id": step_id,
        "signal": "approval_resolved",
    }


def signal_execution_approval_sync(
    tenant_id: str,
    execution_id: str,
    step_id: str,
    approved: bool,
    actor_id: str,
    reason: str = "",
) -> dict:
    return asyncio.run(
        signal_execution_approval(
            tenant_id,
            execution_id,
            step_id,
            approved,
            actor_id,
            reason,
        )
    )


async def start_process(definition: ProcessDefinition):
    client = await get_temporal_client()

    payload = definition.model_dump(mode="json")

    workflow_id = execution_workflow_id(
        definition.tenant_id,
        definition.process_id,
    )

    handle = await client.start_workflow(
        EnterpriseProcessWorkflow.run,
        payload,
        id=workflow_id,
        task_queue=TASK_QUEUE,
    )

    return {
        "workflow_id": handle.id,
        "run_id": handle.result_run_id,
        "status": "started",
    }


if __name__ == "__main__":
    definition = ProcessDefinition(
        process_id="MAX-OPS-002",
        process_name="Enterprise System Health Verification",
        tenant_id="max-myanmar",
        company_id="max-group",
        initiated_by="system",
        steps=[
            {
                "step_id": "STEP-001",
                "name": "Verify system health",
                "action_key": "system.health_check",
                "risk_level": "low",
            },
            {
                "step_id": "STEP-002",
                "name": "Verify execution registry",
                "action_key": "system.echo",
                "risk_level": "low",
                "parameters": {
                    "engine": "APEXIVEAI",
                    "environment": "enterprise",
                },
            },
        ],
    )

    print(asyncio.run(start_process(definition)))
