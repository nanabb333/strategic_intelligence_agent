# Strategic Intelligence Decision Companion

A Decision Intelligence Platform for evidence-aware strategic decision support.

- Structured decision reasoning
- Historical analogue analysis
- Evidence-aware recommendations
- Qualitative confidence assessment
- Deterministic decision quality evaluation

## Why This Project Exists

Most AI systems are designed to answer questions. This platform is designed to structure complex decisions.

Strategic decisions often involve uncertain source material, incomplete evidence, trade-offs, historical context, and changing conditions. A useful decision-support system should not only summarize what was provided. It should clarify the decision, separate evidence from inference, surface assumptions, compare relevant historical analogues, identify monitoring signals, and make limitations visible.

Strategic Intelligence Decision Companion exists to make that workflow reviewable. It turns business, policy, supply-chain, market-access, and geopolitical source material into structured decision briefs that can be inspected by analysts, engineers, product leaders, and external reviewers.

The product does not predict the future. It supports human judgment by organizing evidence, reasoning, confidence, and evaluation in a repeatable local workflow.

## Product Overview

```text
User Input
  |
  v
Decision Intelligence Framework
  |
  v
Evidence
  |
  v
Historical Knowledge
  |
  v
Reasoning
  |
  v
Confidence
  |
  v
Evaluation
  |
  v
Decision Brief
```

The output is a local decision brief with downloadable Markdown, TXT, JSON, trace, metadata, and input artifacts.

## Core Capabilities

| Capability | Purpose | Representative Components |
| --- | --- | --- |
| Decision Framework | Structures ambiguous source material into a decision-support workflow. | [Decision Intelligence Framework](docs/DecisionIntelligenceFramework.md), [Product Overview](docs/ProductOverview.md) |
| Evidence Ledger | Makes supporting observations, inferences, limitations, and claims reviewable. | [Evidence Architecture](docs/EvidenceArchitecture.md), `evidence_ledger` |
| Historical Analogues | Compares current situations with relevant historical structures. | Local knowledge base, historical analogue retrieval |
| Confidence Assessment | States qualitative confidence, assumptions, unknowns, and change triggers. | `confidence_assessment`, [Evidence Architecture](docs/EvidenceArchitecture.md) |
| Decision Quality Evaluation | Applies deterministic product-quality checks to generated analysis artifacts. | `decision_quality_evaluation`, [Evaluation Strategy](docs/EvaluationStrategy.md) |
| Monitoring Signals | Identifies what should be watched as conditions change. | Decision brief monitoring sections, change triggers |
| Case Studies | Shows evidence, confidence, and evaluation in reviewer-friendly examples. | [V2 Case Studies](docs/case_studies/semiconductor_export_controls.md) |
| Research Direction | Separates product QA from future research validation. | [Research Agenda](docs/research/ResearchAgenda.md), [Benchmark Strategy](docs/research/BenchmarkStrategy.md) |

## Example Workflow

User asks:

```text
What should a semiconductor manufacturer monitor after new export controls?
```

The platform structures the work as:

```text
Input
  |
  v
Evidence extraction
  |
  v
Historical analogue comparison
  |
  v
Decision recommendation
  |
  v
Confidence and assumptions
  |
  v
Monitoring signals
  |
  v
Decision quality evaluation
```

The result is not a standalone answer or forecast. It is a reviewable decision brief that distinguishes evidence, inference, recommendation, uncertainty, and follow-up monitoring.

## Repository Architecture

| Area | Role |
| --- | --- |
| `app.py` | Thin FastAPI entrypoint for local routes and dashboard serving. |
| `src/` | Analysis service, deterministic pipeline, artifact generation, evidence, confidence, and evaluation modules. |
| `dashboard/` | Static local dashboard for input, run review, and artifact downloads. |
| `knowledge_base/` | Local mechanism, analogue, outcome, and playbook records. |
| `docs/` | Product, engineering, governance, evidence, evaluation, research, and review documentation. |
| `docs/case_studies/` | V2 case studies showing evidence-aware decision quality artifacts. |
| `docs/research/` | V3 research validation foundation and future research direction. |
| `demo_case_outputs/` | Bundled generated examples for reviewer inspection. |
| `tests/` | Pytest coverage for API behavior and decision-quality foundations. |

## Documentation Guide

Recommended reading path for first-time reviewers:

1. [README](README.md)
2. [Product Overview](docs/ProductOverview.md)
3. [Decision Intelligence Framework](docs/DecisionIntelligenceFramework.md)
4. [Evidence Architecture](docs/EvidenceArchitecture.md)
5. [Review Guide](docs/ReviewGuide.md)
6. [Case Studies](docs/case_studies/semiconductor_export_controls.md)
7. [Research Agenda](docs/research/ResearchAgenda.md)

For the full documentation map, start with the [Documentation Index](docs/DocumentationIndex.md).

## Engineering Highlights

| Area | Implementation |
| --- | --- |
| Application | Local FastAPI app with browser dashboard. |
| Architecture | Thin `app.py`, separated service layer, deterministic analysis pipeline. |
| Artifacts | Markdown, TXT, JSON, trace, metadata, and input records per run. |
| Quality | Ruff, compile checks, pytest, and GitHub Actions CI. |
| Testing | API smoke coverage and focused tests for decision-quality foundations. |
| Maintainability | Stable module boundaries and documentation-first product governance. |

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

## Research Direction

The repository separates four concerns:

| Layer | Role |
| --- | --- |
| Product | Helps users structure strategic decisions from source material. |
| Engineering | Keeps the system local, deterministic, testable, and maintainable. |
| Evaluation | Checks product-quality properties of generated decision-support artifacts. |
| Research | Defines future validation questions without claiming benchmark superiority. |

Version 3 establishes a research-aware foundation. The current repository implements product QA and deterministic decision-quality evaluation; future research work is documented separately in [docs/research](docs/research/ResearchAgenda.md).

## Current Status

| Area | Status |
| --- | --- |
| Architecture | Stable local Decision Intelligence Platform. |
| Documentation | Product, engineering, governance, evidence, evaluation, and research layers complete. |
| Evidence | Decision Case Schema, Evidence Ledger, and Confidence Assessment implemented as additive artifacts. |
| Evaluation | Deterministic Decision Quality Evaluation Harness implemented. |
| Research | V3 research validation foundation documented. |
| CI | Ruff, compile checks, and pytest passing. |
| Portfolio Readiness | Prepared for external review as a mature AI product architecture project. |

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

These are product boundaries, not missing features. The platform is designed for local, reviewable, human-controlled decision support.
