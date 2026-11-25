from security.policies import can_run_robot

def test_robot_policy():
    assert can_run_robot("operator", "production")
    assert not can_run_robot("viewer", "production")
