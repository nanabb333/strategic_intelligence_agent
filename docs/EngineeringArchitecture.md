# Engineering Architecture

This implementation-focused document describes how the current local application executes the product flow defined by the canonical [Architecture Overview](architecture.md). It does not define a competing product architecture or planned infrastructure.

## Related Docs

- [Documentation Index](DocumentationIndex.md)
- [Product Overview](ProductOverview.md)
- [Analysis Pipeline](Pipeline.md)
- [Folder Structure](FolderStructure.md)
- [Testing](Testing.md)
- [Documentation Archive](archive/README.md)

## Runtime Shape

```text
Decision Question + Decision Context + Supporting Evidence
  |
  v
Browser Decision Assessment interface
  |
  v
FastAPI app.py
  |
  v
Service Layer
src/analysis_service.py
  |
  v
Pipeline Orchestration
src/analysis_pipeline.py
  |
  v
Intelligence Modules
issue extraction, scenario classification, retrieval, assessment, brief generation
  |
  v
V2 Decision-Quality Layer
decision case, evidence ledger, confidence assessment, evaluation
  |
  v
Artifact Generation
analysis JSON, Markdown brief, text brief, compatibility trace, metadata
  |
  v
Run Storage + Downloads
outputs/runs/run_YYYYMMDD_NNN/
```

## Layer Responsibilities

### FastAPI Entrypoint

`app.py` owns HTTP concerns:

- FastAPI application setup
- CORS and static dashboard mounting
- Pydantic request and response models
- Route definitions
- File upload text extraction endpoint
- Run lookup and artifact download endpoints

The `/analyze` route delegates the business workflow to `run_analysis(...)`.

### Service Layer

`src/analysis_service.py` is the public service entrypoint for the analysis workflow. It keeps the API-facing function `run_analysis(...)` stable and delegates orchestration to the pipeline.

### Pipeline Layer

`src/analysis_pipeline.py` owns the ordered workflow:

- prepare input text
- create a run folder
- run deterministic intelligence modules
- generate the brief
- build JSON artifacts
- write run outputs
- return the response payload used by `app.py`

The pipeline intentionally remains explicit so the workflow is easy to inspect.

### Helper Modules

- `src/analysis_input.py`: text, URL, and analysis-text preparation
- `src/analysis_metadata.py`: metadata artifact construction
- `src/agent_trace.py`: compatibility trace artifact construction; the filename is retained for schema and code stability
- `src/analysis_artifact.py`: analysis JSON artifact construction
- `src/decision_case.py`: additive Decision Case schema for the primary decision issue
- `src/evidence_ledger.py`: additive Evidence Ledger records for reviewable evidence items
- `src/confidence_layer.py`: qualitative Confidence Assessment and Evidence and Confidence brief section
- `src/decision_quality_evaluator.py`: deterministic Decision Quality Evaluation for generated artifacts
- `src/serialization.py`: dataclass/list/dict serialization helper
- `src/markdown_utils.py`: markdown-to-text conversion
- `src/run_storage.py`: run directory and JSON storage helpers
- `src/url_reader.py`: readable webpage text extraction
- `src/pdf_reader.py`: text-based PDF extraction

## Project Context And Storage

`src/project_workspace.py` persists the optional Current Project context: questions, accepted evidence, decision history, delta, and review state. Project persistence supports the Decision Assessment flow; it is not the primary product workflow. Run artifacts are stored locally under `outputs/runs/`, and project JSON is stored under `data/projects/`.

## Constraints

The product is a local, single-user decision-support application. It does not provide autonomous agents or research, background monitoring, forecasting, probability estimates, preferred-option selection, trading recommendations, legal advice, investment advice, authentication, or cloud deployment.
