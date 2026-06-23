"""Retrieve historical outcomes linked to retrieved historical analogues."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from historical_retriever import HistoricalAnalogue


@dataclass
class HistoricalOutcome:
    """Observed outcome and response pattern for a historical case."""

    case_id: str
    case_name: str
    event_family: str
    year: str
    actor: str
    sector: str
    observed_outcome: str
    strategic_response: str
    time_horizon: str
    confidence: str
    source_status: str
    retrieval_reason: str
    evidence_references: list[str]


def load_historical_outcomes(path: str | Path = "knowledge_base/historical_outcomes.csv") -> list[dict[str, str]]:
    """Load curated historical outcome records."""
    with Path(path).open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def retrieve_historical_outcomes(
    analogues: dict[str, list[HistoricalAnalogue]],
    outcomes_path: str | Path = "knowledge_base/historical_outcomes.csv",
    limit: int = 5,
) -> dict[str, list[HistoricalOutcome]]:
    """Retrieve outcomes using analogue title and event-family overlap."""
    records = load_historical_outcomes(outcomes_path)
    results: dict[str, list[HistoricalOutcome]] = {}
    for issue_title, issue_analogues in analogues.items():
        scored: list[tuple[int, dict[str, str], list[str]]] = []
        analogue_titles = [item.case_title.lower() for item in issue_analogues]
        analogue_families = [item.scenario_type.lower() for item in issue_analogues]
        for record in records:
            reasons: list[str] = []
            score = 0
            case_name = record["case_name"].lower()
            event_family = record["event_family"].lower()
            if any(case_name in title or title in case_name for title in analogue_titles):
                score += 10
                reasons.append("case-name match with retrieved analogue")
            if event_family in analogue_families:
                score += 6
                reasons.append(f"event-family match: {record['event_family']}")
            if any(event_family in title for title in analogue_titles):
                score += 3
                reasons.append("event-family/title overlap")
            scored.append((score, record, reasons))

        top_records = sorted(scored, key=lambda item: item[0], reverse=True)[:limit]
        outcomes: list[HistoricalOutcome] = []
        for _, record, reasons in top_records:
            outcomes.append(
                HistoricalOutcome(
                    case_id=record["case_id"],
                    case_name=record["case_name"],
                    event_family=record["event_family"],
                    year=record["year"],
                    actor=record["actor"],
                    sector=record["sector"],
                    observed_outcome=record["observed_outcome"],
                    strategic_response=record["strategic_response"],
                    time_horizon=record["time_horizon"],
                    confidence=record["confidence"],
                    source_status=record["source_status"],
                    retrieval_reason="; ".join(reasons) if reasons else "general outcome relevance",
                    evidence_references=[
                        f"{record['case_name']} ({record['year']}) - Historical Outcomes Database",
                    ],
                )
            )
        results[issue_title] = outcomes
    return results
