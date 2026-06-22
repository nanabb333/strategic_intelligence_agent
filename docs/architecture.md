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
  -> context_retriever
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
src/                Application source code.
```

## Source Modules

| Module | Responsibility |
| --- | --- |
| `document_loader.py` | Load and normalize source documents. |
| `issue_extractor.py` | Extract key issues, actors, events, and uncertainties. |
| `scenario_classifier.py` | Classify issues into scenario types and strategic frames. |
| `historical_retriever.py` | Retrieve relevant historical analogues from a knowledge base. |
| `context_retriever.py` | Retrieve current context from configured sources or supplied material. |
| `implication_analyzer.py` | Analyze implications, risks, opportunities, and decision relevance. |
| `brief_generator.py` | Produce the final executive intelligence brief. |
| `run_agent.py` | Orchestrate the end-to-end workflow. |

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

