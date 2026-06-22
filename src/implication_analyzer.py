"""Implication analysis for Strategic Intelligence Agent."""

from dataclasses import dataclass, field

from context_retriever import CurrentContext
from historical_retriever import HistoricalAnalogue
from issue_extractor import ExtractedIssue
from scenario_classifier import ScenarioClassification


@dataclass
class ImplicationAnalysis:
    """Strategic implications derived from issues, analogues, and context."""

    issue_title: str
    implications: list[str] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)
    decision_relevance: str = ""


def analyze_implications(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    analogues: dict[str, list[HistoricalAnalogue]],
    contexts: list[CurrentContext],
) -> list[ImplicationAnalysis]:
    """Analyze strategic implications for each extracted issue."""
    _ = classifications
    _ = analogues
    context_by_issue = {context.issue_title: context for context in contexts}

    analyses: list[ImplicationAnalysis] = []
    for issue in issues:
        context = context_by_issue.get(issue.title)
        context_note = context.summary if context else "No current context available."
        analyses.append(
            ImplicationAnalysis(
                issue_title=issue.title,
                implications=[
                    "Assess stakeholder exposure and operational dependencies.",
                    f"Context note: {context_note}",
                ],
                uncertainties=issue.uncertainties,
                decision_relevance="Supports executive discussion; does not provide investment advice.",
            )
        )
    return analyses

