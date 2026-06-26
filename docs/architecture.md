# Architecture

## Project Vision

Repo 5 is a Strategic Decision Intelligence platform designed to improve decision quality under uncertainty.

Unlike traditional AI analysis tools that primarily summarize information or predict future outcomes, Repo 5 helps users structure complex decisions through explicit reasoning, transparent trade-offs, and evidence-based judgment.

Historical intelligence provides supporting evidence.

Strategic reasoning provides the decision framework.

The objective is not to predict the future.

The objective is to help users make better decisions with incomplete information.

## Architecture at a Glance

Repo 5 is organized as a layered decision intelligence system.

Rather than treating strategic analysis as a single report generation task, the system processes every request through a sequence of specialized layers. Each layer performs one responsibility before passing structured outputs to the next stage.

```text
Presentation Layer
    ↓
Decision Layer
    ↓
Reasoning Layer
    ↓
Understanding Layer
    ↓
Input Layer

## Layer Responsibilities

### Presentation Layer

Responsible for:

- Dashboard
- Output Adapter
- Localization
- User-facing presentation

---

### Decision Layer

Purpose

Transform structured analysis into explicit decision guidance.

Core Components

- Decision Question
- Decision Criteria
- Decision Paths
- Option Ranking
- Preferred Path
- Trade-offs

---

### Reasoning Layer

Responsible for:

- Historical Analogues
- Historical Outcomes
- Strategic Lessons
- Multi-Lens Analysis
- Evidence Assessment

---

### Understanding Layer

Responsible for:

- Event Understanding
- Event Context
- Issue Extraction
- Scenario Classification

---

### Input Layer

Responsible for:

- User Question
- Uploaded File
- URL
- Plain Text

## High-Level Design

Strategic Intelligence Agent is organized as a deterministic, tool-selecting
strategic intelligence workflow. The architecture emphasizes current-event
framing, traceable retrieval, historical analogue reasoning, historical outcome
patterns, strategic lessons, and evidence-aware executive communication.

```text
Single assistant input
  -> pasted text / uploaded file / user-provided URL / question-only request
  -> language / output mode selection
  -> event_context
  -> event_understanding
  -> document_loader
  -> agent_router
  -> tool_registry
  -> selected tools
  -> outcome_retriever
  -> strategic_lessons
  -> result synthesis
  -> multi_lens_analyzer
  -> evidence_assessor
  -> brief_generator
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
knowledge_base/historical_outcomes.csv Curated historical outcome records.
knowledge_base/current_context/ Local current-context knowledge base files.
examples/                      Example inputs, runs, and generated artifacts.
demo_cases/                    Fictional educational current-event demo inputs.
demo_case_outputs/             Generated artifacts for reviewer-facing demo cases.
evaluation/                    Benchmark cases, generated results, and evaluation summary.
outputs/                       Generated briefs and intermediate workflow outputs.
outputs/runs/                  Local app run folders and downloadable artifacts.
scripts/                       Validation and utility scripts.
src/                           Application source code.
```

## Source Modules

| Module | Layer | Responsibility |
|--------|-------|----------------|
| `agent_router.py` | Input | Analyze document metadata and select the appropriate deterministic processing route. |
| `tool_registry.py` | Input | Register available deterministic tools for extensibility and orchestration. |
| `document_loader.py` | Input | Load and normalize source documents from supported inputs. |
| `event_context.py` | Understanding | Extract deterministic current-event context before strategic reasoning. |
| `event_understanding.py` | Understanding | Identify event families, comparison guardrails, and scenario characteristics before decision analysis. |
| `issue_extractor.py` | Understanding | Extract core issues, actors, regions, industries, companies, policies, document types, and uncertainties. |
| `scenario_classifier.py` | Understanding | Classify issues into deterministic scenario categories. |
| `historical_retriever.py` | Reasoning | Retrieve the most relevant historical analogues from the historical knowledge base. |
| `context_retriever.py` | Reasoning | Retrieve current contextual information from the local knowledge base. |
| `implication_analyzer.py` | Reasoning | Combine historical evidence and current context into structured decision implications and key considerations. |
| `mechanism_detector.py` | Reasoning | Identify strategic mechanisms that explain why similar situations evolved as they did. |
| `multi_lens_analyzer.py` | Reasoning | Generate competing interpretations across multiple strategic analysis lenses. |
| `evidence_assessor.py` | Reasoning | Assess supporting, weakening, and missing evidence for competing explanations. |
| `response_playbook_retriever.py` | Reasoning | Retrieve historical organizational responses, observed outcomes, and strategic lessons supporting decision evaluation. |
| `outcome_retriever.py` | Reasoning | Retrieve observed historical outcomes from analogous cases. |
| `strategic_lessons.py` | Reasoning | Generate recurring strategic lessons derived from historical outcomes. |
| `brief_generator.py` | Decision | Construct the complete decision-first report, including decision questions, criteria, decision paths, option comparison, preferred path, trade-offs, assumptions, monitoring, historical evidence, and limitations. |
| `output_adapter.py` | Presentation | Transform the decision report into Beginner, Analyst, and Executive experiences while preserving localization parity and consistent information architecture. |
| `evaluator.py` | Evaluation | Run benchmark cases and calculate scenario, mechanism, reasoning, and overall evaluation scores. |
| `run_agent.py` | Orchestration | Execute the complete end-to-end Strategic Intelligence workflow. |

## Current Event Context Layer

The current-event layer extracts event type, primary actor, secondary actor,
affected sectors, affected regions, policy domain, strategic significance,
summary, confidence, and limitations from the submitted document. It runs
before issue extraction and scenario classification so reviewers can see what
kind of current event is being analyzed before historical analogues are used.

This layer is deterministic. It does not use live web search, external news
APIs, vector retrieval, or LLM calls. Its confidence label describes internal
classification support, not real-world accuracy.

## V12 Product Rebuild Layer

V12 rebuilds the user entry point around a single assistant-style input area:

1. Users ask a question, paste source text, include a URL, or upload a file.
2. The backend uses the real deterministic pipeline rather than dashboard-only demo logic.
3. `event_understanding.py` maps the input to a product-facing event family such as Corporate Restructuring, Trade Restriction, Financial Product Risk, State Support, or Supply Chain Disruption.
4. The strategic assessment uses the event family as a comparison guardrail so irrelevant historical cases are not promoted without a clear rationale.
5. The default brief answers practical questions first: what happened, why it matters, similar cases, responses, outcomes, market expectations versus outcomes, lessons, and what to monitor next.
6. Method-heavy sections remain available for analyst review but are not the default beginner experience.

````markdown
## V13 Decision Intelligence Layer

V13 transforms the brief from a strategic analysis report into a criteria-driven decision workspace.

The system now follows this decision-first structure:

```text
User Input
    ↓
