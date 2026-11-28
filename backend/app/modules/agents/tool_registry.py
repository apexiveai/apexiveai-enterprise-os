from dataclasses import dataclass
from typing import Any, Callable

from app.engines.process_automation.actions import ACTION_REGISTRY


@dataclass(frozen=True)
class ToolDefinition:
    tool_key: str
    description: str
    risk_level: str
    handler: Callable[[dict[str, Any]], dict[str, Any]]


TOOL_REGISTRY = {
    "system.health_check": ToolDefinition(
        tool_key="system.health_check",
        description="Return a health status and timestamp.",
        risk_level="low",
        handler=ACTION_REGISTRY["system.health_check"],
    ),
    "system.echo": ToolDefinition(
        tool_key="system.echo",
        description="Return the provided parameters without side effects.",
        risk_level="low",
        handler=ACTION_REGISTRY["system.echo"],
    ),
}


class ToolNotFoundError(Exception):
    pass


def list_tools() -> list[ToolDefinition]:
    return list(TOOL_REGISTRY.values())


def validate_tool_keys(tool_keys: list[str]) -> None:
    unknown = sorted(set(tool_keys) - TOOL_REGISTRY.keys())
    if unknown:
        raise ValueError(f"Unknown tools: {', '.join(unknown)}")


def execute_tool(tool_key: str, parameters: dict[str, Any]) -> dict[str, Any]:
    tool = TOOL_REGISTRY.get(tool_key)
    if tool is None:
        raise ToolNotFoundError(tool_key)
    return tool.handler(parameters)
