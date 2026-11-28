
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from app.core.config import settings

from .workflows import EnterpriseProcessWorkflow
from .activities import (
    mark_execution_started,
    authorize_step,
    request_step_approval,
    execute_step,
    finalize_execution,
)


TASK_QUEUE = settings.temporal_task_queue


async def main():
    address = settings.temporal_address

    client = await Client.connect(address)

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[
            EnterpriseProcessWorkflow,
        ],
        activities=[
            mark_execution_started,
            authorize_step,
            request_step_approval,
            execute_step,
            finalize_execution,
        ],
    )

    print("=" * 60)
    print("APEXIVEAI PROCESS RUNTIME ONLINE")
    print(f"Temporal Server : {address}")
    print(f"Namespace       : {client.namespace}")
    print(f"Task Queue      : {TASK_QUEUE}")
    print("Workflows       : 1")
    print("Activities      : 5")
    print("=" * 60)

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
