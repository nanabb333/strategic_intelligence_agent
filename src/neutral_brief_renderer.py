"""Render the structured analysis artifact as a rich neutral assessment.

This module formats existing pipeline outputs only. It does not classify the
input, derive new evidence, rank pathways, or select a course of action.
"""

from __future__ import annotations

from typing import Any, Iterable


def render_rich_neutral_assessment(analysis: dict[str, Any]) -> str:
    """Render one canonical structured artifact into detailed Markdown."""
    assessment = _mapping(analysis.get("decision_assessment"))
    lines = ["# Neutral Decision Assessment", ""]

    _add_text_section(
        lines,
        "Decision Question",
        _text(assessment.get("decision_question")) or "The decision question was not specified.",
    )
    _add_text_section(
        lines,
        "Assessment Summary",
        _text(assessment.get("assessment_summary"))
        or "The available material did not establish an assessment summary.",
    )
    _add_section(lines, "Current Event Context", _current_event_context(analysis))
    _add_section(lines, "Evidence Overview", _evidence_overview(analysis))
    _add_section(
        lines,
        "Evidence Credibility and Limitations",
        _evidence_credibility(analysis),
    )
    _add_section(lines, "Mechanisms Detected", _mechanisms(analysis))
    _add_section(
        lines,
        "Historical Analogues and Outcomes",
        _historical_analysis(analysis),
    )
    _add_section(lines, "Similarities and Differences", _similarities(analysis))
    _add_section(lines, "Competing Interpretations", _competing_interpretations(analysis))
    _add_section(lines, "Multi-Lens Analysis", _multi_lens_analysis(analysis))
    _add_section(lines, "Pathways for Review", _pathways(assessment))
    _add_section(
        lines,
        "Pathway Implications and Trade-offs",
        _pathway_implications(assessment),
    )
    _add_section(lines, "Strategic Considerations", _strategic_considerations(analysis))
    _add_section(lines, "Monitoring Considerations", _monitoring(analysis))
    _add_section(lines, "Change Triggers", _change_triggers(assessment))
    _add_section(
        lines,
        "Assumptions, Unknowns and Constraints",
        _assumptions_unknowns_constraints(assessment),
    )
    _add_section(lines, "Reviewer Questions", _reviewer_questions(assessment, analysis))
    _add_section(lines, "Evidence Sufficiency", _evidence_sufficiency(analysis))
    _add_section(lines, "Artifact Completeness", _artifact_completeness(analysis))
    _add_section(lines, "Judgment Boundary", _judgment_boundary(assessment))

    return "\n".join(lines).strip() + "\n"


def _current_event_context(analysis: dict[str, Any]) -> list[str]:
    event = _mapping(analysis.get("event_context"))
    scenario = _mapping(analysis.get("scenario"))
    issue = _mapping(analysis.get("issue"))
    output: list[str] = []
    if event:
        _subheading(output, "Source-derived event frame")
        _field(output, "Event type", event.get("event_type"))
        _field(output, "Event summary", event.get("event_summary"))
        _field(output, "Primary actor", event.get("primary_actor"))
        _field(output, "Secondary actor", event.get("secondary_actor"))
        _field(output, "Affected sectors", _joined(event.get("affected_sectors")))
        _field(output, "Affected regions", _joined(event.get("affected_regions")))
        _field(output, "Policy domain", event.get("policy_domain"))
        _field(output, "Strategic significance", event.get("strategic_significance"))
    if scenario:
        _subheading(output, "Deterministic scenario frame")
        _field(output, "Primary scenario", scenario.get("primary_scenario"))
        _field(output, "Matched source terms", _joined(scenario.get("matched_keywords")))
        _field(output, "Rule-match descriptor", scenario.get("confidence_label"))
        output.append("- This descriptor reports deterministic rule matching; it is not calibrated confidence or a forecast.")
    entity_fields = [
        ("Actors", issue.get("actors")),
        ("Countries or regions", issue.get("countries_or_regions")),
        ("Industries", issue.get("industries")),
        ("Policy terms", issue.get("policy_terms")),
        ("Companies", issue.get("companies")),
    ]
    if any(_values(value) for _, value in entity_fields):
        _subheading(output, "Extracted context")
        for label, value in entity_fields:
            _field(output, label, _joined(value))
    contexts = _records(analysis.get("current_context"))
    if contexts:
        _subheading(output, "Curated current context")
        for context in contexts:
            title = " — ".join(
                value for value in [_text(context.get("industry")), _text(context.get("scenario_type"))] if value
            ) or "Context record"
            output.extend([f"#### {title}", ""])
            _field(output, "Context", context.get("context_summary"))
            _field(output, "Why it matters", context.get("why_it_matters"))
            _field(output, "Stakeholders", context.get("stakeholders"))
            _field(output, "Retrieval reason", context.get("similarity_reason"))
            _field(output, "Source origin", context.get("evidence_trace"))
    return output


