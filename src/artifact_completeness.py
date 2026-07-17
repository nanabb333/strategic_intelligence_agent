"""Deterministic completeness checks for generated assessment artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean

from decision_assessment import NeutralDecisionAssessment
from evidence_ledger import EvidenceLedger
from evidence_sufficiency import EvidenceSufficiencyAssessment


@dataclass(frozen=True)
class CompletenessDimension:
    name: str
    complete: bool
    explanation: str


@dataclass(frozen=True)
class ArtifactCompletenessCheck:
    status: str
    completion_rate: float
    passed_checks: int
    total_checks: int
    dimensions: list[CompletenessDimension]
    missing_elements: list[str] = field(default_factory=list)
    interpretation_boundary: str = (
        "Completeness checks field presence and review structure only. It does not validate factual accuracy, "
        "pathway correctness, evidence validity, decision quality, or real-world usefulness."
    )


def check_artifact_completeness(
    *,
    assessment: NeutralDecisionAssessment,
    evidence_ledger: EvidenceLedger,
    evidence_sufficiency: EvidenceSufficiencyAssessment,
) -> ArtifactCompletenessCheck:
    """Check current neutral assessment contract fields without judging quality."""
    dimensions = [
        _dimension("decision_question", bool(assessment.decision_question), "A decision question is present."),
        _dimension("assessment_summary", bool(assessment.assessment_summary), "An assessment summary is present."),
        _dimension(
            "neutral_pathways",
            len(assessment.pathways_for_review) >= 2,
            "At least two neutral pathways are available for reviewer comparison.",
        ),
        _dimension(
            "pathway_review_fields",
            bool(assessment.pathways_for_review)
            and all(pathway.description and pathway.pathway_tradeoffs for pathway in assessment.pathways_for_review),
            "Each pathway contains a description and trade-offs.",
        ),
        _dimension("evidence_ledger", bool(evidence_ledger.items), "At least one inspectable ledger item is present."),
        _dimension(
            "change_triggers",
            bool(assessment.change_triggers),
            "Change triggers are available for reassessment.",
        ),
        _dimension(
            "limitations",
            bool(assessment.limitations or evidence_sufficiency.limitations),
            "Limitations remain visible.",
        ),
        _dimension(
            "reviewer_boundary",
            assessment.judgment_boundary.owner == "reviewer" and not assessment.reviewer_selected_path,
            "Final judgment is reserved for the reviewer and no pathway is auto-selected.",
        ),
    ]
    rate = round(mean(1.0 if item.complete else 0.0 for item in dimensions), 3)
    status = "Complete" if rate == 1.0 else "Incomplete"
    return ArtifactCompletenessCheck(
        status=status,
        completion_rate=rate,
        passed_checks=sum(1 for item in dimensions if item.complete),
        total_checks=len(dimensions),
        dimensions=dimensions,
        missing_elements=[item.name for item in dimensions if not item.complete],
    )


def render_artifact_completeness(check: ArtifactCompletenessCheck) -> str:
    """Render completeness results with their non-evaluative boundary."""
    lines = [
        "## Artifact Completeness Check",
        "",
        f"**Status:** {check.status}",
        f"**Structural checks:** {check.passed_checks} of {check.total_checks} passed",
        "",
        check.interpretation_boundary,
        "",
    ]
    lines.extend(["### Passed Structural Checks", ""])
    for dimension in (item for item in check.dimensions if item.complete):
        lines.append(f"- **{dimension.name}.** {dimension.explanation}")
    lines.extend(["", "### Missing Structural Checks", ""])
    missing = [item for item in check.dimensions if not item.complete]
    if not missing:
        lines.append("- None.")
    for dimension in missing:
        lines.append(f"- **{dimension.name}.** {dimension.explanation}")
    lines.extend(["", "### Check Details", ""])
    for dimension in check.dimensions:
        marker = "Present" if dimension.complete else "Missing"
        lines.append(f"- **{dimension.name}: {marker}.** {dimension.explanation}")
    return "\n".join(lines).strip() + "\n"


def _dimension(name: str, complete: bool, explanation: str) -> CompletenessDimension:
    return CompletenessDimension(name=name, complete=complete, explanation=explanation)
