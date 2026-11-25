
from dataclasses import dataclass

from .contracts import ProcessStep, RiskLevel

@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    requires_approval: bool
    reason: str

REGISTERED_ACTIONS = {
    "system.health_check",
    "system.echo",
}

APPROVAL_REQUIRED = {
    RiskLevel.HIGH,
    RiskLevel.CRITICAL,
}

def evaluate_step(step: ProcessStep) -> PolicyDecision:
    if step.action_key not in REGISTERED_ACTIONS:
        return PolicyDecision(
            allowed=False,
            requires_approval=False,
            reason="Action is not registered in the execution registry",
        )

    requires_approval = (
        step.risk_level in APPROVAL_REQUIRED
    )

    return PolicyDecision(
        allowed=True,
        requires_approval=requires_approval,
        reason=(
            "Human approval required"
            if requires_approval
            else "Allowed by execution policy"
        ),
    )