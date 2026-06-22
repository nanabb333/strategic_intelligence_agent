"""Deterministic implication analysis for Strategic Intelligence Agent."""

from dataclasses import dataclass, field

from context_retriever import CurrentContext
from historical_retriever import HistoricalAnalogue
from issue_extractor import ExtractedIssue
from scenario_classifier import ScenarioClassification


@dataclass
class ImplicationAnalysis:
    """Strategic implications derived from issues, analogues, and context."""

    issue_title: str
    observed_similarities: list[str] = field(default_factory=list)
    observed_differences: list[str] = field(default_factory=list)
    business_considerations: list[str] = field(default_factory=list)
    operational_considerations: list[str] = field(default_factory=list)
    geopolitical_considerations: list[str] = field(default_factory=list)
    strategic_questions: list[str] = field(default_factory=list)
    evidence_trace: list[str] = field(default_factory=list)

    @property
    def business_implications(self) -> list[str]:
        """Backward-compatible alias."""
        return self.business_considerations

    @property
    def geopolitical_implications(self) -> list[str]:
        """Backward-compatible alias."""
        return self.geopolitical_considerations

    @property
    def market_context_implications(self) -> list[str]:
        """Backward-compatible alias."""
        return self.observed_similarities

    @property
    def operational_risk_implications(self) -> list[str]:
        """Backward-compatible alias."""
        return self.operational_considerations

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
    contexts: dict[str, list[CurrentContext]],
) -> list[ImplicationAnalysis]:
    """Analyze strategic implications for each extracted issue."""
    classification_by_issue = {classification.issue_title: classification for classification in classifications}

    analyses: list[ImplicationAnalysis] = []
    for issue in issues:
        classification = classification_by_issue.get(issue.title)
        scenario = classification.primary_scenario if classification else "Other"
        issue_analogues = analogues.get(issue.title, [])
        issue_contexts = contexts.get(issue.title, [])
        analogue_titles = ", ".join(f"{item.case_title} ({item.year})" for item in issue_analogues[:2]) or "the retrieved historical analogue set"
        context_industries = ", ".join(sorted({context.industry for context in issue_contexts[:3]})) or "the retrieved context set"
        evidence_trace = [item.evidence_trace for item in issue_analogues] + [
            item.evidence_trace for item in issue_contexts
        ]

        analyses.append(
            ImplicationAnalysis(
                issue_title=issue.title,
                observed_similarities=[
                    f"The issue may resemble {analogue_titles} because the retrieved cases share characteristics with the {scenario.lower()} scenario frame.",
                    f"The current context findings from {context_industries} share characteristics with the extracted industries and policy terms.",
                ],
                observed_differences=[
                    "The source document differs from historical analogues because current actors, implementation details, and timing are document-specific.",
                    "The retrieved context differs from historical cases because it describes standing monitoring considerations rather than a completed event.",
                ],
                business_considerations=[
                    f"The issue may indicate changing constraints for {', '.join(issue.industries[:3]) or 'affected business operations'} and requires monitoring of stakeholder exposure.",
                    f"The {scenario.lower()} frame raises questions about compliance, supplier exposure, customer communication, and executive briefing needs.",
                    "Historical and context evidence should be used to structure diligence, not to imply an outcome.",
                ],
                operational_considerations=[
                    "Operational teams may need to monitor counterparties, implementation timelines, documentation requirements, and contingency plans.",
                    "The issue could affect supplier continuity, licensing workflows, routing choices, or internal escalation paths depending on the scenario.",
                ],
                geopolitical_considerations=[
                    f"The issue could affect cross-border coordination involving {', '.join(issue.countries_or_regions[:3]) or 'relevant jurisdictions'}.",
                    "Government actions, regulatory updates, and security conditions require monitoring because they can alter operating assumptions.",
                ],
                strategic_questions=[
                    "Which stakeholders are most exposed to this issue?",
                    "What facts would change the current scenario classification?",
                    "Which historical analogue is structurally closest, and where does the comparison differ from current context?",
                    "Which current-context findings require source verification before executive discussion?",
                    "What decisions require more source verification before executive action?",
                ],
                evidence_trace=evidence_trace,
            )
        )
    return analyses
