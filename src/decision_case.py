"""Deprecated compatibility boundary for the superseded DecisionCase contract."""

from __future__ import annotations

import warnings
from typing import Any

from decision_assessment import normalize_stored_decision_assessment


MIGRATION_MESSAGE = (
    "decision_case is deprecated. Use decision_assessment.NeutralDecisionAssessment; "
    "the superseded module no longer generates recommendations or preferred paths."
)

warnings.warn(MIGRATION_MESSAGE, DeprecationWarning, stacklevel=2)


class DeprecatedDecisionContractError(RuntimeError):
    """Raised when superseded recommendation-producing behavior is requested."""


class DecisionCase:
    """Import-compatible sentinel that cannot construct the superseded contract."""

    def __init__(self, *_: Any, **__: Any) -> None:
        raise DeprecatedDecisionContractError(MIGRATION_MESSAGE)


def build_decision_case(*_: Any, **__: Any) -> Any:
    """Reject the retired builder rather than recreating a preferred path."""
    raise DeprecatedDecisionContractError(MIGRATION_MESSAGE)


def normalize_legacy_decision_case(payload: dict[str, Any]) -> dict[str, Any]:
    """Parse a legacy shape into the current neutral read-only view."""
    analysis = payload if "decision_case" in payload else {"decision_case": payload}
    return normalize_stored_decision_assessment(analysis)
