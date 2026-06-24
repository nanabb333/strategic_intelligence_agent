"""Validate Strategic Intelligence Agent V7.5 evidence credibility layer."""

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
from evidence_credibility import assess_evidence_credibility  # noqa: E402
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
    "evidence_note",
}


def validate_outcome_evidence_notes() -> None:
    with (ROOT / "knowledge_base/historical_outcomes.csv").open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
    if not REQUIRED_OUTCOME_COLUMNS.issubset(set(reader.fieldnames or [])):
        raise AssertionError("Historical outcomes CSV is missing evidence credibility columns.")
    if any(not row.get("evidence_note") for row in rows):
        raise AssertionError("Every historical outcome must include evidence_note.")


def validate_module_output() -> None:
    text = load_document(ROOT / "examples/chips_act_example.md")
    issues = extract_issues(text)
    classifications = classify_scenarios(issues)
    analogues = retrieve_historical_analogues(issues, classifications)
    outcomes = retrieve_historical_outcomes(analogues)
    lessons = generate_strategic_lessons(outcomes)
    credibility = assess_evidence_credibility(outcomes, lessons)
    issue_title = issues[0].title
    item = credibility.get(issue_title)
    if not item:
        raise AssertionError("Evidence credibility module returned no result.")
    if not item.evidence_summary or not item.confidence_distribution or not item.source_status_distribution:
        raise AssertionError("Evidence credibility summary is incomplete.")
    if not item.key_limitations or "Source URLs are not fabricated" not in " ".join(item.key_limitations):
        raise AssertionError("Evidence credibility limitations are incomplete.")


def validate_api_artifact() -> None:
    client = TestClient(app)
    response = client.post(
        "/analyze",
        json={
            "text": "# V7.5 Credibility Test\n\nExport controls affect semiconductor equipment licensing, restricted customers, supplier qualification, and compliance documentation.",
            "language": "en",
            "output_mode": "analyst",
            "question_id": "limitations",
            "question_text": "What is missing from the evidence?",
        },
    )
    if response.status_code != 200:
        raise AssertionError(f"Analyze endpoint failed: {response.status_code} {response.text}")
    run_id = response.json()["run_id"]
    analysis = json.loads((RUNS_DIR / run_id / "analysis.json").read_text(encoding="utf-8"))
    credibility = analysis.get("evidence_credibility")
    if not credibility:
        raise AssertionError("analysis.json missing evidence_credibility.")
    for key in ["evidence_summary", "confidence_distribution", "source_status_distribution", "key_limitations", "reviewer_note"]:
        if key not in credibility:
            raise AssertionError(f"evidence_credibility missing {key}")


def validate_brief_section() -> None:
    output_path = Path("/private/tmp/strategic_intelligence_agent_v75_brief.md")
    run_agent(ROOT / "examples/chips_act_example.md", output_path)
    text = output_path.read_text(encoding="utf-8")
    if "## Evidence Used" not in text:
        raise AssertionError("Brief missing Evidence Used section.")
    if "Local historical outcome records" not in text:
        raise AssertionError("Brief missing historical outcome evidence note.")
    if "## Limitations" not in text:
        raise AssertionError("Brief missing final limitations section.")


def validate_dashboard_and_docs() -> None:
    html = (ROOT / "dashboard/index.html").read_text(encoding="utf-8")
    js = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    if "Evidence Review" not in html or "evidence-credibility-section" not in html:
        raise AssertionError("Dashboard missing Evidence Review / credibility target section.")
    if "renderEvidenceCredibility" not in js or "source_status_distribution" not in js:
        raise AssertionError("Dashboard JS missing Evidence Credibility rendering.")
    if not (ROOT / "docs/repo5_case_study.md").exists():
        raise AssertionError("Repo 5 case study is missing.")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "docs/repo5_case_study.md" not in readme:
        raise AssertionError("README does not link to repo5_case_study.md.")
    if "Evidence & Limitations" not in readme:
        raise AssertionError("README missing Evidence & Limitations section.")


def main() -> None:
    validate_outcome_evidence_notes()
    validate_module_output()
    validate_api_artifact()
    validate_brief_section()
    validate_dashboard_and_docs()
    print("V7.5 validation passed.")


if __name__ == "__main__":
    main()
