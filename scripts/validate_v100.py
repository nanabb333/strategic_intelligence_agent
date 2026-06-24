"""Validate V10 product experience overhaul."""

from __future__ import annotations

import csv
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
from knowledge_localization import localize_knowledge_text  # noqa: E402


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_dataset() -> None:
    rows = list(csv.DictReader((ROOT / "knowledge_base" / "historical_outcomes.csv").open(encoding="utf-8")))
    require(len(rows) >= 100, f"Expected at least 100 cases, found {len(rows)}.")
    require(not any(row.get(None) for row in rows), "historical_outcomes.csv has malformed rows.")
    audit = ROOT / "docs" / "intelligence_dataset_v10_audit.md"
    require(audit.exists(), "V10 dataset audit missing.")
    audit_text = audit.read_text(encoding="utf-8")
    for phrase in ["Current case count:** 105", "Category Distribution", "Outcome Distribution", "Mechanism Distribution", "Confidence Distribution"]:
        require(phrase in audit_text, f"V10 audit missing {phrase}.")


def validate_knowledge_localization() -> None:
    require((ROOT / "src" / "knowledge_localization.py").exists(), "knowledge_localization.py missing.")
    sample = "Strategic Dependency; Supply Chain Reconfiguration; Industrial Subsidy; Alliance Coordination"
    simplified = localize_knowledge_text(sample, "zh-CN")
    traditional = localize_knowledge_text(sample, "zh-TW")
    for english in ["Strategic Dependency", "Supply Chain Reconfiguration", "Industrial Subsidy", "Alliance Coordination"]:
        require(english not in simplified, f"Untranslated zh-CN mechanism label: {english}.")
        require(english not in traditional, f"Untranslated zh-TW mechanism label: {english}.")
    require("戰略依賴" in traditional and "供應鏈重構" in traditional, "Traditional Chinese knowledge terms missing.")


def validate_dashboard_workflow() -> None:
    index = read("dashboard/index.html")
    app_js = read("dashboard/app.js")
    styles = read("dashboard/styles.css")
    for phrase in ["STEP 1", "Paste Document", "STEP 2", "Ask a Question", "STEP 3", "Analyze"]:
        require(phrase in index, f"Dashboard missing workflow phrase: {phrase}.")
    require("advanced-settings" in index, "Advanced settings are not collapsed.")
    for phrase in ["Lesson", "Why it matters", "Supporting historical cases", "Observed pattern", "Relevant cases"]:
        require(phrase in app_js, f"Result card copy missing: {phrase}.")
    require("card-kicker" in styles, "Result card styling missing.")

    executive = index.find("executiveBrief")
    lessons = index.find("strategicLessons")
    outcomes = index.find("historicalOutcomes")
    analogues = index.find("historicalAnalogues")
    event = index.find("currentEventContext")
    mechanisms = index.find("mechanisms")
    evidence = index.find("evidenceReview")
    trace = index.find("executionTrace")
    require(
        executive < lessons < outcomes < analogues < event < mechanisms < evidence < trace,
        "Result order does not match V10 value-first sequence.",
    )


def validate_localized_app_output() -> None:
    client = TestClient(app)
    response = client.post(
        "/analyze",
        json={
            "text": "Export controls affect semiconductor suppliers, strategic dependency, and supply chain reconfiguration.",
            "language": "zh-TW",
            "output_mode": "analyst",
            "question_text": "這和哪些歷史事件相似？",
        },
    )
    require(response.status_code == 200, f"zh-TW analyze failed: {response.text}")
    payload = response.json()
    brief = payload["brief_markdown"]
    mechanisms = str(payload["analysis"].get("mechanisms", []))
    for english in ["Strategic Dependency", "Supply Chain Reconfiguration", "Industrial Subsidy", "Alliance Coordination"]:
        require(english not in brief, f"Brief left major mechanism label untranslated: {english}.")
        require(english not in mechanisms, f"Analysis left major mechanism label untranslated: {english}.")
    require("策略經驗" in brief, "Traditional Chinese brief missing localized Strategic Lessons heading.")


def validate_readme() -> None:
    readme = read("README.md")
    require("Product Evolution Through User Testing" in readme, "README missing user-testing evolution section.")
    require("105 educational cases" in readme, "README missing V10 dataset count.")
    require("Step 1 / Step 2 / Step 3" in readme, "README missing simplified workflow summary.")


def main() -> None:
    validate_dataset()
    validate_knowledge_localization()
    validate_dashboard_workflow()
    validate_localized_app_output()
    validate_readme()
    print("V10.0 validation passed.")


if __name__ == "__main__":
    main()
