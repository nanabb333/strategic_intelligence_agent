"""Executive brief generation for Strategic Intelligence Agent."""

from historical_retriever import HistoricalAnalogue
from implication_analyzer import ImplicationAnalysis
from issue_extractor import ExtractedIssue
from scenario_classifier import ScenarioClassification


def generate_brief(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    analogues: dict[str, list[HistoricalAnalogue]],
    analyses: list[ImplicationAnalysis],
) -> str:
    """Generate a Markdown executive intelligence brief."""
    classification_by_issue = {item.issue_title: item for item in classifications}
    analysis_by_issue = {item.issue_title: item for item in analyses}

    lines = [
        "# Executive Intelligence Brief",
        "",
        "This output is for decision-support and analyst productivity only. It does not provide forecasts, probabilities, trading advice, or investment recommendations.",
        "",
    ]

    for issue in issues:
        classification = classification_by_issue.get(issue.title)
        analysis = analysis_by_issue.get(issue.title)
        issue_analogues = analogues.get(issue.title, [])

        lines.extend(
            [
                "## 1. Key Issue",
                "",
                f"**Title:** {issue.title}",
                "",
                f"**Core issue:** {issue.core_issue}",
                "",
                f"**Summary:** {issue.summary}",
                "",
                "## 2. Scenario Classification",
                "",
            ]
        )
        if classification:
            lines.extend(
                [
                    f"- **Primary scenario:** {classification.primary_scenario}",
                    f"- **Matched keywords:** {', '.join(classification.matched_keywords) or 'None'}",
                    f"- **Classification confidence:** {classification.confidence_label}",
                    "- **Note:** Confidence describes deterministic keyword classification quality, not a forecast.",
                ]
            )
        else:
            lines.append("- **Primary scenario:** Unclassified")

        lines.extend(
            [
                "",
                "## 3. Extracted Entities",
                "",
                f"- **Document type guess:** {issue.document_type_guess}",
                f"- **Actors:** {', '.join(issue.actors) or 'None detected'}",
                f"- **Countries / regions:** {', '.join(issue.countries_or_regions) or 'None detected'}",
                f"- **Industries:** {', '.join(issue.industries) or 'None detected'}",
                f"- **Policy terms:** {', '.join(issue.policy_terms) or 'None detected'}",
                f"- **Companies:** {', '.join(issue.companies) or 'None detected'}",
                "",
                "## 4. Historical Analogues",
                "",
            ]
        )
        for analogue in issue_analogues:
            lines.extend(
                [
                    f"### {analogue.case_title} ({analogue.year})",
                    "",
                    f"- **Scenario type:** {analogue.scenario_type}",
                    f"- **Similarity reason:** {analogue.similarity_reason}",
                    f"- **Business relevance:** {analogue.business_relevance}",
                    f"- **Geopolitical relevance:** {analogue.geopolitical_relevance}",
                    f"- **Caution note:** {analogue.caution_note}",
                    f"- **Source note:** {analogue.source or 'Public-history reference'}",
                    "",
                ]
            )

        lines.extend(
            [
                "## 5. Current Relevance",
                "",
                f"- The document may indicate a current {classification.primary_scenario if classification else 'strategic'} issue requiring structured monitoring.",
                "- Current relevance is based only on the supplied document and the local historical analogue knowledge base.",
                "- No external current-data retrieval or paid API is used in V0.5.",
                "",
                "## 6. Business and Geopolitical Implications",
                "",
                "### Business Implications",
            ]
        )
        if analysis:
            for item in analysis.business_implications:
                lines.append(f"- {item}")
            lines.extend(["", "### Geopolitical Implications"])
            for item in analysis.geopolitical_implications:
                lines.append(f"- {item}")
            lines.extend(["", "### Market Context Implications"])
            for item in analysis.market_context_implications:
                lines.append(f"- {item}")
            lines.extend(["", "### Operational Risk Implications"])
            for item in analysis.operational_risk_implications:
                lines.append(f"- {item}")
        else:
            lines.append("- No implication analysis available.")

        lines.extend(["", "## 7. Strategic Questions for Decision-Makers", ""])
        if analysis:
            for question in analysis.strategic_questions:
                lines.append(f"- {question}")
        else:
            lines.append("- What additional source material is needed?")

        lines.extend(
            [
                "",
                "## 8. Analyst Notes and Limitations",
                "",
                "- V0.5 uses deterministic keyword and overlap matching.",
                "- Historical analogues support structured comparison, not prediction.",
                "- Classification confidence is not a probability.",
                "- Outputs should be reviewed against primary sources before executive use.",
                "",
            ]
        )

    return "\n".join(lines).strip() + "\n"
