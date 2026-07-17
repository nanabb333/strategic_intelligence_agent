"""Deprecated boundary for the superseded automated Decision Quality evaluator."""

from __future__ import annotations

import warnings
from typing import Any


MIGRATION_MESSAGE = (
    "decision_quality_evaluator is deprecated. Use artifact_completeness for structural "
    "checks; automated Decision Quality scores are no longer produced."
)

warnings.warn(MIGRATION_MESSAGE, DeprecationWarning, stacklevel=2)


class DeprecatedDecisionQualityContractError(RuntimeError):
    """Raised when the superseded quality evaluator is requested."""


class DecisionQualityEvaluation:
    """Import-compatible sentinel that cannot create a quality score."""

    def __init__(self, *_: Any, **__: Any) -> None:
        raise DeprecatedDecisionQualityContractError(MIGRATION_MESSAGE)


def evaluate_decision_quality(*_: Any, **__: Any) -> Any:
    """Reject the retired evaluator rather than restoring a score."""
    raise DeprecatedDecisionQualityContractError(MIGRATION_MESSAGE)


def render_decision_quality_review(*_: Any, **__: Any) -> str:
    """Reject the retired score renderer."""
    raise DeprecatedDecisionQualityContractError(MIGRATION_MESSAGE)


def normalize_legacy_decision_quality(_: dict[str, Any]) -> dict[str, Any]:
    """Return an explicit marker without carrying forward legacy scores."""
    return {
        "legacy_compatibility": {"read_only": True, "contract_status": "superseded"},
        "statement": "Legacy Decision Quality scores are not part of the current assessment contract.",
    }
