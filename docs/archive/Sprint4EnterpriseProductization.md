# Sprint 4 Enterprise Productization

Repo 5 remains a local-first deterministic Decision Intelligence workspace. Sprint 4 adds release operations support around the stable Version 4 workflow without changing the Decision Brief, reasoning pipeline, evidence model, dashboard identity, or FastAPI analysis contract.

## Configuration Layer

Default configuration lives in `config/defaults.json` and is loaded by `src/config.py`.

The loader is intentionally conservative:

- Missing config files fall back to safe in-code defaults.
- Malformed config files produce warnings through diagnostics rather than stopping the app.
- JSON is used to avoid new dependencies.
- Configuration does not select new providers, agents, databases, or cloud services.

## Workspace Management

`src/project_workspace.py` continues to store projects as local JSON files under `data/projects`.

Sprint 4 adds operational helpers:

- `inspect_project_files()` reports unreadable or malformed project files.
- `workspace_summary()` summarizes project, question, evidence, and decision counts.
- `archive_project()` and `restore_project()` mark project state without deleting data.
- `project_metadata()` returns reviewer-friendly counts and status.

Malformed project files are warnings, not fatal errors. User data is not deleted by diagnostics or recovery helpers.

## Artifact Management

`src/run_storage.py` remains the owner of local run folders under `outputs/runs`.

Sprint 4 adds:

- `list_run_metadata()` for resilient run listing.
- `artifact_metadata(run_id)` for expected artifact existence and size checks.
- `runs_summary()` for release validation diagnostics.

Expected run artifacts remain:

- `input.txt`
- `analysis.json`
- `brief.md`
- `brief.txt`
- `agent_trace.json`
- `metadata.json`

## Diagnostics

`src/diagnostics.py` builds a read-only snapshot for release validation. FastAPI exposes it at:

```text
GET /diagnostics
```

Diagnostics include:

- app config status
- project workspace summary
- run artifact summary
- warnings for malformed project files or missing metadata
- non-fatal check states

Diagnostics do not run analysis, mutate evidence, trigger retrieval, or make recommendations.

## Deployment Readiness

Sprint 4 preserves the existing local startup model:

```bash
python3 -m uvicorn app:app --reload
```

Open the dashboard at:

```text
http://127.0.0.1:8000/dashboard/
```

Review diagnostics at:

```text
http://127.0.0.1:8000/diagnostics
```

## What Did Not Change

- No autonomous agents were added.
- No autonomous browsing, monitoring, or scheduled retrieval was added.
- No database, microservice, cloud service, or external UI framework was added.
- The deterministic analysis engine is unchanged.
- Decision Brief generation is unchanged.
- Dashboard lavender-grey identity is unchanged.
