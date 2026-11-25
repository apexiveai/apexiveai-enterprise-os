
import asyncio
import os

from temporalio.client import Client
from temporalio.worker import Worker

from .workflows import EnterpriseProcessWorkflow
from .activities import authorize_step, execute_step

async def main():
    address = os.getenv(
        "TEMPORAL_ADDRESS",
        "localhost:7233",
    )

    client = await Client.connect(address)

    worker = Worker(
        client,
        task_queue="apexive.enterprise.processes",
        workflows=[
            EnterpriseProcessWorkflow,
        ],
        activities=[
            authorize_step,
            execute_step,
        ],
    )

    print("APEXIVEAI PROCESS RUNTIME ONLINE")
    print("Task Queue: apexive.enterprise.processes")

    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())