# Strategic Intelligence Agent

An agentic decision-support workflow that converts documents, articles, policy texts, and earnings excerpts into structured executive intelligence briefs.

## Project Overview

Strategic Intelligence Agent is a V1.0 portfolio project that demonstrates how a modular agent workflow can support analyst productivity. It takes source text, extracts strategic issues, classifies the scenario, retrieves historical analogues, retrieves current context from a local knowledge base, synthesizes similarities and differences, and generates a concise executive intelligence brief.

The project evolved from an earlier `financial_rubric_agent`. That older logic is preserved under `legacy/financial_rubric_agent/` for project history, but the active V1.0 workflow lives in `src/`.

## Business Problem

Executives and analysts often need to turn messy source material into decision-ready intelligence quickly. Source documents can include policy announcements, market commentary, company disclosures, earnings excerpts, or operational memos. The challenge is not simply summarization; the useful output should identify issues, frame the scenario, surface analogues, add current context, separate similarities from differences, and produce a brief that supports discussion.

Strategic Intelligence Agent is designed to make that workflow repeatable, inspectable, and evidence-aware.

## What This Is / Is Not

This is:

- An analyst productivity tool.
- A strategic decision-support workflow.
- A modular agent architecture for structured intelligence briefs.
- A portfolio demonstration of retrieval, workflow orchestration, and business analytics.

This is not:

- A trading advisor.
- A forecasting system.
- An investment recommendation system.
- A source of buy, sell, hold, timing, or portfolio allocation advice.

## Agent Workflow

```text
Document
-> Issue Extraction
-> Scenario Classification
-> Historical Analogue Retrieval
-> Current Context Retrieval
-> Intelligence Synthesis
-> Executive Intelligence Brief
```

The V1.0 implementation is deterministic and uses only local files plus the Python standard library. It does not use paid APIs or LLM calls.

## Repository Structure

```text
docs/                          Project documentation and portfolio narrative.
data/                          Local input data and future fixtures.
examples/                      Example source documents.
knowledge_base/                Curated historical analogue records.
knowledge_base/current_context/ Local current-context KB files by domain.
legacy/financial_rubric_agent/ Preserved prior project code and historical reports.
outputs/                       Generated executive intelligence briefs.
scripts/                       Validation scripts.
src/                           Active V1.0 agent workflow modules.
```

Key active modules:

| File | Purpose |
| --- | --- |
| `src/document_loader.py` | Loads plain text and Markdown documents. |
| `src/issue_extractor.py` | Extracts core issue, actors, regions, industries, policy terms, companies, and document type. |
| `src/scenario_classifier.py` | Classifies issues using deterministic keyword matching. |
| `src/historical_retriever.py` | Retrieves top historical analogues from `knowledge_base/historical_analogues.csv`. |
| `src/context_retriever.py` | Retrieves current context from local Markdown context KB files. |
| `src/implication_analyzer.py` | Combines historical analogues and current context into similarities, differences, considerations, and questions. |
| `src/brief_generator.py` | Generates the Markdown executive intelligence brief with evidence traces. |
| `src/run_agent.py` | Orchestrates the full workflow. |

## V0.5 Capabilities

- Added `knowledge_base/historical_analogues.csv` with public-history analogue cases.
- Extracted structured fields from source documents using deterministic keyword and pattern matching.
- Classified scenarios into categories such as Export Controls, Industrial Policy, Sanctions, Supply Chain Disruption, Regulatory Action, Military / Security Shock, Earnings / Corporate Disclosure, Strategic Investment, Trade Policy, and Other.
- Retrieved the top three historical analogues using scenario match, keyword overlap, industry overlap, and actor overlap.
- Generated upgraded executive briefs and validation coverage.

## V1.0 Capabilities

- Adds deterministic current-context retrieval from `knowledge_base/current_context/`.
- Adds 20 context entries across semiconductors, banking, supply chain, energy, trade policy, export controls, industrial policy, and sanctions.
- Combines historical analogues with current context in an intelligence synthesis layer.
- Generates observed similarities, observed differences, business considerations, operational considerations, geopolitical considerations, and strategic questions.
- Adds evidence traceability for source document findings, historical analogue records, and current context records.
- Upgrades the executive brief format for portfolio-ready decision-support output.
- Adds `scripts/validate_v10.py` for context retrieval, analogue retrieval, output generation, evidence trace, and forbidden language checks.

## Historical Analogue Retrieval

The historical retriever is intentionally simple and inspectable:

1. Load cases from `knowledge_base/historical_analogues.csv`.
2. Score each case against the extracted issue and scenario classification.
3. Add points for matching scenario type, overlapping keywords, overlapping industries, and overlapping actors.
4. Return the top three cases with a similarity reason, caution note, and evidence trace.

Historical analogues are used for comparison and structured reasoning only. They are not forecasts.

## Current Context Retrieval

Historical analogues alone are useful but incomplete. A past case can show structural similarity, while current context explains standing constraints, stakeholders, and monitoring considerations relevant to the present issue.

The V1.0 context retriever:

1. Identifies extracted industries and scenario classification.
2. Loads Markdown entries from `knowledge_base/current_context/`.
3. Scores entries using industry match, scenario match, and keyword overlap.
4. Returns top context findings with evidence traces.

This improves decision support because the brief can compare what the issue may resemble with what currently requires monitoring.

## Sample Run

```bash
python3 src/run_agent.py examples/chips_act_example.md --output outputs/chips_act_brief.md
```

Expected result:

```text
Wrote executive brief to outputs/chips_act_brief.md
```

## Example Commands

```bash
python3 src/run_agent.py examples/chips_act_example.md --output outputs/chips_act_brief.md
python3 src/run_agent.py examples/banking_earnings_example.md --output outputs/banking_earnings_brief.md
python3 src/run_agent.py examples/red_sea_shipping_example.md --output outputs/red_sea_shipping_brief.md
python3 scripts/validate_v10.py
```

Sample outputs:

- `outputs/chips_act_brief.md`
- `outputs/banking_earnings_brief.md`
- `outputs/red_sea_shipping_brief.md`
- `outputs/export_controls_brief.md`
- `outputs/earnings_disclosure_brief.md`
- `outputs/supply_chain_brief.md`

## Limitations

- V1.0 is deterministic and keyword-based.
- It does not call LLMs or paid APIs.
- It does not perform live web retrieval.
- It does not generate forecasts or probabilities.
- It does not provide trading advice or investment recommendations.
- Historical and context records are concise local examples and should be checked against primary sources for production use.

## Portfolio Value

This project demonstrates:

- Agent workflow decomposition.
- Deterministic retrieval over local knowledge bases.
- Evidence-aware synthesis.
- Structured document analysis.
- Strategic and business analytics framing.
- Executive-facing brief generation.
- Responsible AI positioning with clear non-advisory boundaries.

The repository is intentionally designed to be easy for reviewers to scan: documentation explains the product direction, `src/` shows the workflow implementation, and `legacy/` preserves the project evolution.

## Roadmap

### V1.0

- Add deterministic current context retrieval.
- Add evidence traceability.
- Add intelligence synthesis across analogues and context.
- Add V1.0 validation and portfolio case study documentation.

### V2.0

- Add optional LLM provider support behind the existing deterministic interfaces.
- Add richer context records with source URLs and dates.
- Add structured JSON intermediate artifacts.
- Add tests for scoring and retrieval edge cases.
- Add a lightweight UI for portfolio demos.

