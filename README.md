# Strategic Intelligence Decision Companion

[![CI](https://github.com/nanabb333/strategic_intelligence_agent/actions/workflows/ci.yml/badge.svg)](https://github.com/nanabb333/strategic_intelligence_agent/actions/workflows/ci.yml)

Strategic Intelligence Decision Companion is a reviewer-first Enterprise Decision Intelligence Platform. It helps reviewers structure complex strategic decisions as local, deterministic, evidence-backed artifacts that remain open to human inspection.

![Legacy interface placeholder for Strategic Intelligence Decision Companion](portfolio_assets/screenshots/historical/dashboard-overview.png)

> Screenshot status: this pre-Sprint 0 placeholder shows an earlier workspace layout and stale terminology. It is retained until a populated screenshot of the current Decision Assessment interface is captured.

## Problem And Product Value

Strategic decisions become difficult when evidence is fragmented, assumptions are hidden, trade-offs are unclear, and teams cannot see what should change their view. Generating a fluent answer does not solve those problems.

The product makes the decision question, reviewer context, supporting evidence, assessment, limitations, and review state explicit. Projects remain available as persistent containers for related questions and artifacts, but project management is not the primary workflow.

It is designed to help reviewers see:

- what decision actually requires judgment
- which context was supplied by the reviewer
- which evidence supports or weakens the assessment
- which assumptions and unknowns remain
- which pathways deserve comparison
- what requires review or later reassessment

## Decision-First Workflow

```text
Decision Question
  -> Decision Context
  -> Supporting Evidence
  -> Decision Assessment
  -> Human Review
  -> Export
```

The reviewer defines the question and context, controls evidence, inspects the assessment, and makes any final decision. The system does not select a preferred option, rank pathways, assign probabilities, or act autonomously.

## Reviewer Workflow

1. Select or create a Current Project if the work should persist.
2. State the Decision Question.
3. Add optional Decision Context such as background, objectives, and constraints.
4. Add Supporting Evidence by pasting text, uploading a supported file, providing a readable URL, or using accepted project evidence.
5. Generate the deterministic Decision Assessment.
6. Review evidence used, confidence, strategic considerations, assumptions, and limitations.
7. Record human review state and export the required artifacts.

## Core Capabilities

| Capability | Reviewer value |
| --- | --- |
| Decision Assessment | Structures the decision, evidence used, strategic considerations, assumptions, and limitations. |
| Evidence support | Accepts pasted text, supported files, readable URLs, and reviewer-approved project evidence. |
| Evidence Intelligence | Surfaces duplicates, conflicts, freshness, coverage, novelty, and source-diversity concerns. |
| Decision Readiness | Maps evidence coverage, assumptions, unknowns, gaps, and reviewer questions. |
| Pathway comparison | Provides categorical scaffolds for comparison without ranking or recommendation. |
| Human review | Preserves reviewer notes, unresolved questions, statuses, timeline, and decision delta. |
| Local artifacts | Exports Markdown, TXT, JSON, trace, and metadata files for inspection. |

## Three-Minute Demo

1. Read the [Demo Walkthrough](docs/DemoWalkthrough.md).
2. Open the bundled [V4 project demo](demo_case_outputs/v4_workspace/README.md).
3. Inspect its [Evidence Library](demo_case_outputs/v4_workspace/evidence_library.json).
4. Review the first [Decision Brief](demo_case_outputs/v4_workspace/question_1_q_export_controls_immediate/brief.md).
5. Compare the [Decision History](demo_case_outputs/v4_workspace/decision_history.json) and [Decision Delta](demo_case_outputs/v4_workspace/decision_delta.json).

The demo artifacts predate the Sprint 0 interface migration but remain useful examples of project persistence and reviewable outputs.

## Architecture

```text
Browser Decision Assessment interface
  -> FastAPI routes
  -> deterministic Python services and analysis pipeline
  -> local project and run storage
  -> Markdown, TXT, JSON, trace, and metadata artifacts
```

| Area | Role |
| --- | --- |
| `app.py` | FastAPI entrypoint, product routes, and downloads. |
| `src/` | Analysis, evidence, readiness, pathway, review, confidence, and evaluation modules. |
| `dashboard/` | Vanilla HTML, CSS, and JavaScript interface. |
| `knowledge_base/` | Local curated mechanism, analogue, outcome, and playbook records. |
| `data/projects/` | Local project state. |
| `outputs/runs/` | Generated local run artifacts. |
| `tests/` | API, workflow, and decision-quality validation. |

See the canonical [Architecture Overview](docs/architecture.md) and implementation-focused [Engineering Architecture](docs/EngineeringArchitecture.md).

Key implementation modules include:

- `src/analysis_service.py`: stable service entrypoint for analysis.
- `src/analysis_pipeline.py`: explicit deterministic pipeline orchestration.
- `src/project_workspace.py`: Current Project persistence and review state.
- `src/evidence_intelligence.py`: evidence-set review support.
- `src/decision_readiness.py`: evidence-to-framework readiness mapping.
- `src/decision_pathways.py`: non-ranked pathway scaffolds.
- `src/pathway_comparison.py`: categorical pathway comparison.
- `src/decision_review.py`: reviewer-controlled notes and status.

## Quick Start

Python 3.10 or later is required. Install dependencies before the first launch:

```bash
python3 -m pip install -r requirements.txt
```

On macOS, double-click:

```text
launch/Launch Strategic Intelligence Decision Companion.command
```

On Windows, double-click:

```text
launch/Launch Strategic Intelligence Decision Companion.bat
```

Or start from a terminal:

```bash
./run_app.sh
# or
python3 launch.py
```

Open `http://localhost:8000` if the browser does not open automatically. Developers can run `python3 -m uvicorn app:app --reload` and use the compatibility route at `http://127.0.0.1:8000/workspace`.

## Validation

The repository CI and local validation use:

```bash
ruff check .
python3 -m py_compile app.py src/*.py launch.py
python3 -m pytest
node --check dashboard/app.js
node --check dashboard/project.js
```

Passing these checks validates repository behavior covered by the test suite; it does not establish real-world factual accuracy, benchmark superiority, security hardening, or deployment readiness.

Validation covers:

- Python style and syntax
- API and workflow tests
- deterministic decision-quality foundations
- dashboard JavaScript syntax
- repository behavior represented by the current test suite

## Boundaries And Limitations

The product is local-first and single-user. It does not provide:

- autonomous research or autonomous agents
- background monitoring
- forecasting or probability estimates
- preferred-option selection or final decision-making
- legal, investment, or compliance advice
- compliance automation
- authentication or multi-user access control
- cloud deployment or public-internet hardening
- OCR for scanned PDFs
- real-world accuracy guarantees

URL retrieval is user-triggered, not autonomous. All outputs require human review before executive, legal, financial, operational, or geopolitical use.

## Current Version Status

| Milestone | Meaning |
| --- | --- |
| V4.9 | Stable V4 freeze baseline and enterprise design assessment. |
| V4.10 | Reviewer workflow layout correction; no new Decision Intelligence capability. |
| V5 Sprint 0 | Current decision-first information architecture migration. It is not a complete final V5 release. |
| Current branch follow-up | Restores the stable enterprise workbench layout after the Sprint 0 migration. |

The dashboard and landing page identify the current milestone as `V5 Sprint 0`. Runtime `/version` metadata retains software version `5.0.0` and the compatibility label `Enterprise Product Release`, while its `milestone` and `stage` fields identify Sprint 0. The milestone and release notes—not the compatibility label alone—define current release status.

## Canonical Documentation

- [Documentation Index](docs/DocumentationIndex.md)
- [Product Overview](docs/ProductOverview.md)
- [Product Vision](docs/ProductVision.md)
- [Product Terminology](docs/ProductTerminology.md)
- [Architecture Overview](docs/architecture.md)
- [Engineering Architecture](docs/EngineeringArchitecture.md)
- [Demo Walkthrough](docs/DemoWalkthrough.md)
- [Release Notes Index](docs/releases/README.md)
- [Changelog](CHANGELOG.md)

Historical milestone and portfolio documents remain in place for context. Use the [Documentation Index](docs/DocumentationIndex.md) to distinguish the current product contract from historical material.
