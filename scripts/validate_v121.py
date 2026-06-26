"""Validate V12.1 decision-first output refinement."""

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


SCENARIOS = {
    "semiconductor_export_controls": "New semiconductor export controls affect advanced chip supply chains and market access. Equipment suppliers are reviewing licensing requirements, customer eligibility, and compliance documentation. Executives want to understand similar historical cases, observed outcomes, and what to monitor next.",
    "usd_insurance_products": "A bank relationship manager is promoting a USD-denominated insurance savings product to clients seeking yield. The client wants to compare the product with USD deposits, Treasuries, and bond ETFs, and understand surrender costs, FX exposure, liquidity limits, and suitability risks.",
    "taiwan_family_asset_allocation": "A Taiwan-based family holds most assets in Taiwan real estate and local equities while future education and business cash flows may require USD liquidity. The family is considering whether to diversify toward US and Singapore assets without selling existing holdings immediately.",
    "earnings_geopolitical_pressure": "A public company reported weaker earnings because sanctions compliance costs, regional demand uncertainty, and shipping expenses reduced margins. Management said it is reviewing customer exposure, compliance staffing, and guidance assumptions.",
    "supply_chain_disruption": "A Red Sea shipping disruption is increasing transit times, insurance costs, and supplier delivery uncertainty. Management wants to understand operational exposure, customer communication needs, and which indicators matter over the next quarter.",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def analyze(text: str, mode: str = "analyst") -> str:
    response = TestClient(app).post(
        "/analyze",
        json={
            "text": text,
            "language": "en",
            "output_mode": mode,
            "question_text": "What is the current recommendation and what should I do next?",
        },
    )
    require(response.status_code == 200, response.text)
    return response.json()["brief_markdown"]


def validate_decision_order() -> None:
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
    for name, text in SCENARIOS.items():
        brief = analyze(text)
        require(brief.strip().startswith("# Executive Intelligence Brief\n\n## Decision Snapshot"), f"{name}: Decision Snapshot is not first.")
        positions = [brief.find(section) for section in required_order]
        require(all(position >= 0 for position in positions), f"{name}: missing required decision-first section.")
        require(positions == sorted(positions), f"{name}: sections are not in decision-first order.")
        require(brief.find("## Decision Criteria") < brief.find("## Decision Paths"), f"{name}: criteria must appear before paths.")
        require(brief.find("## Decision Paths") < brief.find("## Option Comparison"), f"{name}: paths must appear before comparison.")
        require(brief.find("## Decision Paths") < brief.find("## Option Ranking"), f"{name}: paths must appear before ranking.")
        require(brief.find("## Action Timeline") < brief.find("## Historical Evidence"), f"{name}: actions must appear before historical evidence.")
        require(brief.find("## Preferred Path") < brief.find("## Historical Evidence"), f"{name}: recommendation must appear before historical evidence.")
        require(brief.count("## Limitations") == 1, f"{name}: limitations should appear once.")


def validate_content_specificity() -> None:
    expectations = {
        "semiconductor_export_controls": ["customer eligibility", "licensing", "supplier exposure", "compliance cost"],
        "usd_insurance_products": ["USD deposits", "Treasuries", "bond ETFs", "surrender", "FX exposure"],
        "taiwan_family_asset_allocation": ["Taiwan / US / Singapore", "future cash flow", "USD cash needs", "quarterly review"],
        "earnings_geopolitical_pressure": ["guidance", "compliance staffing", "regional", "shipping cost"],
        "supply_chain_disruption": ["transit-time", "freight and insurance", "inventory coverage", "customer communication"],
    }
    for name, text in SCENARIOS.items():
        brief = analyze(text)
        for phrase in expectations[name]:
            require(phrase.lower() in brief.lower(), f"{name}: missing concrete phrase '{phrase}'.")
        require("Option B currently ranks first" in brief, f"{name}: preferred path does not explicitly rank Option B.")
        require("What would make it wrong" in brief, f"{name}: missing evidence that would change the answer.")


def validate_beginner_mode() -> None:
    beginner = analyze(SCENARIOS["usd_insurance_products"], mode="beginner")
    for heading in [
        "## Decision Snapshot",
        "## What this means",
        "## Why it matters",
        "## Your choices",
        "## Best current path",
        "## What to watch next",
        "## What could change this answer",
        "## Action Timeline",
        "## Limitations",
    ]:
        require(heading in beginner, f"Beginner output missing {heading}.")
    for forbidden in ["Mechanism Layer", "Historical Outcome Engine", "Agent Router", "Tool Registry", "Political Economy"]:
        require(forbidden not in beginner, f"Beginner output leaked internal label: {forbidden}.")


def validate_ui_readability() -> None:
    index = (ROOT / "dashboard/index.html").read_text(encoding="utf-8")
    styles = (ROOT / "dashboard/styles.css").read_text(encoding="utf-8")
    app_js = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    require('id="brief-section" class="brief-output"' in index, "Brief section target missing.")
    require("renderBriefCards(run.brief_markdown" in app_js, "Dashboard does not render brief as structured cards.")
    require(".decision-card" in styles, "Decision Snapshot card style missing.")
    require("max-height: 520px" not in styles, "Old fixed-height nested brief scrollbar remains.")
    require("background: #0f1720" not in styles, "Old dark markdown textbox style remains.")


def main() -> None:
    validate_decision_order()
    validate_content_specificity()
    validate_beginner_mode()
    validate_ui_readability()
    print("V12.1 decision-first refinement validation passed.")


if __name__ == "__main__":
    main()
