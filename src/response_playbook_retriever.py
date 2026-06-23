"""Retrieve observed historical response patterns and lessons."""

from dataclasses import dataclass, field

from historical_retriever import HistoricalAnalogue
from mechanism_detector import Mechanism


@dataclass
class ResponsePattern:
    """Observed historical response pattern."""

    issue_title: str
    pattern_name: str
    observed_historical_choices: list[str] = field(default_factory=list)
    observed_outcomes: list[str] = field(default_factory=list)
    business_lessons: list[str] = field(default_factory=list)
    cross_domain_lessons: list[str] = field(default_factory=list)
    evidence_references: list[str] = field(default_factory=list)


def retrieve_response_patterns(
    analogues: dict[str, list[HistoricalAnalogue]],
    mechanisms: dict[str, list[Mechanism]],
) -> dict[str, list[ResponsePattern]]:
    """Retrieve deterministic response patterns from analogues and mechanisms."""
    results: dict[str, list[ResponsePattern]] = {}
    for issue_title, issue_analogues in analogues.items():
        issue_mechanisms = mechanisms.get(issue_title, [])
        mechanism_names = [item.mechanism_name for item in issue_mechanisms[:3]]
        analogue_names = [item.case_title for item in issue_analogues[:3]]
        evidence = [item.evidence_trace for item in issue_analogues[:3]]
        evidence += [f"{item.mechanism_name} (Mechanism Framework)" for item in issue_mechanisms[:3]]
        results[issue_title] = [
            ResponsePattern(
                issue_title=issue_title,
                pattern_name="Monitoring and contingency planning",
                observed_historical_choices=[
                    "Organizations reviewed counterparties, suppliers, and implementation details.",
                    "Teams created monitoring routines around policy updates and operational constraints.",
                ],
                observed_outcomes=[
                    "Observed outcomes varied across cases and should not be treated as predictive.",
                    f"Relevant analogues include {', '.join(analogue_names) or 'retrieved analogue records'}.",
                ],
                business_lessons=[
                    "Decision-makers may wish to monitor exposure, stakeholder communication, and operating dependencies.",
                    "Cross-functional review can help separate compliance, operational, and strategic questions.",
                ],
                cross_domain_lessons=[
                    f"Mechanisms such as {', '.join(mechanism_names) or 'detected mechanisms'} can appear across policy, security, and business domains.",
                    "Historical response patterns are most useful when paired with current context and source verification.",
                ],
                evidence_references=evidence,
            )
        ]
    return results