Event Understanding
    ↓
Decision Question
    ↓
Decision Criteria
    ↓
Decision Paths
    ↓
Option Comparison
    ↓
Option Ranking
    ↓
Preferred Path
    ↓
Assumptions
    ↓
Trade-offs
    ↓
Change Triggers
    ↓
Action Timeline
    ↓
Monitoring
    ↓
Historical Evidence
    ↓
Limitations
```

### Design Intent

Traditional AI analysis tools focus on generating answers.

Repo 5 focuses on improving decision quality.

Instead of asking:

> "What will happen?"

the system asks:

> "What decision needs to be made, what factors matter, and what evidence would change today's judgment?"

The objective is **not** to predict the future.

The objective is to reduce decision uncertainty through structured reasoning, explicit trade-offs, transparent assumptions, and evidence-based recommendations.

### Design Principles

The Decision Intelligence layer follows four core principles:

1. Reframe the user's question before attempting to answer it.
2. Define what matters before comparing available options.
3. Make reasoning transparent instead of presenting conclusions only.
4. Use historical cases as supporting evidence rather than treating history itself as the decision.

As a result, historical intelligence becomes **evidence**, while strategic reasoning becomes **the product**.

## Demo Case Library

The repository includes a reviewer-facing demo library in `demo_cases/`,
`demo_case_outputs/`, and `docs/demo_case_library.md`.

The demo cases demonstrate the same decision-first architecture operating across:

- Export controls
- Industrial policy
- Supply chain disruption
- Financial earnings risk
- Digital market regulation

Each case showcases how the system converts raw events into structured decision reasoning rather than simply generating analytical summaries.
````

## V6 Local App Layer

V6 adds `app.py`, a local-only FastAPI backend:

1. `POST /analyze` receives dashboard text and user selections.
2. The backend runs the existing deterministic pipeline.
3. A unique run folder is created under `outputs/runs/`.
4. `analysis.json`, `brief.md`, `brief.txt`, `agent_trace.json`,
   `metadata.json`, and `input.txt` are saved.
5. `GET /runs` and `GET /run/{run_id}` support history and retrieval.
6. Download endpoints serve Markdown, TXT, and JSON artifacts.

## V7 Historical Outcomes Layer

V7 extends analogue analysis without adding new agents or live retrieval:

1. `historical_outcomes.csv` stores simplified outcome and response records.
2. `outcome_retriever.py` maps retrieved analogues to outcome records.
3. `strategic_lessons.py` groups recurring lessons across retrieved outcomes.
4. The executive brief includes Historical Outcomes, Strategic Lessons, and
   Decision Considerations.
5. `analysis.json` includes `historical_outcomes` and `strategic_lessons`.

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
