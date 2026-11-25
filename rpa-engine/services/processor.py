def validate_robot_name(name: str) -> str:
    normalized = name.strip()
    if not normalized:
        raise ValueError("Robot name is required")
    return normalized
