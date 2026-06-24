"""Validate V8 current-event context and demo case library artifacts."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO_CASES = [
    "semiconductor_export_controls",
    "industrial_policy_subsidy",
    "geopolitical_escalation_supply_chain",
    "financial_earnings_geopolitical_risk",
    "regulatory_action_digital_markets",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_event_context_module() -> None:
    module_path = ROOT / "src" / "event_context.py"
    require(module_path.exists(), "src/event_context.py missing.")
    source = module_path.read_text(encoding="utf-8")
    for term in ["EventContext", "extract_event_context", "event_type", "context_limitations"]:
        require(term in source, f"event_context.py missing {term}.")


def validate_dashboard_and_readme() -> None:
    index = read("dashboard/index.html")
    app_js = read("dashboard/app.js")
    readme = read("README.md")
    require("Current Event Context" in index, "Dashboard missing Current Event Context section.")
    require("event-context-section" in index, "Dashboard missing event-context-section target.")
    require("renderEventContext" in app_js, "Dashboard JS missing event context renderer.")
    require("docs/demo_case_library.md" in readme, "README missing demo case library link.")
    require(
        "## Event Understanding Layer" in readme or "## Current Event Intelligence Layer" in readme,
        "README missing current-event or event-understanding layer section.",
    )
    version_mentions = len(re.findall(r"\bV\d+(?:\.\d+)?\b", readme))
    require(version_mentions <= 3, "README appears too version-history heavy.")


def validate_demo_inputs() -> None:
    for case_name in DEMO_CASES:
        path = ROOT / "demo_cases" / f"{case_name}.txt"
        require(path.exists(), f"Missing demo input: {path}")
        word_count = len(path.read_text(encoding="utf-8").split())
        require(word_count >= 200, f"Demo input too short: {case_name}")


def validate_demo_outputs() -> None:
    required_files = ["analysis.json", "brief.md", "brief.txt", "agent_trace.json", "metadata.json"]
    for case_name in DEMO_CASES:
        case_dir = ROOT / "demo_case_outputs" / case_name
        require(case_dir.exists(), f"Missing demo output folder: {case_name}")
        for filename in required_files:
            require((case_dir / filename).exists(), f"Missing {filename} for {case_name}.")

        analysis = json.loads((case_dir / "analysis.json").read_text(encoding="utf-8"))
        brief = (case_dir / "brief.md").read_text(encoding="utf-8")
        trace = json.loads((case_dir / "agent_trace.json").read_text(encoding="utf-8"))
        require("event_context" in analysis, f"analysis.json missing event_context for {case_name}.")
        require(analysis["event_context"].get("event_type"), f"event_context missing event_type for {case_name}.")
        require("Current Event Context" in brief, f"brief.md missing Current Event Context for {case_name}.")
        require("Evidence Credibility Note" in brief, f"brief.md missing evidence credibility note for {case_name}.")
        require(
            "Current event context extraction" in trace.get("reasoning_stages", []),
            f"agent_trace missing current event context stage for {case_name}.",
        )


def validate_walkthroughs_and_docs() -> None:
    for case_name in DEMO_CASES:
        path = ROOT / "docs" / "demo_case_walkthroughs" / f"{case_name}.md"
        require(path.exists(), f"Missing walkthrough doc: {case_name}")
        text = path.read_text(encoding="utf-8")
        for heading in [
            "## Input Summary",
            "## Current Event Context",
            "## What the System Detected",
            "## Evidence Credibility Note",
            "## What This Demonstrates in the Portfolio",
        ]:
            require(heading in text, f"{case_name} walkthrough missing {heading}.")

    require((ROOT / "docs" / "demo_case_library.md").exists(), "docs/demo_case_library.md missing.")
    require((ROOT / "docs" / "v80_current_event_layer.md").exists(), "docs/v80_current_event_layer.md missing.")


def main() -> None:
    validate_event_context_module()
    validate_dashboard_and_readme()
    validate_demo_inputs()
    validate_demo_outputs()
    validate_walkthroughs_and_docs()
    print("V8.0 validation passed.")


if __name__ == "__main__":
    main()
