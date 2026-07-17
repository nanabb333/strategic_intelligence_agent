from fastapi.testclient import TestClient
import json
import pytest

import app as app_module
from app import app
from evidence_retrieval import source_tier
from helpers import ANALYZE_PAYLOAD, create_analysis_run
import project_workspace


@pytest.fixture(autouse=True)
def isolate_project_storage(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")


def test_health_returns_ok() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_cors_allows_local_origin_and_rejects_unlisted_origin() -> None:
    client = TestClient(app)
    allowed = client.options(
        "/health",
        headers={"Origin": "http://127.0.0.1:8000", "Access-Control-Request-Method": "GET"},
    )
    blocked = client.options(
        "/health",
        headers={"Origin": "https://untrusted.example", "Access-Control-Request-Method": "GET"},
    )

    assert allowed.headers.get("access-control-allow-origin") == "http://127.0.0.1:8000"
    assert blocked.headers.get("access-control-allow-origin") is None


def test_dashboard_static_files_load() -> None:
    client = TestClient(app)

    dashboard = client.get("/dashboard/")
    project_js = client.get("/dashboard/project.js")
    styles = client.get("/dashboard/styles.css")

    assert dashboard.status_code == 200
    assert "Decision Intelligence" in dashboard.text or "Decision Companion" in dashboard.text
    assert "Evidence Intelligence" in dashboard.text
    assert project_js.status_code == 200
    assert "getActiveProjectAnalysisContext" in project_js.text
    assert "fetchEvidenceIntelligence" in project_js.text
    assert styles.status_code == 200
    assert "evidence-intelligence-panel" in styles.text
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
    assert "## Evidence Sufficiency" in payload["brief_markdown"]
    assessment = payload["analysis"]["decision_assessment"]
    assert assessment["decision_question"]
    assert assessment["reviewer_selected_path"] == ""
    assert assessment["selection_status"] == "No pathway selected"
    assert "recommended_path" not in assessment
    assert payload["analysis"]["evidence_ledger"]["items"]
    assert payload["analysis"]["evidence_sufficiency"]["tier"] in {
        "Insufficient", "Limited", "Reviewable", "Evidence-rich"
    }
    completeness = payload["analysis"]["artifact_completeness"]
    assert 0.0 <= completeness["completion_rate"] <= 1.0
    assert completeness["passed_checks"] <= completeness["total_checks"]
    assert completeness["interpretation_boundary"]


@pytest.mark.parametrize("output_mode", ["analyst", "beginner", "executive"])
def test_all_output_modes_remain_neutral(output_mode: str) -> None:
    payload = TestClient(app).post(
        "/analyze",
        json={**ANALYZE_PAYLOAD, "output_mode": output_mode},
    ).json()

    assessment = payload["analysis"]["decision_assessment"]
    assert assessment["reviewer_selected_path"] == ""
    assert "recommended_path" not in assessment
    assert "Option B (Recommended)" not in payload["brief_markdown"]
    assert "## Preferred Path" not in payload["brief_markdown"]
    assert "## Option Ranking" not in payload["brief_markdown"]


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
        "tool_routing_trace",
        "brief_markdown",
        "brief_text",
        "downloads",
    }
    assert payload["metadata"]["run_id"] == run_id


def test_legacy_run_is_rendered_as_neutral_read_only_view(tmp_path, monkeypatch) -> None:
    run_dir = tmp_path / "legacy_run"
    run_dir.mkdir()
    (run_dir / "metadata.json").write_text(json.dumps({"run_id": "legacy_run"}), encoding="utf-8")
    (run_dir / "analysis.json").write_text(
        json.dumps(
            {
                "decision_case": {
                    "decision_question": "What should reviewers compare?",
                    "situation": "Legacy situation",
                    "recommended_path": "Option B legacy system recommendation",
                },
                "confidence_assessment": {"confidence_level": "Moderate"},
            }
        ),
        encoding="utf-8",
    )
    (run_dir / "agent_trace.json").write_text("{}", encoding="utf-8")
    (run_dir / "brief.md").write_text("## Preferred Path\nOption B", encoding="utf-8")
    (run_dir / "brief.txt").write_text("Option B", encoding="utf-8")
    monkeypatch.setattr(app_module, "run_dir_or_404", lambda run_id: run_dir)

    payload = TestClient(app).get("/run/legacy_run").json()

    assert payload["analysis"]["decision_assessment"]["reviewer_selected_path"] == ""
    assert payload["analysis"]["decision_assessment"]["selection_rationale"] == ""
    assert "decision_case" not in payload["analysis"]
    assert "confidence_assessment" not in payload["analysis"]
    assert "decision_quality_evaluation" not in payload["analysis"]
    assert "Option B" not in payload["brief_markdown"]
    assert "former system-generated recommendation is not displayed" in payload["brief_markdown"]
    assert "#" not in payload["brief_text"]
    assert "**" not in payload["brief_text"]
    assert payload["legacy_contract"]["contract_status"] == "superseded"
    assert payload["historical_raw_downloads"]["markdown"].endswith("/historical-raw/markdown")


