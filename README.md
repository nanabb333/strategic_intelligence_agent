# Strategic Intelligence Decision Companion

An AI Decision Intelligence Platform that helps people structure complex strategic decisions, not just summarize information.

Strategic decisions rarely fail because no one can generate text. They fail because evidence is incomplete, trade-offs are unclear, assumptions are hidden, and teams do not know what should change their view.

This project turns ambiguous source material into reviewable decision briefs with evidence, historical analogues, confidence, monitoring signals, and deterministic quality checks.

## The Problem

Modern AI systems are excellent at answering questions, summarizing documents, and generating fluent text. Those capabilities are useful, but they are not the same as decision support.

Strategic decisions require a different shape of reasoning. A product leader, analyst, or executive needs to know what decision is actually being made, which evidence matters, what trade-offs exist, how much uncertainty remains, whether historical cases are relevant, and what should be monitored next.

Strategic Intelligence Decision Companion was built to structure decision-making rather than generate answers. It separates evidence from inference, recommendations from facts, and confidence from certainty. The goal is not to predict outcomes. The goal is to make strategic reasoning explicit enough for human review.

## Before And After

| Traditional AI | Decision Companion |
| --- | --- |
| Summarizes source material | Structures a decision-support workflow |
| Answers a question | Clarifies the decision being made |
| Generates text | Builds a reviewable decision brief |
| Produces a response | Produces evidence-aware recommendations |
| Treats uncertainty as prose | Exposes assumptions, unknowns, and change triggers |
| Ends at the answer | Adds monitoring signals and quality review |

## Product Walkthrough

A semiconductor manufacturer faces new export controls. Management needs to decide whether investment plans, customer exposure reviews, and supply-chain monitoring should change.

The standalone analysis path structures one decision question as:

```text
Source Material
  |
  v
Decision Question
  |
  v
Evidence
  |
  v
Historical Analogues
  |
  v
Decision Brief
  |
  v
Confidence
  |
  v
Monitoring Signals
  |
  v
Decision Quality Review
```

Instead of returning only a summary, the system identifies the decision context, extracts relevant evidence, compares historical patterns, states a recommendation, explains confidence, and records what would require reassessment.

Version 4 adds a local Decision Workspace around that same deterministic engine:

```text
Project
  |
  v
Questions
  |
  v
Evidence Library
  |
  v
Analysis Runs
  |
  v
Decision Timeline
  |
  v
Decision Delta
```

Projects are not chats. A Project is a long-running decision problem. Questions remain independently reviewable analyses, evidence notes are stored in a reusable local library, and completed runs are linked back into a project-level timeline.

Version 4.5 is sequenced around a Decision Context layer before live retrieval:

```text
Project + Question
  |
  v
Selected Evidence IDs
  |
  v
Evidence Bundle
  |
  v
Analysis Run Metadata + Evidence Ledger
  |
  v
Decision Timeline + Decision Delta
```

Live retrieval should only be added after project evidence can flow into this traceable Decision Context. Retrieved evidence never enters analysis automatically. It must be reviewed and accepted into the project evidence library, then selected into an Evidence Bundle before it can affect a run.

## Example Output

```text
Recommendation:
Prepare a staged response rather than immediate restructuring.

Confidence:
Moderate.

Supporting Evidence:
6 evidence items covering customer eligibility, licensing uncertainty,
supplier exposure, compliance burden, market access, and operational timing.

Historical Analogues:
Huawei Entity List restrictions.
ASML export-control exposure.

Next 30-90 Days:
Monitor supplier exposure, licensing approvals, customer eligibility,
implementation rules, margin pressure, and management guidance.

Decision Quality Review:
Checks direct answer quality, evidence use, analogue relevance,
risk identification, monitoring triggers, and overconfidence control.
```

This output is a decision-support artifact. It is not investment advice, legal advice, trading advice, or a claim of future accuracy.

## Core Capabilities

