"""Local configuration loading with safe defaults."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "defaults.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "app": {
        "name": "Strategic Intelligence Decision Companion",
        "api_title": "Strategic Intelligence Decision Companion Local App",
        "version": "5.0.0",
    },
    "release": {
        "version": "5.0.0",
        "label": "Enterprise Product Release",
        "milestone": "V5 Sprint 0",
        "stage": "sprint-0",
        "released_on": "2026-06-30",
        "compatibility": "Compatible with Version 4 and Version 4.5 local project JSON workspaces.",
        "storage_schema": "local-json-v1",
        "positioning": "Enterprise Decision Intelligence Platform",
    },
    "defaults": {
        "language": "en",
        "output_mode": "analyst",
    },
    "features": {
        "project_workspace": True,
        "evidence_retrieval": True,
        "diagnostics": True,
    },
    "storage": {
        "projects_directory": "data/projects",
        "runs_directory": "outputs/runs",
    },
    "evidence": {
        "default_allowed_tiers": [
            "Tier 1 Official",
            "Tier 2 Company",
            "Tier 3 Reputable News",
        ],
        "review_required": True,
    },
    "dashboard": {
        "theme": "lavender-grey",
        "primary": "#B8A7E8",
        "background": "#F7F4FF",
        "soft_highlight": "#EFEAFB",
    },
}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def load_config(path: Path | str | None = None) -> dict[str, Any]:
    """Load local JSON config, falling back to deterministic safe defaults."""
    config_path = Path(path) if path is not None else CONFIG_PATH
    if not config_path.exists():
        return copy.deepcopy(DEFAULT_CONFIG)
    try:
        loaded = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return copy.deepcopy(DEFAULT_CONFIG)
    if not isinstance(loaded, dict):
        return copy.deepcopy(DEFAULT_CONFIG)
    return _deep_merge(DEFAULT_CONFIG, loaded)


def config_status(path: Path | str | None = None) -> dict[str, Any]:
    """Return config health without raising on missing or malformed files."""
    config_path = Path(path) if path is not None else CONFIG_PATH
    warnings: list[str] = []
    exists = config_path.exists()
    loaded = False
    if not exists:
        warnings.append("Configuration file is missing; safe defaults are active.")
    else:
        try:
            parsed = json.loads(config_path.read_text(encoding="utf-8"))
            loaded = isinstance(parsed, dict)
            if not loaded:
                warnings.append("Configuration file must contain a JSON object; safe defaults are active.")
        except (OSError, json.JSONDecodeError) as exc:
            warnings.append(f"Configuration file could not be loaded; safe defaults are active: {exc}")
    return {
        "path": str(config_path),
        "exists": exists,
        "loaded": loaded,
        "using_defaults": not loaded,
        "warnings": warnings,
    }


def configured_path(section: str, key: str, path: Path | str | None = None) -> Path:
    """Resolve a relative configured path under the repository root."""
    value = str(load_config(path).get(section, {}).get(key, "")).strip()
    resolved = Path(value)
    if resolved.is_absolute():
        return resolved
    return ROOT / resolved


def release_metadata(path: Path | str | None = None) -> dict[str, Any]:
    """Return product release metadata with app identity included."""
    config = load_config(path)
    release = copy.deepcopy(config.get("release", {}))
    release.setdefault("version", config.get("app", {}).get("version", "5.0.0"))
    release["app_name"] = config.get("app", {}).get("name", DEFAULT_CONFIG["app"]["name"])
    return release
