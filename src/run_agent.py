"""Run the Strategic Intelligence Agent workflow."""

from pathlib import Path

from agent_router import route_document
from brief_generator import generate_brief
from document_loader import load_document
from evidence_assessor import assess_evidence
from evidence_credibility import assess_evidence_credibility
from event_context import extract_event_context
from mechanism_detector import detect_mechanisms
from multi_lens_analyzer import analyze_lenses
from outcome_retriever import retrieve_historical_outcomes
from response_playbook_retriever import retrieve_response_patterns
from strategic_lessons import generate_strategic_lessons
from tool_registry import build_default_registry


def run_agent(input_path: str | Path, output_path: str | Path = "outputs/brief.md") -> Path:
    """Run the V3 routed agent workflow and write a Markdown brief."""
    document_text = load_document(input_path)
    registry = build_default_registry()
    route = route_document(document_text, registry)

    event_context = extract_event_context(document_text)
    issues = registry["IssueExtractor"].callable(document_text)
    classifications = registry["ScenarioClassifier"].callable(issues)
    analogues = registry["HistoricalRetriever"].callable(issues, classifications)
    contexts = (
        registry["ContextRetriever"].callable(issues, classifications)
        if "ContextRetriever" in route.selected_tools
        else {issue.title: [] for issue in issues}
    )
    analyses = registry["ImplicationAnalyzer"].callable(issues, classifications, analogues, contexts)
    mechanisms = detect_mechanisms(issues, classifications)
    interpretations = analyze_lenses(issues, classifications, mechanisms, analogues, contexts)
    evidence_assessments = assess_evidence(interpretations)
    historical_outcomes = retrieve_historical_outcomes(analogues)
    strategic_lessons = generate_strategic_lessons(historical_outcomes)
    evidence_credibility = assess_evidence_credibility(historical_outcomes, strategic_lessons)
    response_patterns = retrieve_response_patterns(analogues, mechanisms)
    brief = registry["BriefGenerator"].callable(
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
        evidence_credibility=evidence_credibility,
        response_patterns=response_patterns,
        event_context=event_context,
    )

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(brief, encoding="utf-8")
    return destination


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Strategic Intelligence Agent.")
    parser.add_argument("input_path", help="Path to a .txt or .md source document.")
    parser.add_argument(
        "--output",
        default="outputs/brief.md",
        help="Path where the generated Markdown brief should be written.",
    )
    args = parser.parse_args()

    result_path = run_agent(args.input_path, args.output)
    print(f"Wrote executive brief to {result_path}")
