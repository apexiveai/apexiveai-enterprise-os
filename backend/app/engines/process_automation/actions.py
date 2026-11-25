
from datetime import datetime, timezone
from typing import Any, Callable

ActionHandler = Callable[[dict[str, Any]], dict[str, Any]]

ACTION_REGISTRY: dict[str, ActionHandler] = {}

def register_action(name: str):
    def decorator(handler: ActionHandler):
        if name in ACTION_REGISTRY:
            raise ValueError(f"Duplicate action: {name}")

        ACTION_REGISTRY[name] = handler
        return handler

    return decorator

@register_action("system.health_check")
def health_check(parameters: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@register_action("system.echo")
def echo(parameters: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "completed",
        "data": parameters,
    }

def execute_action(
    action_key: str,
    parameters: dict[str, Any],
) -> dict[str, Any]:

    handler = ACTION_REGISTRY.get(action_key)

    if handler is None:
        raise PermissionError(
            f"Unregistered action: {action_key}"
        )

    return handler(parameters)