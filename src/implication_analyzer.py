"""Deterministic implication analysis for Strategic Intelligence Agent."""

from dataclasses import dataclass, field

from historical_retriever import HistoricalAnalogue
from issue_extractor import ExtractedIssue
from scenario_classifier import ScenarioClassification


@dataclass
class ImplicationAnalysis:
    """Strategic implications derived from issues, analogues, and context."""

    issue_title: str
    business_implications: list[str] = field(default_factory=list)
    geopolitical_implications: list[str] = field(default_factory=list)
    market_context_implications: list[str] = field(default_factory=list)
    operational_risk_implications: list[str] = field(default_factory=list)
    strategic_questions: list[str] = field(default_factory=list)

    @property
    def implications(self) -> list[str]:
        """Backward-compatible combined implication list."""
        return (
            self.business_implications
            + self.geopolitical_implications
            + self.market_context_implications
            + self.operational_risk_implications
        )

    @property
    def decision_relevance(self) -> str:
        """Backward-compatible non-advisory decision-support note."""
        return "Supports executive discussion and analyst productivity only."


def analyze_implications(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    analogues: dict[str, list[HistoricalAnalogue]],
) -> list[ImplicationAnalysis]:
    """Analyze strategic implications for each extracted issue."""
    classification_by_issue = {classification.issue_title: classification for classification in classifications}

    analyses: list[ImplicationAnalysis] = []
    for issue in issues:
        classification = classification_by_issue.get(issue.title)
        scenario = classification.primary_scenario if classification else "Other"
        issue_analogues = analogues.get(issue.title, [])
        analogue_titles = ", ".join(f"{item.case_title} ({item.year})" for item in issue_analogues[:2])
        analogue_note = analogue_titles or "the available analogue set"

        analyses.append(
            ImplicationAnalysis(
                issue_title=issue.title,
                business_implications=[
                    f"The issue may indicate changing constraints for {', '.join(issue.industries[:3]) or 'affected business operations'}.",
                    f"The {scenario.lower()} frame raises questions about compliance, supplier exposure, and executive communication needs.",
                    f"Comparable cases such as {analogue_note} could help analysts structure follow-up research.",
                ],
                geopolitical_implications=[
                    f"The issue could affect cross-border coordination involving {', '.join(issue.countries_or_regions[:3]) or 'relevant jurisdictions'}.",
                    "The policy and security context requires monitoring because government actions can alter operating assumptions.",
                ],
                market_context_implications=[
                    "The event may shape market narratives around resilience, access, and regulatory exposure.",
                    "Analysts should separate observed facts from broader market interpretation.",
                ],
                operational_risk_implications=[
                    "The issue could affect supplier continuity, licensing workflows, or contingency planning.",
                    "Operational teams may need to monitor counterparties, timelines, and implementation details.",
                ],
                strategic_questions=[
                    "Which stakeholders are most exposed to this issue?",
                    "What facts would change the current scenario classification?",
                    "Which historical analogue is structurally closest, and where does the comparison break down?",
                    "What decisions require more source verification before executive action?",
                ],
            )
        )
    return analyses
