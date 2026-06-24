"""Executive brief generation for Strategic Intelligence Agent."""

from context_retriever import CurrentContext
from event_context import EventContext
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


def _format_distribution(distribution: dict[str, int]) -> str:
    if not distribution:
        return "None"
    return ", ".join(f"{key}: {value}" for key, value in sorted(distribution.items()))


def _format_event_context(event_context: EventContext | None) -> list[str]:
    if not event_context:
        return ["- No current-event context was extracted."]
    lines = [
        f"- **Event type:** {event_context.event_type}",
        f"- **Primary actor:** {event_context.primary_actor}",
        f"- **Secondary actor:** {event_context.secondary_actor}",
        f"- **Affected sectors:** {', '.join(event_context.affected_sectors) or 'Not specified'}",
        f"- **Affected regions:** {', '.join(event_context.affected_regions) or 'Not specified'}",
        f"- **Policy domain:** {event_context.policy_domain}",
        f"- **Strategic significance:** {event_context.strategic_significance}",
        f"- **Event summary:** {event_context.event_summary}",
        f"- **Confidence:** {event_context.confidence}",
        "- **Evidence trace:** Source Document + deterministic current-event rules",
    ]
    if event_context.context_limitations:
        lines.append("- **Limitations:** " + " ".join(event_context.context_limitations))
    return lines


