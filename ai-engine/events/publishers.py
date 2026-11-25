def publish_agent_completed(agent: str, execution_id: str) -> dict:
    return {"event": "agent.completed", "agent": agent, "execution_id": execution_id}
