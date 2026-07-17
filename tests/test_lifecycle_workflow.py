import pytest

from decision_lifecycle import (
    DRAFT,
    REVIEWED,
    default_decision_state,
    transition_decision_state,
)
from evidence_lifecycle import (
    ACCEPTED,
    ARCHIVED,
    NEEDS_REVIEW,
    REFERENCED,
    REJECTED,
    default_evidence_lifecycle_state,
)
from evidence_retrieval import confidence_impact_metadata, normalize_evidence_item
import project_workspace


@pytest.fixture(autouse=True)
def isolate_project_storage(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")


def test_evidence_lifecycle_default_states_are_migration_safe() -> None:
    assert default_evidence_lifecycle_state({}) == "retrieved"
    assert default_evidence_lifecycle_state({"status": "Accepted"}) == ACCEPTED
    assert default_evidence_lifecycle_state({"status": "Used"}) == REFERENCED
    assert default_evidence_lifecycle_state({"status": "Conflicting"}) == NEEDS_REVIEW
    assert default_evidence_lifecycle_state({"status": "Archived"}) == ARCHIVED


def test_review_actions_append_accepted_rejected_needs_review_and_archive_ledger_entries() -> None:
    project = project_workspace.create_project("Lifecycle Workspace")
    project = project_workspace.add_evidence_to_project(
        project["project_id"],
        {
            "title": "Reviewer note",
            "source_type": "Manual note",
            "text_excerpt": "Evidence entered by a reviewer.",
            "status": "User Provided",
        },
    )
    evidence_id = project["evidence_library"][0]["evidence_id"]

    project = project_workspace.review_project_evidence(
        project["project_id"],
        evidence_id,
        action="mark_needs_review",
        review_reason="Source date is missing.",
    )
    project = project_workspace.review_project_evidence(
        project["project_id"],
        evidence_id,
        action="accept",
        review_reason="Reviewer verified the source context.",
    )
    project = project_workspace.review_project_evidence(
        project["project_id"],
        evidence_id,
        action="reject",
        review_reason="Later review found the evidence was not applicable.",
    )
    project = project_workspace.review_project_evidence(
        project["project_id"],
        evidence_id,
        action="archive",
        review_reason="Kept for traceability only.",
    )

    assert project["evidence_library"][0]["lifecycle_state"] == ARCHIVED
    assert [entry["reviewer_action"] for entry in project["evidence_audit_log"]] == [
        "mark_needs_review",
        "accept",
        "reject",
        "archive",
    ]
    assert [entry["lifecycle_state"] for entry in project["evidence_audit_log"]] == [
        NEEDS_REVIEW,
        ACCEPTED,
        REJECTED,
        ARCHIVED,
    ]
    assert all(entry["evidence_id"] == evidence_id for entry in project["evidence_audit_log"])


def test_accept_retrieved_evidence_adds_acceptance_ledger_entry() -> None:
    project = project_workspace.create_project("Accept Ledger Workspace")
    item = normalize_evidence_item(
        {
            "title": "Official source",
            "source_type": "Government / regulator",
            "source_name": "Official Government Release",
            "source_url": "https://agency.gov/update",
            "published_at": "2026-06-30",
            "excerpt": "Official update text.",
            "trace_id": "trace_source",
        },
        query="official update",
        retrieved_at="2026-06-30T10:00:00",
    )

    project = project_workspace.accept_retrieved_evidence(project["project_id"], [item.__dict__])

    evidence = project["evidence_library"][0]
    ledger = project["evidence_audit_log"][0]
    assert evidence["lifecycle_state"] == ACCEPTED
    assert evidence["reviewer_status"] == ACCEPTED
    assert evidence["evidence_action"] == "accept"
    assert ledger["reviewer_action"] == "accept"
    assert ledger["trace_id"] == "trace_source"
    assert ledger["confidence_effect"] == "strengthens_confidence_metadata"


def test_referenced_evidence_remains_traceable_when_used_in_decision() -> None:
    project = project_workspace.create_project("Referenced Evidence Workspace")
    project = project_workspace.add_question_to_project(project["project_id"], "Should we proceed?")
    question_id = project["questions"][0]["question_id"]
    project = project_workspace.add_evidence_to_project(
        project["project_id"],
        {
            "title": "Accepted note",
            "source_type": "Manual note",
            "text_excerpt": "Evidence selected for analysis.",
            "status": "Accepted",
        },
    )
    evidence_id = project["evidence_library"][0]["evidence_id"]

    project = project_workspace.attach_run_to_question(
        project["project_id"],
        question_id=question_id,
        run_id="run_test",
        analysis={
            "decision_assessment": {
                "assessment_summary": "Review exposure across neutral pathways.",
                "reviewer_selected_path": "",
            },
            "evidence_sufficiency": {"tier": "Reviewable"},
            "artifact_completeness": {"completion_rate": 0.8, "passed_checks": 8, "total_checks": 10},
        },
        evidence_ids=[evidence_id],
    )

    assert project["evidence_library"][0]["lifecycle_state"] == REFERENCED
    assert project["decision_history"][0]["decision_status"] == REVIEWED
    assert project["decision_history"][0]["supporting_evidence_count"] == 1
    assert project["decision_history"][0]["artifact_completeness_passed"] == 8
    assert project["decision_history"][0]["artifact_completeness_total"] == 10
    assert project["evidence_audit_log"][-1]["reviewer_action"] == "reference_in_decision"
    assert project["evidence_audit_log"][-1]["decision_run_id"] == "run_test"
    assert project["evidence_audit_log"][-1]["project_question_id"] == question_id


def test_decision_lifecycle_default_and_safe_transitions() -> None:
    assert default_decision_state({}) == DRAFT
    assert default_decision_state({"run_id": "run_1"}) == REVIEWED
    assert transition_decision_state(DRAFT, "evidence_review") == "evidence_review"
    assert transition_decision_state("evidence_review", REVIEWED) == REVIEWED
    with pytest.raises(ValueError):
        transition_decision_state("archived", REVIEWED)


def test_old_project_evidence_remains_compatible() -> None:
    project = project_workspace.create_project("Old Evidence Workspace")
    project["evidence_library"].append(
        {
            "evidence_id": "old_1",
            "title": "Old note",
            "source_type": "Manual note",
            "summary": "Legacy shape without lifecycle fields.",
            "status": "Accepted",
        }
    )
    project = project_workspace.save_project(project)

    bundle = project_workspace.evidence_bundle_for_project(project, ["old_1"])

    assert bundle[0]["evidence_id"] == "old_1"
    assert project["workspace_state"]["evidence_count"] == 1


def test_legacy_history_recommendation_is_not_exposed_as_current_assessment() -> None:
    project = project_workspace.create_project("Legacy History Workspace")
    project["decision_history"] = [
        {
            "decision_id": "legacy_1",
            "recommendation_summary": "Option B was selected by the old system.",
            "created_at": "2025-01-01T00:00:00",
        }
    ]
    project = project_workspace.save_project(project)

    assert "Option B" not in project["workspace_state"]["current_assessment"]
    assert "suppressed" in project["workspace_state"]["current_assessment"]


def test_confidence_metadata_remains_additive() -> None:
    item = normalize_evidence_item(
        {
            "title": "Conflicting report",
            "source_type": "Reputable news",
            "source_name": "Reuters",
            "source_url": "https://www.reuters.com/",
            "published_at": "2026-06-30",
            "excerpt": "Report contains potentially conflicting context.",
            "conflict_status": "Potential Conflict",
            "status": "Accepted",
        },
        query="conflicting context",
        retrieved_at="2026-06-30T10:00:00",
    )

    metadata = confidence_impact_metadata([item])

    assert item.evidence_id in metadata["confidence_reducers"]
    assert "confidence_level" not in metadata
