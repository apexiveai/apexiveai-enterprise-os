from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "MAX ENTERPRISE OS"
    assert data["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"


def test_health_response_structure():
    response = client.get("/health")

    assert "application" in response.json()
    assert "version" in response.json()
    assert "status" in response.json()
