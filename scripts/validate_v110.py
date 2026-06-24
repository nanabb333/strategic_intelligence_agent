"""Validate V11 strategic assessment engine."""

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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def analyze(language: str, mode: str) -> dict:
    client = TestClient(app)
    response = client.post(
        "/analyze",
        json={
            "text": (
                "New semiconductor export controls affect advanced chip supply chains, "
                "supplier access, compliance documentation, customer eligibility, and market access."
            ),
            "language": language,
            "output_mode": mode,
            "question_text": "What does this mean and what should I monitor next?",
        },
    )
    require(response.status_code == 200, f"{language}/{mode} analyze failed: {response.text}")
    return response.json()


def validate_analyst_assessment() -> None:
    payload = analyze("en", "analyst")
    brief = payload["brief_markdown"]
    analysis = payload["analysis"]
    required_sections = [
        "## Direct Answer",
        "## Similar Cases",
        "## What Happened Then",
        "## How Organizations Responded",
        "## What Happened After",
        "## Market Expectations vs Actual Outcomes",
        "## What This Means Now",
        "## What To Watch Next",
        "## Evidence Used",
        "## Limitations",
    ]
    for section in required_sections:
        require(section in brief, f"Analyst brief missing V11 section: {section}.")
    require(brief.find("## Direct Answer") < brief.find("## Evidence Used"), "Direct Answer does not appear before evidence.")
    require("strategic_assessment" in analysis, "analysis.json missing strategic_assessment.")
    assessment = analysis["strategic_assessment"]
    for key in [
        "direct_answer",
        "historical_patterns",
        "outcome_distribution",
        "expectation_vs_reality",
        "strategic_watchlist",
        "role_based_monitoring",
    ]:
        require(key in assessment, f"strategic_assessment missing {key}.")
    require(assessment["historical_patterns"], "Historical patterns are empty.")
    require(assessment["outcome_distribution"], "Outcome distribution is empty.")
    require(assessment["expectation_vs_reality"], "Expectation gap analysis is empty.")


def validate_beginner_assessment() -> None:
    payload = analyze("en", "beginner")
    brief = payload["brief_markdown"]
    for section in [
        "## What This Means",
        "## Similar Historical Cases",
        "## Common Responses",
        "## What Happened After",
        "## What to monitor next",
        "## Important Limitations",
    ]:
        require(section in brief, f"Beginner brief missing section: {section}.")
    for internal in ["Tool Registry", "Agent Router", "Mechanism Framework", "Benchmark results", "source pending"]:
        require(internal not in brief, f"Beginner brief leaked internal label: {internal}.")
    require(brief.count("limitations") <= 1, "Beginner brief repeats limitations language.")


def validate_chinese_assessment() -> None:
    payload = analyze("zh-TW", "beginner")
    brief = payload["brief_markdown"]
    for phrase in ["這意味著什麼", "相似歷史案例", "常見應對方式", "後來通常發生什麼", "接下來可以關注什麼", "限制說明"]:
        require(phrase in brief, f"zh-TW beginner brief missing V11 phrase: {phrase}.")
    for english in [
        "Direct Answer",
        "Historical Patterns",
        "Outcome Distribution",
        "Expectation vs Reality",
        "Role-Based Monitoring",
        "Tool Registry",
        "Agent Router",
        "source pending",
    ]:
        require(english not in brief, f"zh-TW output leaked English/internal phrase: {english}.")


def main() -> None:
    validate_analyst_assessment()
    validate_beginner_assessment()
    validate_chinese_assessment()
    print("V11.0 validation passed.")


if __name__ == "__main__":
    main()