def _evidence_overview(analysis: dict[str, Any]) -> list[str]:
    output: list[str] = []
    ledger = _mapping(analysis.get("evidence_ledger"))
    items = _records(ledger.get("items"))
    if items:
        _subheading(output, "Evidence ledger")
        for item in items:
            label = _text(item.get("evidence_id")) or "Evidence item"
            source_type = _text(item.get("source_type"))
            output.extend([f"#### {label}{f' — {source_type}' if source_type else ''}", ""])
            _field(output, "Observation", item.get("observation"))
            _field(output, "Inference", item.get("inference"))
            _field(output, "Claim supported", item.get("claim_supported"))
            _field(output, "Evidence text", item.get("evidence_text"))
            _field(output, "Source status", item.get("source_status"))
            _field(output, "Source identity", item.get("source_identity"))
            _field(output, "Relevance", item.get("relevance"))
            _field(output, "Limitation", item.get("limitations"))
    assessments = _records(analysis.get("evidence"))
    if assessments:
        _subheading(output, "Interpretation-level evidence boundaries")
        for item in assessments:
            lens = _text(item.get("lens")) or "Interpretation"
            output.extend([f"#### {lens}", ""])
            _labeled_bullets(output, "Supporting observations", item.get("supporting_evidence"))
            _labeled_bullets(output, "Weakening evidence", item.get("weakening_evidence"))
            _labeled_bullets(output, "Missing evidence", item.get("missing_evidence"))
    trace = _mapping(analysis.get("tool_routing_trace"))
    if trace:
        _subheading(output, "Deterministic analysis trace")
        _field(output, "Document type", trace.get("document_type"))
        _field(output, "Scenario type", trace.get("scenario_type"))
        _field(output, "Selected tools", _joined(trace.get("selected_tools")))
        _field(output, "Skipped tools", _joined(trace.get("skipped_tools")))
        for step in _records(trace.get("trace")):
            event = _text(step.get("event")) or "Trace step"
            detail = _text(step.get("detail"))
            output.append(f"- **{event}:** {detail}" if detail else f"- {event}")
        for decision in _records(trace.get("reasoning_record")):
            tool = _text(decision.get("tool")) or "Tool"
            choice = _text(decision.get("decision"))
            reason = _text(decision.get("why"))
            contribution = _text(decision.get("expected_contribution"))
            output.append(f"- **{tool}:** {choice}" if choice else f"- **{tool}**")
            if reason:
                output.append(f"  Reason recorded by router: {reason}")
            if contribution:
                output.append(f"  Expected deterministic contribution: {contribution}")
    return output


def _evidence_credibility(analysis: dict[str, Any]) -> list[str]:
    output: list[str] = []
    credibility = _mapping(analysis.get("evidence_credibility"))
    if credibility:
        output.extend(
            [
                "Credibility metadata below reports internal evidence coding and source status only; it is not calibrated confidence.",
                "",
            ]
        )
        _field(output, "Evidence summary", credibility.get("evidence_summary"))
        _field(output, "Source-status distribution", _distribution(credibility.get("source_status_distribution")))
        _field(output, "Reviewer note", credibility.get("reviewer_note"))
        _labeled_bullets(output, "Key credibility limitations", credibility.get("key_limitations"))
    limitations: list[str] = []
    limitations.extend(_values(_mapping(analysis.get("event_context")).get("context_limitations")))
    limitations.extend(_values(_mapping(analysis.get("decision_assessment")).get("limitations")))
    limitations.extend(_values(_mapping(analysis.get("strategic_assessment")).get("important_limitations")))
    for lens in _records(analysis.get("lenses")):
        limitations.extend(_values(lens.get("limitations")))
    _labeled_bullets(output, "Detailed limitations", _unique(limitations))
    return output


