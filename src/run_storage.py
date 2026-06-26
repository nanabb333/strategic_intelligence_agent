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


def download_links(run_id: str) -> dict[str, str]:
    return {
        "markdown": f"/run/{run_id}/download/markdown",
        "txt": f"/run/{run_id}/download/txt",
        "json": f"/run/{run_id}/download/json",
    }