def test_legacy_current_exports_are_neutral_and_historical_raw_is_explicit(tmp_path, monkeypatch) -> None:
    run_dir = tmp_path / "legacy_exports"
    run_dir.mkdir()
    legacy_analysis = {
        "decision_case": {
            "decision_question": "What should reviewers compare?",
            "situation": "Legacy situation",
            "recommended_path": "Option B legacy system recommendation",
        },
        "confidence_assessment": {"confidence_level": "High"},
        "decision_quality_evaluation": {"overall_score": 1.0},
        "evidence_ledger": {"items": [{"evidence_id": "E1", "confidence": "High"}]},
    }
    (run_dir / "metadata.json").write_text(json.dumps({"run_id": "legacy_exports"}), encoding="utf-8")
    (run_dir / "analysis.json").write_text(json.dumps(legacy_analysis), encoding="utf-8")
    (run_dir / "agent_trace.json").write_text("{}", encoding="utf-8")
    (run_dir / "brief.md").write_text("## Preferred Path\nOption B", encoding="utf-8")
    (run_dir / "brief.txt").write_text("Option B", encoding="utf-8")
    monkeypatch.setattr(app_module, "run_dir_or_404", lambda run_id: run_dir)
    client = TestClient(app)

    markdown = client.get("/run/legacy_exports/download/markdown")
    text = client.get("/run/legacy_exports/download/txt")
    current_json = client.get("/run/legacy_exports/download/json")

    for response in (markdown, text, current_json):
        assert response.status_code == 200
        assert "Option B" not in response.text
        assert "Preferred Path" not in response.text
        assert "overall_score" not in response.text
    assert "#" not in text.text
    assert "**" not in text.text
    assert current_json.json()["decision_assessment"]["reviewer_selected_path"] == ""
    assert current_json.json()["decision_assessment"]["selection_rationale"] == ""
    assert "confidence" not in current_json.json()["evidence_ledger"]["items"][0]
    assert current_json.json()["decision_assessment"]["assessment_summary"] == (
        "Legacy assessment artifact normalized for current neutral review."
    )

    raw_markdown = client.get("/run/legacy_exports/download/historical-raw/markdown")
    raw_json = client.get("/run/legacy_exports/download/historical-raw/json")
    assert "Option B" in raw_markdown.text
    assert raw_json.json()["decision_case"]["recommended_path"].startswith("Option B")
    assert raw_markdown.headers["x-artifact-mode"] == "historical-raw-read-only"
    assert raw_markdown.headers["x-artifact-contract"] == "superseded"
    assert "historical-raw-read-only" in raw_markdown.headers["content-disposition"]
    assert (run_dir / "brief.md").read_text(encoding="utf-8") == "## Preferred Path\nOption B"


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