def _mechanisms(analysis: dict[str, Any]) -> list[str]:
    output: list[str] = []
    for item in _records(analysis.get("mechanisms")):
        output.extend([f"### {_text(item.get('mechanism_name')) or 'Mechanism'}", ""])
        _field(output, "Description", item.get("description"))
        _field(output, "Detection reason", item.get("detection_reason"))
        _field(output, "Possible observations", item.get("possible_observations"))
        _field(output, "Evidence references", _joined(item.get("evidence_references")))
    return output


def _historical_analysis(analysis: dict[str, Any]) -> list[str]:
    output: list[str] = []
    analogues = _records(analysis.get("analogues"))
    if analogues:
        _subheading(output, "Historical analogues")
        for item in analogues:
            title = _text(item.get("case_title")) or "Historical analogue"
            year = _text(item.get("year"))
            output.extend([f"#### {title}{f' ({year})' if year else ''}", ""])
            _field(output, "Scenario type", item.get("scenario_type"))
            _field(output, "Similarity reason", item.get("similarity_reason"))
            _field(output, "Business relevance", item.get("business_relevance"))
            _field(output, "Geopolitical relevance", item.get("geopolitical_relevance"))
            _field(output, "Caution", item.get("caution_note"))
            _field(output, "Source title", item.get("source_title"))
            _field(output, "Source URL", item.get("source_url"))
            _field(output, "Evidence trace", item.get("evidence_trace"))
    outcomes = _records(analysis.get("historical_outcomes"))
    if outcomes:
        _subheading(output, "Observed historical outcomes")
        for item in outcomes:
            title = _text(item.get("case_name")) or "Historical outcome"
            year = _text(item.get("year"))
            output.extend([f"#### {title}{f' ({year})' if year else ''}", ""])
            _field(output, "Event family", item.get("event_family"))
            _field(output, "Observed outcome", item.get("observed_outcome"))
            _field(output, "Observed strategic response", item.get("strategic_response"))
            _field(output, "Time horizon", item.get("time_horizon"))
            _field(output, "Source status", item.get("source_status"))
            _field(output, "Retrieval reason", item.get("retrieval_reason"))
            _field(output, "Evidence references", _joined(item.get("evidence_references")))
    gaps = _records(_mapping(analysis.get("strategic_assessment")).get("expectation_vs_reality"))
    if gaps:
        _subheading(output, "Recorded expectation-versus-outcome gaps")
        for item in gaps:
            output.extend([f"#### {_text(item.get('event')) or 'Historical record'}", ""])
            _field(output, "Recorded expectation", item.get("consensus_expectation"))
            _field(output, "Observed outcome", item.get("observed_outcome"))
            _field(output, "Expectation gap", item.get("expectation_gap"))
            _field(output, "Case-derived lesson", item.get("strategic_lesson"))
    strategic = _mapping(analysis.get("strategic_assessment"))
    patterns = _records(strategic.get("historical_patterns"))
    if patterns:
        _subheading(output, "Patterns within the local curated cases")
        output.append(
            "Frequencies below describe only the retrieved local case set. They are not real-world probabilities."
        )
        output.append("")
        for item in patterns:
            pattern = _text(item.get("pattern")) or "Historical pattern"
            frequency = _text(item.get("frequency_percent"))
            output.append(f"- **{pattern}:** {frequency}% of the retrieved local cases" if frequency else f"- **{pattern}**")
            _field(output, "Interpretation", item.get("interpretation"))
            _field(output, "Supporting cases", _joined(item.get("supporting_cases")))
    distribution = _records(strategic.get("outcome_distribution"))
    if distribution:
        _subheading(output, "Observed outcome categories in the local case set")
        output.append("These are local case counts, not forecasts or population estimates.")
        output.append("")
        for item in distribution:
            outcome_type = _text(item.get("outcome_type")) or "Outcome category"
            count = _text(item.get("case_count"))
            frequency = _text(item.get("frequency_percent"))
            detail = f"{count} local case(s)" if count else "Local case count unavailable"
            if frequency:
                detail += f"; {frequency}% of the retrieved local set"
            output.append(f"- **{outcome_type}:** {detail}")
            _field(output, "Interpretation", item.get("interpretation"))
    return output


