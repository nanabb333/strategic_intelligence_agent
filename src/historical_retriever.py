"""Historical analogue retrieval for Strategic Intelligence Agent."""

import csv
from dataclasses import dataclass
from pathlib import Path
import re

from issue_extractor import ExtractedIssue
from scenario_classifier import ScenarioClassification
from event_understanding import EventUnderstanding


@dataclass
class HistoricalAnalogue:
    """A historical event or case with structural similarity to a scenario."""

    case_title: str
    year: str
    scenario_type: str
    similarity_reason: str
    business_relevance: str
    geopolitical_relevance: str
    caution_note: str
    source: str | None = None
    evidence_trace: str = ""
    source_title: str = "source pending"
    source_type: str = "source pending"
    source_date: str = "source pending"
    source_url: str = "source pending"
    confidence_note: str = "source pending"

    @property
    def title(self) -> str:
        """Backward-compatible alias for earlier V0.1 code."""
        return self.case_title

    @property
    def relevance(self) -> str:
        """Backward-compatible summary for earlier V0.1 code."""
        return self.similarity_reason


def _tokenize(value: str) -> set[str]:
    stop_words = {
        "and",
        "the",
        "for",
        "with",
        "from",
        "into",
        "over",
        "under",
        "that",
        "this",
        "could",
        "would",
        "about",
    }
    return {
        token
        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9-]+", value.lower())
        if len(token) >= 3 and token not in stop_words
    }


def load_historical_analogues(
    knowledge_base_path: str | Path = "knowledge_base/historical_analogues.csv",
) -> list[dict[str, str]]:
    """Load curated historical analogue records from CSV."""
    csv_path = Path(knowledge_base_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Historical analogue knowledge base not found: {csv_path}")
    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def _score_case(
    issue: ExtractedIssue,
    classification: ScenarioClassification,
    case: dict[str, str],
) -> tuple[int, list[str]]:
    reasons: list[str] = []
    score = 0

    if case["scenario_type"] == classification.primary_scenario:
        score += 8
        reasons.append(f"scenario match on {classification.primary_scenario}")

    issue_keywords = _tokenize(
        " ".join(
            [
                issue.title,
                issue.summary,
                issue.core_issue,
                " ".join(issue.policy_terms),
                " ".join(classification.matched_keywords),
            ]
        )
    )
    case_keywords = _tokenize(
        " ".join(
            [
                case["case_title"],
                case["core_issue"],
                case["why_it_matters"],
                case["business_relevance"],
                case["geopolitical_relevance"],
                case["market_relevance"],
            ]
        )
    )
    keyword_overlap = sorted(issue_keywords & case_keywords)
    if keyword_overlap:
        score += min(6, len(keyword_overlap) * 2)
        reasons.append(f"keyword overlap: {', '.join(keyword_overlap[:4])}")

    industry_overlap = sorted(_tokenize(" ".join(issue.industries)) & _tokenize(case["industries"]))
    if industry_overlap:
        score += min(4, len(industry_overlap) * 2)
        reasons.append(f"industry overlap: {', '.join(industry_overlap[:3])}")

    actor_overlap = sorted(_tokenize(" ".join(issue.actors + issue.companies)) & _tokenize(case["actors"]))
    if actor_overlap:
        score += min(4, len(actor_overlap) * 2)
        reasons.append(f"actor overlap: {', '.join(actor_overlap[:3])}")

    return score, reasons


def retrieve_historical_analogues(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    knowledge_base_path: str | Path = "knowledge_base/historical_analogues.csv",
    event_understanding: EventUnderstanding | None = None,
) -> dict[str, list[HistoricalAnalogue]]:
    """Retrieve top historical analogues using deterministic overlap scoring."""
    cases = load_historical_analogues(knowledge_base_path)
    if event_understanding and event_understanding.relevant_families:
        allowed_families = set(event_understanding.relevant_families)
        filtered_cases = [
            case for case in cases
            if case.get("scenario_type") in allowed_families
        ]
        if filtered_cases:
            cases = filtered_cases
    issue_by_title = {issue.title: issue for issue in issues}
    results: dict[str, list[HistoricalAnalogue]] = {}

    for classification in classifications:
        issue = issue_by_title[classification.issue_title]
        scored_cases = []
        for case in cases:
            score, reasons = _score_case(issue, classification, case)
            scored_cases.append((score, reasons, case))

        top_cases = sorted(scored_cases, key=lambda item: item[0], reverse=True)[:3]
        results[classification.issue_title] = [
            HistoricalAnalogue(
                case_title=case["case_title"],
                year=case["year"],
                scenario_type=case["scenario_type"],
                similarity_reason="; ".join(reasons) if reasons else "general strategic pattern similarity",
                business_relevance=case["business_relevance"],
                geopolitical_relevance=case["geopolitical_relevance"],
                caution_note="Historical analogues support comparison, not prediction.",
                source=case["source_note"],
                evidence_trace=f"{case['case_title']} ({case['year']}) - Historical Database",
                source_title=case.get("source_title", "source pending"),
                source_type=case.get("source_type", "source pending"),
                source_date=case.get("source_date", "source pending"),
                source_url=case.get("source_url", "source pending"),
                confidence_note=case.get("confidence_note", "source pending"),
            )
            for _, reasons, case in top_cases
        ]

    return results
