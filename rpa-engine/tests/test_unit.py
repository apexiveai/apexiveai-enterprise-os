from services.processor import validate_robot_name

def test_validate_robot_name():
    assert validate_robot_name("  finance-sync ") == "finance-sync"
