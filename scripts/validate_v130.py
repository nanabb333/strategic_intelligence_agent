"""Validate V13 reasoning transparency."""

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


def analyze(mode: str = "analyst") -> str:
    response = TestClient(app).post(
        "/analyze",
        json={
            "text": SAMPLE,
            "language": "en",
            "output_mode": mode,
            "question_text": "Explain why this recommendation is preferred and what would change it.",
        },
    )
    require(response.status_code == 200, response.text)
    return response.json()["brief_markdown"]


def validate_transparency_sections() -> None:
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
        "## Assumptions",
        "## Trade-offs",
        "## What Could Change This Recommendation",
        "## Action Timeline",
        "## What to Monitor",
        "## Historical Evidence",
        "## Limitations",
    ]
    positions = [brief.find(section) for section in required_order]
    require(all(position >= 0 for position in positions), "Missing V13 transparency section.")
    require(positions == sorted(positions), "V13 sections are not in decision-first transparency order.")


def validate_recommendation_explains_alternatives() -> None:
    brief = analyze()
    preferred = brief[brief.find("## Preferred Path"):brief.find("## Why This Reasoning Holds")]
    for phrase in [
        "Why Option B ranks first",
        "Why Option A does not rank first",
        "Why Option C does not rank first",
        "What would change the ranking",
    ]:
        require(phrase in preferred, f"Preferred Path missing alternative explanation: {phrase}")


def validate_assumptions_tradeoffs_change_triggers() -> None:
    brief = analyze()
    for phrase in [
        "## Assumptions",
        "The input text is directionally accurate",
        "No immediate evidence",
        "## Trade-offs",
        "Benefits gained",
        "Costs accepted",
        "Opportunities sacrificed",
        "## What Could Change This Recommendation",
        "Option A becomes more reasonable",
        "Option C becomes more reasonable",
    ]:
        require(phrase in brief, f"Missing reasoning transparency phrase: {phrase}")


def validate_historical_evidence_supports() -> None:
    brief = analyze()
    historical = brief[brief.find("## Historical Evidence"):brief.find("## Market Expectations")]
    for phrase in [
        "**Case:**",
        "**Why it supports the recommendation:**",
        "**Key limitation:**",
        "**Decision lesson:**",
    ]:
        require(phrase in historical, f"Historical evidence missing support field: {phrase}")
    require("**What happened after:**" not in historical, "Historical evidence remains too descriptive.")
    require(brief.find("## Historical Evidence") > brief.find("## What Could Change This Recommendation"), "Historical evidence should remain secondary.")


def validate_ui_cards() -> None:
    styles = (ROOT / "dashboard/styles.css").read_text(encoding="utf-8")
    app_js = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    for selector in [".assumption-card", ".tradeoff-card", ".change-card", ".supporting-card"]:
        require(selector in styles, f"Missing transparency card style: {selector}")
    for title in ["Assumptions", "Trade-offs", "What Could Change This Recommendation"]:
        require(title in app_js, f"Dashboard class mapping missing {title}")


def validate_beginner_transparency() -> None:
    beginner = analyze(mode="beginner")
    for heading in [
        "## What could change this answer",
        "## Assumptions behind this answer",
        "## Trade-offs",
    ]:
        require(heading in beginner, f"Beginner output missing transparency heading: {heading}")
    for forbidden in ["Agent Router", "Tool Registry", "Mechanism Layer", "Historical Outcome Engine"]:
        require(forbidden not in beginner, f"Beginner output leaked internal label: {forbidden}")


def main() -> None:
    validate_transparency_sections()
    validate_recommendation_explains_alternatives()
    validate_assumptions_tradeoffs_change_triggers()
    validate_historical_evidence_supports()
    validate_ui_cards()
    validate_beginner_transparency()
    print("V13 reasoning transparency validation passed.")


if __name__ == "__main__":
    main()
