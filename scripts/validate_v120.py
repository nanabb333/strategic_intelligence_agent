"""Validate V12 product rebuild sprint behavior."""

from __future__ import annotations

from pathlib import Path
import sys

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402
from event_understanding import detect_event_understanding  # noqa: E402


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def analyze(text: str, mode: str = "analyst") -> dict:
    client = TestClient(app)
    response = client.post(
        "/analyze",
        json={
            "text": text,
            "language": "en",
            "output_mode": mode,
            "question_text": "What happened, which similar cases matter, and what should I monitor next?",
        },
    )
    require(response.status_code == 200, response.text)
    return response.json()


def validate_dashboard_rebuild() -> None:
    index = read("dashboard/index.html")
    app_js = read("dashboard/app.js")
    require('id="assistant-input"' in index, "Dashboard missing single assistant input.")
    require("What should I monitor over the next 90 days?" in index, "Assistant placeholder missing monitor example.")
    require("input-mode-tabs" not in index, "Legacy input-mode tabs remain visible.")
    require('id="question-input"' not in index, "Legacy separate question box remains.")
    require('id="document-input"' not in index, "Legacy separate document box remains.")
    require("parseAssistantInput" in app_js, "Assistant input parser missing.")
    require("assistant_url" in app_js, "URL-only assistant flow missing.")


def validate_event_understanding() -> None:
    layoffs = detect_event_understanding("Intel announced layoffs and workforce reductions after margin pressure.")
    export_controls = detect_event_understanding("New semiconductor export controls affect advanced chip licensing.")
    bank_product = detect_event_understanding("A bank is promoting a high-yield product to retail customers.")
    require(layoffs.event_family == "Corporate Restructuring", "Layoff event did not map to Corporate Restructuring.")
    require("Export Controls" not in layoffs.relevant_families, "Layoff guardrail should not compare directly with export controls.")
    require(export_controls.event_family == "Trade Restriction", "Export-control event did not map to Trade Restriction.")
    require(bank_product.event_family == "Financial Product Risk", "Bank product event did not map to Financial Product Risk.")


def validate_output_shape() -> None:
    payload = analyze(
        "New semiconductor export controls affect advanced chip supply chains, equipment licensing, customer eligibility, and market access."
    )
    brief = payload["brief_markdown"]
    analysis = payload["analysis"]
    required_order = [
        "## Decision Snapshot",
        "## Decision Question",
        "## Decision Criteria",
        "## Decision Paths",
        "## Option Ranking",
        "## Option Comparison",
        "## Preferred Path",
        "## Why This Reasoning Holds",
        "## Action Timeline",
        "## What to Monitor",
        "## Historical Evidence",
        "## Limitations",
    ]
    for section in required_order:
        require(section in brief, f"Analyst brief missing decision-first section: {section}.")
    positions = [brief.find(section) for section in required_order]
    require(positions == sorted(positions), "Decision-first sections are not in required order.")
    for phrase in [
        "**Current Position:**",
        "**Confidence:**",
        "**Why:**",
        "**Next 30-90 Days:**",
        "### Option A",
        "### Option B (Recommended)",
        "### Option C",
        "| Option | Risk Reduction | Opportunity Cost | Execution Difficulty | Reversibility | Robustness | Information Value |",
        "**Option B currently ranks first**",
        "## Market Expectations vs Actual Outcomes",
        "### Investor",
        "### Corporate Strategy",
        "### Supply Chain",
        "### Policy",
    ]:
        require(phrase in brief, f"Analyst brief missing V12 phrase: {phrase}.")
    require(brief.find("## Decision Paths") < brief.find("## Historical Evidence"), "Options must be defined before historical cases.")
    require(brief.find("## Action Timeline") < brief.find("## Historical Evidence"), "Actions must appear before historical evidence.")
    require(brief.count("## Limitations") == 1, "Limitations should appear once.")
    for internal in ["## Mechanisms", "## Agent Execution Trace", "Political Economy"]:
        require(internal not in brief, f"Default brief leaked internal framework section: {internal}.")
    require("event_understanding" in analysis, "analysis.json missing event_understanding.")
    require(analysis["event_understanding"]["event_family"] == "Trade Restriction", "Artifact event family is wrong.")
    require("Event-family understanding" in analysis["agent_trace"]["reasoning_stages"], "Trace missing event-family stage.")


def validate_beginner_shape() -> None:
    beginner = analyze(
        "A logistics disruption is affecting Red Sea shipping routes, insurance terms, transit time, and supplier delivery planning.",
        mode="beginner",
    )["brief_markdown"]
    required_sections = [
        "## Decision Snapshot",
        "## What this means",
        "## Why it matters",
        "## Your choices",
        "## Best current path",
        "## What to watch next",
        "## What could change this answer",
        "## Limitations",
    ]
    for section in required_sections:
        require(section in beginner, f"Beginner output missing section: {section}.")
    for forbidden in ["Mechanism", "Framework", "Agent Router", "Execution Trace", "Political Economy"]:
        require(forbidden not in beginner, f"Beginner output leaked internal term: {forbidden}.")
    require(beginner.count("## Limitations") == 1, "Beginner limitations section should appear once.")


def validate_docs_and_demos() -> None:
    readme = read("README.md")
    for phrase in [
        "Download -> Open App -> Ask Question",
        "Developer Setup",
        "Normal User Vision",
        "Strategic Intelligence Assistant",
    ]:
        require(phrase in readme, f"README missing V12 positioning phrase: {phrase}.")
    screenshot = ROOT / "docs" / "screenshots" / "v12_assistant_workbench.svg"
    require(screenshot.exists(), "V12 assistant screenshot missing.")
    demo_dir = ROOT / "demo_outputs" / "v12_rebuild"
    files = sorted(demo_dir.glob("*.md"))
    require(len(files) >= 5, f"Expected at least 5 V12 demo outputs, found {len(files)}.")
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in ["What happened", "Why it matters", "Market Expectations", "What To Watch Next"]:
            require(phrase in text, f"{path.name} missing {phrase}.")


def main() -> None:
    validate_dashboard_rebuild()
    validate_event_understanding()
    validate_output_shape()
    validate_beginner_shape()
    validate_docs_and_demos()
    print("V12 product rebuild validation passed.")


if __name__ == "__main__":
    main()
