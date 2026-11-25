
import asyncio
import os

from temporalio.client import Client

from .contracts import ProcessDefinition
from .workflows import EnterpriseProcessWorkflow

async def start_process(definition: ProcessDefinition):
    client = await Client.connect(
        os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    )

    payload = definition.model_dump(mode="json")

    handle = await client.start_workflow(
        EnterpriseProcessWorkflow.run,
        payload,
        id=f"enterprise-{definition.tenant_id}-{definition.process_id}",
        task_queue="apexive.enterprise.processes",
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