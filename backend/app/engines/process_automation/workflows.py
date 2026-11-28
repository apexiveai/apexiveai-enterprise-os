
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from .activities import (
        mark_execution_started,
        authorize_step,
        request_step_approval,
        execute_step,
        finalize_execution,
    )


DATABASE_ACTIVITY_RETRY = RetryPolicy(
    initial_interval=timedelta(seconds=2),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=30),
    maximum_attempts=3,
)

EXECUTE_STEP_RETRY = RetryPolicy(
    initial_interval=timedelta(seconds=2),
    maximum_attempts=1,
)


@workflow.defn
class EnterpriseProcessWorkflow:

    def __init__(self):
        self.approvals = {}

    @workflow.signal
    def resolve_approval(
        self,
        step_id: str,
        approved: bool,
        actor_id: str,
        reason: str = "",
    ):
        self.approvals[step_id] = {
            "approved": approved,
            "actor_id": actor_id,
            "reason": reason,
        }

    @workflow.run
    async def run(self, process: dict) -> dict:
        execution_id = process["process_id"]
        completed = []
        outputs = {}
        failed_step = None

        try:
            await workflow.execute_activity(
                mark_execution_started,
                {"execution_id": execution_id},
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=DATABASE_ACTIVITY_RETRY,
            )

            for step in process["steps"]:
                step_id = step["step_id"]

                authorization = await workflow.execute_activity(
                    authorize_step,
                    {"step": step},
                    start_to_close_timeout=timedelta(seconds=15),
                    retry_policy=DATABASE_ACTIVITY_RETRY,
                )

                if not authorization["allowed"]:
                    failed_step = step_id
                    error = authorization["reason"]

                    await workflow.execute_activity(
                        finalize_execution,
                        {
                            "execution_id": execution_id,
                            "status": "rejected",
                            "error": error,
                        },
                        start_to_close_timeout=timedelta(seconds=30),
                        retry_policy=DATABASE_ACTIVITY_RETRY,
                    )

                    return {
                        "process_id": execution_id,
                        "status": "rejected",
                        "completed_steps": completed,
                        "failed_step": failed_step,
                        "outputs": outputs,
                        "error": error,
                    }

                if authorization["requires_approval"]:
                    await workflow.execute_activity(
                        request_step_approval,
                        {
                            "execution_id": execution_id,
                            "step_id": step_id,
                        },
                        start_to_close_timeout=timedelta(seconds=30),
                        retry_policy=DATABASE_ACTIVITY_RETRY,
                    )

                    await workflow.wait_condition(
                        lambda: step_id in self.approvals,
                        timeout=timedelta(days=7),
                    )

                    decision = self.approvals[step_id]

                    if not decision["approved"]:
                        failed_step = step_id
                        error = (
                            decision["reason"]
                            or "Human approval rejected"
                        )

                        await workflow.execute_activity(
                            finalize_execution,
                            {
                                "execution_id": execution_id,
                                "status": "rejected",
                                "error": error,
                            },
                            start_to_close_timeout=timedelta(seconds=30),
                            retry_policy=DATABASE_ACTIVITY_RETRY,
                        )

                        return {
                            "process_id": execution_id,
                            "status": "rejected",
                            "completed_steps": completed,
                            "failed_step": failed_step,
                            "outputs": outputs,
                            "error": error,
                        }

                failed_step = step_id

                result = await workflow.execute_activity(
                    execute_step,
                    {
                        "execution_id": execution_id,
                        "step": step,
                    },
                    start_to_close_timeout=timedelta(
                        seconds=step.get("timeout_seconds", 60)
                    ),
                    retry_policy=EXECUTE_STEP_RETRY,
                )

                completed.append(step_id)
                outputs[step_id] = result.get("result")

            await workflow.execute_activity(
                finalize_execution,
                {
                    "execution_id": execution_id,
                    "status": "completed",
                    "error": None,
                },
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=DATABASE_ACTIVITY_RETRY,
            )

            return {
                "process_id": execution_id,
                "status": "completed",
                "completed_steps": completed,
                "failed_step": None,
                "outputs": outputs,
                "error": None,
            }

        except TimeoutError:
            error = "Approval deadline exceeded"

            await workflow.execute_activity(
                finalize_execution,
                {
                    "execution_id": execution_id,
                    "status": "approval_timeout",
                    "error": error,
                },
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=DATABASE_ACTIVITY_RETRY,
            )

            return {
                "process_id": execution_id,
                "status": "approval_timeout",
                "completed_steps": completed,
                "failed_step": failed_step,
                "outputs": outputs,
                "error": error,
            }

        except Exception as exc:
            error = f"{type(exc).__name__}: {str(exc)[:1500]}"

            await workflow.execute_activity(
                finalize_execution,
                {
                    "execution_id": execution_id,
                    "status": "failed",
                    "error": error,
                },
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=DATABASE_ACTIVITY_RETRY,
            )

            return {
                "process_id": execution_id,
                "status": "failed",
                "completed_steps": completed,
                "failed_step": failed_step,
                "outputs": outputs,
                "error": error,
            }
