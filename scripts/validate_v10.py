"""Validate Strategic Intelligence Agent V1.0 intelligence context layer."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from document_loader import load_document  # noqa: E402
from issue_extractor import extract_issues  # noqa: E402
from scenario_classifier import classify_scenarios  # noqa: E402
from historical_retriever import retrieve_historical_analogues  # noqa: E402
from context_retriever import load_context_entries, retrieve_current_context  # noqa: E402
from run_agent import run_agent  # noqa: E402


EXAMPLE_RUNS = {
    "examples/chips_act_example.md": "outputs/chips_act_brief.md",
    "examples/banking_earnings_example.md": "outputs/banking_earnings_brief.md",
    "examples/red_sea_shipping_example.md": "outputs/red_sea_shipping_brief.md",
}

FORBIDDEN_PHRASES = [
    "buy",
    "sell",
    "hold",
    "price target",
    "expected return",
]


def _run_pipeline(input_path: Path):
    text = load_document(input_path)
    issues = extract_issues(text)
    classifications = classify_scenarios(issues)
    analogues = retrieve_historical_analogues(issues, classifications)
    contexts = retrieve_current_context(issues, classifications)
    return issues, classifications, analogues, contexts


def validate_context_kb() -> None:
    entries = load_context_entries(ROOT / "knowledge_base" / "current_context")
    if len(entries) < 20:
        raise AssertionError(f"Expected at least 20 context entries, found {len(entries)}")
    required = {
        "industry",
        "context_summary",
        "why_it_matters",
        "stakeholders",
        "monitoring_considerations",
    }
    for entry in entries:
        missing = [field for field in required if not entry.get(field)]
        if missing:
            raise AssertionError(f"Context entry {entry.get('entry_id')} missing {missing}")


def validate_retrieval() -> None:
    for input_file in EXAMPLE_RUNS:
        issues, classifications, analogues, contexts = _run_pipeline(ROOT / input_file)
        if not issues or not classifications:
            raise AssertionError(f"Pipeline did not extract/classify {input_file}")
        for issue in issues:
            if not analogues.get(issue.title):
                raise AssertionError(f"No historical analogues returned for {input_file}")
            if not contexts.get(issue.title):
                raise AssertionError(f"No current context returned for {input_file}")
            if not all(item.evidence_trace for item in analogues[issue.title]):
                raise AssertionError(f"Missing analogue evidence trace for {input_file}")
            if not all(item.evidence_trace for item in contexts[issue.title]):
                raise AssertionError(f"Missing context evidence trace for {input_file}")


def validate_outputs() -> None:
    for input_file, output_file in EXAMPLE_RUNS.items():
        output_path = ROOT / output_file
        run_agent(ROOT / input_file, output_path)
        if not output_path.exists():
            raise AssertionError(f"Output was not created: {output_file}")
        text = output_path.read_text(encoding="utf-8")
        if "Evidence Trace" not in text:
            raise AssertionError(f"Evidence trace section missing from {output_file}")
        if "Current Context" not in text:
            raise AssertionError(f"Current context section missing from {output_file}")
        lowered = text.lower()
        for phrase in FORBIDDEN_PHRASES:
            pattern = r"\b" + re.escape(phrase) + r"\b"
            if re.search(pattern, lowered):
                raise AssertionError(f"Forbidden advice phrase found in {output_file}: {phrase}")


def main() -> None:
    validate_context_kb()
    validate_retrieval()
    validate_outputs()
    print("V1.0 validation passed.")


if __name__ == "__main__":
    main()

