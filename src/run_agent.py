"""Run the Strategic Intelligence Agent workflow."""

from pathlib import Path

from brief_generator import generate_brief
from document_loader import load_document
from historical_retriever import retrieve_historical_analogues
from implication_analyzer import analyze_implications
from issue_extractor import extract_issues
from scenario_classifier import classify_scenarios


def run_agent(input_path: str | Path, output_path: str | Path = "outputs/brief.md") -> Path:
    """Run the full V0.5 workflow and write a Markdown brief."""
    document_text = load_document(input_path)
    issues = extract_issues(document_text)
    classifications = classify_scenarios(issues)
    analogues = retrieve_historical_analogues(issues, classifications)
    analyses = analyze_implications(issues, classifications, analogues)
    brief = generate_brief(issues, classifications, analogues, analyses)

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
