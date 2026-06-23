# Architecture

## High-Level Design

Strategic Intelligence Agent is organized as a deterministic, tool-selecting
agent. V3 keeps the existing modular tools but adds an Agent Router that decides
which tools should run for a given document.
V4 adds an intelligence reasoning layer that interprets the same event through
multiple analytic lenses.
V4.5 adds a bilingual non-AI user layer with guided questions and deterministic
output adaptation.
V5 adds an evaluation layer that benchmarks the existing workflow without
changing the analytical pipeline.
V6 adds a local FastAPI application layer that lets the dashboard call the real
Python pipeline and save run artifacts.

```text
Input Document
  -> language / guided question / output mode selection
  -> document_loader
  -> agent_router
  -> tool_registry
  -> selected tools
  -> result synthesis
  -> multi_lens_analyzer
  -> evidence_assessor
  -> output_adapter
  -> outputs/
  -> evaluator
  -> evaluation/
  -> FastAPI app
  -> outputs/runs/
```

## Directory Layout

```text
docs/                          Project documentation and portfolio narrative.
data/                          Local input data, sample source material, and fixtures.
knowledge_base/                Curated historical analogues.
knowledge_base/current_context/ Local current-context knowledge base files.
examples/                      Example inputs, runs, and generated artifacts.
evaluation/                    Benchmark cases, generated results, and evaluation summary.
outputs/                       Generated briefs and intermediate workflow outputs.
outputs/runs/                  Local app run folders and downloadable artifacts.
scripts/                       Validation and utility scripts.
src/                           Application source code.
```

## Source Modules

| Module | Responsibility |
| --- | --- |
| `agent_router.py` | Analyze document metadata and select tools for the route. |
| `tool_registry.py` | Register available deterministic tools for future extensibility. |
| `document_loader.py` | Load and normalize source documents. |
| `issue_extractor.py` | Extract core issue, actors, regions, industries, policy terms, companies, document type, and uncertainties. |
| `scenario_classifier.py` | Classify issues into deterministic scenario categories using keyword matches. |
| `historical_retriever.py` | Retrieve top historical analogues from `knowledge_base/historical_analogues.csv`. |
| `context_retriever.py` | Retrieve top current-context findings from local Markdown KB files. |
| `implication_analyzer.py` | Combine historical analogues and current context into similarities, differences, considerations, and questions. |
| `brief_generator.py` | Produce the final executive intelligence brief with evidence traces. |
| `mechanism_detector.py` | Map scenarios and issue metadata to strategic mechanisms. |
| `multi_lens_analyzer.py` | Generate competing interpretations across analytic lenses. |
| `evidence_assessor.py` | Assess supporting, weakening, and missing evidence with qualitative labels. |
| `response_playbook_retriever.py` | Retrieve observed historical choices, outcomes, and cross-domain lessons. |
| `output_adapter.py` | Adapt generated briefs into beginner, analyst, and executive formats with deterministic localization framing. |
| `evaluator.py` | Run benchmark cases and calculate scenario, mechanism, lens, response, and overall scores. |
| `run_agent.py` | Orchestrate the end-to-end workflow. |

## V6 Local App Layer

V6 adds `app.py`, a local-only FastAPI backend:

1. `POST /analyze` receives dashboard text and user selections.
2. The backend runs the existing deterministic pipeline.
3. A unique run folder is created under `outputs/runs/`.
4. `analysis.json`, `brief.md`, `brief.txt`, `agent_trace.json`,
   `metadata.json`, and `input.txt` are saved.
5. `GET /runs` and `GET /run/{run_id}` support history and retrieval.
6. Download endpoints serve Markdown, TXT, and JSON artifacts.

## V5 Evaluation Layer

V5 measures the existing pipeline rather than adding analytical features:

1. Benchmark cases define expected scenarios, mechanisms, lenses, and response
   categories.
2. The evaluator runs the existing deterministic modules.
3. Results are written to `evaluation/benchmark_results.csv`.
4. Aggregate metrics are summarized in `evaluation/evaluation_summary.md`.
5. The dashboard displays the latest benchmark results and known limitations.

## V4.5 Non-AI User Layer

V4.5 adds product controls around the existing pipeline:

1. Users select English, Simplified Chinese, or Traditional Chinese.
2. Users choose a guided question instead of writing a prompt.
3. Users choose beginner, analyst, or executive output mode.
4. The dashboard keeps source labels visible while presenting localized UI text.
5. The output adapter generates deterministic localized framing without using
   external translation APIs.

## V4 Intelligence Reasoning Layer

V4 adds reasoning artifacts after retrieval:

1. Mechanisms are detected from scenario and issue metadata.
2. The event is interpreted through economics, political economy,
   international relations, legislative / regulatory, and business strategy
   lenses.
3. Evidence support is assessed as Limited, Moderate, or Substantial.
4. Historical response patterns and cross-domain lessons are added.
5. Monitoring considerations are presented without advice language.

## V3 Agent Router

V2 always ran a mostly fixed sequence. V3 introduces deterministic tool
selection:

1. The router inspects document type, scenario type, industries, actors, and
   keywords.
2. The registry exposes available tools.
3. The router selects or skips tools and records why.
4. The runner executes selected tools in route order.
5. The brief includes Agent Execution Trace, Tool Decisions, Evidence Sources,
   and Analysis Path.

Example routing:

- Export Controls: run issue extraction, classification, historical retrieval,
  context retrieval, implication analysis, and brief generation.
- Corporate Earnings: run issue extraction, classification, historical
  retrieval, implication analysis, and brief generation; skip context retrieval
  when policy or operational context is not relevant.
- Supply Chain Disruption: run the full route including context retrieval.

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
- Agent Router.
- Tool Registry.

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
