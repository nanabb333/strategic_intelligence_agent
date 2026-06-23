"""Validate Strategic Intelligence Agent V7 historical outcomes layer."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient  # noqa: E402
from app import RUNS_DIR, app  # noqa: E402
from document_loader import load_document  # noqa: E402
from historical_retriever import retrieve_historical_analogues  # noqa: E402
from issue_extractor import extract_issues  # noqa: E402
from outcome_retriever import retrieve_historical_outcomes  # noqa: E402
from run_agent import run_agent  # noqa: E402
from scenario_classifier import classify_scenarios  # noqa: E402
from strategic_lessons import generate_strategic_lessons  # noqa: E402


REQUIRED_OUTCOME_COLUMNS = {
    "case_id",
    "case_name",
    "event_family",
    "year",
    "actor",
    "sector",
    "observed_outcome",
    "strategic_response",
    "time_horizon",
    "confidence",
    "source_status",
}


def validate_outcome_database() -> None:
    path = ROOT / "knowledge_base/historical_outcomes.csv"
    if not path.exists():
        raise AssertionError("historical_outcomes.csv is missing.")
    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
    if len(rows) < 20:
        raise AssertionError("Expected at least 20 historical outcome records.")
    if set(reader.fieldnames or []) != REQUIRED_OUTCOME_COLUMNS:
        raise AssertionError("Historical outcome columns do not match V7 schema.")
    required_families = {"Export Controls", "Sanctions", "Industrial Policy", "Supply Chain Disruption", "Technology Competition", "Geopolitical Escalation"}
    present_families = {row["event_family"] for row in rows}
    missing = required_families - present_families
    if missing:
        raise AssertionError(f"Outcome database missing event families: {sorted(missing)}")


def validate_retrieval_and_lessons() -> None:
    text = load_document(ROOT / "examples/chips_act_example.md")
    issues = extract_issues(text)
    classifications = classify_scenarios(issues)
    analogues = retrieve_historical_analogues(issues, classifications)
    outcomes = retrieve_historical_outcomes(analogues)
    lessons = generate_strategic_lessons(outcomes)
    issue_title = issues[0].title
    if not outcomes.get(issue_title):
        raise AssertionError("Outcome retrieval returned no outcomes.")
    if not lessons.get(issue_title):
        raise AssertionError("Strategic lesson generation returned no lessons.")
    first_lesson = lessons[issue_title][0]
    if not first_lesson.supporting_cases or first_lesson.confidence not in {"High", "Medium", "Low"}:
        raise AssertionError("Strategic lesson is missing supporting cases or confidence.")


def validate_brief_generation() -> None:
    output_path = Path("/private/tmp/strategic_intelligence_agent_v70_brief.md")
    run_agent(ROOT / "examples/chips_act_example.md", output_path)
    text = output_path.read_text(encoding="utf-8")
    for section in ["## Historical Outcomes", "## Strategic Lessons", "## Decision Considerations"]:
        if section not in text:
            raise AssertionError(f"Brief missing V7 section: {section}")
    forbidden = ["will happen", "must invest", "you should invest", "this is legal advice"]
    lowered = text.lower()
    for phrase in forbidden:
        if phrase in lowered:
            raise AssertionError(f"Forbidden language found in V7 brief: {phrase}")


def validate_api_artifacts() -> None:
    client = TestClient(app)
    response = client.post(
        "/analyze",
        json={
            "text": "# Export Controls Note\n\nNew export controls affect semiconductor equipment licensing, supplier qualification, restricted customers, and compliance documentation.",
            "language": "en",
            "output_mode": "analyst",
            "question_id": "lessons",
            "question_text": "What lessons appear in similar cases?",
        },
    )
    if response.status_code != 200:
        raise AssertionError(f"Analyze failed: {response.status_code} {response.text}")
    payload = response.json()
    run_id = payload["run_id"]
    analysis_path = RUNS_DIR / run_id / "analysis.json"
    trace_path = RUNS_DIR / run_id / "agent_trace.json"
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    if not analysis.get("historical_outcomes"):
        raise AssertionError("analysis.json missing historical_outcomes.")
    if not analysis.get("strategic_lessons"):
        raise AssertionError("analysis.json missing strategic_lessons.")
    if "Historical outcome retrieval" not in trace.get("reasoning_stages", []):
        raise AssertionError("agent_trace.json missing outcome retrieval stage.")
    if "Strategic lesson generation" not in trace.get("reasoning_stages", []):
        raise AssertionError("agent_trace.json missing lesson generation stage.")


def validate_dashboard_and_docs() -> None:
    html = (ROOT / "dashboard/index.html").read_text(encoding="utf-8")
    js = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    for marker in ["outcomes-section", "lessons-section", "historicalOutcomes", "strategicLessons"]:
        if marker not in html and marker not in js:
            raise AssertionError(f"Dashboard missing V7 marker: {marker}")
    for path in [
        "docs/v70_historical_outcomes.md",
        "docs/strategic_lessons_framework.md",
    ]:
        if not (ROOT / path).exists():
            raise AssertionError(f"Missing V7 doc: {path}")


def main() -> None:
    validate_outcome_database()
    validate_retrieval_and_lessons()
    validate_brief_generation()
    validate_api_artifacts()
    validate_dashboard_and_docs()
    print("V7.0 validation passed.")


if __name__ == "__main__":
    main()
