"""Pipeline orchestration for analysis runs."""

from __future__ import annotations

from typing import Any

from agent_router import route_document
from agent_trace import build_agent_trace
from analysis_artifact import build_analysis_artifact
from analysis_input import prepare_analysis_input
from analysis_metadata import build_analysis_metadata
from artifact_completeness import check_artifact_completeness
from context_retriever import retrieve_current_context
from decision_assessment import build_neutral_decision_assessment
from decision_pathways import build_decision_pathway_drafts
from decision_readiness import build_decision_readiness_map
from evidence_assessor import assess_evidence
from evidence_credibility import assess_evidence_credibility
from evidence_ledger import build_evidence_ledger
from evidence_sufficiency import assess_evidence_sufficiency
from event_context import extract_event_context
from event_understanding import detect_event_understanding
from historical_retriever import retrieve_historical_analogues
from implication_analyzer import analyze_implications
from issue_extractor import extract_issues
from knowledge_localization import localize_analysis_payload
from localization import localized_question_route
from markdown_utils import markdown_to_text
from mechanism_detector import detect_mechanisms
from multi_lens_analyzer import analyze_lenses
from neutral_brief_renderer import render_rich_neutral_assessment
from output_adapter import adapt_output
from outcome_retriever import retrieve_historical_outcomes
from pathway_comparison import build_pathway_comparison_matrix
from question_router import route_question
from response_playbook_retriever import retrieve_response_patterns
from run_storage import create_run_dir, download_links, write_json
from scenario_classifier import classify_scenarios
from strategic_assessment import generate_strategic_assessments
from strategic_lessons import generate_strategic_lessons
from tool_registry import build_default_registry


