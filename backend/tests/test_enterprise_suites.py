from app.modules.enterprise_suites import SUITES


def test_enterprise_suite_registry_is_complete():
    assert len(SUITES) == 15
    names = {suite["name"] for suite in SUITES}
    assert "AI Bot Studio" in names
    assert "Automation Center" in names
    assert "Digital Twin" in names
