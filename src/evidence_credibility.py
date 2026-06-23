"""Assess credibility metadata for historical outcomes and strategic lessons."""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import Counter

from outcome_retriever import HistoricalOutcome
from strategic_lessons import StrategicLesson


@dataclass
class EvidenceCredibility:
    """Credibility summary for reviewer-facing evidence transparency."""

    evidence_summary: str
    confidence_distribution: dict[str, int] = field(default_factory=dict)
    source_status_distribution: dict[str, int] = field(default_factory=dict)
    key_limitations: list[str] = field(default_factory=list)
    reviewer_note: str = ""


def assess_evidence_credibility(
    historical_outcomes: dict[str, list[HistoricalOutcome]],
    strategic_lessons: dict[str, list[StrategicLesson]],
) -> dict[str, EvidenceCredibility]:
    """Evaluate retrieved outcomes and lessons for transparent credibility notes."""
    results: dict[str, EvidenceCredibility] = {}
    issue_titles = set(historical_outcomes) | set(strategic_lessons)
    for issue_title in issue_titles:
        outcomes = historical_outcomes.get(issue_title, [])
        lessons = strategic_lessons.get(issue_title, [])
        confidence_counts = Counter(outcome.confidence or "Unspecified" for outcome in outcomes)
        source_counts = Counter(outcome.source_status or "source pending" for outcome in outcomes)
        confidence_phrase = _distribution_phrase(confidence_counts)
        evidence_summary = (
            f"{len(outcomes)} historical outcomes were retrieved. {confidence_phrase}. "
            "Source URLs are not fabricated; source status is reported separately."
        )
        if lessons:
            evidence_summary += f" {len(lessons)} rule-based strategic lesson(s) were generated from those outcomes."
        results[issue_title] = EvidenceCredibility(
            evidence_summary=evidence_summary,
            confidence_distribution=dict(confidence_counts),
            source_status_distribution=dict(source_counts),
            key_limitations=[
                "Historical outcomes are simplified educational summaries.",
                "Confidence reflects internal evidence coding, not real-world predictive accuracy.",
                "Lessons are pattern-based and should be reviewed by a human analyst.",
                "Source URLs are not fabricated; missing source links remain marked as source pending.",
            ],
            reviewer_note=(
                "Use these outcomes and lessons as decision-support context. "
                "They do not prove factual, legal, geopolitical, financial, or predictive accuracy."
            ),
        )
    return results


def _distribution_phrase(counts: Counter[str]) -> str:
    if not counts:
        return "No confidence-coded outcomes were available"
    parts = [f"{count} are {label.lower()} confidence" for label, count in sorted(counts.items())]
    return " and ".join(parts)
