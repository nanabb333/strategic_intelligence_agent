"""Scenario classification stage for Strategic Intelligence Agent."""

from dataclasses import dataclass

from issue_extractor import ExtractedIssue


@dataclass
class ScenarioClassification:
    """Scenario type assigned to an extracted issue."""

    issue_title: str
    scenario_type: str
    rationale: str


def classify_scenarios(issues: list[ExtractedIssue]) -> list[ScenarioClassification]:
    """Classify extracted issues into strategic scenario categories."""
    classifications: list[ScenarioClassification] = []
    for issue in issues:
        classifications.append(
            ScenarioClassification(
                issue_title=issue.title,
                scenario_type="strategic_uncertainty",
                rationale="Initial placeholder classification pending domain rules or LLM analysis.",
            )
        )
    return classifications

