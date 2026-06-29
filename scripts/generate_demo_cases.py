"""Generate reviewer-facing demo case artifacts through the local FastAPI pipeline."""

from __future__ import annotations

import json
from pathlib import Path
import sys

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402


DEMO_CASES_DIR = ROOT / "demo_cases"
OUTPUT_DIR = ROOT / "demo_case_outputs"


def main() -> None:
    """Process all demo case files and write portfolio artifacts."""
    client = TestClient(app)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for input_path in sorted(DEMO_CASES_DIR.glob("*.txt")):
        case_name = input_path.stem
        text = input_path.read_text(encoding="utf-8")
        response = client.post(
            "/analyze",
            json={
                "text": text,
                "language": "en",
                "output_mode": "analyst",
                "question_id": "meaning",
                "question_text": "What does this issue mean?",
            },
        )
        response.raise_for_status()
        payload = response.json()
        case_dir = OUTPUT_DIR / case_name
        case_dir.mkdir(parents=True, exist_ok=True)
        metadata = payload["metadata"]
        metadata["demo_case"] = case_name
        metadata["source_input"] = f"demo_cases/{input_path.name}"
        metadata["note"] = "Fictional educational demo case generated through the local FastAPI pipeline."
        agent_trace = payload["analysis"].get("agent_trace", {})
        (case_dir / "analysis.json").write_text(
            json.dumps(payload["analysis"], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (case_dir / "brief.md").write_text(payload["brief_markdown"], encoding="utf-8")
        (case_dir / "brief.txt").write_text(payload["brief_text"], encoding="utf-8")
        (case_dir / "agent_trace.json").write_text(
            json.dumps(agent_trace, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (case_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Generated demo artifacts for {case_name}")


if __name__ == "__main__":
    main()
