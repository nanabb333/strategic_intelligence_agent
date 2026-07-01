# Folder Structure

This document describes the current repository layout.

## Related Docs

- [Documentation Index](DocumentationIndex.md)
- [Product Overview](ProductOverview.md)
- [Engineering Architecture](EngineeringArchitecture.md)
- [Analysis Pipeline](Pipeline.md)
- [Testing](Testing.md)

```text
.
├── app.py
├── dashboard/
├── data/
├── demo_cases/
├── demo_case_outputs/
├── docs/
│   ├── Architecture/
│   ├── Developer/
│   ├── GettingStarted/
│   └── Reference/
├── evaluation/
├── examples/
├── knowledge_base/
├── outputs/
├── scripts/
├── src/
├── tests/
└── requirements.txt
```

## Key Folders

### `app.py`

Local FastAPI entrypoint. It defines request/response models and HTTP routes.

### `dashboard/`

Static browser dashboard served by FastAPI.

### `src/`

Application and analysis modules. The main flow is:

```text
analysis_service.py
  -> analysis_pipeline.py
      -> analysis_input.py
      -> intelligence modules
      -> analysis_artifact.py
      -> analysis_metadata.py
      -> agent_trace.py
      -> run_storage.py
```

Enterprise decision modules include:

```text
evidence_intelligence.py
  -> decision_readiness.py
      -> decision_pathways.py
          -> pathway_comparison.py
              -> decision_review.py
```

Shared dependency-free decision helpers live in `decision_support_utils.py`.

### `knowledge_base/`

Local curated data used by deterministic retrieval and reasoning layers.

### `outputs/`

Generated run artifacts. Runtime run folders under `outputs/runs/` are ignored by git.

### `tests/`

Pytest suite for helper modules and FastAPI endpoint smoke tests.

### `docs/Architecture/`

Enterprise architecture and module-boundary documentation.

### `docs/Developer/`

Developer-facing conventions such as API naming and compatibility guidance.

### `docs/GettingStarted/`

Reviewer and demo-scenario entry points.

### `docs/Reference/`

Reference material such as naming review.

### `.github/workflows/`

Continuous integration workflow for compile and test validation.

## Runtime Artifact Note

Runtime analysis folders under `outputs/runs/` are intentionally ignored by git. They are local outputs created when a user runs an analysis through the dashboard or API.
