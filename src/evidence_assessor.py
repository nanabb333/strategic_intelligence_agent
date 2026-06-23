"""Assess evidence support for multi-lens interpretations."""

from dataclasses import dataclass, field

from multi_lens_analyzer import LensInterpretation


@dataclass
class EvidenceAssessment:
    """Evidence support assessment without probability language."""

    issue_title: str
    lens: str
    supporting_evidence: list[str] = field(default_factory=list)
    weakening_evidence: list[str] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    confidence_language: str = "Limited"


def assess_evidence(
    interpretations: dict[str, list[LensInterpretation]],
) -> dict[str, list[EvidenceAssessment]]:
    """Evaluate support for each interpretation using qualitative confidence language."""
    results: dict[str, list[EvidenceAssessment]] = {}
    for issue_title, issue_interpretations in interpretations.items():
        assessments: list[EvidenceAssessment] = []
        for interpretation in issue_interpretations:
            evidence_count = len(set(interpretation.evidence_references))
            confidence = "Substantial" if evidence_count >= 5 else "Moderate" if evidence_count >= 3 else "Limited"
            assessments.append(
                EvidenceAssessment(
                    issue_title=issue_title,
                    lens=interpretation.lens,
                    supporting_evidence=interpretation.supporting_observations,
                    weakening_evidence=interpretation.limitations,
                    missing_evidence=[
                        "Primary-source confirmation of implementation details.",
                        "Stakeholder-specific exposure data.",
                        "Updated source material that confirms whether conditions have changed.",
                    ],
                    confidence_language=confidence,
                )
            )
        results[issue_title] = assessments
    return results

