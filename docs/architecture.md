# Architecture

## High-Level Design

Strategic Intelligence Agent is organized as a deterministic, modular pipeline.
Each module has a narrow responsibility and passes structured data to the next
stage.

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
docs/                          Project documentation and portfolio narrative.
data/                          Local input data, sample source material, and fixtures.
knowledge_base/                Curated historical analogues.
knowledge_base/current_context/ Local current-context knowledge base files.
examples/                      Example inputs, runs, and generated artifacts.
outputs/                       Generated briefs and intermediate workflow outputs.
scripts/                       Validation and utility scripts.
src/                           Application source code.
```

## Source Modules

| Module | Responsibility |
| --- | --- |
| `document_loader.py` | Load and normalize source documents. |
| `issue_extractor.py` | Extract core issue, actors, regions, industries, policy terms, companies, document type, and uncertainties. |
| `scenario_classifier.py` | Classify issues into deterministic scenario categories using keyword matches. |
| `historical_retriever.py` | Retrieve top historical analogues from `knowledge_base/historical_analogues.csv`. |
| `context_retriever.py` | Retrieve top current-context findings from local Markdown KB files. |
| `implication_analyzer.py` | Combine historical analogues and current context into similarities, differences, considerations, and questions. |
| `brief_generator.py` | Produce the final executive intelligence brief with evidence traces. |
| `run_agent.py` | Orchestrate the end-to-end workflow. |

## V1.0 Intelligence Layer

The V1.0 system does not use paid APIs or LLM calls. Retrieval and synthesis
are deterministic:

1. The extractor identifies structured terms from the input document.
2. The classifier assigns one primary scenario and a classification confidence
   label of High, Medium, or Low.
3. The historical retriever scores analogue cases using scenario type match,
   keyword overlap, industry overlap, and actor overlap.
4. The context retriever scores local context entries using industry match,
   scenario match, and keyword overlap.
5. The implication analyzer compares historical analogues with current context
   and produces observed similarities, observed differences, business
   considerations, operational considerations, geopolitical considerations, and
   strategic questions.
6. The brief generator reports the source origin for retrieved evidence.

## Evidence Traceability

V1.0 uses explicit source origins:

- Source Document.
- Historical Database.
- Current Context KB.

The goal is not formal citation management. The goal is to make the reasoning
path visible enough for an analyst to review what came from the input document,
what came from historical analogues, and what came from current context records.

## Design Constraints

- Keep financial and strategic analysis separate from investment advice.
- Preserve traceability from conclusions back to source material.
- Prefer structured intermediate outputs over opaque free-form text.
- Make each workflow stage testable independently.
- Treat historical analogues as comparison aids, not predictions.
- Treat current context as monitoring support, not live fact retrieval.

