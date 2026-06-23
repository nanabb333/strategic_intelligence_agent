"""Detect strategic mechanisms from scenarios and extracted issue metadata."""

import csv
from dataclasses import dataclass
from pathlib import Path
import re

from issue_extractor import ExtractedIssue
from scenario_classifier import ScenarioClassification


@dataclass
class Mechanism:
    """Strategic mechanism detected for an issue."""

    mechanism_id: str
    mechanism_name: str
    description: str
    related_scenarios: str
    typical_actors: str
    historical_examples: str
    possible_observations: str
    detection_reason: str
    evidence_references: list[str]


def _tokens(value: str) -> set[str]:
    return {token for token in re.findall(r"[a-zA-Z][a-zA-Z0-9-]+", value.lower()) if len(token) > 3}


def load_mechanisms(path: str | Path = "knowledge_base/mechanism_framework.csv") -> list[dict[str, str]]:
    """Load mechanism records."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Mechanism framework not found: {csv_path}")
    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def detect_mechanisms(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    mechanism_path: str | Path = "knowledge_base/mechanism_framework.csv",
    limit: int = 4,
) -> dict[str, list[Mechanism]]:
    """Map scenario and issue metadata to multiple possible mechanisms."""
    records = load_mechanisms(mechanism_path)
    classification_by_issue = {classification.issue_title: classification for classification in classifications}
    results: dict[str, list[Mechanism]] = {}

    for issue in issues:
        classification = classification_by_issue.get(issue.title)
        scenario = classification.primary_scenario if classification else "Other"
        issue_terms = _tokens(
            " ".join(
                [
                    issue.title,
                    issue.summary,
                    issue.core_issue,
                    " ".join(issue.industries),
                    " ".join(issue.actors),
                    " ".join(issue.policy_terms),
                ]
            )
        )
        scored: list[tuple[int, dict[str, str], list[str]]] = []
        for record in records:
            reasons: list[str] = []
            score = 0
            scenarios = [item.strip() for item in record["related_scenarios"].split(";")]
            if scenario in scenarios:
                score += 8
                reasons.append(f"scenario match: {scenario}")
            overlap = sorted(issue_terms & _tokens(record["possible_observations"] + " " + record["description"]))
            if overlap:
                score += min(6, len(overlap) * 2)
                reasons.append(f"observation overlap: {', '.join(overlap[:4])}")
            actor_overlap = sorted(_tokens(" ".join(issue.actors)) & _tokens(record["typical_actors"]))
            if actor_overlap:
                score += min(4, len(actor_overlap) * 2)
                reasons.append(f"actor overlap: {', '.join(actor_overlap[:3])}")
            scored.append((score, record, reasons))

        top_records = sorted(scored, key=lambda item: item[0], reverse=True)[:limit]
        results[issue.title] = [
            Mechanism(
                mechanism_id=record["mechanism_id"],
                mechanism_name=record["mechanism_name"],
                description=record["description"],
                related_scenarios=record["related_scenarios"],
                typical_actors=record["typical_actors"],
                historical_examples=record["historical_examples"],
                possible_observations=record["possible_observations"],
                detection_reason="; ".join(reasons) if reasons else "general mechanism relevance",
                evidence_references=["Source Document", f"{record['mechanism_name']} (Mechanism Framework)"],
            )
            for _, record, reasons in top_records
        ]

    return results