def _similarities(analysis: dict[str, Any]) -> list[str]:
    similarities: list[str] = []
    differences: list[str] = []
    for item in _records(analysis.get("implications")):
        similarities.extend(_values(item.get("observed_similarities")))
        differences.extend(_values(item.get("observed_differences")))
    output: list[str] = []
    _labeled_bullets(output, "Observed similarities", _unique(similarities))
    _labeled_bullets(output, "Observed differences", _unique(differences))
    return output


def _competing_interpretations(analysis: dict[str, Any]) -> list[str]:
    output: list[str] = []
    for item in _records(analysis.get("lenses")):
        output.extend([f"### {_text(item.get('lens')) or 'Interpretation'}", ""])
        _field(output, "Hypothesis", item.get("hypothesis"))
        _field(output, "Evidence references", _joined(item.get("evidence_references")))
    return output


def _multi_lens_analysis(analysis: dict[str, Any]) -> list[str]:
    output: list[str] = []
    for item in _records(analysis.get("lenses")):
        output.extend([f"### {_text(item.get('lens')) or 'Lens'}", ""])
        _labeled_bullets(output, "Supporting observations", item.get("supporting_observations"))
        _labeled_bullets(output, "Limitations", item.get("limitations"))
    return output


def _pathways(assessment: dict[str, Any]) -> list[str]:
    output: list[str] = []
    criteria = _values(assessment.get("comparison_criteria"))
    _labeled_bullets(output, "Comparison criteria", criteria)
    pathways = _records(assessment.get("pathways_for_review"))
    if pathways:
        output.append(
            "Pathways below are deterministic archetypes populated with case-derived references and constraints. "
            "Their order is not a ranking, and template content is not presented as externally validated evidence."
        )
        output.append("")
    for item in pathways:
        output.extend([f"### {_text(item.get('title')) or 'Pathway'}", ""])
        _field(output, "Archetype family", item.get("pathway_family"))
        description = _text(item.get("description"))
        if description:
            output.extend([description, ""])
        supporting = _records(_mapping(item.get("pathway_evidence")).get("supporting"))
        if supporting:
            output.extend(["**Case-derived evidence references**", ""])
            for reference in supporting:
                label = _text(reference.get("title")) or _text(reference.get("evidence_id")) or "Evidence reference"
                url = _text(reference.get("source_url"))
                output.append(f"- {label}{f' — {url}' if url else ''}")
            output.append("")
    return output


def _pathway_implications(assessment: dict[str, Any]) -> list[str]:
    output: list[str] = []
    for item in _records(assessment.get("pathways_for_review")):
        output.extend([f"### {_text(item.get('title')) or 'Pathway'}", ""])
        _field(output, "Reversibility", item.get("reversibility"))
        _field(output, "Timing implications", item.get("timing_implications"))
        _labeled_bullets(output, "Trade-offs", item.get("pathway_tradeoffs"))
        _labeled_bullets(output, "Risk categories", item.get("risks"))
        conditions = _mapping(item.get("pathway_conditions"))
        _labeled_bullets(output, "More supportable when", conditions.get("more_supportable_when"))
        _labeled_bullets(output, "Less supportable when", conditions.get("less_supportable_when"))
        _labeled_bullets(output, "Pathway limitations", item.get("limitations"))
    return output


