"""Operational diagnostics for local-first release validation."""

from __future__ import annotations

from typing import Any

from config import config_status, load_config, release_metadata
from project_workspace import inspect_project_files, workspace_summary
from run_storage import runs_summary


def build_diagnostics() -> dict[str, Any]:
    """Build a non-fatal diagnostic snapshot for reviewers and operators."""
    config = load_config()
    diagnostics: dict[str, Any] = {
        "status": "ok",
        "app": config.get("app", {}),
        "release": release_metadata(),
        "config": config_status(),
        "storage": {
            "projects": workspace_summary(),
            "runs": runs_summary(),
        },
        "warnings": [],
        "checks": {
            "project_workspace": "ok",
            "run_artifacts": "ok",
            "configuration": "ok",
        },
    }

    config_warnings = diagnostics["config"].get("warnings") or []
    project_inspection = inspect_project_files()
    project_warnings = project_inspection.get("warnings") or []
    run_warnings = diagnostics["storage"]["runs"].get("warnings") or []

    diagnostics["warnings"].extend(config_warnings)
    diagnostics["warnings"].extend(project_warnings)
    diagnostics["warnings"].extend(run_warnings)

    if config_warnings:
        diagnostics["checks"]["configuration"] = "warning"
    if project_warnings:
        diagnostics["checks"]["project_workspace"] = "warning"
    if run_warnings:
        diagnostics["checks"]["run_artifacts"] = "warning"
    if diagnostics["warnings"]:
        diagnostics["status"] = "warning"
    return diagnostics
