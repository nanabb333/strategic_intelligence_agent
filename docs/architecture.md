# Architecture

Strategic Intelligence Decision Companion is a deterministic, auditable, reviewer-first strategic decision-support system. It helps reviewers structure decisions with evidence, deterministic analysis, sufficiency checks, neutral pathway comparison, and auditable human review.

This document is the current canonical architecture overview. Older architecture notes remain in `docs/` as portfolio history and should not be treated as the active product contract.

## Product Architecture

```text
Decision Question
  -> Decision Context
  -> Supporting Evidence
  -> Decision Assessment
  -> Human Review
  -> Export
```

Current Project is a secondary persistent container for related questions, evidence, assessments, timeline, delta, and review state. The system does not choose a best pathway, rank decisions, assign probabilities, provide legal advice, provide investment advice, or make final decisions.

## Runtime Architecture

```text
Browser Decision Assessment interface
  -> FastAPI app.py
  -> Local JSON project storage
  -> Deterministic Python modules
  -> Markdown, TXT, JSON, trace, and metadata artifacts
```

## Primary Layers

| Layer | Responsibility |
| --- | --- |
| Launch Experience | Starts the local app and opens `http://localhost:8000`. |
| Product Entry | Landing page at `/`; `/workspace` remains a compatibility route to the current interface. |
| Assessment UI | Vanilla HTML/CSS/JavaScript under `dashboard/`. |
| API Layer | FastAPI routes in `app.py`. |
| Project Storage | Local JSON project, evidence, review, timeline, and delta state. |
| Decision Engine | Deterministic analysis, evidence sufficiency, neutral pathway, and artifact completeness modules. |
| Review Layers | Evidence Intelligence, Decision Readiness, Pathways, Comparison, and Review. |
| Artifacts | Local Markdown, TXT, JSON, trace, and metadata files. |

## Key Modules

| Module | Purpose |
| --- | --- |
| `app.py` | FastAPI entrypoint, product routes, project routes, analysis routes, and artifact downloads. |
| `src/project_workspace.py` | Local project storage, questions, evidence library, timeline, delta, and review state. |
| `src/evidence_intelligence.py` | Deterministic evidence duplicate, conflict, novelty, freshness, coverage, and source-diversity support. |
| `src/decision_readiness.py` | Evidence-to-framework readiness mapping with gaps, assumptions, unknowns, and reviewer questions. |
| `src/decision_pathways.py` | Reviewer-facing pathway drafts without ranking or recommendation. |
| `src/pathway_comparison.py` | Categorical side-by-side pathway comparison. |
| `src/decision_review.py` | Reviewer-controlled statuses, notes, unresolved questions, and review summary. |
| `src/decision_assessment.py` | Neutral assessment contract, renderer, and isolated legacy normalization. |
| `src/evidence_sufficiency.py` | Deterministic evidence-workflow tier with explicit non-probability boundary. |
| `src/artifact_completeness.py` | Internal field-presence and review-structure checks. |
| `src/analysis_service.py` | Coordinates deterministic analysis execution and artifact persistence. |
| `dashboard/project.js` | Browser behavior for Current Project context and project-backed review panels. |

## Data Flow

```text
Reviewer selects an optional Current Project
  -> defines the Decision Question
  -> adds Decision Context
  -> supplies or accepts Supporting Evidence
  -> generates a deterministic Decision Assessment
  -> performs Human Review
  -> exports local artifacts
```

Evidence Intelligence, Decision Readiness, pathway drafts, comparison, timeline, and delta remain supporting review capabilities behind this primary flow.

## Storage Model

The repository uses local files:

- Project JSON files under `data/projects/`.
- Run artifacts under `outputs/runs/`.
- Demo artifacts under `demo_case_outputs/`.
- Static dashboard assets under `dashboard/`.

No database, cloud storage, queue, background worker, or managed infrastructure is required.

## Product Boundaries

The architecture intentionally avoids:

- autonomous browsing
- autonomous monitoring
- autonomous agents
- hidden LLM orchestration
- external RAG frameworks
- databases
- cloud deployment
- legal conclusions
- investment recommendations
- final decision automation

Evidence retrieval, when used, creates reviewable evidence candidates. Accepted evidence enters the project Evidence Library only after reviewer action.

## Enterprise Quality Principles

- Deterministic outputs should be reproducible from local inputs and project state.
- Evidence should remain traceable through durable IDs and metadata.
- Reviewer state should be explicit and auditable.
- Public documentation should distinguish current product behavior from historical roadmap material.
- Launch and setup should feel like opening local software, not operating a developer server.