def _strategic_considerations(analysis: dict[str, Any]) -> list[str]:
    output: list[str] = []
    business: list[str] = []
    operational: list[str] = []
    geopolitical: list[str] = []
    for item in _records(analysis.get("implications")):
        business.extend(_values(item.get("business_considerations")))
        operational.extend(_values(item.get("operational_considerations")))
        geopolitical.extend(_values(item.get("geopolitical_considerations")))
    _labeled_bullets(output, "Business considerations", _unique(business))
    _labeled_bullets(output, "Operational considerations", _unique(operational))
    _labeled_bullets(output, "Geopolitical considerations", _unique(geopolitical))
    lessons = _records(analysis.get("strategic_lessons"))
    if lessons:
        _subheading(output, "Case-derived strategic lessons")
        for item in lessons:
            lesson = _text(item.get("lesson"))
            if lesson:
                output.append(f"- **{lesson}**")
                rationale = _text(item.get("rationale"))
                if rationale:
                    output.append(f"  - Rationale: {rationale}")
                cases = _joined(item.get("supporting_cases"))
                if cases:
                    output.append(f"  - Supporting cases: {cases}")
    patterns = _records(analysis.get("response_playbooks"))
    if patterns:
        _subheading(output, "Observed historical response patterns")
        for item in patterns:
            output.extend([f"#### {_text(item.get('pattern_name')) or 'Response pattern'}", ""])
            _labeled_bullets(output, "Observed historical choices", item.get("observed_historical_choices"))
            _labeled_bullets(output, "Observed outcomes", item.get("observed_outcomes"))
            _labeled_bullets(output, "Business lessons", item.get("business_lessons"))
            _labeled_bullets(output, "Cross-domain lessons", item.get("cross_domain_lessons"))
            _field(output, "Evidence references", _joined(item.get("evidence_references")))
            _field(output, "Source title", item.get("source_title"))
            _field(output, "Source type", item.get("source_type"))
            _field(output, "Source URL", item.get("source_url"))
            _field(output, "Pattern limitation", item.get("confidence_note"))
    return output


