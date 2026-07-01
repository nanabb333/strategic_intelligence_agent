import json

from fastapi.testclient import TestClient

from app import app
from config import config_status, load_config, release_metadata
import project_workspace
from project_workspace import (
    archive_project,
    create_project,
    list_projects,
    inspect_project_files,
    project_metadata,
    restore_project,
    workspace_summary,
)
import run_storage
from run_storage import artifact_metadata, runs_summary


def test_config_missing_file_uses_safe_defaults(tmp_path) -> None:
    config = load_config(tmp_path / "missing.json")
    status = config_status(tmp_path / "missing.json")

    assert config["app"]["name"] == "Strategic Intelligence Decision Companion"
    assert config["release"]["version"] == "5.0.0"
    assert config["storage"]["projects_directory"] == "data/projects"
    assert status["using_defaults"] is True
    assert status["warnings"]


def test_config_file_deep_merges_defaults(tmp_path) -> None:
    path = tmp_path / "config.json"
    path.write_text(
        json.dumps(
            {
                "app": {"version": "12.1"},
                "features": {"diagnostics": False},
            }
        ),
        encoding="utf-8",
    )

    config = load_config(path)

    assert config["app"]["version"] == "12.1"
    assert config["app"]["name"] == "Strategic Intelligence Decision Companion"
    assert config["release"]["label"] == "Enterprise Product Release"
    assert config["features"]["diagnostics"] is False
    assert config["features"]["project_workspace"] is True


def test_release_metadata_includes_app_identity() -> None:
    release = release_metadata()

    assert release["version"] == "5.0.0"
    assert release["label"] == "Enterprise Product Release"
    assert release["app_name"] == "Strategic Intelligence Decision Companion"
    assert release["storage_schema"] == "local-json-v1"


def test_config_malformed_file_reports_warning_and_falls_back(tmp_path) -> None:
    path = tmp_path / "broken.json"
    path.write_text("{broken", encoding="utf-8")

    config = load_config(path)
    status = config_status(path)

    assert config["defaults"]["output_mode"] == "analyst"
    assert status["using_defaults"] is True
    assert status["warnings"]


def test_malformed_project_files_are_reported_without_breaking_listing(tmp_path, monkeypatch) -> None:
    projects_dir = tmp_path / "projects"
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", projects_dir)
    project = create_project("Recovery Workspace")
    (projects_dir / "broken.json").write_text("{broken", encoding="utf-8")

    inspection = inspect_project_files()
    summary = workspace_summary()

    assert inspection["file_count"] == 2
    assert inspection["readable_count"] == 1
    assert inspection["malformed_count"] == 1
    assert inspection["warnings"]
    assert summary["project_count"] == 1
    assert summary["files"]["malformed_count"] == 1
    assert project["project_id"]


def test_older_project_json_without_new_fields_remains_compatible(tmp_path, monkeypatch) -> None:
    projects_dir = tmp_path / "projects"
    projects_dir.mkdir(parents=True)
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", projects_dir)
    old_project = {
        "project_id": "legacy01",
        "name": "Legacy Workspace",
        "created_at": "2026-06-01T00:00:00",
        "updated_at": "2026-06-01T00:00:00",
        "questions": [{"question_id": "q1"}],
        "evidence_library": [{"evidence_id": "e1"}],
        "decision_history": [{"decision_id": "d1"}],
    }
    (projects_dir / "legacy01.json").write_text(json.dumps(old_project), encoding="utf-8")

    projects = list_projects()
    metadata = project_metadata(projects[0])

    assert projects[0]["project_id"] == "legacy01"
    assert metadata["status"] == "Active"
    assert metadata["question_count"] == 1
    assert metadata["evidence_count"] == 1
    assert metadata["decision_count"] == 1


def test_archive_and_restore_project_preserve_project_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")
    project = create_project("Archive Workspace")
    project_path = project_workspace.PROJECTS_DIR / f"{project['project_id']}.json"

    archived = archive_project(project["project_id"])
    restored = restore_project(project["project_id"])

    assert project_path.exists()
    assert archived["archived"] is True
    assert archived["archived_at"]
    assert restored["archived"] is False
    assert restored["restored_at"]


def test_run_artifact_metadata_reports_missing_artifacts(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(run_storage, "RUNS_DIR", tmp_path / "runs")
    run_dir = run_storage.RUNS_DIR / "run_20260630_001"
    run_dir.mkdir(parents=True)
    (run_dir / "metadata.json").write_text(json.dumps({"run_id": "run_20260630_001"}), encoding="utf-8")
    (run_dir / "analysis.json").write_text("{}", encoding="utf-8")

    metadata = artifact_metadata("run_20260630_001")
    summary = runs_summary()

    assert metadata["exists"] is True
    assert metadata["artifacts"]["metadata"]["exists"] is True
    assert metadata["artifacts"]["brief_markdown"]["exists"] is False
    assert metadata["warnings"]
    assert summary["run_count"] == 1
    assert summary["metadata_count"] == 1


def test_diagnostics_route_returns_release_validation_snapshot(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(project_workspace, "PROJECTS_DIR", tmp_path / "projects")
    monkeypatch.setattr(run_storage, "RUNS_DIR", tmp_path / "runs")
    create_project("Diagnostics Workspace")
    client = TestClient(app)

    response = client.get("/diagnostics")

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) >= {"status", "app", "release", "config", "storage", "warnings", "checks"}
    assert payload["release"]["version"] == "5.0.0"
    assert payload["storage"]["projects"]["project_count"] == 1
    assert payload["storage"]["runs"]["run_count"] == 0
    assert payload["checks"]["project_workspace"] in {"ok", "warning"}


def test_existing_health_and_runs_routes_remain_compatible(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(run_storage, "RUNS_DIR", tmp_path / "runs")
    run_dir = run_storage.RUNS_DIR / "run_20260630_001"
    run_dir.mkdir(parents=True)
    (run_dir / "metadata.json").write_text(json.dumps({"run_id": "run_20260630_001"}), encoding="utf-8")
    client = TestClient(app)

    health = client.get("/health")
    runs = client.get("/runs")

    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert runs.status_code == 200
    assert runs.json() == [{"run_id": "run_20260630_001"}]


def test_version_route_returns_enterprise_release_metadata() -> None:
    response = TestClient(app).get("/version")

    assert response.status_code == 200
    payload = response.json()
    assert payload["version"] == "5.0.0"
    assert payload["label"] == "Enterprise Product Release"
    assert payload["positioning"] == "Enterprise Decision Intelligence Platform"