def execute_analysis_pipeline(
    *,
    text: str,
    language: str,
    output_mode: str,
    question_id: str,
    question_text: str,
    source_url: str,
    input_mode: str,
    uploaded_filename: str,
    file_type: str,
    project_id: str = "",
    project_question_id: str = "",
    evidence_bundle: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Execute the ordered analysis workflow and persist artifacts."""
    prepared_input = prepare_analysis_input(
        text=text,
        source_url=source_url,
        question_text=question_text,
    )
    text = prepared_input["text"]
    source_url = prepared_input["source_url"]
    analysis_text = prepared_input["analysis_text"]

    run_id, run_dir = create_run_dir()

    registry = build_default_registry()
    route = route_document(analysis_text, registry)
    question_route = route_question(question_text)
    event_context = extract_event_context(analysis_text)
    event_understanding = detect_event_understanding(analysis_text, question_text)
    issues = extract_issues(analysis_text)
    classifications = classify_scenarios(issues)
    analogues = retrieve_historical_analogues(
        issues,
        classifications,
        event_understanding=event_understanding,
    )
    contexts = (
        retrieve_current_context(issues, classifications)
        if "ContextRetriever" in route.selected_tools
        else {issue.title: [] for issue in issues}
    )
    analyses = analyze_implications(issues, classifications, analogues, contexts)
    mechanisms = detect_mechanisms(issues, classifications)
    interpretations = analyze_lenses(issues, classifications, mechanisms, analogues, contexts)
    evidence_assessments = assess_evidence(interpretations)
    historical_outcomes = retrieve_historical_outcomes(analogues)
    strategic_lessons = generate_strategic_lessons(historical_outcomes)
    strategic_assessments = generate_strategic_assessments(
        issues,
        classifications,
        historical_outcomes,
        event_understanding=event_understanding,
    )
    evidence_credibility = assess_evidence_credibility(historical_outcomes, strategic_lessons)
    response_patterns = retrieve_response_patterns(analogues, mechanisms)
    primary_issue = issues[0] if issues else None
    primary_title = primary_issue.title if primary_issue else "Untitled issue"
    primary_classification = classifications[0] if classifications else None
    evidence_bundle = evidence_bundle or []
    evidence_bundle_ids = [
        str(item.get("evidence_id"))
        for item in evidence_bundle
        if item.get("evidence_id")
    ]
    evidence_ledger = build_evidence_ledger(
        issue=primary_issue,
        source_url=source_url,
        analogues=analogues.get(primary_title, []),
        mechanisms=mechanisms.get(primary_title, []),
        evidence_assessments=evidence_assessments.get(primary_title, []),
        historical_outcomes=historical_outcomes.get(primary_title, []),
        contexts=contexts.get(primary_title, []),
        project_evidence=evidence_bundle,
    )
    readiness_evidence = _readiness_evidence(evidence_bundle, evidence_ledger)
    readiness_map = build_decision_readiness_map(
        decision_question=question_text,
        decision_context=text[:4000],
        evidence_items=readiness_evidence,
    )
    pathway_draft_set = build_decision_pathway_drafts(
        decision_question=question_text,
        decision_context=text[:4000],
        readiness_map=readiness_map,
        accepted_evidence_refs=_accepted_evidence_refs(readiness_evidence),
    )
    pathway_comparison = build_pathway_comparison_matrix(
        decision_question=question_text,
        pathway_draft_set=pathway_draft_set,
        readiness_map=readiness_map,
        domain_evaluation=readiness_map.get("domain_evaluation", {}),
    )
    decision_assessment = build_neutral_decision_assessment(
        assessment_summary=_assessment_summary(primary_issue, primary_classification),
        pathway_draft_set=pathway_draft_set,
        comparison_matrix=pathway_comparison,
    )
    evidence_sufficiency = assess_evidence_sufficiency(decision_assessment, evidence_ledger)
    artifact_completeness = check_artifact_completeness(
        assessment=decision_assessment,
        evidence_ledger=evidence_ledger,
        evidence_sufficiency=evidence_sufficiency,
    )

    metadata = build_analysis_metadata(
        run_id=run_id,
        language=language,
        output_mode=output_mode,
        question_id=question_id,
        question_route=question_route,
        source_url=source_url,
        input_mode=input_mode,
        uploaded_filename=uploaded_filename,
        file_type=file_type,
        project_id=project_id,
        project_question_id=project_question_id,
        evidence_ids=evidence_bundle_ids,
    )
    analysis = build_analysis_artifact(
        issues=issues,
        classifications=classifications,
        analogues=analogues,
        contexts=contexts,
        analyses=analyses,
        mechanisms=mechanisms,
        interpretations=interpretations,
        evidence_assessments=evidence_assessments,
        historical_outcomes=historical_outcomes,
        strategic_lessons=strategic_lessons,
        strategic_assessments=strategic_assessments,
        evidence_credibility=evidence_credibility,
        response_patterns=response_patterns,
        event_context=event_context,
        event_understanding=event_understanding,
        question_route=question_route,
        localized_question_route=localized_question_route(question_route, language),
        source_url=source_url,
        input_mode=input_mode,
        uploaded_filename=uploaded_filename,
        file_type=file_type,
        route=route,
        metadata=metadata,
        decision_assessment=decision_assessment,
        decision_readiness=readiness_map,
        decision_pathways=pathway_draft_set,
        pathway_comparison=pathway_comparison,
        evidence_ledger=evidence_ledger,
        evidence_sufficiency=evidence_sufficiency,
        artifact_completeness=artifact_completeness,
        evidence_bundle=evidence_bundle,
    )
    analysis = localize_analysis_payload(analysis, language)
    base_brief = render_rich_neutral_assessment(analysis)
    brief_markdown = adapt_output(base_brief, mode=output_mode, language=language)
    brief_text = markdown_to_text(brief_markdown)
    agent_trace = build_agent_trace(route)

    (run_dir / "input.txt").write_text(text, encoding="utf-8")
    write_json(run_dir / "analysis.json", analysis)
    (run_dir / "brief.md").write_text(brief_markdown, encoding="utf-8")
    (run_dir / "brief.txt").write_text(brief_text, encoding="utf-8")
    write_json(run_dir / "agent_trace.json", agent_trace)
    write_json(run_dir / "metadata.json", metadata)

    return {
        "run_id": run_id,
        "metadata": metadata,
        "analysis": analysis,
        "brief_markdown": brief_markdown,
        "brief_text": brief_text,
        "downloads": download_links(run_id),
    }


def _readiness_evidence(evidence_bundle: list[dict[str, Any]], evidence_ledger: Any) -> list[dict[str, Any]]:
    """Normalize current evidence for neutral pathway generation."""
    if evidence_bundle:
        return [dict(item) for item in evidence_bundle]
    return [
        {
            "evidence_id": item.evidence_id,
            "title": item.observation or item.claim_supported,
            "source_type": item.source_type,
            "source_name": item.source_type,
            "source_url": "",
            "excerpt": item.evidence_text,
            "summary": item.evidence_text,
            "status": "User Provided" if item.source_type.startswith("User-provided") else "Retrieved",
        }
        for item in evidence_ledger.items
    ]


def _accepted_evidence_refs(evidence_items: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "evidence_id": str(item.get("evidence_id") or ""),
            "title": str(item.get("title") or "Evidence item"),
            "source_url": str(item.get("source_url") or ""),
        }
        for item in evidence_items
        if item.get("evidence_id")
    ]


def _assessment_summary(issue: Any | None, classification: Any | None) -> str:
    if issue is None:
        return "The supplied material did not produce a structured issue; reviewer clarification is required."
    scenario = getattr(classification, "primary_scenario", "") if classification else ""
    summary = getattr(issue, "core_issue", "") or getattr(issue, "summary", "") or getattr(issue, "title", "")
    suffix = f" The deterministic scenario frame is {scenario}." if scenario else ""
    return f"{summary}{suffix}".strip()
