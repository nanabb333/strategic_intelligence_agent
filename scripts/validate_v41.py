"""Validate Strategic Intelligence Agent V4.1 reasoning framework."""

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
from mechanism_detector import detect_mechanisms  # noqa: E402
from historical_retriever import retrieve_historical_analogues  # noqa: E402
from context_retriever import retrieve_current_context  # noqa: E402
from multi_lens_analyzer import analyze_lenses  # noqa: E402
from evidence_assessor import assess_evidence  # noqa: E402
from response_playbook_retriever import retrieve_response_patterns  # noqa: E402
from run_agent import run_agent  # noqa: E402


EXAMPLES = {
    "examples/v4_export_controls_reasoning.md": "outputs/v4_export_controls_reasoning_brief.md",
    "examples/v4_banking_reasoning.md": "outputs/v4_banking_reasoning_brief.md",
    "examples/v4_industrial_policy_reasoning.md": "outputs/v4_industrial_policy_reasoning_brief.md",
    "examples/v4_supply_chain_reasoning.md": "outputs/v4_supply_chain_reasoning_brief.md",
}

FORBIDDEN = ["buy", "sell", "hold", "price target", "expected return", "will happen", "should invest"]


def validate_reasoning_pipeline() -> None:
    for input_file, output_file in EXAMPLES.items():
        text = load_document(ROOT / input_file)
        issues = extract_issues(text)
        classifications = classify_scenarios(issues)
        mechanisms = detect_mechanisms(issues, classifications)
        analogues = retrieve_historical_analogues(issues, classifications)
        contexts = retrieve_current_context(issues, classifications)
        interpretations = analyze_lenses(issues, classifications, mechanisms, analogues, contexts)
        assessments = assess_evidence(interpretations)
        patterns = retrieve_response_patterns(analogues, mechanisms)

        for issue in issues:
            if not mechanisms.get(issue.title):
                raise AssertionError(f"Mechanisms missing for {input_file}")
            if len(interpretations.get(issue.title, [])) < 5:
                raise AssertionError(f"Lens analysis missing for {input_file}")
            if not assessments.get(issue.title):
                raise AssertionError(f"Evidence assessment missing for {input_file}")
            if not patterns.get(issue.title):
                raise AssertionError(f"Response patterns missing for {input_file}")

        output_path = ROOT / output_file
        run_agent(ROOT / input_file, output_path)
        output_text = output_path.read_text(encoding="utf-8")
        required_sections = [
            "## Competing Interpretations",
            "## Multi-Lens Analysis",
            "## Supporting Evidence",
            "## Weakening Evidence",
            "## Missing Evidence",
            "## Historical Response Patterns",
            "## Cross-Domain Lessons",
            "## Monitoring Considerations",
        ]
        for section in required_sections:
            if section not in output_text:
                raise AssertionError(f"{output_file} missing {section}")
        lowered = output_text.lower()
        for phrase in FORBIDDEN:
            if re.search(r"\b" + re.escape(phrase) + r"\b", lowered):
                raise AssertionError(f"Forbidden advice or prediction phrase found in {output_file}: {phrase}")


def main() -> None:
    validate_reasoning_pipeline()
    print("V4.1 validation passed.")


if __name__ == "__main__":
    main()

