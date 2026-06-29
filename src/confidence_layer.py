"""Qualitative confidence and assumption layer."""

from __future__ import annotations

from dataclasses import dataclass, field

from decision_case import DecisionCase
from evidence_ledger import EvidenceLedger


@dataclass
class ConfidenceAssessment:
    """Qualitative confidence record for one decision case."""

    confidence_level: str = "Low"
    key_assumptions: list[str] = field(default_factory=list)
    what_would_change_this_view: list[str] = field(default_factory=list)
    unknown_or_uncertain: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    rationale: str = ""


def assess_confidence(decision_case: DecisionCase, evidence_ledger: EvidenceLedger) -> ConfidenceAssessment:
    """Assess qualitative confidence without statistical claims."""
    evidence_count = len(evidence_ledger.items)
    high_confidence_items = sum(1 for item in evidence_ledger.items if item.confidence == "High")
    low_confidence_items = sum(1 for item in evidence_ledger.items if item.confidence == "Low")
    has_limitations = bool(decision_case.limitations)
    has_analogues = bool(decision_case.historical_analogues)

    if evidence_count >= 5 and high_confidence_items >= 2 and low_confidence_items == 0 and not has_limitations:
        level = "High"
    elif evidence_count >= 3 and has_analogues:
        level = "Moderate"
    else:
        level = "Low"

    if has_limitations and level == "High":
        level = "Moderate"

    unknowns = _unknowns(decision_case, evidence_ledger)
    limitations = decision_case.limitations or ["Evidence limits were not fully specified by the current pipeline."]
    rationale = _rationale(level, evidence_count, has_analogues, has_limitations)

    decision_case.confidence_level = level
    return ConfidenceAssessment(
        confidence_level=level,
        key_assumptions=decision_case.assumptions,
        what_would_change_this_view=decision_case.change_triggers,
        unknown_or_uncertain=unknowns,
        limitations=limitations,
        rationale=rationale,
    )


def render_evidence_confidence_section(
    *,
    evidence_ledger: EvidenceLedger,
    confidence_assessment: ConfidenceAssessment,
) -> str:
    """Render a concise Markdown evidence and confidence section."""
    lines = [
        "## Evidence and Confidence",
        "",
        f"**Confidence level:** {confidence_assessment.confidence_level}",
        "",
        f"**Confidence rationale:** {confidence_assessment.rationale}",
        "",
        "### Evidence Ledger",
        "",
    ]
    for item in evidence_ledger.items:
        lines.extend(
            [
                f"- **{item.evidence_id} ({item.source_type})**",
                f"  - Observation: {item.observation}",
                f"  - Inference: {item.inference}",
                f"  - Supports: {item.claim_supported}",
                f"  - Relevance: {item.relevance}; Confidence: {item.confidence}",
                f"  - Limitations: {item.limitations}",
            ]
        )

    lines.extend(["", "### Key Assumptions", ""])
    lines.extend(_bullets(confidence_assessment.key_assumptions, "No key assumptions were generated."))
    lines.extend(["", "### What Would Change This View", ""])
    lines.extend(_bullets(confidence_assessment.what_would_change_this_view, "No change triggers were generated."))
    lines.extend(["", "### What Is Unknown Or Uncertain", ""])
    lines.extend(_bullets(confidence_assessment.unknown_or_uncertain, "No uncertainty notes were generated."))
    lines.extend(["", "### Evidence Limitations", ""])
    lines.extend(_bullets(confidence_assessment.limitations, "No evidence limitations were generated."))
    return "\n".join(lines).strip() + "\n"


def _unknowns(decision_case: DecisionCase, evidence_ledger: EvidenceLedger) -> list[str]:
    unknowns = [
        "The current brief does not verify information outside the supplied input and local records.",
        "Organization-specific exposure, timing, and implementation constraints require human review.",
    ]
    if not decision_case.stakeholders or decision_case.stakeholders[0].startswith("Affected decision-makers"):
        unknowns.append("Stakeholders are not fully specified in the extracted material.")
    if any(item.confidence == "Low" for item in evidence_ledger.items):
        unknowns.append("At least one evidence item has low confidence and should be reviewed before use.")
    return unknowns


def _rationale(level: str, evidence_count: int, has_analogues: bool, has_limitations: bool) -> str:
    pieces = [f"{evidence_count} reviewable evidence items were recorded"]
    pieces.append("historical analogues are available" if has_analogues else "historical analogue support is limited")
    if has_limitations:
        pieces.append("limitations remain visible")
    return f"{level} confidence because " + ", ".join(pieces) + "."


def _bullets(items: list[str], fallback: str) -> list[str]:
    return [f"- {item}" for item in items] if items else [f"- {fallback}"]
