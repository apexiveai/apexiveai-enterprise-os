def can_execute_agent(role: str, agent: str) -> bool:
    return role in {"admin", "operator", "analyst"} and bool(agent)