| Capability | What It Provides | Where To Learn More |
| --- | --- | --- |
| Decision Framework | A structured path from ambiguous input to decision brief. | [Decision Intelligence Framework](docs/DecisionIntelligenceFramework.md) |
| Evidence Ledger | Reviewable observations, inferences, supported claims, and limitations. | [Evidence Architecture](docs/EvidenceArchitecture.md) |
| Historical Analogues | Historical comparison without treating past cases as predictions. | [Product Overview](docs/ProductOverview.md) |
| Confidence Assessment | Qualitative confidence, assumptions, unknowns, and change triggers. | [Evidence Architecture](docs/EvidenceArchitecture.md) |
| Decision Quality Evaluation | Deterministic checks for product-quality properties of generated briefs. | [Evaluation Strategy](docs/EvaluationStrategy.md) |
| V4 Project Workspace | Local projects, linked questions, evidence library, decision timeline, and decision delta. | [Version 4 Architecture](docs/Version4Architecture.md) |
| V4.5 Decision Context | Project/question/run linkage, selected Evidence Bundles, durable evidence IDs, workspace state, and retrieval readiness. | [Version 4 Architecture](docs/Version4Architecture.md) |
| Case Studies | Reviewer-friendly examples of evidence, confidence, and evaluation. | [V2 Case Studies](docs/case_studies/semiconductor_export_controls.md) |
| Research Direction | A separate path from product QA toward future research validation. | [Research Agenda](docs/research/ResearchAgenda.md) |
| V4 Architecture | Long-term direction for projects, evidence bundles, traceability, and decision evolution. | [Version 4 Architecture](docs/Version4Architecture.md) |

## Architecture

The repository is a local FastAPI application with a deterministic analysis pipeline, local project workspace storage, and downloadable artifacts.

```text
User Input
  |
  v
FastAPI App
  |
  v
Project Workspace + Analysis Service
  |
  v
Decision Intelligence Pipeline
  |
  v
Evidence + Analogues + Confidence + Evaluation
  |
  v
Markdown, TXT, JSON, Trace, Metadata
```

| Area | Role |
| --- | --- |
| `app.py` | Thin FastAPI entrypoint for health, analysis, run artifacts, downloads, and V4 project routes. |
| `src/` | Analysis service, pipeline, artifacts, evidence, confidence, and evaluation modules. |
| `src/project_workspace.py` | Local JSON project workspace utilities for projects, questions, evidence, decision history, and decision delta. |
| `src/evidence_retrieval.py` | Deterministic user-triggered retrieval candidate module. It should remain downstream of the Decision Context workflow. |
| `dashboard/` | Local browser dashboard, including `dashboard/project.js` for project workspace behavior. |
| `knowledge_base/` | Local mechanism, analogue, outcome, and playbook records. |
| `docs/` | Product, engineering, governance, evidence, evaluation, and research documentation. |
| `demo_case_outputs/` | Bundled generated artifacts for review. |
| `tests/` | Pytest coverage for API behavior and decision-quality foundations. |

V4 uses local JSON files under `data/projects/` for project state. It does not add PostgreSQL, SQLite, Redis, background workers, authentication, cloud services, autonomous browsing, or autonomous monitoring.

V4.5 prioritizes Decision Context before live retrieval. Project-aware runs store project and question linkage, selected evidence IDs, and an Evidence Bundle in run artifacts. Retrieval remains a candidate interface, not an autonomous research system; accepted items are stored only when the user explicitly accepts them into a project.

## Repository Guide

Start here:

1. [Product Overview](docs/ProductOverview.md)
2. [Decision Intelligence Framework](docs/DecisionIntelligenceFramework.md)
3. [Evidence Architecture](docs/EvidenceArchitecture.md)
4. [Review Guide](docs/ReviewGuide.md)
5. [Case Studies](docs/case_studies/semiconductor_export_controls.md)
6. [Research Agenda](docs/research/ResearchAgenda.md)

For the complete map, see the [Documentation Index](docs/DocumentationIndex.md).

## Engineering

