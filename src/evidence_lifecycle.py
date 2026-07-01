"""Deterministic evidence lifecycle helpers for reviewer-controlled workflows."""

from __future__ import annotations

from datetime import datetime
from typing import Any


RETRIEVED = "retrieved"
VALIDATED = "validated"
RANKED = "ranked"
NEEDS_REVIEW = "needs_review"
ACCEPTED = "accepted"
REJECTED = "rejected"
REFERENCED = "referenced"
ARCHIVED = "archived"

EVIDENCE_LIFECYCLE_STATES = {
    RETRIEVED,
    VALIDATED,
    RANKED,
    NEEDS_REVIEW,
    ACCEPTED,
    REJECTED,
    REFERENCED,
    ARCHIVED,
}

REVIEWER_ACTIONS = {
    "accept",
    "reject",
    "mark_needs_review",
    "archive",
    "reference_in_decision",
}

ACTION_TO_STATE = {
    "accept": ACCEPTED,
    "reject": REJECTED,
    "mark_needs_review": NEEDS_REVIEW,
    "archive": ARCHIVED,
    "reference_in_decision": REFERENCED,
}


def now_iso() -> str:
    """Return local ISO timestamp for local JSON workflow metadata."""
    return datetime.now().isoformat(timespec="seconds")


def default_evidence_lifecycle_state(evidence: dict[str, Any] | None = None) -> str:
    """Return migration-safe lifecycle state for old and new evidence records."""
    if evidence:
        state = str(evidence.get("lifecycle_state") or "").strip().lower()
        if state in EVIDENCE_LIFECYCLE_STATES:
            return state
        status = str(evidence.get("status") or "").strip().lower()
        if status in {"accepted", "verified", "corroborated"}:
            return ACCEPTED
        if status in {"used", "referenced"}:
            return REFERENCED
        if status in {"outdated", "unavailable", "archived"}:
            return ARCHIVED
        if status in {"conflicting", "single source"}:
            return NEEDS_REVIEW
        validation_status = str(evidence.get("validation_status") or "").strip().lower()
        if validation_status == "valid":
            return VALIDATED
        if validation_status:
            return NEEDS_REVIEW
    return RETRIEVED


def apply_reviewer_action(
    evidence: dict[str, Any],
    *,
    action: str,
    reviewer_note: str = "",
    review_reason: str = "",
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Apply a reviewer-controlled lifecycle action to an evidence record."""
    if action not in REVIEWER_ACTIONS:
        raise ValueError(f"Unsupported reviewer action: {action}")
    reviewed_at = timestamp or now_iso()
    state = ACTION_TO_STATE[action]
    evidence["lifecycle_state"] = state
    evidence["reviewer_status"] = state
    evidence["evidence_action"] = action
    evidence["reviewed_at"] = reviewed_at
    if reviewer_note:
        evidence["reviewer_note"] = reviewer_note
    if review_reason:
        evidence["review_reason"] = review_reason
    evidence["status"] = _status_for_state(state, evidence.get("status"))
    return evidence


def lifecycle_metadata(
    evidence: dict[str, Any],
    *,
    default_state: str | None = None,
) -> dict[str, Any]:
    """Return additive lifecycle and reviewer metadata for storage."""
    state = default_state or default_evidence_lifecycle_state(evidence)
    return {
        "lifecycle_state": state,
        "reviewer_status": str(evidence.get("reviewer_status") or state).strip(),
        "reviewer_note": str(evidence.get("reviewer_note") or "").strip(),
        "reviewed_at": str(evidence.get("reviewed_at") or "").strip(),
        "review_reason": str(evidence.get("review_reason") or "").strip(),
        "evidence_action": str(evidence.get("evidence_action") or "").strip(),
    }


def _status_for_state(state: str, current: Any) -> str:
    if state == ACCEPTED:
        return "Accepted"
    if state == REJECTED:
        return "Rejected"
    if state == REFERENCED:
        return "Used"
    if state == ARCHIVED:
        return "Archived"
    if state == NEEDS_REVIEW:
        return "Pending Review"
    return str(current or "Retrieved")