def test_retrieve_evidence_returns_deterministic_review_queue_shape() -> None:
    client = TestClient(app)

    response = client.post(
        "/retrieve-evidence",
        json={"query": "semiconductor export controls licensing"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["retrieval_id"]
    assert payload["query"] == "semiconductor export controls licensing"
    assert payload["retrieved_at"]
    assert payload["items"]
    assert {item["credibility_tier"] for item in payload["items"]} <= {
        "Tier 1 Official",
        "Tier 2 Company",
        "Tier 3 Reputable News",
    }
    first = payload["items"][0]
    assert set(first) >= {
        "evidence_id",
        "title",
        "source_name",
        "source_url",
        "source_type",
        "publisher",
        "author",
        "published_at",
        "retrieved_at",
        "excerpt",
        "summary",
        "status",
        "credibility_tier",
        "credibility_score",
        "freshness_note",
        "relevance_score",
        "validation_status",
        "validation_notes",
        "conflict_status",
        "trace_id",
    }
    assert first["status"] == "Retrieved"
    assert first["validation_status"] == "Valid"


def test_retrieved_items_are_not_automatically_added_to_project() -> None:
    client = TestClient(app)
    project = client.post("/projects", json={"name": "Retrieval Workspace"}).json()

    response = client.post(
        "/retrieve-evidence",
        json={
            "query": "export controls",
            "project_id": project["project_id"],
        },
    )

    assert response.status_code == 200
    refreshed = client.get(f"/projects/{project['project_id']}").json()
    assert refreshed["evidence_library"] == []


def test_accept_retrieved_items_adds_traceable_evidence_to_project() -> None:
    client = TestClient(app)
    project = client.post("/projects", json={"name": "Accept Evidence Workspace"}).json()
    retrieved = client.post(
        "/retrieve-evidence",
        json={"query": "semiconductor export controls"},
    ).json()
    selected = retrieved["items"][:2]

    response = client.post(
        f"/projects/{project['project_id']}/evidence/accept",
        json={"items": selected},
    )

    assert response.status_code == 200
    evidence = response.json()["evidence_library"]
    assert len(evidence) == 2
    assert evidence[0]["status"] == "Accepted"
    assert evidence[0]["source_url"]
    assert evidence[0]["source_name"]
    assert evidence[0]["retrieved_at"]
    assert evidence[0]["published_at"]
    assert evidence[0]["credibility_tier"].startswith("Tier ")
    assert evidence[0]["validation_status"]
    assert evidence[0]["trace_id"]
    assert evidence[0]["conflict_status"] == "No Conflict"
    assert evidence[0]["freshness_note"]


def test_source_tiering_rules() -> None:
    assert source_tier("SEC", "https://www.sec.gov/", "regulator") == "Tier 1 Official"
    assert source_tier("Issuer", "", "10-K annual report") == "Tier 2 Company"
    assert source_tier("Reuters", "https://www.reuters.com/", "news") == "Tier 3 Reputable News"
    assert source_tier("AP", "", "news") == "Tier 3 Reputable News"
    assert source_tier("FT", "", "news") == "Tier 3 Reputable News"
    assert source_tier("OECD", "https://www.oecd.org/", "research") == "Tier 4 Research"
    assert source_tier("Personal Blog", "https://example.com/blog", "blog") == "Tier 5 Other"


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
    assert refreshed["decision_history"][0]["assessment_summary"]
    assert refreshed["decision_history"][0]["reviewer_selected_path"] == ""
    assert 0.0 <= refreshed["decision_history"][0]["artifact_completeness_rate"] <= 1.0

    delta = client.get(f"/projects/{project['project_id']}/delta")
    assert delta.status_code == 200
    delta_payload = delta.json()
    assert delta_payload["available"] is True
    assert set(delta_payload) >= {
        "previous_assessment",
        "current_assessment",
        "evidence_sufficiency_change",
        "artifact_completeness_change",
        "evidence_added",
        "evidence_missing_or_weakened",
        "assessment_changed",
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


def test_project_analysis_persists_decision_context_and_project_evidence_ids() -> None:
    client = TestClient(app)
    project = client.post("/projects", json={"name": "Decision Context Workspace"}).json()
    project = client.post(
        f"/projects/{project['project_id']}/questions",
        json={"question": "Should management change the shipment plan?"},
    ).json()
    question_id = project["questions"][0]["question_id"]
    project = client.post(
        f"/projects/{project['project_id']}/evidence",
        json={
            "title": "Customer exposure note",
            "source_type": "Manual note",
            "text_excerpt": "A named customer depends on components covered by the export-control update.",
            "status": "Accepted",
        },
    ).json()
    evidence_id = project["evidence_library"][0]["evidence_id"]

    response = client.post(
        "/analyze",
        json={
            **ANALYZE_PAYLOAD,
            "project_id": project["project_id"],
            "project_question_id": question_id,
            "question_text": "Should management change the shipment plan?",
            "evidence_ids": [evidence_id],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["metadata"]["project_id"] == project["project_id"]
    assert payload["metadata"]["project_question_id"] == question_id
    assert payload["metadata"]["evidence_ids"] == [evidence_id]
    assert payload["analysis"]["evidence_bundle"][0]["evidence_id"] == evidence_id
    assert any(
        item["evidence_id"] == evidence_id
        for item in payload["analysis"]["evidence_ledger"]["items"]
    )

    refreshed = client.get(f"/projects/{project['project_id']}").json()
    assert refreshed["decision_history"][0]["evidence_ids"] == [evidence_id]
    assert refreshed["evidence_library"][0]["status"] == "Used"
    assert refreshed["workspace_state"]["last_analyzed_question_id"] == question_id
    assert refreshed["workspace_state"]["evidence_count"] == 1
    assert refreshed["workspace_state"]["decision_count"] == 1
