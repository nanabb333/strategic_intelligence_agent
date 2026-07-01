import json

from fastapi.testclient import TestClient

from app import app
from decision_review import ALLOWED_REVIEW_STATUSES, default_decision_review_state, update_decision_review_state
import project_workspace
from project_workspace import create_project


def _project():
    return {
        "project_id": "p1",
        "name": "Review Workspace",
        "questions": [{"question_id": "q1", "question": "Compare pathways."}],
        "evidence_library": [{"evidence_id": "ev1", "title": "Evidence"}],
        "decision_history": [{"decision_id": "d1", "brief_path": "outputs/runs/run_1/brief.md"}],
    }


def test_default_empty_review_state_for_legacy_project() -> None:
    state = default_decision_review_state(_project())

    assert state["project_id"] == "p1"
    assert state["decision_question"] == "Compare pathways."
    assert state["pathway_reviews"] == []
    assert state["review_summary"]["reviewed_pathways_count"] == 0


def test_pathway_review_update_and_note() -> None:
    project = _project()
    state = update_decision_review_state(
        project,
        {
            "target_type": "pathway",
            "target_id": "pathway_draft_1",
            "review_status": "reviewed",
            "reviewer_note": "Evidence reviewed by product reviewer.",
            "related_evidence_refs": [{"evidence_id": "ev1", "title": "Evidence"}],
        },
    )

    assert state["pathway_reviews"][0]["pathway_id"] == "pathway_draft_1"
    assert state["pathway_reviews"][0]["review_status"] == "reviewed"
    assert state["reviewer_notes"][0]["note"] == "Evidence reviewed by product reviewer."
    assert state["review_summary"]["reviewed_pathways_count"] == 1


def test_comparison_cell_review_update() -> None:
    state = update_decision_review_state(
        _project(),
        {
            "target_type": "comparison_cell",
            "target_id": "pathway_draft_1",
            "comparison_dimension": "unknowns_remaining",
            "review_status": "needs_more_evidence",
        },
    )

    cell = state["comparison_cell_reviews"][0]
    assert cell["pathway_id"] == "pathway_draft_1"
    assert cell["comparison_dimension"] == "unknowns_remaining"
    assert state["review_summary"]["needs_more_evidence_count"] == 1


def test_assumption_unknown_and_trigger_reviews_update() -> None:
    project = _project()
    state = update_decision_review_state(project, {"target_type": "assumption", "target_id": "market_continuity", "review_status": "questioned"})
    project["decision_review_state"] = state
    state = update_decision_review_state(project, {"target_type": "unknown", "target_id": "missing_timeline", "review_status": "unresolved"})
    project["decision_review_state"] = state
    state = update_decision_review_state(project, {"target_type": "decision_trigger", "target_id": "new_evidence", "review_status": "needs_legal_or_compliance_review"})

    assert state["assumption_reviews"][0]["review_status"] == "questioned"
    assert state["unknown_reviews"][0]["review_status"] == "unresolved"
    assert state["trigger_reviews"][0]["review_status"] == "needs_legal_or_compliance_review"
    assert state["review_summary"]["needs_legal_or_compliance_review_count"] == 1


def test_unresolved_questions_persisted() -> None:
    state = update_decision_review_state(
        _project(),
        {
            "target_type": "pathway",
            "target_id": "pathway_draft_2",
            "review_status": "unresolved",
            "unresolved_question": "Which evidence would resolve timing uncertainty?",
        },
    )

    assert state["unresolved_questions"][0]["question"] == "Which evidence would resolve timing uncertainty?"
    assert state["review_summary"]["unresolved_decision_questions_count"] == 1


def test_review_state_rejects_forbidden_statuses() -> None:
    assert "approved" not in ALLOWED_REVIEW_STATUSES
    assert "rejected" not in ALLOWED_REVIEW_STATUSES
    assert "selected" not in ALLOWED_REVIEW_STATUSES
    assert "recommended" not in ALLOWED_REVIEW_STATUSES


def test_review_state_does_not_mutate_evidence_or_decision_history() -> None:
    project = _project()
    evidence_before = json.loads(json.dumps(project["evidence_library"]))
    history_before = json.loads(json.dumps(project["decision_history"]))

    update_decision_review_state(
        project,
        {"target_type": "pathway", "target_id": "pathway_draft_1", "review_status": "reviewed"},
    )

    assert project["evidence_library"] == evidence_before
    assert project["decision_history"] == history_before


def test_decision_review_api_read_write_behavior(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")
    project = create_project("Review API Workspace")
    project["questions"] = [{"question_id": "q1", "question": "Compare pathways."}]
    project["evidence_library"] = [{"evidence_id": "ev1", "title": "Evidence"}]
    project_workspace.save_project(project)
    client = TestClient(app)

    empty = client.get(f"/projects/{project['project_id']}/decision/review")
    update = client.put(
        f"/projects/{project['project_id']}/decision/review",
        json={
            "target_type": "comparison_cell",
            "target_id": "pathway_draft_1",
            "comparison_dimension": "risk_exposure",
            "review_status": "needs_more_evidence",
            "reviewer_note": "Need second source.",
        },
    )
    loaded = client.get(f"/projects/{project['project_id']}/decision/review")

    assert empty.status_code == 200
    assert empty.json()["comparison_cell_reviews"] == []
    assert update.status_code == 200
    assert loaded.json()["comparison_cell_reviews"][0]["review_status"] == "needs_more_evidence"
    assert loaded.json()["reviewer_notes"][0]["note"] == "Need second source."


def test_decision_review_api_does_not_mutate_evidence_or_brief_path(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")
    project = create_project("Review Mutation Workspace")
    project["questions"] = [{"question_id": "q1", "question": "Compare pathways.", "brief_path": "outputs/runs/run_1/brief.md"}]
    project["evidence_library"] = [{"evidence_id": "ev1", "title": "Evidence"}]
    project_workspace.save_project(project)
    path = project_workspace.PROJECTS_DIR / f"{project['project_id']}.json"
    before = json.loads(path.read_text(encoding="utf-8"))

    response = TestClient(app).put(
        f"/projects/{project['project_id']}/decision/review",
        json={"target_type": "pathway", "target_id": "pathway_draft_1", "review_status": "reviewed"},
    )
    after = json.loads(path.read_text(encoding="utf-8"))

    assert response.status_code == 200
    assert after["evidence_library"] == before["evidence_library"]
    assert after["questions"][0]["brief_path"] == before["questions"][0]["brief_path"]
    assert "decision_review_state" in after
