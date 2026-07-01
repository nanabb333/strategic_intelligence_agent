# Strategic Intelligence Decision Companion

Strategic Intelligence Decision Companion is a local-first Enterprise Decision Intelligence Platform. It helps reviewers structure complex decisions through evidence, deterministic analysis, decision readiness, pathway drafting, pathway comparison, and auditable human review.

It is not a chatbot, autonomous researcher, monitoring system, forecasting engine, investment advisor, legal advisor, or autonomous decision maker.

## Problem

Strategic decisions often fail because evidence is fragmented, assumptions are hidden, trade-offs are hard to compare, and teams do not know what would change their view. General text generation does not solve those workflow problems by itself.

Repo 5 turns ambiguous source material and project evidence into structured decision-support artifacts that remain reviewable, traceable, and bounded by deterministic rules.

## Solution

The product provides a reviewer-first workspace:

```text
Project
  -> Questions
  -> Evidence Library
  -> Evidence Intelligence
  -> Decision Readiness
  -> Domain Decision Evaluation
  -> Decision Pathway Drafts
  -> Pathway Comparison Matrix
  -> Decision Review
  -> Decision Timeline and Delta
```

Evidence can be retrieved only through explicit user action. Retrieved items enter a review queue first. Accepted evidence becomes part of the project Evidence Library. Analysis and decision-support views remain deterministic and do not bypass reviewer control.

## Core Components

| Component | Purpose |
| --- | --- |
| Decision Workspace | Project-scoped questions, evidence, runs, timeline, delta, and review state. |
| Evidence Library | Local JSON evidence store for manual notes and accepted retrieved evidence. |
| Evidence Retrieval | User-triggered candidate retrieval; no autonomous browsing or monitoring. |
| Evidence Intelligence | Deterministic duplicate, conflict, novelty, freshness, coverage, and source-diversity support. |
| Decision Readiness | Evidence and framework coverage map with assumptions, unknowns, gaps, and reviewer questions. |
| Decision Framework Library | Deterministic framework classification for decision questions. |
| Domain Decision Evaluation | Domain-specific evidence mapping with advisory boundaries. |
| Decision Pathway Drafts | Reviewer-facing pathway scaffolds; not rankings or recommendations. |
| Pathway Comparison Matrix | Categorical side-by-side comparison; no scores or probabilities. |
| Decision Review | Reviewer-controlled statuses, notes, unresolved questions, and review summary. |
| Decision Brief | Existing deterministic analysis artifact with evidence, confidence, monitoring signals, and quality checks. |

## Architecture

```text
Dashboard (vanilla HTML/CSS/JS)
  -> FastAPI app.py
  -> Project Workspace (local JSON)
  -> Deterministic Decision Engine
  -> Evidence / Readiness / Pathway / Review modules
  -> Markdown, TXT, JSON run artifacts
```

The platform uses local files and deterministic Python modules. It does not require a database, cloud service, background worker, external UI framework, LangGraph, RAG framework, autonomous agents, or scheduled retrieval.

Important modules:

- `app.py`: FastAPI routes for health, analysis, project workspace, retrieval, and read-only decision views.
- `src/project_workspace.py`: local JSON project storage, questions, evidence library, timeline, delta, and review state.
- `src/evidence_intelligence.py`: deterministic evidence-set review support.
- `src/decision_readiness.py`: evidence-to-framework readiness mapping.
- `src/decision_pathways.py`: deterministic pathway draft generation.
- `src/pathway_comparison.py`: categorical pathway comparison.
- `src/decision_review.py`: reviewer-controlled review layer.
- `dashboard/project.js`: Decision Workspace dashboard behavior.

## Enterprise Design Principles

- Deterministic: no hidden autonomous reasoning loop.
- Reviewer-first: humans review evidence, pathway drafts, comparison items, and notes.
- Evidence-backed: accepted evidence keeps durable IDs and trace metadata.
- Auditable: project runs link back to project, question, and evidence IDs.
- Local-first: project and run artifacts are stored locally as JSON, Markdown, and TXT.
- English-only: English is the official product language for this release.

## Local Testing

Install dependencies, then run:

```bash
python3 -m pytest
```

Start the local API:

```bash
python3 -m uvicorn app:app --reload
```

Open the dashboard:

```text
http://127.0.0.1:8000/dashboard/
```

Reviewer workflow:

1. Create a project.
2. Add a decision question.
3. Add or accept evidence into the Evidence Library.
4. Select evidence for analysis.
5. Run the deterministic analysis.
6. Inspect Evidence Intelligence, Decision Readiness, Domain Decision Evaluation, Decision Pathway Drafts, and Pathway Comparison Matrix.
7. Record Decision Review statuses, notes, and unresolved questions.
8. Review Decision Timeline, Decision Delta, and downloadable Markdown/TXT/JSON artifacts.

## Demo Scenarios

Consolidated demo walkthroughs are documented in [docs/GettingStarted/DemoScenarios.md](docs/GettingStarted/DemoScenarios.md):

- Federal Reserve Rate Hike
- Export Controls
- Supply Chain Disruption
- Insurance Company Review
- Strategic Partnership

Generated workspace artifacts are available under `demo_case_outputs/`, including the V4 workspace demo.

## Documentation

Start with [docs/DocumentationIndex.md](docs/DocumentationIndex.md).

Key consolidation documents:

- [Product Terminology](docs/ProductTerminology.md)
- [Repository Maturity Review](docs/RepositoryMaturityReview.md)
- [Enterprise Architecture](docs/Architecture/EnterpriseArchitecture.md)
- [Module Boundaries](docs/Architecture/ModuleBoundaries.md)
- [API Conventions](docs/Developer/APIConventions.md)
- [Naming Review](docs/Reference/NamingReview.md)
- [Changelog](CHANGELOG.md)

## Future Roadmap

Recommended next roadmap:

1. Continue consolidating older historical docs into the new hierarchy.
2. Add tests for enterprise terminology and English-only dashboard/API boundaries.
3. Add reviewer-controlled Decision Record only after the current Decision Review layer stabilizes.
4. Integrate future retrieval providers behind the existing provider interface without adding autonomous behavior.
