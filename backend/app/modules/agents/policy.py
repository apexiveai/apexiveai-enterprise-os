from app.modules.agents.models import AgentDefinition
from app.modules.agents.tool_registry import TOOL_REGISTRY


class AgentPolicyError(Exception):
    pass


def validate_tool_access(agent: AgentDefinition, tool_key: str) -> None:
    if agent.status != "active":
        raise AgentPolicyError("Agent is not active.")
    if tool_key not in agent.allowed_tools:
        raise AgentPolicyError("Tool is not authorized for this agent.")
    tool = TOOL_REGISTRY.get(tool_key)
    if tool is None:
        raise AgentPolicyError("Tool is not registered.")
    if tool.risk_level != "low":
        raise AgentPolicyError("Tool requires an approval policy that is not enabled.")


def validate_agent_run(agent: AgentDefinition, prompt: str) -> None:
    if agent.status != "active":
        raise AgentPolicyError("Agent is not active.")
    if not prompt.strip():
        raise AgentPolicyError("Prompt must not be empty.")
    if len(prompt) > 12000:
        raise AgentPolicyError("Prompt exceeds the 12000 character limit.")
