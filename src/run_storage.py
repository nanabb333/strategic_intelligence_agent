"""Run artifact storage utilities."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import HTTPException


ROOT = Path(__file__).resolve().parent.parent
RUNS_DIR = ROOT / "outputs" / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)


def next_run_id() -> str:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    date_part = datetime.now().strftime("%Y%m%d")
    existing = {path.name for path in RUNS_DIR.glob(f"run_{date_part}_*")}
    next_index = 1
    while True:
        candidate = f"run_{date_part}_{next_index:03d}"
        if candidate not in existing and not (RUNS_DIR / candidate).exists():
            return candidate
        next_index += 1


def create_run_dir() -> tuple[str, Path]:
    """Create a unique run directory, retrying if concurrent requests collide."""
    for _ in range(100):
        run_id = next_run_id()
        run_dir = RUNS_DIR / run_id
        try:
            run_dir.mkdir(parents=True, exist_ok=False)
            return run_id, run_dir
        except FileExistsError:
            continue
    raise HTTPException(status_code=500, detail="Could not allocate a run folder.")


def run_dir_or_404(run_id: str) -> Path:
    run_dir = RUNS_DIR / run_id
    if not run_dir.exists() or not run_dir.is_dir():
        raise HTTPException(status_code=404, detail="Run not found.")
    return run_dir


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


ARTIFACT_FILENAMES = {
    "input": "input.txt",
    "analysis": "analysis.json",
    "brief_markdown": "brief.md",
    "brief_text": "brief.txt",
    "tool_routing_trace": "agent_trace.json",
    "metadata": "metadata.json",
}


def list_run_metadata() -> list[dict[str, Any]]:
    """Return metadata for stored runs, skipping malformed metadata files."""
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    runs = []
    for metadata_path in sorted(RUNS_DIR.glob("*/metadata.json"), reverse=True):
        try:
            metadata = read_json(metadata_path)
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(metadata, dict):
            runs.append(metadata)
    return runs


def artifact_metadata(run_id: str) -> dict[str, Any]:
    """Return existence and size metadata for expected run artifacts."""
    run_dir = RUNS_DIR / run_id
    artifacts: dict[str, dict[str, Any]] = {}
    warnings: list[str] = []
    if not run_dir.exists() or not run_dir.is_dir():
        return {
            "run_id": run_id,
            "run_directory": str(run_dir),
            "exists": False,
            "artifacts": artifacts,
            "warnings": [f"Run directory not found: {run_id}"],
        }
    for artifact, filename in ARTIFACT_FILENAMES.items():
        path = run_dir / filename
        exists = path.exists()
        artifacts[artifact] = {
            "filename": filename,
            "path": str(path),
            "exists": exists,
            "size_bytes": path.stat().st_size if exists else 0,
        }
        if not exists:
            warnings.append(f"Missing run artifact {filename} for {run_id}.")
    return {
        "run_id": run_id,
        "run_directory": str(run_dir),
        "exists": True,
        "artifacts": artifacts,
        "warnings": warnings,
    }


def runs_summary() -> dict[str, Any]:
    """Return a lightweight summary of local run artifact storage."""
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    run_dirs = [path for path in RUNS_DIR.glob("run_*") if path.is_dir()]
    metadata = list_run_metadata()
    warnings = []
    if len(metadata) < len(run_dirs):
        warnings.append("One or more run directories are missing readable metadata.json files.")
    return {
        "runs_directory": str(RUNS_DIR),
        "run_count": len(run_dirs),
        "metadata_count": len(metadata),
        "warnings": warnings,
    }


def download_links(run_id: str) -> dict[str, str]:
    return {
        "markdown": f"/run/{run_id}/download/markdown",
        "txt": f"/run/{run_id}/download/txt",
        "json": f"/run/{run_id}/download/json",
    }
