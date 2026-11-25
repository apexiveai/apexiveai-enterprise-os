def can_run_robot(role: str, environment: str) -> bool:
    if role not in {"admin", "operator"}:
        return False
    return environment in {"development", "staging", "production"}
