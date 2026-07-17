"""Neutral compatibility brief for callers that still use the legacy tool name.

The current analysis pipeline renders ``NeutralDecisionAssessment`` directly.
This module retains only the public ``generate_brief`` signature required by the
tool registry; it does not rank pathways or select a recommendation.
"""

from __future__ import annotations

from typing import Any


def _value(item: Any, name: str, default: Any = "") -> Any:
    if isinstance(item, dict):
        return item.get(name, default)
    return getattr(item, name, default)


def _first_text(items: list[Any], name: str, fallback: str) -> str:
    for item in items:
        value = str(_value(item, name, "")).strip()
        if value:
            return value
    return fallback


def _items(value: Any) -> list[Any]:
    if isinstance(value, dict):
        return list(value.values())
    if isinstance(value, (list, tuple)):
        return list(value)
    return []


def generate_brief(
    issues: list[Any],
    classifications: list[Any],
    analogues: list[Any],
    contexts: list[Any],
    analyses: list[Any],
    **_: Any,
) -> str:
    """Return a deterministic, non-ranking summary for legacy callers.

    The function deliberately accepts extra keyword arguments so older tool
    invocations continue to run, but none can set a preferred pathway.
    """

    decision_question = _first_text(
        issues,
        "issue_statement",
        "What decision should the reviewer examine using the available evidence?",
    )
    scenario = _first_text(classifications, "scenario_type", "Not classified")
    context = _first_text(
        contexts,
        "strategic_significance",
        "No additional current-context statement was produced.",
    )
    implication = _first_text(
        analyses,
        "implication",
        "No strategic implication was produced.",
    )

    analogue_lines = []
    for analogue in _items(analogues)[:3]:
        name = str(_value(analogue, "event_name", "")).strip()
        if not name:
            name = str(_value(analogue, "analogue_name", "")).strip()
        if name:
            analogue_lines.append(f"- {name}")
    if not analogue_lines:
        analogue_lines.append("- No historical analogue was retrieved.")

    return "\n".join(
        [
            "# Neutral Decision Assessment",
            "",
            "## Decision Question",
            decision_question,
            "",
            "## Assessment Context",
            f"- Scenario classification: {scenario}",
            f"- Current context: {context}",
            f"- Strategic consideration: {implication}",
            "",
            "## Historical Analogues for Review",
            *analogue_lines,
            "",
            "## Selection Status",
            "No pathway selected. Pathway choice and rationale remain reviewer inputs.",
            "",
            "## Boundary",
            "This deterministic artifact organizes evidence and comparisons. It does not forecast outcomes, estimate probabilities, or recommend a pathway. Final judgment remains with the reviewer.",
        ]
    )
