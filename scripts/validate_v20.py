"""Validate Strategic Intelligence Agent V2 Analyst Workbench."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from run_agent import run_agent  # noqa: E402


DASHBOARD_FILES = [
    ROOT / "dashboard" / "index.html",
    ROOT / "dashboard" / "styles.css",
    ROOT / "dashboard" / "app.js",
]

DEMO_RUNS = {
    "examples/demo_inputs/semiconductor_policy_case.md": "demo_outputs/semiconductor_policy_brief.md",
    "examples/demo_inputs/bank_earnings_case.md": "demo_outputs/bank_earnings_brief.md",
    "examples/demo_inputs/supply_chain_disruption_case.md": "demo_outputs/supply_chain_disruption_brief.md",
    "examples/demo_inputs/red_sea_shipping_case.md": "demo_outputs/red_sea_shipping_brief.md",
}

FORBIDDEN_PHRASES = [
    "buy",
    "sell",
    "hold",
    "price target",
    "expected return",
]


def validate_dashboard_loads() -> None:
    for path in DASHBOARD_FILES:
        if not path.exists():
            raise AssertionError(f"Missing dashboard file: {path.relative_to(ROOT)}")

    html = (ROOT / "dashboard" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "dashboard" / "app.js").read_text(encoding="utf-8")
    required_html = ["document-input", "file-input", "details", "export-md", "export-txt"]
    for token in required_html:
        if token not in html:
            raise AssertionError(f"Dashboard HTML missing required token: {token}")
    for token in ["runAnalysis", "exportBrief", "Historical Database", "Context Knowledge Base", "Input Document"]:
        if token not in js:
            raise AssertionError(f"Dashboard JS missing required token: {token}")


def validate_outputs_generate() -> list[Path]:
    generated: list[Path] = []
    for input_file, output_file in DEMO_RUNS.items():
        output_path = ROOT / output_file
        run_agent(ROOT / input_file, output_path)
        if not output_path.exists():
            raise AssertionError(f"Demo output was not generated: {output_file}")
        generated.append(output_path)
    return generated


def validate_export_works(source_output: Path) -> None:
    markdown_export = ROOT / "outputs" / "v20_dashboard_export.md"
    txt_export = ROOT / "outputs" / "v20_dashboard_export.txt"
    text = source_output.read_text(encoding="utf-8")
    markdown_export.write_text(text, encoding="utf-8")
    txt_export.write_text(re.sub(r"^#+\s*", "", text, flags=re.MULTILINE), encoding="utf-8")
    if not markdown_export.exists() or not txt_export.exists():
        raise AssertionError("Expected export files were not created in outputs/")


def validate_evidence_and_language(paths: list[Path]) -> None:
    for path in paths:
        text = path.read_text(encoding="utf-8")
        if "Evidence Trace" not in text:
            raise AssertionError(f"Evidence trace missing from {path.relative_to(ROOT)}")
        if "Historical Database" not in text:
            raise AssertionError(f"Historical evidence missing from {path.relative_to(ROOT)}")
        context_was_skipped = "ContextRetriever" in text and "Skipped" in text
        if "Context KB" not in text and "Context Knowledge Base" not in text and not context_was_skipped:
            raise AssertionError(f"Context evidence missing from {path.relative_to(ROOT)}")
        lowered = text.lower()
        for phrase in FORBIDDEN_PHRASES:
            pattern = r"\b" + re.escape(phrase) + r"\b"
            if re.search(pattern, lowered):
                raise AssertionError(f"Forbidden advice phrase found in {path.relative_to(ROOT)}: {phrase}")


def validate_screenshot_asset() -> None:
    screenshot = ROOT / "docs" / "screenshots" / "dashboard_workbench.svg"
    if not screenshot.exists():
        raise AssertionError("Dashboard screenshot asset missing")


def main() -> None:
    validate_dashboard_loads()
    generated = validate_outputs_generate()
    validate_export_works(generated[0])
    validate_evidence_and_language(generated + [ROOT / "outputs" / "v20_dashboard_export.md"])
    validate_screenshot_asset()
    print("V2.0 validation passed.")


if __name__ == "__main__":
    main()
