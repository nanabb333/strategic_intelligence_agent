from fastapi.testclient import TestClient

from app import app


def test_health_returns_ok() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_returns_current_response_shape() -> None:
    response = TestClient(app).post(
        "/analyze",
        json={
            "text": "New semiconductor export controls affect advanced chip supply chains and market access.",
            "language": "en",
            "output_mode": "analyst",
            "question_text": "What should determine this decision?",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == {
        "run_id",
        "metadata",
        "analysis",
        "brief_markdown",
        "brief_text",
        "downloads",
    }
    assert payload["run_id"]
    assert payload["downloads"]["markdown"]
    assert payload["downloads"]["txt"]
    assert payload["downloads"]["json"]


def test_markdown_download_route_returns_analyze_artifact() -> None:
    client = TestClient(app)
    analyze_response = client.post(
        "/analyze",
        json={
            "text": "New semiconductor export controls affect advanced chip supply chains and market access.",
            "language": "en",
            "output_mode": "analyst",
            "question_text": "What should determine this decision?",
        },
    )
    assert analyze_response.status_code == 200
    run_id = analyze_response.json()["run_id"]

    download_response = client.get(f"/run/{run_id}/download/markdown")

    assert download_response.status_code == 200
