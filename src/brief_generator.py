"""Executive brief generation for Strategic Intelligence Agent."""

from context_retriever import CurrentContext
from historical_retriever import HistoricalAnalogue
from implication_analyzer import ImplicationAnalysis
from issue_extractor import ExtractedIssue
from scenario_classifier import ScenarioClassification


def generate_brief(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    analogues: dict[str, list[HistoricalAnalogue]],
    contexts: list[CurrentContext],
    analyses: list[ImplicationAnalysis],
) -> str:
    """Generate a Markdown executive intelligence brief."""
    classification_by_issue = {item.issue_title: item for item in classifications}
    context_by_issue = {item.issue_title: item for item in contexts}
    analysis_by_issue = {item.issue_title: item for item in analyses}

    lines = [
        "# Executive Intelligence Brief",
        "",
        "This brief is for strategic decision support. It is not investment advice.",
        "",
    ]

    for issue in issues:
        classification = classification_by_issue.get(issue.title)
        context = context_by_issue.get(issue.title)
        analysis = analysis_by_issue.get(issue.title)
        issue_analogues = analogues.get(issue.title, [])

        lines.extend(
            [
                f"## {issue.title}",
                "",
                f"**Summary:** {issue.summary}",
                "",
                f"**Scenario:** {classification.scenario_type if classification else 'Unclassified'}",
                "",
                "**Historical Analogues:**",
            ]
        )
        for analogue in issue_analogues:
            lines.append(f"- {analogue.title}: {analogue.relevance}")

        lines.extend(["", "**Current Context:**"])
        lines.append(context.summary if context else "No current context available.")

        lines.extend(["", "**Implications:**"])
        if analysis:
            for implication in analysis.implications:
                lines.append(f"- {implication}")
            lines.extend(["", f"**Decision Relevance:** {analysis.decision_relevance}"])
        else:
            lines.append("- No implication analysis available.")

        lines.append("")

    return "\n".join(lines).strip() + "\n"

