# Strategic Intelligence Agent

An agentic decision-support workflow that converts documents, articles, policy texts, and earnings excerpts into structured executive intelligence briefs.

## Project Overview

Strategic Intelligence Agent is a V0.1 portfolio project that demonstrates how a modular LLM-oriented workflow can support analyst productivity. It takes source text, extracts strategic issues, classifies the scenario, retrieves placeholder historical and current context, analyzes implications, and generates a concise executive intelligence brief.

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
-> Current Context Retrieval
-> Implication Analysis
-> Executive Intelligence Brief
```

The V0.1 implementation uses simple deterministic placeholders behind stable module interfaces. Later versions can replace those placeholders with retrieval, structured prompts, external tools, or LLM calls without redesigning the repository.

## Repository Structure

```text
docs/                         Project documentation and migration roadmap.
data/                         Local input data and future fixtures.
examples/                     Example source documents.
knowledge_base/               Future curated historical analogue records.
legacy/financial_rubric_agent/ Preserved prior project code and historical reports.
outputs/                      Strategic Intelligence Agent generated outputs.
src/                          Active V0.1 agent workflow modules.
```

Key active modules:

| File | Purpose |
| --- | --- |
| `src/document_loader.py` | Loads plain text and Markdown documents. |
| `src/issue_extractor.py` | Extracts initial structured issue records. |
| `src/scenario_classifier.py` | Classifies issues into strategic scenario categories. |
| `src/historical_retriever.py` | Provides the historical analogue retrieval interface. |
| `src/context_retriever.py` | Provides the current context retrieval interface. |
| `src/implication_analyzer.py` | Converts issues, classifications, analogues, and context into implications. |
| `src/brief_generator.py` | Generates the Markdown executive intelligence brief. |
| `src/run_agent.py` | Orchestrates the full workflow. |

## V0.1 Capabilities

- Loads `.txt`, `.md`, and `.markdown` source documents.
- Runs the full Strategic Intelligence Agent workflow from the command line.
- Produces a Markdown executive intelligence brief.
- Includes a sample source document and sample generated output.
- Preserves the prior financial rubric project in `legacy/` without mixing it into the active workflow.
- Keeps the project positioned as decision support, not investment advice.

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

- Add structured JSON intermediate outputs.
- Add a small curated historical analogue knowledge base.
- Improve scenario classification rules.
- Add tests for each workflow stage.
- Add richer sample documents across policy, market, and company contexts.

### V1.0

- Add configurable LLM provider support.
- Add retrieval over curated analogues.
- Add source traceability and citations.
- Add current context retrieval through approved sources.
- Add a CLI or lightweight UI for portfolio demos.

