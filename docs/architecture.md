# Architecture

## High-Level Design

Strategic Intelligence Agent is organized as a modular pipeline. Each module has
a narrow responsibility and passes structured data to the next stage.

```text
Input Document
  -> document_loader
  -> issue_extractor
  -> scenario_classifier
  -> historical_retriever
  -> implication_analyzer
  -> brief_generator
  -> outputs/
```

## Directory Layout

```text
docs/               Project documentation and portfolio narrative.
data/               Local input data, sample source material, and fixtures.
knowledge_base/     Curated historical analogues and reference material.
examples/           Example inputs, runs, and generated artifacts.
outputs/            Generated briefs and intermediate workflow outputs.
scripts/            Validation and utility scripts.
src/                Application source code.
```

## Source Modules

| Module | Responsibility |
| --- | --- |
| `document_loader.py` | Load and normalize source documents. |
| `issue_extractor.py` | Extract core issue, actors, regions, industries, policy terms, companies, document type, and uncertainties. |
| `scenario_classifier.py` | Classify issues into deterministic scenario categories using keyword matches. |
| `historical_retriever.py` | Retrieve top historical analogues from `knowledge_base/historical_analogues.csv`. |
| `implication_analyzer.py` | Analyze business, geopolitical, market-context, and operational-risk implications. |
| `brief_generator.py` | Produce the final executive intelligence brief. |
| `run_agent.py` | Orchestrate the end-to-end workflow. |

## V0.5 Retrieval Design

The V0.5 system does not use paid APIs or LLM calls. Historical retrieval is
deterministic:

1. The extractor identifies structured terms from the input document.
2. The classifier assigns one primary scenario and a classification confidence
   label of High, Medium, or Low.
3. The retriever loads the local analogue CSV and scores cases using scenario
   type match, keyword overlap, industry overlap, and actor overlap.
4. The top three cases are passed into implication analysis and brief
   generation.

## Reuse From Prior Project

The prior `financial_rubric_agent` architecture can map cleanly into this
system if the old files are recovered:

| Prior Concept | New Strategic Intelligence Concept |
| --- | --- |
| Document input | Document loader |
| Rubric scoring | Scenario classification and issue assessment |
| AI writing | Executive brief generation |
| Prompt templates | Stage-specific analysis prompts |
| CLI runner | Agent workflow orchestrator |

## Design Constraints

- Keep financial and strategic analysis separate from investment advice.
- Preserve traceability from conclusions back to source material.
- Prefer structured intermediate outputs over opaque free-form text.
- Make each workflow stage testable independently.
- Treat historical analogues as comparison aids, not predictions.
