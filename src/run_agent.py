"""Run the Strategic Intelligence Agent workflow."""

from pathlib import Path

from agent_router import route_document
from brief_generator import generate_brief
from document_loader import load_document
from tool_registry import build_default_registry


def run_agent(input_path: str | Path, output_path: str | Path = "outputs/brief.md") -> Path:
    """Run the V3 routed agent workflow and write a Markdown brief."""
    document_text = load_document(input_path)
    registry = build_default_registry()
    route = route_document(document_text, registry)

    issues = registry["IssueExtractor"].callable(document_text)
    classifications = registry["ScenarioClassifier"].callable(issues)
    analogues = registry["HistoricalRetriever"].callable(issues, classifications)
    contexts = (
        registry["ContextRetriever"].callable(issues, classifications)
        if "ContextRetriever" in route.selected_tools
        else {issue.title: [] for issue in issues}
    )
    analyses = registry["ImplicationAnalyzer"].callable(issues, classifications, analogues, contexts)
    brief = registry["BriefGenerator"].callable(
        issues,
        classifications,
        analogues,
        contexts,
        analyses,
        agent_route=route,
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
