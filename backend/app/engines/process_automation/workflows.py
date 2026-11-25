
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from .activities import authorize_step, execute_step

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
        completed = []
        outputs = {}

        try:
            for step in process["steps"]:
                authorization = await workflow.execute_activity(
                    authorize_step,
                    step,
                    start_to_close_timeout=timedelta(seconds=15),
                    retry_policy=RetryPolicy(maximum_attempts=3),
                )

                if not authorization["allowed"]:
                    return {
                        "process_id": process["process_id"],
                        "status": "rejected",
                        "completed_steps": completed,
                        "failed_step": step["step_id"],
                        "error": authorization["reason"],
                        "outputs": outputs,
                    }

                if authorization["requires_approval"]:
                    await workflow.wait_condition(
                        lambda: step["step_id"] in self.approvals,
                        timeout=timedelta(days=7),
                    )

                    decision = self.approvals[step["step_id"]]

                    if not decision["approved"]:
                        return {
                            "process_id": process["process_id"],
                            "status": "rejected",
                            "completed_steps": completed,
                            "failed_step": step["step_id"],
                            "error": "Human approval rejected",
                            "outputs": outputs,
                        }

                result = await workflow.execute_activity(
                    execute_step,
                    step,
                    start_to_close_timeout=timedelta(
                        seconds=step.get("timeout_seconds", 60)
                    ),
                    retry_policy=RetryPolicy(
                        initial_interval=timedelta(seconds=2),
                        backoff_coefficient=2.0,
                        maximum_interval=timedelta(seconds=30),
                        maximum_attempts=3,
                    ),
                )

                completed.append(step["step_id"])
                outputs[step["step_id"]] = result

            return {
                "process_id": process["process_id"],
                "status": "completed",
                "completed_steps": completed,
                "failed_step": None,
                "outputs": outputs,
                "error": None,
            }

        except TimeoutError:
            return {
                "process_id": process["process_id"],
                "status": "approval_timeout",
                "completed_steps": completed,
                "failed_step": None,
                "outputs": outputs,
                "error": "Approval deadline exceeded",
            }