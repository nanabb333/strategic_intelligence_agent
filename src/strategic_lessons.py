"""Generate rule-based strategic lessons from historical outcomes."""

from __future__ import annotations

from dataclasses import dataclass, field

from outcome_retriever import HistoricalOutcome


@dataclass
class StrategicLesson:
    """Recurring lesson inferred from retrieved historical outcomes."""

    lesson: str
    supporting_cases: list[str] = field(default_factory=list)
    confidence: str = "Low"
    rationale: str = ""
    evidence_references: list[str] = field(default_factory=list)


LESSON_RULES = [
    (
        "Supply chain diversification frequently appears after export-control or disruption shocks.",
        ["export", "supply", "supplier", "route", "inventory", "qualification", "chokepoint"],
    ),
    (
        "Compliance and screening routines often expand after sanctions, export controls, or regulatory changes.",
        ["compliance", "screening", "license", "documentation", "restricted", "legal"],
    ),
    (
        "Industrial policy episodes often require monitoring eligibility, domestic content, and implementation details.",
        ["incentive", "eligibility", "domestic", "subsidy", "tax credit", "site selection"],
    ),
    (
        "Geopolitical escalation cases often lead organizations to review continuity plans and exposure concentration.",
        ["security", "conflict", "escalation", "continuity", "alternative sourcing", "geography"],
    ),
    (
        "Periods of uncertainty often increase the value of executive communication and monitoring routines.",
        ["uncertainty", "visibility", "monitoring", "communication", "guidance"],
    ),
]


def generate_strategic_lessons(
    historical_outcomes: dict[str, list[HistoricalOutcome]],
) -> dict[str, list[StrategicLesson]]:
    """Generate explainable lessons from retrieved historical outcomes."""
    results: dict[str, list[StrategicLesson]] = {}
    for issue_title, outcomes in historical_outcomes.items():
        lessons: list[StrategicLesson] = []
        for lesson_text, keywords in LESSON_RULES:
            supporting = []
            evidence = []
            for outcome in outcomes:
                searchable = " ".join(
                    [
                        outcome.event_family,
                        outcome.observed_outcome,
                        outcome.strategic_response,
                        outcome.sector,
                    ]
                ).lower()
                if any(keyword in searchable for keyword in keywords):
                    supporting.append(f"{outcome.case_name} ({outcome.year})")
                    evidence.extend(outcome.evidence_references)
            if supporting:
                lessons.append(
                    StrategicLesson(
                        lesson=lesson_text,
                        supporting_cases=supporting,
                        confidence=_confidence_label(len(supporting)),
                        rationale=f"Matched {len(supporting)} retrieved outcome case(s) with rule keywords: {', '.join(keywords[:4])}.",
                        evidence_references=sorted(set(evidence)),
                    )
                )
        results[issue_title] = lessons[:4]
    return results


def _confidence_label(case_count: int) -> str:
    if case_count >= 3:
        return "High"
    if case_count == 2:
        return "Medium"
    return "Low"
