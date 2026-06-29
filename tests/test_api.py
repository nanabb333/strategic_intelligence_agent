from fastapi.testclient import TestClient

from app import app
from helpers import ANALYZE_PAYLOAD, create_analysis_run


def test_health_returns_ok() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_returns_current_response_shape() -> None:
    response = TestClient(app).post("/analyze", json=ANALYZE_PAYLOAD)

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
    assert "## Evidence and Confidence" in payload["brief_markdown"]
    assert payload["analysis"]["decision_case"]["decision_question"]
    assert payload["analysis"]["evidence_ledger"]["items"]
    assert payload["analysis"]["confidence_assessment"]["confidence_level"] in {"Low", "Moderate", "High"}
    evaluation = payload["analysis"]["decision_quality_evaluation"]
    assert 0.0 <= evaluation["overall_score"] <= 1.0
    assert set(evaluation) >= {
        "direct_answer_quality",
        "historical_analogue_relevance",
        "evidence_use",
        "option_clarity",
        "risk_identification",
        "change_trigger_quality",
        "localization_quality",
        "overconfidence_control",
    }


def test_markdown_download_route_returns_analyze_artifact() -> None:
    client = TestClient(app)
    run_id = create_analysis_run(client)["run_id"]

    download_response = client.get(f"/run/{run_id}/download/markdown")

    assert download_response.status_code == 200


def test_get_run_returns_stored_artifact_shape() -> None:
    client = TestClient(app)
    run_id = create_analysis_run(client)["run_id"]

    response = client.get(f"/run/{run_id}")

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == {
        "metadata",
        "analysis",
        "agent_trace",
        "brief_markdown",
        "brief_text",
        "downloads",
    }
    assert payload["metadata"]["run_id"] == run_id


def test_all_download_routes_return_success() -> None:
    client = TestClient(app)
    run_id = create_analysis_run(client)["run_id"]

    for artifact in ["markdown", "txt", "json"]:
        response = client.get(f"/run/{run_id}/download/{artifact}")
        assert response.status_code == 200