def generate_brief(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    analogues: dict[str, list[HistoricalAnalogue]],
    contexts: dict[str, list[CurrentContext]],
    analyses: list[ImplicationAnalysis],
    agent_route=None,
    mechanisms=None,
    interpretations=None,
    evidence_assessments=None,
    historical_outcomes=None,
    strategic_lessons=None,
    strategic_assessments=None,
    evidence_credibility=None,
    response_patterns=None,
    event_context: EventContext | None = None,
    source_url: str = "",
) -> str:
    """Generate a Markdown executive intelligence brief."""
    classification_by_issue = {item.issue_title: item for item in classifications}
    analysis_by_issue = {item.issue_title: item for item in analyses}

    lines = ["# Executive Intelligence Brief", ""]

    for issue in issues:
        classification = classification_by_issue.get(issue.title)
        scenario = classification.primary_scenario if classification else "Other"
        analysis = analysis_by_issue.get(issue.title)
        issue_analogues = analogues.get(issue.title, [])
        issue_contexts = contexts.get(issue.title, [])
        issue_mechanisms = (mechanisms or {}).get(issue.title, [])
        issue_interpretations = (interpretations or {}).get(issue.title, [])
        issue_assessments = (evidence_assessments or {}).get(issue.title, [])
        issue_historical_outcomes = (historical_outcomes or {}).get(issue.title, [])
        issue_strategic_lessons = (strategic_lessons or {}).get(issue.title, [])
        issue_strategic_assessment = (strategic_assessments or {}).get(issue.title)
        issue_evidence_credibility = (evidence_credibility or {}).get(issue.title)
        issue_response_patterns = (response_patterns or {}).get(issue.title, [])

        if issue_strategic_assessment:
            similar_cases = ", ".join(item.case_name for item in issue_historical_outcomes[:3]) or "No close historical cases retrieved"
            happened_then = issue_historical_outcomes[0].observed_outcome if issue_historical_outcomes else "No observed historical outcome was retrieved."
            response_then = issue_historical_outcomes[0].strategic_response if issue_historical_outcomes else "No historical response pattern was retrieved."
            happened_after = (
                f"{issue_strategic_assessment.outcome_distribution[0].outcome_type} was the most common retrieved outcome category "
                f"({issue_strategic_assessment.outcome_distribution[0].frequency_percent}% of retrieved cases)."
                if issue_strategic_assessment.outcome_distribution
                else "No outcome distribution was available."
            )
            watch_now = " ".join(issue_strategic_assessment.strategic_watchlist[:2])
            lines.extend(
                [
                    "## Direct Answer",
                    "",
                    f"- **Similar cases:** {similar_cases}.",
                    f"- **What happened then:** {happened_then}",
                    f"- **How organizations responded:** {response_then}",
                    f"- **What happened after:** {happened_after}",
                    f"- **What to watch now:** {watch_now}",
                    f"- **Assessment:** {issue_strategic_assessment.direct_answer}",
                    "",
                    "## Historical Patterns",
                    "",
                ]
            )
            if issue_strategic_assessment.historical_patterns:
                for pattern in issue_strategic_assessment.historical_patterns:
                    lines.extend(
                        [
                            f"- **{pattern.frequency_percent}%:** {pattern.pattern}",
                            f"  - {pattern.interpretation}",
                            f"  - Supporting cases: {', '.join(pattern.supporting_cases) or 'None listed'}",
                        ]
                    )
            else:
                lines.append("- No cross-case patterns were available from retrieved outcomes.")
            lines.extend(["", "## Historical Outcome Distribution", ""])
            if issue_strategic_assessment.outcome_distribution:
                for item in issue_strategic_assessment.outcome_distribution:
                    lines.extend(
                        [
                            f"- **{item.outcome_type}: {item.frequency_percent}%** ({item.case_count} retrieved case(s))",
                            f"  - {item.interpretation}",
                        ]
                    )
            else:
                lines.append("- No outcome distribution was available from retrieved outcomes.")
            lines.extend(["", "## Market Expectations vs Outcomes", ""])
            if issue_strategic_assessment.expectation_vs_reality:
                for gap in issue_strategic_assessment.expectation_vs_reality:
                    lines.extend(
                        [
                            f"### {gap.event}",
                            "",
                            f"- **Mainstream expectation:** {gap.consensus_expectation}",
                            f"- **Market / user behavior:** {gap.market_user_behavior}",
                            f"- **Actual outcome:** {gap.observed_outcome}",
                            f"- **Expectation gap:** {gap.expectation_gap}",
                            f"- **Strategic lesson:** {gap.strategic_lesson}",
                            "",
                        ]
                    )
            else:
                lines.append("- No expectation-gap comparison was available.")
            lines.extend(["## Strategic Watchlist", ""])
            lines.extend(_bullet_list(issue_strategic_assessment.strategic_watchlist, "No monitoring recommendations generated."))
            lines.extend(["", "## Role-Based Monitoring", "", "### Investor View", ""])
            lines.extend(_bullet_list(issue_strategic_assessment.role_based_monitoring.investor_view, "No investor monitoring priorities generated."))
            lines.extend(["", "### Corporate Strategy View", ""])
            lines.extend(
                _bullet_list(
                    issue_strategic_assessment.role_based_monitoring.corporate_strategy_view,
                    "No corporate strategy monitoring priorities generated.",
                )
            )
            lines.extend(["", "### Supply Chain View", ""])
            lines.extend(_bullet_list(issue_strategic_assessment.role_based_monitoring.supply_chain_view, "No supply-chain monitoring priorities generated."))
            lines.append("")

        lines.extend(
            [
                "## Executive Summary",
                "",
                f"- The document describes {_article_for(scenario)} {scenario} issue involving {', '.join(issue.industries[:3]) or 'strategic operations'}.",
                "- Evidence traces identify whether each finding comes from the source document, the historical database, or the current context knowledge base.",
                "",
            ]
        )

        if agent_route:
            lines.extend(
                [
                    "## Agent Execution Trace",
                    "",
                    f"- **Document type detected:** {agent_route.document_type}",
                    f"- **Scenario detected:** {agent_route.scenario_type}",
                    f"- **Selected tools:** {', '.join(agent_route.selected_tools) or 'None'}",
                    f"- **Skipped tools:** {', '.join(agent_route.skipped_tools) or 'None'}",
                    "",
                ]
            )
            for step in agent_route.trace:
                lines.append(f"{step.step}. **{step.event}:** {step.detail}")
            lines.extend(["", "## Tool Decisions", ""])
            for decision in agent_route.reasoning_record:
                lines.extend(
                    [
                        f"### {decision.tool}",
                        "",
                        f"- **Decision:** {decision.decision}",
                        f"- **Why:** {decision.why}",
                        f"- **Expected contribution:** {decision.expected_contribution}",
                        "",
                    ]
                )
            lines.extend(
                [
                    "## Analysis Path",
                    "",
                    "- Agent Router reviewed document type, scenario, industries, actors, and keywords.",
                    "- Tool Registry provided available deterministic tools.",
                    "- Selected tools executed in route order.",
                    "- Result synthesis generated the executive brief with evidence sources.",
                    "",
                ]
            )

        lines.extend(
            [
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
                "## Current Event Context",
                "",
            ]
        )
        lines.extend(_format_event_context(event_context))
        if source_url:
            lines.extend(["", f"- **Source Link:** {source_url}", "- **Source Link note:** Captured as source metadata. Live web retrieval is not enabled."])
        lines.extend(
            [
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

        lines.extend(["## Historical Outcomes", ""])
        if issue_historical_outcomes:
            for outcome in issue_historical_outcomes:
                lines.extend(
                    [
                        f"### {outcome.case_name} ({outcome.year})",
                        "",
                        f"- **Event family:** {outcome.event_family}",
                        f"- **Observed outcome:** {outcome.observed_outcome}",
                        f"- **Strategic response:** {outcome.strategic_response}",
                        f"- **Time horizon:** {outcome.time_horizon}",
                        f"- **Confidence:** {outcome.confidence}",
                        f"- **Source status:** {outcome.source_status}",
                        f"- **Retrieval reason:** {outcome.retrieval_reason}",
                        "",
                    ]
                )
        else:
            lines.append("- No historical outcomes retrieved.")

        lines.extend(["## Strategic Lessons", ""])
        if issue_strategic_lessons:
            for lesson in issue_strategic_lessons:
                lines.extend(
                    [
                        f"### {lesson.lesson}",
                        "",
                        f"- **Supporting cases:** {', '.join(lesson.supporting_cases)}",
                        f"- **Confidence:** {lesson.confidence}",
                        f"- **Rationale:** {lesson.rationale}",
                        "",
                    ]
                )
        else:
            lines.append("- No recurring strategic lessons generated.")

        lines.extend(["## Evidence Credibility Note", ""])
        if issue_evidence_credibility:
            lines.extend(
                [
                    f"- **Evidence summary:** {issue_evidence_credibility.evidence_summary}",
                    f"- **Confidence distribution:** {_format_distribution(issue_evidence_credibility.confidence_distribution)}",
                    f"- **Source status distribution:** {_format_distribution(issue_evidence_credibility.source_status_distribution)}",
                    f"- **Reviewer note:** {issue_evidence_credibility.reviewer_note}",
                    "",
                    "**Key limitations:**",
                ]
            )
            lines.extend(_bullet_list(issue_evidence_credibility.key_limitations, "No credibility limitations listed."))
            lines.append("")
        else:
            lines.extend(["- No evidence credibility assessment generated.", ""])

        lines.extend(
            [
                "## Decision Considerations",
                "",
                "- Decision-makers may wish to compare current issue details against the retrieved outcomes before acting.",
                "- Decision-makers may wish to separate recurring historical lessons from case-specific facts.",
                "",
            ]
        )

        lines.extend(["## Current Context", ""])
        if not issue_contexts:
            lines.extend(
                [
                    "- ContextRetriever was skipped or no current-context findings were returned for this route.",
                    "- **Source origin:** Agent Router",
                    "",
                ]
            )
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

        lines.extend(["", "## Mechanisms Detected", ""])
        if issue_mechanisms:
            for mechanism in issue_mechanisms:
                lines.extend(
                    [
                        f"### {mechanism.mechanism_name}",
                        "",
                        f"- **Description:** {mechanism.description}",
                        f"- **Detection reason:** {mechanism.detection_reason}",
                        f"- **Possible observations:** {mechanism.possible_observations}",
                        f"- **Evidence references:** {', '.join(mechanism.evidence_references)}",
                        "",
                    ]
                )
        else:
            lines.append("- No mechanisms detected.")

        lines.extend(["## Competing Interpretations", ""])
        if issue_interpretations:
            for interpretation in issue_interpretations:
                lines.extend(
                    [
                        f"### {interpretation.lens}",
                        "",
                        f"- **Hypothesis:** {interpretation.hypothesis}",
                        f"- **Evidence references:** {', '.join(sorted(set(interpretation.evidence_references)))}",
                        "",
                    ]
                )
        else:
            lines.append("- No competing interpretations generated.")

        lines.extend(["## Multi-Lens Analysis", ""])
        if issue_interpretations:
            for interpretation in issue_interpretations:
                lines.extend([f"### {interpretation.lens}", "", "**Supporting observations:**"])
                lines.extend(_bullet_list(interpretation.supporting_observations, "No supporting observations generated."))
                lines.append("")
                lines.append("**Limitations:**")
                lines.extend(_bullet_list(interpretation.limitations, "No limitations generated."))
                lines.append("")
        else:
            lines.append("- No lens analysis generated.")

        lines.extend(["## Supporting Evidence", ""])
        if issue_assessments:
            for assessment in issue_assessments:
                lines.append(f"### {assessment.lens} ({assessment.confidence_language})")
                lines.extend(_bullet_list(assessment.supporting_evidence, "No supporting evidence listed."))
                lines.append("")
        else:
            lines.append("- No evidence assessment generated.")

        lines.extend(["## Weakening Evidence", ""])
        if issue_assessments:
            for assessment in issue_assessments:
                lines.append(f"### {assessment.lens}")
                lines.extend(_bullet_list(assessment.weakening_evidence, "No weakening evidence listed."))
                lines.append("")
        else:
            lines.append("- No weakening evidence generated.")

        lines.extend(["## Missing Evidence", ""])
        if issue_assessments:
            for assessment in issue_assessments:
                lines.append(f"### {assessment.lens}")
                lines.extend(_bullet_list(assessment.missing_evidence, "No missing evidence listed."))
                lines.append("")
        else:
            lines.append("- No missing evidence generated.")

        lines.extend(["## Historical Response Patterns", ""])
        if issue_response_patterns:
            for pattern in issue_response_patterns:
                lines.extend([f"### {pattern.pattern_name}", "", "**Observed Historical Choices:**"])
                lines.extend(_bullet_list(pattern.observed_historical_choices, "No historical choices listed."))
                lines.append("")
                lines.append("**Observed Outcomes:**")
                lines.extend(_bullet_list(pattern.observed_outcomes, "No observed outcomes listed."))
                lines.append("")
                lines.append("**Business Lessons:**")
                lines.extend(_bullet_list(pattern.business_lessons, "No business lessons listed."))
                lines.append("")
            lines.extend(["## Cross-Domain Lessons", ""])
            for pattern in issue_response_patterns:
                lines.extend(_bullet_list(pattern.cross_domain_lessons, "No cross-domain lessons listed."))
        else:
            lines.append("- No response patterns generated.")

        lines.extend(["", "## Monitoring Considerations", ""])
        lines.append("- Decision-makers may wish to monitor source updates, implementation details, stakeholder responses, and evidence gaps.")
        lines.append("- Decision-makers may wish to monitor whether new evidence strengthens or weakens each interpretation.")

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
                "- V3 uses an Agent Router to select tools before execution.",
                "- Current context retrieval uses local Markdown knowledge-base entries.",
                "- The synthesis uses phrases such as may resemble, shares characteristics with, differs from, and requires monitoring by design.",
                "",
                "### Evidence Trace",
                "",
            ]
        )
        evidence_items = ["Source Document"] + [item.evidence_trace for item in issue_analogues]
        evidence_items += [item.evidence_trace for item in issue_contexts]
        for mechanism in issue_mechanisms:
            evidence_items += mechanism.evidence_references
        for interpretation in issue_interpretations:
            evidence_items += interpretation.evidence_references
        for pattern in issue_response_patterns:
            evidence_items += pattern.evidence_references
        for outcome in issue_historical_outcomes:
            evidence_items += outcome.evidence_references
        for lesson in issue_strategic_lessons:
            evidence_items += lesson.evidence_references
        if agent_route:
            evidence_items.append("Agent Router: deterministic tool selection trace")
            evidence_items.append("Tool Registry: registered deterministic analysis tools")
        if analysis:
            evidence_items += analysis.evidence_trace
        for evidence in sorted(set(evidence_items)):
            lines.append(f"- {evidence}")
        lines.append("")

        if agent_route:
            context_source_line = (
                "- **Context Knowledge Base:** selected current-context findings when the router selected ContextRetriever."
                if issue_contexts
                else "- **Context Knowledge Base:** not used for this route because ContextRetriever was skipped or returned no findings."
            )
            lines.extend(
                [
                    "## Evidence Sources",
                    "",
                    "- **Input Document:** issue fields, scenario keywords, and extracted entities.",
                    "- **Historical Database:** retrieved analogue cases and similarity reasons.",
                    context_source_line,
                    "- **Agent Router:** selected and skipped tool decisions.",
                    "",
                ]
            )
        if issue_strategic_assessment:
            lines.extend(["## Important Limitations", ""])
            lines.extend(_bullet_list(issue_strategic_assessment.important_limitations, "No limitations generated."))
            lines.append("")

    return "\n".join(lines).strip() + "\n"
