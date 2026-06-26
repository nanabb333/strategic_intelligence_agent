"""Pipeline orchestration for analysis runs."""

from __future__ import annotations

from typing import Any

from agent_router import route_document
from agent_trace import build_agent_trace
from analysis_artifact import build_analysis_artifact
from analysis_input import prepare_analysis_input
from analysis_metadata import build_analysis_metadata
from brief_generator import generate_brief
from context_retriever import retrieve_current_context
from evidence_assessor import assess_evidence
from evidence_credibility import assess_evidence_credibility
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
from output_adapter import adapt_output
from outcome_retriever import retrieve_historical_outcomes
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
    base_brief = generate_brief(
        issues,
        classifications,
        analogues,
        contexts,
        analyses,
        agent_route=route,
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
        source_url=source_url,
    )
    brief_markdown = adapt_output(base_brief, mode=output_mode, language=language)
    brief_text = markdown_to_text(brief_markdown)

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
    )
    analysis = localize_analysis_payload(analysis, language)
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
