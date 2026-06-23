"""Validate Strategic Intelligence Agent V6 local app."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient  # noqa: E402
from app import RUNS_DIR, app  # noqa: E402


REQUIRED_RUN_FILES = {
    "input.txt",
    "analysis.json",
    "brief.md",
    "brief.txt",
    "agent_trace.json",
    "metadata.json",
}

REQUIRED_ANALYSIS_FIELDS = {
    "issue",
    "scenario",
    "mechanisms",
    "analogues",
    "response_playbooks",
    "lenses",
    "evidence",
    "agent_trace",
    "evaluation_metadata",
}

SOURCE_METADATA_FIELDS = {
    "source_title",
    "source_type",
    "source_date",
    "source_url",
    "confidence_note",
}


def validate_dashboard_wiring() -> None:
    app_js = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    index = (ROOT / "dashboard/index.html").read_text(encoding="utf-8")
    for marker in ["fetch(`${API_BASE}/analyze`", "fetch(`${API_BASE}/runs`", "Download JSON"]:
        if marker not in app_js and marker not in index:
            raise AssertionError(f"Dashboard API marker missing: {marker}")
    if "history-list" not in index:
        raise AssertionError("Dashboard history panel is missing.")


def validate_source_metadata() -> None:
    for path in [
        ROOT / "knowledge_base/historical_analogues.csv",
        ROOT / "knowledge_base/mechanism_framework.csv",
    ]:
        with path.open(newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            if not SOURCE_METADATA_FIELDS.issubset(set(reader.fieldnames or [])):
                raise AssertionError(f"Source metadata fields missing from {path}")


def validate_api_and_runs() -> None:
    client = TestClient(app)
    health = client.get("/health")
    if health.status_code != 200 or health.json().get("status") != "ok":
        raise AssertionError("FastAPI health endpoint failed.")

    payload = {
        "text": "# V6 Validation\n\nThe CHIPS Act affects semiconductor supply chain planning, domestic manufacturing incentives, supplier qualification, and compliance documentation.",
        "language": "en",
        "output_mode": "analyst",
        "question_id": "meaning",
        "question_text": "What does this issue mean?",
    }
    response = client.post("/analyze", json=payload)
    if response.status_code != 200:
        raise AssertionError(f"Analyze endpoint failed: {response.status_code} {response.text}")
    data = response.json()
    run_id = data["run_id"]
    run_dir = RUNS_DIR / run_id
    if not run_dir.exists():
        raise AssertionError("Run folder was not created.")
    existing_files = {path.name for path in run_dir.iterdir() if path.is_file()}
    missing_files = REQUIRED_RUN_FILES - existing_files
    if missing_files:
        raise AssertionError(f"Run folder missing artifacts: {sorted(missing_files)}")

    analysis = json.loads((run_dir / "analysis.json").read_text(encoding="utf-8"))
    missing_fields = REQUIRED_ANALYSIS_FIELDS - set(analysis)
    if missing_fields:
        raise AssertionError(f"analysis.json missing fields: {sorted(missing_fields)}")
    if not analysis["agent_trace"].get("selected_tools"):
        raise AssertionError("agent_trace missing selected tools.")
    if not analysis["analogues"]:
        raise AssertionError("analysis.json missing historical analogues.")
    if not SOURCE_METADATA_FIELDS.issubset(set(analysis["analogues"][0])):
        raise AssertionError("Historical analogue source metadata missing in analysis.json.")

    for artifact in ["markdown", "txt", "json"]:
        download = client.get(f"/run/{run_id}/download/{artifact}")
        if download.status_code != 200 or not download.content:
            raise AssertionError(f"Download failed for {artifact}.")

    runs = client.get("/runs")
    if runs.status_code != 200 or not any(item["run_id"] == run_id for item in runs.json()):
        raise AssertionError("Run history did not include the created run.")

    fetched = client.get(f"/run/{run_id}")
    if fetched.status_code != 200 or fetched.json()["metadata"]["run_id"] != run_id:
        raise AssertionError("Run retrieval failed.")


def validate_uvicorn_starts() -> None:
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8765"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        last_error: Exception | None = None
        for _ in range(30):
            try:
                with urllib.request.urlopen("http://127.0.0.1:8765/health", timeout=1) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                    if payload.get("status") != "ok":
                        raise AssertionError("Uvicorn health payload was not ok.")
                with urllib.request.urlopen("http://127.0.0.1:8765/dashboard/", timeout=1) as response:
                    html = response.read().decode("utf-8")
                    if "Strategic Intelligence Agent" not in html:
                        raise AssertionError("Dashboard did not load through FastAPI.")
                return
            except Exception as exc:  # noqa: BLE001 - collect startup errors for validation reporting.
                last_error = exc
                time.sleep(0.2)
        if last_error and "Operation not permitted" in str(last_error):
            health = TestClient(app).get("/health")
            if health.status_code == 200 and health.json().get("status") == "ok":
                return
        raise AssertionError(f"Uvicorn server did not start: {last_error}")
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def main() -> None:
    validate_dashboard_wiring()
    validate_source_metadata()
    validate_api_and_runs()
    validate_uvicorn_starts()
    print("V6.0 validation passed.")


if __name__ == "__main__":
    main()
