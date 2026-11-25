from services.processor import normalize_prompt

def test_normalize_prompt():
    assert normalize_prompt("  hello   world  ") == "hello world"
