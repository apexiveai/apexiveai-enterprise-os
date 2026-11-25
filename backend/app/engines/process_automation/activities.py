
from temporalio import activity

from .contracts import ProcessStep
from .policy import evaluate_step
from .actions import execute_action

@activity.defn
async def authorize_step(payload: dict) -> dict:
    step = ProcessStep.model_validate(payload)

    decision = evaluate_step(step)

    return {
        "allowed": decision.allowed,
        "requires_approval": decision.requires_approval,
        "reason": decision.reason,
    }

@activity.defn
async def execute_step(payload: dict) -> dict:
    step = ProcessStep.model_validate(payload)

    decision = evaluate_step(step)

    if not decision.allowed:
        raise PermissionError(decision.reason)

    result = execute_action(
        step.action_key,
        step.parameters,
    )

    return {
        "step_id": step.step_id,
        "action": step.action_key,
        "status": "completed",
        "result": result,
    }