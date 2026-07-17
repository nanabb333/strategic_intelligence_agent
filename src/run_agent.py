"""Compatibility CLI for the current neutral decision-assessment workflow."""

from pathlib import Path

from analysis_service import run_analysis
from document_loader import load_document


def run_agent(input_path: str | Path, output_path: str | Path = "outputs/brief.md", source_url: str = "") -> Path:
    """Run the current deterministic workflow and write its neutral assessment."""
    document_text = load_document(input_path)
    result = run_analysis(
        text=document_text,
        language="en",
        output_mode="analyst",
        question_id="meaning",
        question_text="What pathways and evidence should reviewers compare?",
        source_url=source_url,
        input_mode="file",
        uploaded_filename=Path(input_path).name,
        file_type=Path(input_path).suffix.lstrip(".") or "text",
    )

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(result["brief_markdown"], encoding="utf-8")
    return destination


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the neutral decision assessment workflow.")
    parser.add_argument("input_path", help="Path to a .txt or .md source document.")
    parser.add_argument(
        "--output",
        default="outputs/brief.md",
        help="Path where the generated Markdown brief should be written.",
    )
    parser.add_argument(
        "--source-url",
        default="",
        help="Optional source URL to include as metadata in the generated brief.",
    )
    args = parser.parse_args()

    result_path = run_agent(args.input_path, args.output, source_url=args.source_url)
    print(f"Wrote neutral decision assessment to {result_path}")
