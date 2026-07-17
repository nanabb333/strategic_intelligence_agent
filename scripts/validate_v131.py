"""RETIRED historical validator for the superseded V13.1 recommendation contract."""

from __future__ import annotations

from pathlib import Path
import re
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
    "semiconductor": "New semiconductor export controls affect advanced chip supply chains and market access. Equipment suppliers are reviewing licensing requirements, customer eligibility, and compliance documentation.",
    "taiwan_family": "A Taiwan-based family holds most assets in Taiwan real estate and local equities while future education and business cash flows may require USD liquidity. The family is considering whether to diversify toward US and Singapore assets without selling existing holdings immediately.",
    "usd_insurance": "A bank relationship manager is promoting a USD-denominated insurance savings product. The client wants to compare the product with USD deposits, Treasuries, and bond ETFs, and understand surrender costs, FX exposure, liquidity limits, and suitability risks.",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def analyze(text: str) -> str:
    response = TestClient(app).post(
        "/analyze",
        json={
            "text": text,
            "language": "en",
            "output_mode": "analyst",
            "question_text": "What criteria should drive this decision?",
        },
    )
    require(response.status_code == 200, response.text)
    return response.json()["brief_markdown"]


def section(text: str, title: str, next_title: str) -> str:
    start = text.find(title)
    end = text.find(next_title)
    require(start >= 0 and end > start, f"Could not locate {title} before {next_title}.")
    return text[start:end]


def criteria_names(criteria_section: str) -> set[str]:
    return set(re.findall(r"- \*\*([^*]+)\*\* — \*\*Importance:", criteria_section))


def validate_criteria_order_and_content() -> None:
    brief = analyze(SCENARIOS["semiconductor"])
    required_order = [
        "## Decision Snapshot",
        "## Decision Question",
        "## Decision Criteria",
        "## Decision Paths",
        "## Option Ranking",
    ]
    positions = [brief.find(item) for item in required_order]
    require(all(position >= 0 for position in positions), "Missing decision criteria order section.")
    require(positions == sorted(positions), "Decision Criteria must appear between question and paths.")
    criteria = section(brief, "## Decision Criteria", "## Decision Paths")
    for phrase in ["Customer exposure", "Licensing uncertainty", "Compliance burden", "Margin impact", "Supply chain resilience"]:
        require(phrase in criteria, f"Semiconductor criteria missing {phrase}.")


def validate_criteria_vary_by_scenario() -> None:
    criteria_by_case = {}
    for name, text in SCENARIOS.items():
        brief = analyze(text)
        criteria_by_case[name] = criteria_names(section(brief, "## Decision Criteria", "## Decision Paths"))
    require(criteria_by_case["semiconductor"] != criteria_by_case["taiwan_family"], "Semiconductor and Taiwan criteria should differ.")
    require(criteria_by_case["semiconductor"] != criteria_by_case["usd_insurance"], "Semiconductor and insurance criteria should differ.")
    require("Jurisdiction concentration" in criteria_by_case["taiwan_family"], "Taiwan criteria missing jurisdiction concentration.")
    require("Net return after costs" in criteria_by_case["usd_insurance"], "Insurance criteria missing net return after costs.")


def validate_options_and_recommendation_reference_criteria() -> None:
    brief = analyze(SCENARIOS["semiconductor"])
    paths = section(brief, "## Decision Paths", "## Option Ranking")
    preferred = section(brief, "## Preferred Path", "## Why This Reasoning Holds")
    for phrase in ["**Criteria Fit**", "Customer exposure", "Licensing uncertainty", "criteria that matter most"]:
        require(phrase in paths or phrase in preferred, f"Criteria-driven evaluation missing {phrase}.")
    require("performs best on the criteria that matter most" in preferred, "Preferred path does not derive from criteria.")


def validate_ui_and_beginner_include_criteria() -> None:
    app_js = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    styles = (ROOT / "dashboard/styles.css").read_text(encoding="utf-8")
    require("Decision Criteria" in app_js and ".criteria-card" in styles, "Dashboard missing criteria card rendering.")
    beginner_response = TestClient(app).post(
        "/analyze",
        json={
            "text": SCENARIOS["semiconductor"],
            "language": "en",
            "output_mode": "beginner",
            "question_text": "What criteria should drive this decision?",
        },
    )
    require(beginner_response.status_code == 200, beginner_response.text)
    beginner = beginner_response.json()["brief_markdown"]
    require("## What matters most" in beginner, "Beginner mode missing criteria explanation.")
    require("Customer exposure" in beginner, "Beginner criteria are not scenario-specific.")


def main() -> None:
    validate_criteria_order_and_content()
    validate_criteria_vary_by_scenario()
    validate_options_and_recommendation_reference_criteria()
    validate_ui_and_beginner_include_criteria()
    print("V13.1 decision criteria validation passed.")


if __name__ == "__main__":
    raise SystemExit("RETIRED: validates the superseded V13.1 preferred-path contract; not a current V5 validator.")
