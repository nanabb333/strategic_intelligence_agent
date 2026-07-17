"""Deprecated compatibility boundary for qualitative legacy confidence."""

from __future__ import annotations

import warnings
from typing import Any

from evidence_sufficiency import normalize_stored_evidence_sufficiency


MIGRATION_MESSAGE = (
    "confidence_layer is deprecated. Use evidence_sufficiency; legacy confidence is not "
    "a probability, calibration result, or current assessment tier."
)

warnings.warn(MIGRATION_MESSAGE, DeprecationWarning, stacklevel=2)


class DeprecatedConfidenceContractError(RuntimeError):
    """Raised when superseded confidence generation is requested."""


class ConfidenceAssessment:
    """Import-compatible sentinel that cannot create a legacy confidence claim."""

    def __init__(self, *_: Any, **__: Any) -> None:
        raise DeprecatedConfidenceContractError(MIGRATION_MESSAGE)


def assess_confidence(*_: Any, **__: Any) -> Any:
    """Reject the retired confidence generator."""
    raise DeprecatedConfidenceContractError(MIGRATION_MESSAGE)


def render_evidence_confidence_section(*_: Any, **__: Any) -> str:
    """Reject the retired confidence renderer."""
    raise DeprecatedConfidenceContractError(MIGRATION_MESSAGE)


def normalize_legacy_confidence(payload: dict[str, Any]) -> dict[str, Any]:
    """Parse a legacy confidence shape into a bounded read-only view."""
    analysis = payload if "confidence_assessment" in payload else {"confidence_assessment": payload}
    return normalize_stored_evidence_sufficiency(analysis)
