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

The platform structures the situation as:

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
| Case Studies | Reviewer-friendly examples of evidence, confidence, and evaluation. | [V2 Case Studies](docs/case_studies/semiconductor_export_controls.md) |
| Research Direction | A separate path from product QA toward future research validation. | [Research Agenda](docs/research/ResearchAgenda.md) |

## Architecture

The repository is a local FastAPI application with a deterministic analysis pipeline and downloadable artifacts.

```text
User Input
  |
  v
FastAPI App
  |
  v
Analysis Service
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
| `app.py` | Thin FastAPI entrypoint. |
| `src/` | Analysis service, pipeline, artifacts, evidence, confidence, and evaluation modules. |
| `dashboard/` | Local browser dashboard. |
| `knowledge_base/` | Local mechanism, analogue, outcome, and playbook records. |
| `docs/` | Product, engineering, governance, evidence, evaluation, and research documentation. |
| `demo_case_outputs/` | Bundled generated artifacts for review. |
| `tests/` | Pytest coverage for API behavior and decision-quality foundations. |

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
