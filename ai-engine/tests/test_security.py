from security.policies import can_execute_agent

def test_agent_policy():
    assert can_execute_agent("admin", "general")
    assert not can_execute_agent("guest", "general")
