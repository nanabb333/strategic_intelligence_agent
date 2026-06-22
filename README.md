# Strategic Intelligence Agent

An agentic decision-support workflow that converts documents, articles, policy texts, and earnings excerpts into structured executive intelligence briefs.

## Project Overview

Strategic Intelligence Agent is a V0.5 portfolio project that demonstrates how a modular agent workflow can support analyst productivity. It takes source text, extracts strategic issues, classifies the scenario, retrieves historical analogues from a local knowledge base, analyzes implications, and generates a concise executive intelligence brief.

The project evolved from an earlier `financial_rubric_agent`. That older logic is preserved under `legacy/financial_rubric_agent/` for project history, but the active V0.1 workflow lives in `src/`.

## Business Problem

Executives and analysts often need to turn messy source material into decision-ready intelligence quickly. Source documents can include policy announcements, market commentary, company disclosures, earnings excerpts, or operational memos. The challenge is not simply summarization; the useful output should identify issues, frame the scenario, surface analogues, separate context from implication, and produce a brief that supports discussion.

Strategic Intelligence Agent is designed to make that workflow repeatable and inspectable.

## What This Is / Is Not

This is:

- An analyst productivity tool.
- A strategic decision-support workflow.
- A modular agent architecture for structured intelligence briefs.
- A portfolio demonstration of LLM applications, workflow orchestration, and business analytics.

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
-> Implication Analysis
-> Executive Intelligence Brief
```

The V0.5 implementation is deterministic and uses only local files plus the Python standard library. It does not use paid APIs or LLM calls.

## Repository Structure

```text
docs/                         Project documentation and migration roadmap.
data/                         Local input data and future fixtures.
examples/                     Example source documents.
knowledge_base/               Curated historical analogue records.
legacy/financial_rubric_agent/ Preserved prior project code and historical reports.
outputs/                      Strategic Intelligence Agent generated outputs.
scripts/                      Validation scripts.
src/                          Active V0.5 agent workflow modules.
```

Key active modules:

| File | Purpose |
| --- | --- |
| `src/document_loader.py` | Loads plain text and Markdown documents. |
| `src/issue_extractor.py` | Extracts core issue, actors, regions, industries, policy terms, companies, and document type. |
| `src/scenario_classifier.py` | Classifies issues using deterministic keyword matching. |
| `src/historical_retriever.py` | Retrieves top historical analogues from `knowledge_base/historical_analogues.csv`. |
| `src/implication_analyzer.py` | Converts issues, classifications, and analogues into structured implications and strategic questions. |
| `src/brief_generator.py` | Generates the Markdown executive intelligence brief. |
| `src/run_agent.py` | Orchestrates the full workflow. |

## V0.1 Capabilities

- Loads `.txt`, `.md`, and `.markdown` source documents.
- Runs the full Strategic Intelligence Agent workflow from the command line.
- Produces a Markdown executive intelligence brief.
- Includes a sample source document and sample generated output.
- Preserves the prior financial rubric project in `legacy/` without mixing it into the active workflow.
- Keeps the project positioned as decision support, not investment advice.

## V0.5 Capabilities

- Adds `knowledge_base/historical_analogues.csv` with public-history analogue cases.
- Extracts structured fields from source documents using deterministic keyword and pattern matching.
- Classifies scenarios into categories such as Export Controls, Industrial Policy, Sanctions, Supply Chain Disruption, Regulatory Action, Military / Security Shock, Earnings / Corporate Disclosure, Strategic Investment, Trade Policy, and Other.
- Retrieves the top three historical analogues using scenario match, keyword overlap, industry overlap, and actor overlap.
- Generates upgraded executive briefs with extracted entities, scenario confidence labels, historical analogues, current relevance, implications, strategic questions, and limitations.
- Includes a validation script that checks the knowledge base, runs examples through the pipeline, confirms outputs exist, and screens generated briefs for advice-style language.

## Historical Analogue Retrieval

The V0.5 retriever is intentionally simple and inspectable:

1. Load cases from `knowledge_base/historical_analogues.csv`.
2. Score each case against the extracted issue and scenario classification.
3. Add points for matching scenario type, overlapping keywords, overlapping industries, and overlapping actors.
4. Return the top three cases with a similarity reason and caution note.

Historical analogues are used for comparison and structured reasoning only. They are not forecasts.

## Sample Run

```bash
python3 src/run_agent.py examples/sample_document.md --output outputs/sample_brief.md
```

Expected result:

```text
Wrote executive brief to outputs/sample_brief.md
```

To verify source syntax:

```bash
python3 -m compileall src
```

## Example Commands

```bash
python3 src/run_agent.py examples/export_controls_example.md --output outputs/export_controls_brief.md
python3 src/run_agent.py examples/earnings_disclosure_example.md --output outputs/earnings_disclosure_brief.md
python3 src/run_agent.py examples/supply_chain_example.md --output outputs/supply_chain_brief.md
python3 scripts/validate_v05.py
```

Sample outputs:

- `outputs/export_controls_brief.md`
- `outputs/earnings_disclosure_brief.md`
- `outputs/supply_chain_brief.md`

## Limitations

- V0.5 is deterministic and keyword-based.
- It does not call LLMs or paid APIs.
- It does not perform live current-context retrieval.
- It does not generate forecasts or probabilities.
- It does not provide trading advice or investment recommendations.
- Historical cases are concise public-history examples and should be checked against primary sources for production use.

## Portfolio Value

This project demonstrates:

- LLM application architecture.
- Agent workflow decomposition.
- Tool-ready module boundaries.
- Structured document analysis.
- Strategic and business analytics framing.
- Executive-facing synthesis.
- Responsible AI positioning with clear non-advisory boundaries.

The repository is intentionally designed to be easy for reviewers to scan: documentation explains the product direction, `src/` shows the workflow implementation, and `legacy/` preserves the project evolution.

## Roadmap

### V0.1

- Establish repository architecture.
- Add deterministic workflow scaffolding.
- Generate a sample executive intelligence brief.
- Preserve legacy financial rubric work separately.

### V0.5

- Add deterministic issue extraction, scenario classification, and historical analogue retrieval.
- Add a curated historical analogue knowledge base.
- Add upgraded executive brief sections.
- Add validation coverage for examples and output language.
- Add richer sample documents across policy, corporate disclosure, and supply chain contexts.

### V1.0

- Add configurable LLM provider support.
- Add retrieval over curated analogues.
- Add source traceability and citations.
- Add current context retrieval through approved sources.
- Add a CLI or lightweight UI for portfolio demos.