The implementation is intentionally lightweight:

- Local FastAPI app
- Thin `app.py`
- Modular service and pipeline structure
- Deterministic analysis components
- Per-run Markdown, TXT, JSON, trace, metadata, and input artifacts
- Ruff, compile checks, pytest, and GitHub Actions CI

## No-VS-Code Local Launch

For non-technical reviewers on macOS:

1. Download or clone this repository.
2. Double-click `start.command`.
3. If macOS blocks it, right-click `start.command`, then choose **Open**.
4. The browser opens the local dashboard at `http://127.0.0.1:8000/dashboard/`.

Run locally:

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn app:app --reload
```

Run validation:

```bash
python3 -m ruff check .
python3 -m compileall app.py src tests
python3 -m pytest
```

## How To Test V4 Locally

1. Start FastAPI:

```bash
python3 -m uvicorn app:app --reload
```

2. Open the dashboard:

```text
http://127.0.0.1:8000/dashboard/
```

3. Create a Project in the V4 Workspace panel.
4. Add and select a project question.
5. Paste source material and click **Build decision brief**.
6. Add a manual Evidence Library note under the active project.
7. Select one or more Evidence Library items to include in the next Evidence Bundle.
8. Add and select a second question, then run analysis again.
9. Inspect the Decision Timeline and Decision Delta in the active project panel.
10. Confirm the run JSON metadata includes `project_id`, `project_question_id`, and selected `evidence_ids`.
11. Use the browser print dialog to print or save PDF. Print styles hide workspace controls and render the results panel full width.

Standalone analysis is still supported: leave no active project selected and run the brief builder as before.

## V4 Release Demo

A complete Version 4 workspace validation demo is stored at:

```text
demo_case_outputs/v4_workspace/
```

It includes a sample project JSON, reusable evidence library sample, two linked question analyses, decision history, deterministic decision delta, and generated Markdown/TXT/JSON run artifacts.

## Research

The repository separates product quality from research validation:

```text
Product QA
  |
  v
Research Validation
  |
  v
Future Human Evaluation
```

The current system implements product QA and deterministic decision-quality evaluation. Future research work is documented separately so the product does not imply scientific proof, benchmark superiority, or real-world predictive accuracy.

## Version 4 Direction

Version 4 evolves the platform into a local Decision Intelligence Workspace: projects, reusable evidence notes, evidence libraries, linked analysis runs, decision history, and traceable recommendation changes over time.

The implemented V4 route is:

```text
Project -> Questions -> Evidence Library -> Analysis Runs -> Decision Timeline -> Decision Delta
```

This remains a professional decision workspace, not a chatbot or autonomous agent. The system does not browse independently, monitor sources in the background, orchestrate agents, or collect evidence without user action.

Version 4.5 introduces Decision Context before live retrieval. A project-aware run can now be traced to the project, project question, selected evidence IDs, and Evidence Bundle used in the deterministic Decision Engine. User-triggered current evidence retrieval remains a later candidate workflow: it creates reviewable items only, does not make decisions, does not update recommendations directly, and does not bypass the deterministic Decision Engine.

## Current Status

| Area | Status |
| --- | --- |
| Architecture | Stable local Decision Intelligence Platform. |
| Documentation | Product, engineering, governance, evidence, evaluation, and research layers complete. |
| Evidence | Decision Case Schema, Evidence Ledger, and Confidence Assessment implemented. |
| Evaluation | Deterministic Decision Quality Evaluation Harness implemented. |
| Research | Version 3 research validation foundation documented. |
| CI | Ruff, compile checks, and pytest passing. |
| Portfolio Readiness | Ready for external review as a mature AI product architecture project. |

## Limitations

The repository intentionally avoids:

- Autonomous web agents
- Live monitoring
- Benchmark superiority claims
- Investment advice
- Legal advice
- Trading advice
- Statistical confidence claims
- Database infrastructure
- Login, auth, or account systems

These boundaries keep the platform local, reviewable, deterministic, and maintainable.
