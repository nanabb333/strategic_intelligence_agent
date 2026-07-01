"""Reviewer-controlled decision review state for pathway comparison workflows."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

from decision_support_utils import latest_or_first_project_question

ALLOWED_REVIEW_STATUSES = {
    "not_reviewed",
    "reviewed",
    "accepted_for_consideration",
    "questioned",
    "needs_more_evidence",
    "needs_legal_or_compliance_review",
    "unresolved",
}
TARGET_TYPES = {
    "pathway",
    "comparison_cell",
    "assumption",
    "unknown",
    "decision_trigger",
}


@dataclass(frozen=True)
class ReviewerNote:
    """Auditable reviewer note without approval or recommendation semantics."""

    note_id: str
    target_type: str
    target_id: str
    note: str
    created_at: str
    reviewed_by: str = ""


@dataclass(frozen=True)
class UnresolvedDecisionQuestion:
    """Reviewer-authored unresolved decision question."""

    question_id: str
    question: str
    target_type: str
    target_id: str
    created_at: str
    reviewed_by: str = ""
    related_evidence_refs: list[dict[str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class PathwayReviewState:
    """Review state for a pathway draft."""

    pathway_id: str
    review_status: str = "not_reviewed"
    reviewer_note: str = ""
    created_at: str = ""
    updated_at: str = ""
    reviewed_by: str = ""
    related_evidence_refs: list[dict[str, str]] = field(default_factory=list)
    related_risk_categories: list[str] = field(default_factory=list)
    related_constraints: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ComparisonCellReviewState:
    """Review state for one pathway comparison matrix cell."""

    pathway_id: str
    comparison_dimension: str
    review_status: str = "not_reviewed"
    reviewer_note: str = ""
    created_at: str = ""
    updated_at: str = ""
    reviewed_by: str = ""
    related_evidence_refs: list[dict[str, str]] = field(default_factory=list)
    related_risk_categories: list[str] = field(default_factory=list)
    related_constraints: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AssumptionReviewState:
    """Review state for an assumption."""

    assumption_id: str
    review_status: str = "not_reviewed"
    reviewer_note: str = ""
    created_at: str = ""
    updated_at: str = ""
    reviewed_by: str = ""
    related_evidence_refs: list[dict[str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class UnknownReviewState:
    """Review state for an unknown or open evidence gap."""

    unknown_id: str
    review_status: str = "not_reviewed"
    reviewer_note: str = ""
    created_at: str = ""
    updated_at: str = ""
    reviewed_by: str = ""
    related_evidence_refs: list[dict[str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class DecisionTriggerReviewState:
    """Review state for a decision trigger."""

    trigger_id: str
    review_status: str = "not_reviewed"
    reviewer_note: str = ""
    created_at: str = ""
    updated_at: str = ""
    reviewed_by: str = ""
    related_evidence_refs: list[dict[str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class DecisionReviewSummary:
    """Deterministic project-level review summary."""

    reviewed_pathways_count: int
    unresolved_issues_count: int
    needs_more_evidence_count: int
    needs_legal_or_compliance_review_count: int
    unresolved_decision_questions_count: int
    latest_reviewer_note_timestamp: str = ""


@dataclass(frozen=True)
class DecisionReviewState:
    """Project-scoped reviewer decision review state."""

    project_id: str
    decision_question: str = ""
    pathway_reviews: list[PathwayReviewState] = field(default_factory=list)
    comparison_cell_reviews: list[ComparisonCellReviewState] = field(default_factory=list)
    assumption_reviews: list[AssumptionReviewState] = field(default_factory=list)
    unknown_reviews: list[UnknownReviewState] = field(default_factory=list)
    trigger_reviews: list[DecisionTriggerReviewState] = field(default_factory=list)
    reviewer_notes: list[ReviewerNote] = field(default_factory=list)
    unresolved_questions: list[UnresolvedDecisionQuestion] = field(default_factory=list)
    review_summary: DecisionReviewSummary | None = None
    created_at: str = ""
    updated_at: str = ""


def default_decision_review_state(project: dict[str, Any]) -> dict[str, Any]:
    """Return backward-compatible default review state without mutating the project."""
    now = _now()
    stored = project.get("decision_review_state")
    if isinstance(stored, dict):
        return _with_summary(_normalize_state(project, stored))
    return asdict(
        DecisionReviewState(
            project_id=str(project.get("project_id") or ""),
            decision_question=_project_question(project),
            created_at=now,
            updated_at=now,
            review_summary=DecisionReviewSummary(0, 0, 0, 0, 0),
        )
    )


def update_decision_review_state(project: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    """Apply a reviewer-controlled review update to project-level review state."""
    state = default_decision_review_state(project)
    now = _now()
    target_type = str(payload.get("target_type") or "pathway").strip()
    if target_type not in TARGET_TYPES:
        raise ValueError("Unsupported review target type.")
    status = _status(payload.get("review_status") or "reviewed")
    target_id = str(payload.get("target_id") or payload.get("pathway_id") or "").strip()
    if not target_id:
        raise ValueError("target_id is required.")
    reviewed_by = str(payload.get("reviewed_by") or "").strip()
    note = str(payload.get("reviewer_note") or "").strip()
    evidence_refs = _list_of_dicts(payload.get("related_evidence_refs"))
    risks = _list_of_strings(payload.get("related_risk_categories"))
    constraints = _list_of_strings(payload.get("related_constraints"))

    if target_type == "pathway":
        _upsert_pathway_review(state, target_id, status, note, now, reviewed_by, evidence_refs, risks, constraints)
    elif target_type == "comparison_cell":
        dimension = str(payload.get("comparison_dimension") or "").strip()
        if not dimension:
            raise ValueError("comparison_dimension is required for comparison cell reviews.")
        _upsert_comparison_review(state, target_id, dimension, status, note, now, reviewed_by, evidence_refs, risks, constraints)
    elif target_type == "assumption":
        _upsert_simple_review(state, "assumption_reviews", "assumption_id", target_id, status, note, now, reviewed_by, evidence_refs)
    elif target_type == "unknown":
        _upsert_simple_review(state, "unknown_reviews", "unknown_id", target_id, status, note, now, reviewed_by, evidence_refs)
    elif target_type == "decision_trigger":
        _upsert_simple_review(state, "trigger_reviews", "trigger_id", target_id, status, note, now, reviewed_by, evidence_refs)

    if note:
        state.setdefault("reviewer_notes", []).append(
            asdict(ReviewerNote(str(uuid4())[:8], target_type, target_id, note, now, reviewed_by))
        )
    question = str(payload.get("unresolved_question") or "").strip()
    if question:
        state.setdefault("unresolved_questions", []).append(
            asdict(
                UnresolvedDecisionQuestion(
                    question_id=str(uuid4())[:8],
                    question=question,
                    target_type=target_type,
                    target_id=target_id,
                    created_at=now,
                    reviewed_by=reviewed_by,
                    related_evidence_refs=evidence_refs,
                )
            )
        )

    state["decision_question"] = _project_question(project)
    state["updated_at"] = now
    return _with_summary(state)


def _normalize_state(project: dict[str, Any], stored: dict[str, Any]) -> dict[str, Any]:
    return {
        "project_id": str(stored.get("project_id") or project.get("project_id") or ""),
        "decision_question": str(stored.get("decision_question") or _project_question(project)),
        "pathway_reviews": list(stored.get("pathway_reviews") or []),
        "comparison_cell_reviews": list(stored.get("comparison_cell_reviews") or []),
        "assumption_reviews": list(stored.get("assumption_reviews") or []),
        "unknown_reviews": list(stored.get("unknown_reviews") or []),
        "trigger_reviews": list(stored.get("trigger_reviews") or []),
        "reviewer_notes": list(stored.get("reviewer_notes") or []),
        "unresolved_questions": list(stored.get("unresolved_questions") or []),
        "created_at": str(stored.get("created_at") or _now()),
        "updated_at": str(stored.get("updated_at") or ""),
    }


def _with_summary(state: dict[str, Any]) -> dict[str, Any]:
    reviews = [
        *state.get("pathway_reviews", []),
        *state.get("comparison_cell_reviews", []),
        *state.get("assumption_reviews", []),
        *state.get("unknown_reviews", []),
        *state.get("trigger_reviews", []),
    ]
    unresolved_statuses = {"questioned", "needs_more_evidence", "needs_legal_or_compliance_review", "unresolved"}
    notes = state.get("reviewer_notes", [])
    latest_note = max((str(note.get("created_at") or "") for note in notes), default="")
    state["review_summary"] = asdict(
        DecisionReviewSummary(
            reviewed_pathways_count=sum(1 for item in state.get("pathway_reviews", []) if item.get("review_status") == "reviewed"),
            unresolved_issues_count=sum(1 for item in reviews if item.get("review_status") in unresolved_statuses),
            needs_more_evidence_count=sum(1 for item in reviews if item.get("review_status") == "needs_more_evidence"),
            needs_legal_or_compliance_review_count=sum(1 for item in reviews if item.get("review_status") == "needs_legal_or_compliance_review"),
            unresolved_decision_questions_count=len(state.get("unresolved_questions", [])),
            latest_reviewer_note_timestamp=latest_note,
        )
    )
    return state


def _upsert_pathway_review(
    state: dict[str, Any],
    pathway_id: str,
    status: str,
    note: str,
    now: str,
    reviewed_by: str,
    evidence_refs: list[dict[str, str]],
    risks: list[str],
    constraints: list[str],
) -> None:
    reviews = state.setdefault("pathway_reviews", [])
    existing = next((item for item in reviews if item.get("pathway_id") == pathway_id), None)
    payload = asdict(
        PathwayReviewState(
            pathway_id=pathway_id,
            review_status=status,
            reviewer_note=note,
            created_at=str(existing.get("created_at") if existing else now),
            updated_at=now,
            reviewed_by=reviewed_by,
            related_evidence_refs=evidence_refs,
            related_risk_categories=risks,
            related_constraints=constraints,
        )
    )
    if existing:
        existing.update(payload)
    else:
        reviews.append(payload)


def _upsert_comparison_review(
    state: dict[str, Any],
    pathway_id: str,
    dimension: str,
    status: str,
    note: str,
    now: str,
    reviewed_by: str,
    evidence_refs: list[dict[str, str]],
    risks: list[str],
    constraints: list[str],
) -> None:
    reviews = state.setdefault("comparison_cell_reviews", [])
    existing = next(
        (
            item
            for item in reviews
            if item.get("pathway_id") == pathway_id and item.get("comparison_dimension") == dimension
        ),
        None,
    )
    payload = asdict(
        ComparisonCellReviewState(
            pathway_id=pathway_id,
            comparison_dimension=dimension,
            review_status=status,
            reviewer_note=note,
            created_at=str(existing.get("created_at") if existing else now),
            updated_at=now,
            reviewed_by=reviewed_by,
            related_evidence_refs=evidence_refs,
            related_risk_categories=risks,
            related_constraints=constraints,
        )
    )
    if existing:
        existing.update(payload)
    else:
        reviews.append(payload)


def _upsert_simple_review(
    state: dict[str, Any],
    collection: str,
    id_key: str,
    target_id: str,
    status: str,
    note: str,
    now: str,
    reviewed_by: str,
    evidence_refs: list[dict[str, str]],
) -> None:
    reviews = state.setdefault(collection, [])
    existing = next((item for item in reviews if item.get(id_key) == target_id), None)
    payload = {
        id_key: target_id,
        "review_status": status,
        "reviewer_note": note,
        "created_at": str(existing.get("created_at") if existing else now),
        "updated_at": now,
        "reviewed_by": reviewed_by,
        "related_evidence_refs": evidence_refs,
    }
    if existing:
        existing.update(payload)
    else:
        reviews.append(payload)


def _status(value: Any) -> str:
    status = str(value or "").strip()
    if status not in ALLOWED_REVIEW_STATUSES:
        raise ValueError("Unsupported review status.")
    return status


def _project_question(project: dict[str, Any]) -> str:
    return str(latest_or_first_project_question(project).get("question") or "")


def _list_of_dicts(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _list_of_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item).strip()]


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")
