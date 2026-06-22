"""Executive brief generation for Strategic Intelligence Agent."""

from context_retriever import CurrentContext
from historical_retriever import HistoricalAnalogue
from implication_analyzer import ImplicationAnalysis
from issue_extractor import ExtractedIssue
from scenario_classifier import ScenarioClassification


DISCLAIMER = (
    "This output is for decision-support and analyst productivity only. It does not provide "
    "forecasts, probabilities, trading advice, or investment recommendations."
)


def _bullet_list(items: list[str], empty_message: str) -> list[str]:
    if not items:
        return [f"- {empty_message}"]
    return [f"- {item}" for item in items]


def _article_for(value: str) -> str:
    return "an" if value[:1].lower() in {"a", "e", "i", "o", "u"} else "a"


def generate_brief(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    analogues: dict[str, list[HistoricalAnalogue]],
    contexts: dict[str, list[CurrentContext]],
    analyses: list[ImplicationAnalysis],
) -> str:
    """Generate a Markdown executive intelligence brief."""
    classification_by_issue = {item.issue_title: item for item in classifications}
    analysis_by_issue = {item.issue_title: item for item in analyses}

    lines = ["# Executive Intelligence Brief", "", DISCLAIMER, ""]

    for issue in issues:
        classification = classification_by_issue.get(issue.title)
        scenario = classification.primary_scenario if classification else "Other"
        analysis = analysis_by_issue.get(issue.title)
        issue_analogues = analogues.get(issue.title, [])
        issue_contexts = contexts.get(issue.title, [])

        lines.extend(
            [
                "## Executive Summary",
                "",
                f"- The document describes {_article_for(scenario)} {scenario} issue involving {', '.join(issue.industries[:3]) or 'strategic operations'}.",
                "- Historical analogues and current context are used for comparison and decision support, not prediction.",
                "- Evidence traces identify whether each finding comes from the source document, the historical database, or the current context knowledge base.",
                "",
                "## Key Issue",
                "",
                f"**Title:** {issue.title}",
                "",
                f"**Core issue:** {issue.core_issue}",
                "",
                f"**Summary:** {issue.summary}",
                "",
                "**Evidence trace:** Source Document",
                "",
                "## Scenario Classification",
                "",
            ]
        )
        if classification:
            lines.extend(
                [
                    f"- **Primary scenario:** {classification.primary_scenario}",
                    f"- **Matched keywords:** {', '.join(classification.matched_keywords) or 'None'}",
                    f"- **Classification confidence:** {classification.confidence_label}",
                    "- **Evidence trace:** Source Document + deterministic keyword classifier",
                    "- **Note:** Confidence describes classification quality only; it is not a forecast.",
                ]
            )
        else:
            lines.append("- **Primary scenario:** Unclassified")

        lines.extend(
            [
                "",
                "## Extracted Entities",
                "",
                f"- **Document type guess:** {issue.document_type_guess} (Evidence trace: Source Document)",
                f"- **Actors:** {', '.join(issue.actors) or 'None detected'} (Evidence trace: Source Document)",
                f"- **Countries / regions:** {', '.join(issue.countries_or_regions) or 'None detected'} (Evidence trace: Source Document)",
                f"- **Industries:** {', '.join(issue.industries) or 'None detected'} (Evidence trace: Source Document)",
                f"- **Policy terms:** {', '.join(issue.policy_terms) or 'None detected'} (Evidence trace: Source Document)",
                f"- **Companies:** {', '.join(issue.companies) or 'None detected'} (Evidence trace: Source Document)",
                "",
                "## Historical Analogues",
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
                    f"- **Source origin:** {analogue.evidence_trace}",
                    "",
                ]
            )

        lines.extend(["## Current Context", ""])
        for context in issue_contexts:
            lines.extend(
                [
                    f"### {context.industry} - {context.scenario_type}",
                    "",
                    f"- **Context summary:** {context.context_summary}",
                    f"- **Why it matters:** {context.why_it_matters}",
                    f"- **Stakeholders:** {context.stakeholders}",
                    f"- **Monitoring considerations:** {context.monitoring_considerations}",
                    f"- **Retrieval reason:** {context.similarity_reason}",
                    f"- **Source origin:** {context.evidence_trace}",
                    "",
                ]
            )

        lines.extend(["## Similarities and Differences", ""])
        if analysis:
            lines.append("### Observed Similarities")
            lines.extend(_bullet_list(analysis.observed_similarities, "No observed similarities generated."))
            lines.append("")
            lines.append("### Observed Differences")
            lines.extend(_bullet_list(analysis.observed_differences, "No observed differences generated."))
        else:
            lines.append("- No synthesis available.")

        lines.extend(["", "## Business Considerations", ""])
        if analysis:
            lines.extend(_bullet_list(analysis.business_considerations, "No business considerations generated."))
        else:
            lines.append("- No business considerations generated.")

        lines.extend(["", "## Operational Considerations", ""])
        if analysis:
            lines.extend(_bullet_list(analysis.operational_considerations, "No operational considerations generated."))
        else:
            lines.append("- No operational considerations generated.")

        lines.extend(["", "## Geopolitical Considerations", ""])
        if analysis:
            lines.extend(_bullet_list(analysis.geopolitical_considerations, "No geopolitical considerations generated."))
        else:
            lines.append("- No geopolitical considerations generated.")

        lines.extend(["", "## Strategic Questions", ""])
        if analysis:
            lines.extend(_bullet_list(analysis.strategic_questions, "No strategic questions generated."))
        else:
            lines.append("- What additional source material is needed?")

        lines.extend(
            [
                "",
                "## Analyst Notes",
                "",
                "- Current context retrieval uses local Markdown knowledge-base entries.",
                "- Historical analogues support structured comparison, not prediction.",
                "- The synthesis uses phrases such as may resemble, shares characteristics with, differs from, and requires monitoring by design.",
                "",
                "## Limitations",
                "",
                "- V1.0 uses deterministic keyword and overlap matching.",
                "- It does not call paid APIs or LLM services.",
                "- It does not generate forecasts or probabilities.",
                "- It does not provide trading advice or investment recommendations.",
                "- Outputs should be reviewed against primary sources before executive use.",
                "",
                "### Evidence Trace",
                "",
            ]
        )
        evidence_items = ["Source Document"] + [item.evidence_trace for item in issue_analogues]
        evidence_items += [item.evidence_trace for item in issue_contexts]
        if analysis:
            evidence_items += analysis.evidence_trace
        for evidence in sorted(set(evidence_items)):
            lines.append(f"- {evidence}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"
