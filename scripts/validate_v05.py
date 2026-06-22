"""Validate Strategic Intelligence Agent V0.5 deterministic workflow."""

import csv
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from run_agent import run_agent  # noqa: E402


REQUIRED_COLUMNS = {
    "case_id",
    "case_title",
    "year",
    "region",
    "scenario_type",
    "actors",
    "industries",
    "core_issue",
    "business_relevance",
    "geopolitical_relevance",
    "market_relevance",
    "why_it_matters",
    "source_note",
}

EXAMPLE_RUNS = {
    "examples/export_controls_example.md": "outputs/export_controls_brief.md",
    "examples/earnings_disclosure_example.md": "outputs/earnings_disclosure_brief.md",
    "examples/supply_chain_example.md": "outputs/supply_chain_brief.md",
}

FORBIDDEN_PHRASES = [
    "buy",
    "sell",
    "hold",
    "price target",
    "expected return",
]


def validate_knowledge_base() -> None:
    path = ROOT / "knowledge_base" / "historical_analogues.csv"
    if not path.exists():
        raise AssertionError("knowledge_base/historical_analogues.csv does not exist")

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise AssertionError(f"Missing required columns: {sorted(missing)}")
        rows = list(reader)
        if len(rows) < 10:
            raise AssertionError("Expected at least 10 historical analogue rows")


def validate_examples() -> None:
    for input_path, output_path in EXAMPLE_RUNS.items():
        source = ROOT / input_path
        destination = ROOT / output_path
        if not source.exists():
            raise AssertionError(f"Missing example input: {input_path}")
        run_agent(source, destination)
        if not destination.exists():
            raise AssertionError(f"Expected output was not created: {output_path}")


def validate_output_language() -> None:
    for output_path in EXAMPLE_RUNS.values():
        text = (ROOT / output_path).read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_PHRASES:
            pattern = r"\b" + re.escape(phrase) + r"\b"
            if re.search(pattern, text):
                raise AssertionError(f"Forbidden advice phrase found in {output_path}: {phrase}")


def main() -> None:
    validate_knowledge_base()
    validate_examples()
    validate_output_language()
    print("V0.5 validation passed.")


if __name__ == "__main__":
    main()
