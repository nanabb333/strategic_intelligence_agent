# Portfolio Narrative

Strategic Intelligence Decision Companion is a portfolio project showing how an AI-oriented product can be organized as a local, testable, decision-support application instead of a one-off prompt demo.

## What The Project Demonstrates

### AI Product Architecture

The project separates the local FastAPI entrypoint from service orchestration, pipeline execution, helper utilities, intelligence modules, artifact generation, and run storage. This makes the system easier to inspect, test, and explain.

### FastAPI Backend Design

`app.py` handles HTTP concerns: routes, request/response models, static dashboard mounting, upload handling, run lookup, and downloads. The analysis workflow is delegated to `src/analysis_service.py` and `src/analysis_pipeline.py`.

### Service And Pipeline Separation

The service layer gives the app a stable workflow entrypoint. The pipeline layer owns the ordered analysis flow:

```text
Input Preparation
  |
  v
Scenario + Issue Analysis
  |
  v
Retrieval + Assessment
  |
  v
Brief Generation
  |
  v
Artifact Construction
  |
  v
Run Storage
```

This structure is useful for product development because the user-facing API can remain stable while pipeline internals are tested and documented.

### Deterministic Workflow Design

The project uses deterministic local workflow orchestration. It does not rely on autonomous planning, multi-agent debate, or live web retrieval. The value comes from breaking a broad strategic-intelligence task into reviewable stages: issue extraction, scenario classification, retrieval, evidence assessment, decision criteria, brief generation, and artifact storage.

### V2 Decision-Quality Layer

The V2 foundation adds reviewable decision-quality structures without changing the product identity: Decision Case, Evidence Ledger, Confidence Assessment, and Decision Quality Evaluation. These are additive artifact fields designed to make evidence, assumptions, confidence, and evaluation easier to inspect.

### Research Validation Boundary

The repository separates product evaluation from research validation. Product evaluation checks whether the local workflow is reliable, reviewable, and internally coherent. Research validation is documented as a future layer for human review, benchmark strategy, failure-mode analysis, and decision-intelligence research. This separation prevents deterministic product-quality checks from being overstated as scientific proof.

### Historical Analogue Reasoning

The app includes local curated records for historical analogues, outcomes, strategic lessons, mechanisms, and response patterns. These records are simplified educational summaries. They support structured comparison but do not prove future outcomes.

### Artifact Generation

Each run creates reviewable artifacts:

- `input.txt`
- `analysis.json`
- `brief.md`
- `brief.txt`
- `agent_trace.json`
- `metadata.json`

This demonstrates product thinking around traceability, download support, and reuse beyond the browser UI.

### Reviewer Workflow And UX Awareness

The dashboard and output structure support beginner, analyst, and executive output modes, showing attention to different reviewer needs while keeping the official product language English-only.

### Testing And CI Maturity

The repository includes:

- Pytest coverage for pure helpers and API smoke tests.
- Ruff linting.
- Compile checks.
- GitHub Actions CI on push and pull request.

These are intentionally lightweight but important for long-term maintenance.

## What This Project Is Not

This is not:

- A production SaaS deployment.
- A live data platform.
- A forecasting system.
- A trading or investment advisor.
- A legal or compliance advisor.
- A replacement for expert review.

The project should be evaluated as a local AI product architecture and strategic intelligence workflow prototype.

## How To Present It

The strongest portfolio framing is:

> I built a local FastAPI decision-support app that takes unstructured strategic source material and produces structured briefs, JSON artifacts, traceable evidence notes, historical analogues, confidence assessments, deterministic decision-quality evaluation, and run history. The project demonstrates AI product architecture, pipeline design, business analytics thinking, and practical software engineering quality.

## Related Documentation

- [README](../../README.md)
- [Documentation Index](../DocumentationIndex.md)
- [Product Overview](../ProductOverview.md)
- [Demo Scenarios](DemoScenarios.md)
- [Engineering Architecture](../EngineeringArchitecture.md)
- [Analysis Pipeline](../Pipeline.md)
- [Research Agenda](../research/ResearchAgenda.md)
- [Testing](../Testing.md)
