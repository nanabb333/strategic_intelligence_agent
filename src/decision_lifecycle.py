"""Lightweight deterministic decision lifecycle helpers."""

from __future__ import annotations

from datetime import datetime
from typing import Any


DRAFT = "draft"
EVIDENCE_REVIEW = "evidence_review"
REVIEWED = "reviewed"
FINALIZED = "finalized"
SUPERSEDED = "superseded"
ARCHIVED = "archived"

DECISION_LIFECYCLE_STATES = {
    DRAFT,
    EVIDENCE_REVIEW,
    REVIEWED,
    FINALIZED,
    SUPERSEDED,
    ARCHIVED,
}

SAFE_TRANSITIONS = {
    DRAFT: {EVIDENCE_REVIEW, REVIEWED, ARCHIVED},
    EVIDENCE_REVIEW: {REVIEWED, ARCHIVED},
    REVIEWED: {FINALIZED, SUPERSEDED, ARCHIVED},
    FINALIZED: {SUPERSEDED, ARCHIVED},
    SUPERSEDED: {ARCHIVED},
    ARCHIVED: set(),
}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def default_decision_state(record: dict[str, Any] | None = None) -> str:
    """Return migration-safe decision state for old and new records."""
    if record:
        state = str(record.get("decision_status") or record.get("decision_lifecycle_state") or "").strip().lower()
        if state in DECISION_LIFECYCLE_STATES:
            return state
        if record.get("run_id"):
            return REVIEWED
    return DRAFT


def transition_decision_state(
    current_state: str,
    next_state: str,
) -> str:
    """Validate a lightweight governance transition."""
    current = current_state if current_state in DECISION_LIFECYCLE_STATES else DRAFT
    if next_state not in DECISION_LIFECYCLE_STATES:
        raise ValueError(f"Unsupported decision state: {next_state}")
    if next_state == current:
        return current
    if next_state not in SAFE_TRANSITIONS[current]:
        raise ValueError(f"Unsafe decision transition: {current} -> {next_state}")
    return next_state


def decision_governance_metadata(
    record: dict[str, Any],
    *,
    evidence_count: int = 0,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Return additive decision governance metadata."""
    state = default_decision_state(record)
    return {
        "decision_status": state,
        "review_status": record.get("review_status") or state,
        "last_reviewed_at": record.get("last_reviewed_at") or (timestamp or now_iso() if state == REVIEWED else ""),
        "supporting_evidence_count": evidence_count,
        "confidence_history": record.get("confidence_history") or [],
        "version_history": record.get("version_history") or [],
    }
