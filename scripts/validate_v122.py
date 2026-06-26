"""Validate V12.2 decision workspace refinement."""

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


SAMPLE = (
    "New semiconductor export controls affect advanced chip supply chains and market access. "
    "Equipment suppliers are reviewing licensing requirements, customer eligibility, and compliance documentation. "
    "Executives want to understand similar historical cases, observed outcomes, and what to monitor next."
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def analyze(text: str = SAMPLE, mode: str = "analyst") -> str:
    response = TestClient(app).post(
        "/analyze",
        json={
            "text": text,
            "language": "en",
            "output_mode": mode,
            "question_text": "What are my choices, which is recommended, and what should I do next?",
        },
    )
    require(response.status_code == 200, response.text)
    return response.json()["brief_markdown"]


def validate_decision_workspace_order() -> None:
    brief = analyze()
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
    require(brief.strip().startswith("# Executive Intelligence Brief\n\n## Decision Snapshot"), "Decision Snapshot must be first.")
    positions = [brief.find(section) for section in required_order]
    require(all(position >= 0 for position in positions), "Missing one or more V12.2 sections.")
    require(positions == sorted(positions), "V12.2 sections are not in decision-workspace order.")
    require(brief.find("## Decision Criteria") < brief.find("## Decision Paths"), "Decision Criteria must appear before paths.")
    require(brief.find("## Decision Paths") < brief.find("## Option Ranking"), "Decision Paths must appear before ranking.")
    require(brief.find("## Action Timeline") < brief.find("## Historical Evidence"), "Actions must appear before historical evidence.")
    require(brief.find("## What to Monitor") < brief.find("## Historical Evidence"), "Monitoring must appear before historical evidence.")
    require(brief.count("## Limitations") == 1, "Limitations should appear once.")


def validate_choices_and_ranking() -> None:
    brief = analyze()
    for phrase in [
        "### Option A",
        "### Option B (Recommended)",
        "### Option C",
        "**Pros**",
        "**Cons**",
        "## Option Ranking",
        "**1. Option B",
        "**2. Option A",
        "**3. Option C",
        "**Option B currently ranks first**",
    ]:
        require(phrase in brief, f"Missing visual choice/ranking phrase: {phrase}")


def validate_timeline_and_monitoring() -> None:
    brief = analyze()
    for phrase in [
        "## Action Timeline",
        "### Immediate",
        "### Next 30 Days",
        "### Next Quarter",
        "## What to Monitor",
        "These signals answer: what could change today's recommendation?",
        "customer eligibility",
        "licensing",
        "compliance cost",
    ]:
        require(phrase.lower() in brief.lower(), f"Missing action/monitoring phrase: {phrase}")
    require(brief.find("## Action Timeline") < brief.find("## What to Monitor"), "Actions and monitoring are not separated in the right order.")


def validate_historical_supporting_role() -> None:
    brief = analyze()
    historical = brief[brief.find("## Historical Evidence"):]
    for phrase in ["**Case:**", "**Why it supports the recommendation:**", "**Key limitation:**", "**Lesson:**"]:
        require(phrase in historical, f"Historical evidence missing compact field: {phrase}")
    for long_field in ["**Key difference:**", "**What happened after:**", "**Lesson for this decision:**"]:
        require(long_field not in historical, f"Historical evidence still uses long V12.1 field: {long_field}")


def validate_ui_workspace() -> None:
    index = (ROOT / "dashboard/index.html").read_text(encoding="utf-8")
    styles = (ROOT / "dashboard/styles.css").read_text(encoding="utf-8")
    app_js = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    require('id="brief-section" class="brief-output"' in index, "Brief workspace target missing.")
    for selector in [".decision-card", ".criteria-card", ".choices-card", ".ranking-card", ".action-card", ".monitor-card", ".supporting-card"]:
        require(selector in styles, f"Missing workspace style: {selector}")
    require("recommended-option" in app_js and "briefSectionClass" in app_js, "Dashboard renderer missing decision workspace classes.")
    require("max-height: 520px" not in styles, "Old nested scrollbar remains.")
    require("background: #0f1720" not in styles, "Old markdown textbox remains.")


def validate_beginner_still_plain() -> None:
    beginner = analyze(mode="beginner")
    for heading in ["## Decision Snapshot", "## Your choices", "## Best current path", "## Action Timeline", "## What to watch next"]:
        require(heading in beginner, f"Beginner output missing {heading}.")
    for forbidden in ["Agent Router", "Tool Registry", "Mechanism Layer", "Historical Outcome Engine"]:
        require(forbidden not in beginner, f"Beginner output leaked internal label: {forbidden}.")


def main() -> None:
    validate_decision_workspace_order()
    validate_choices_and_ranking()
    validate_timeline_and_monitoring()
    validate_historical_supporting_role()
    validate_ui_workspace()
    validate_beginner_still_plain()
    print("V12.2 decision workspace validation passed.")


if __name__ == "__main__":
    main()
