from fastapi.testclient import TestClient
import pytest

from app import app
from helpers import ANALYZE_PAYLOAD, create_analysis_run
import project_workspace


@pytest.fixture(autouse=True)
def isolate_project_storage(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")


def test_health_returns_ok() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_dashboard_static_files_load() -> None:
    client = TestClient(app)

    dashboard = client.get("/dashboard/")
    project_js = client.get("/dashboard/project.js")
    styles = client.get("/dashboard/styles.css")

    assert dashboard.status_code == 200
    assert "Decision Intelligence" in dashboard.text or "Decision Companion" in dashboard.text
    assert project_js.status_code == 200
    assert "getActiveProjectAnalysisContext" in project_js.text
    assert styles.status_code == 200
    assert "@media print" in styles.text


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


def test_project_creation_listing_and_questions() -> None:
    client = TestClient(app)

    create_response = client.post(
        "/projects",
        json={"name": "Export Controls Workspace", "description": "Long-running decision"},
    )

    assert create_response.status_code == 200
    project = create_response.json()
    assert project["project_id"]
    assert project["questions"] == []
    assert project["evidence_library"] == []
    assert project["decision_history"] == []

    list_response = client.get("/projects")
    assert list_response.status_code == 200
    assert any(item["project_id"] == project["project_id"] for item in list_response.json()["projects"])

    question_response = client.post(
        f"/projects/{project['project_id']}/questions",
        json={"question": "What should management decide first?"},
    )
    assert question_response.status_code == 200
    assert question_response.json()["questions"][0]["question"] == "What should management decide first?"


def test_project_evidence_routes() -> None:
    client = TestClient(app)
    project = client.post("/projects", json={"name": "Evidence Workspace"}).json()

    add_response = client.post(
        f"/projects/{project['project_id']}/evidence",
        json={
            "title": "Policy bulletin",
            "source_type": "Manual note",
            "text_excerpt": "New export-control rules affect advanced chips.",
            "status": "User Provided",
        },
    )

    assert add_response.status_code == 200
    assert add_response.json()["evidence_library"][0]["status"] == "User Provided"

    list_response = client.get(f"/projects/{project['project_id']}/evidence")
    assert list_response.status_code == 200
    assert list_response.json()["evidence"][0]["title"] == "Policy bulletin"


def test_project_analyze_creates_question_decision_history_and_delta() -> None:
    client = TestClient(app)
    project = client.post("/projects", json={"name": "Decision Timeline Workspace"}).json()

    first_payload = {
        **ANALYZE_PAYLOAD,
        "project_id": project["project_id"],
        "question_text": "Should management pause affected shipments?",
    }
    first = client.post("/analyze", json=first_payload)
    assert first.status_code == 200

    second_payload = {
        **ANALYZE_PAYLOAD,
        "text": "New semiconductor export controls now include clearer licensing paths and customer exemptions.",
        "project_id": project["project_id"],
        "question_text": "Should management resume lower-risk customer shipments?",
    }
    second = client.post("/analyze", json=second_payload)
    assert second.status_code == 200

    refreshed = client.get(f"/projects/{project['project_id']}").json()
    assert len(refreshed["questions"]) == 2
    assert refreshed["questions"][0]["run_id"] == first.json()["run_id"]
    assert len(refreshed["decision_history"]) == 2
    assert refreshed["decision_history"][0]["recommendation_summary"]
    assert 0.0 <= refreshed["decision_history"][0]["decision_quality_score"] <= 1.0

    delta = client.get(f"/projects/{project['project_id']}/delta")
    assert delta.status_code == 200
    delta_payload = delta.json()
    assert delta_payload["available"] is True
    assert set(delta_payload) >= {
        "previous_recommendation",
        "current_recommendation",
        "confidence_change",
        "decision_quality_change",
        "evidence_added",
        "evidence_missing_or_weakened",
        "recommendation_changed",
    }


def test_project_analyze_links_existing_question_record() -> None:
    client = TestClient(app)
    project = client.post("/projects", json={"name": "Linked Question Workspace"}).json()
    project = client.post(
        f"/projects/{project['project_id']}/questions",
        json={"question": "Should management continue affected orders?"},
    ).json()
    question_id = project["questions"][0]["question_id"]

    response = client.post(
        "/analyze",
        json={
            **ANALYZE_PAYLOAD,
            "project_id": project["project_id"],
            "project_question_id": question_id,
            "question_text": "Should management continue affected orders?",
        },
    )

    assert response.status_code == 200
    refreshed = client.get(f"/projects/{project['project_id']}").json()
    assert len(refreshed["questions"]) == 1
    assert refreshed["questions"][0]["question_id"] == question_id
    assert refreshed["questions"][0]["run_id"] == response.json()["run_id"]
    assert refreshed["decision_history"][0]["question_id"] == question_id
