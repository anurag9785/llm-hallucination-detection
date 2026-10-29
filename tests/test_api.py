
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200


def test_analyze_supported_claim():
    response = client.post(
        "/analyze",
        json={"answer": "Earth revolves around the Sun."},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["total_claims"] == 1
    assert data["claims"][0]["label"] == "Supported"


def test_analyze_empty_answer():
    response = client.post(
        "/analyze",
        json={"answer": ""},
    )

    assert response.status_code == 422


def test_analyze_missing_answer():
    response = client.post(
        "/analyze",
        json={},
    )

    assert response.status_code == 422


def test_analyze_contradicted_claim():
    response = client.post(
        "/analyze",
        json={"answer": "The Sun is not a star."},
    )

    assert response.status_code == 200
    assert response.json()["claims"][0]["label"] == "Contradicted"