def _monitoring(analysis: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for item in _records(analysis.get("current_context")):
        values.extend(_values(item.get("monitoring_considerations")))
        if _text(item.get("monitoring_considerations")):
            values.append(_text(item.get("monitoring_considerations")))
    monitoring = _mapping(_mapping(analysis.get("strategic_assessment")).get("role_based_monitoring"))
    for key in ("investor_view", "corporate_strategy_view", "supply_chain_view", "policy_view"):
        values.extend(_values(monitoring.get(key)))
    values.extend(_values(_mapping(analysis.get("strategic_assessment")).get("strategic_watchlist")))
    return _bullet_lines(_unique(values))


def _change_triggers(assessment: dict[str, Any]) -> list[str]:
    values = _values(assessment.get("change_triggers"))
    for item in _records(assessment.get("pathways_for_review")):
        values.extend(_values(item.get("change_triggers")))
    return _bullet_lines(_unique(values))


def _assumptions_unknowns_constraints(assessment: dict[str, Any]) -> list[str]:
    output: list[str] = []
    assumptions = _values(assessment.get("assumptions"))
    unknowns = _values(assessment.get("unknowns"))
    constraints = _values(assessment.get("constraints"))
    limitations = _values(assessment.get("limitations"))
    for item in _records(assessment.get("pathways_for_review")):
        assumptions.extend(_values(item.get("assumptions")))
        unknowns.extend(_values(item.get("unknowns")))
        constraints.extend(_values(item.get("constraints")))
        limitations.extend(_values(item.get("limitations")))
    _labeled_bullets(output, "Assumptions", _unique(assumptions))
    _labeled_bullets(output, "Unknowns", _unique(unknowns))
    _labeled_bullets(output, "Constraints", _unique(constraints))
    _labeled_bullets(output, "Assessment limitations", _unique(limitations))
    return output


def _reviewer_questions(assessment: dict[str, Any], analysis: dict[str, Any]) -> list[str]:
    values = _values(assessment.get("reviewer_questions"))
    for item in _records(assessment.get("pathways_for_review")):
        values.extend(_values(item.get("reviewer_questions")))
    for item in _records(analysis.get("implications")):
        values.extend(_values(item.get("strategic_questions")))
    return _bullet_lines(_unique(values))


def _evidence_sufficiency(analysis: dict[str, Any]) -> list[str]:
    item = _mapping(analysis.get("evidence_sufficiency"))
    if not item:
        return []
    output: list[str] = []
    tier = _text(item.get("tier")) or "Not assessed"
    output.extend([f"**Tier:** {tier} — Structural assessment only", ""])
    _field(output, "Why this tier", item.get("rationale"))
    _field(output, "Deterministic rule", item.get("rule_explanation"))
    boundary = _text(item.get("interpretation_boundary"))
    if boundary:
        output.extend([boundary, ""])
    _labeled_bullets(output, "Missing or unresolved evidence", item.get("missing_evidence"))
    _labeled_bullets(output, "Sufficiency limitations", item.get("limitations"))
    return output


def _artifact_completeness(analysis: dict[str, Any]) -> list[str]:
    item = _mapping(analysis.get("artifact_completeness"))
    if not item:
        return []
    output: list[str] = []
    _field(output, "Status", item.get("status"))
    passed = item.get("passed_checks")
    total = item.get("total_checks")
    if isinstance(passed, int) and isinstance(total, int):
        output.append(f"- **Structural checks:** {passed} of {total} passed")
    boundary = _text(item.get("interpretation_boundary"))
    if boundary:
        output.extend(["", boundary, ""])
    dimensions = _records(item.get("dimensions"))
    present = [entry for entry in dimensions if bool(entry.get("complete"))]
    missing = [entry for entry in dimensions if not bool(entry.get("complete"))]
    if present:
        _subheading(output, "Passed structural checks")
        for entry in present:
            output.append(f"- **{_text(entry.get('name'))}.** {_text(entry.get('explanation'))}")
    if missing:
        _subheading(output, "Missing structural checks")
        for entry in missing:
            output.append(f"- **{_text(entry.get('name'))}.** {_text(entry.get('explanation'))}")
    elif dimensions:
        _subheading(output, "Missing structural checks")
        output.append("- None.")
    return output


def _judgment_boundary(assessment: dict[str, Any]) -> list[str]:
    boundary = _mapping(assessment.get("judgment_boundary"))
    output = [f"**Selection status:** {_text(assessment.get('selection_status')) or 'No pathway selected'}", ""]
    _field(output, "Owner", boundary.get("owner") or "reviewer")
    statement = _text(boundary.get("statement"))
    if statement:
        output.extend([statement, ""])
    if _text(assessment.get("reviewer_selected_path")) or _text(assessment.get("selection_rationale")):
        output.append("Reviewer-authored selection fields are present in this artifact.")
    else:
        output.append("No reviewer pathway selection or selection rationale has been recorded.")
    return output


def _add_text_section(lines: list[str], title: str, text: str) -> None:
    _add_section(lines, title, [text])


def _add_section(lines: list[str], title: str, body: list[str]) -> None:
    clean = _trim(body)
    if not clean:
        return
    lines.extend([f"## {title}", "", *clean, ""])


def _subheading(lines: list[str], title: str) -> None:
    if lines and lines[-1] != "":
        lines.append("")
    lines.extend([f"### {title}", ""])


def _field(lines: list[str], label: str, value: Any) -> None:
    text = _text(value)
    if text:
        lines.append(f"- **{label}:** {text}")


def _labeled_bullets(lines: list[str], label: str, values: Any) -> None:
    items = _values(values)
    if not items:
        return
    if lines and lines[-1] != "":
        lines.append("")
    lines.extend([f"**{label}**", "", *[f"- {item}" for item in items], ""])


def _bullet_lines(values: Iterable[Any]) -> list[str]:
    return [f"- {item}" for item in _unique(_text(value) for value in values)]


def _mapping(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _records(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [dict(item) for item in value if isinstance(item, dict)]
    return []


def _values(value: Any) -> list[str]:
    if isinstance(value, list):
        return _unique(_text(item) for item in value)
    text = _text(value)
    return [text] if text else []


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (dict, list, tuple, set)):
        return ""
    return str(value).strip()


def _joined(value: Any) -> str:
    return ", ".join(_values(value))


def _distribution(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    return ", ".join(f"{key}: {item}" for key, item in sorted(value.items()))


def _unique(values: Iterable[Any]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = _text(value)
        if text and text not in seen:
            seen.add(text)
            output.append(text)
    return output


def _trim(lines: list[str]) -> list[str]:
    output = list(lines)
    while output and not output[0].strip():
        output.pop(0)
    while output and not output[-1].strip():
        output.pop()
    return output
