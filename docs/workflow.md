# Workflow

## Target Workflow

```text
Question, pasted document, uploaded file, or user-provided URL
-> Language / Output Mode
-> Current Event Context
-> Event Understanding
-> Tool Router
-> Tool Selection
-> Tool Execution
-> Result Synthesis
-> Historical Outcomes
-> Strategic Lessons
-> Multi-Lens Reasoning
-> Executive Intelligence Brief
-> Evaluation Reporting
-> Local Run Storage / Downloads
```

## Stage Details

### 1. Assistant Input

The app starts with one assistant-style input area. A user can ask a question,
paste an article, paste a policy excerpt, include a readable webpage URL, or
upload a `.txt`, `.md`, `.markdown`, or text-based `.pdf` file.

If a user provides only a question, the system answers from local historical
cases and knowledge-base records. If a user provides content, the system uses
that content plus local historical cases. If URL extraction fails, the backend
returns a clear error and does not generate filler.

### 2. Non-AI User Controls

The product controls are intentionally minimal:

- Product language: English.
- Output mode: beginner, analyst, or executive.

The controls reduce prompt-writing burden while preserving the same underlying
analysis pipeline.

### 3. Current Event Context

The current-event layer extracts event type, primary actor, secondary actor,
affected sectors, affected regions, policy domain, strategic significance,
event summary, confidence, and context limitations from the submitted text.

This step helps reviewers understand what kind of current event is being
analyzed before the workflow retrieves historical analogues and outcomes. It
uses deterministic keyword rules and does not perform live web search or source
verification.

### 4. Event Understanding

The event-understanding layer maps the input to a practical event family before
historical comparison:

- Layoff -> Corporate Restructuring.
- Earnings Miss -> Earnings Shock.
- Export Controls -> Trade Restriction.
- Sanctions -> Economic Coercion.
- New Bank Product -> Financial Product Risk.
- Industrial Subsidy -> State Support.
- Supply Chain Disruption -> Supply Chain Disruption.

This prevents weak comparisons such as treating a corporate layoff as directly
comparable to export controls unless the input source gives a clear reason.

### 5. Tool Router

The router inspects document type, scenario type, industries, actors, and
keywords. It creates an Agent Trace and a reasoning record before selected tools
execute.

### 6. Tool Selection

The router selects from the Tool Registry:

- IssueExtractor.
- ScenarioClassifier.
- HistoricalRetriever.
- ContextRetriever.
- ImplicationAnalyzer.
- BriefGenerator.

ContextRetriever can be skipped for routes where current context is not likely
to add value, such as a narrow corporate earnings disclosure.

### 7. Issue Extraction

The extractor identifies:

- Core issue.
- Relevant actors.
- Countries or regions.
- Industries.
- Policy terms.
- Companies.
- Document type guess.
- Uncertainties.
- Evidence snippets.

### 8. Scenario Classification

The classifier assigns the issue to strategic categories such as:

- Export Controls.
- Industrial Policy.
- Sanctions.
- Supply Chain Disruption.
- Regulatory Action.
- Military / Security Shock.
- Earnings / Corporate Disclosure.
- Strategic Investment.
- Trade Policy.
- Other.

Classification uses deterministic keyword matching. The confidence label
describes classification quality only; it is not a forecast probability.

### 9. Historical Analogue Retrieval

The retriever searches curated examples for structurally similar events. The
goal is not prediction; the goal is to support better reasoning by comparison.

The retriever loads `knowledge_base/historical_analogues.csv` and scores cases
using:

- Scenario type match.
- Keyword overlap.
- Industry overlap.
- Actor overlap.

### 10. Current Context Retrieval

The context retriever loads local Markdown files from
`knowledge_base/current_context/` and scores entries using:

- Industry match.
- Scenario match.
- Keyword overlap.

Historical analogues alone are insufficient because they show what an issue may
resemble, but not which current stakeholders, constraints, and monitoring
considerations are relevant. The context layer improves decision support by
adding present-domain framing without making forecasts.

### 11. Historical Outcome Retrieval

V7 retrieves observed historical outcomes linked to the retrieved analogue
cases. Outcomes include observed consequence, strategic response, time horizon,
confidence, and source status. The layer supports learning from past cases
without implying that outcomes will repeat.

### 12. Strategic Lesson Generation

The strategic lesson generator groups retrieved outcomes into recurring lessons
using rule-based keyword groups. Each lesson lists supporting cases, confidence,
rationale, and evidence references.

### 13. Intelligence Synthesis

The analyzer combines historical analogues and current context into:

- Observed similarities.
- Observed differences.
- Business considerations.
- Operational considerations.
- Geopolitical considerations.
- Strategic questions.

The language avoids forecasts, probabilities, and investment recommendations.
It uses phrasing such as "may resemble", "shares characteristics with",
"differs from", and "requires monitoring".

### 14. Multi-Lens Reasoning

V4 adds competing interpretations of the same event:

- Economics.
- Political Economy.
- International Relations.
- Legislative / Regulatory.
- Business Strategy.

Each lens includes a hypothesis, supporting observations, limitations, and
evidence references. Evidence support is labeled Limited, Moderate, or
Substantial without using probability language.

### 15. Executive Brief Generation

The generator writes a concise brief with these sections:

- Executive Summary.
- Key Issue.
- Current Event Context.
- Scenario Classification.
- Extracted Entities.
- Historical Analogues.
- Historical Outcomes.
- Strategic Lessons.
- Decision Considerations.
- Current Context.
- Similarities and Differences.
- Business Considerations.
- Operational Considerations.
- Geopolitical Considerations.
- Strategic Questions.
- Analyst Notes.
- Limitations.
- Execution Trace.
- Tool Decisions.
- Evidence Sources.
- Analysis Path.
- Competing Interpretations.
- Multi-Lens Analysis.
- Supporting Evidence.
- Weakening Evidence.
- Missing Evidence.
- Historical Response Patterns.
- Cross-Domain Lessons.
- Monitoring Considerations.

Each brief includes an evidence trace section showing source origins.

### 15. Output Adaptation

V4.5 can adapt generated briefs into beginner, analyst, or executive format.
The adapter uses deterministic templates and localized framing. It does not use
external translation APIs and does not alter the project guardrails against
forecasts, probabilities, or investment advice.

### 16. Evaluation Reporting

V5 checks the existing pipeline against synthetic regression fixtures. It reports
separate scenario-contract, expected-mechanism, fixed-lens, and fixed-response
components without an overall score. Artifacts under `evaluation/` support
engineering regression detection, not research credibility or external validity.

### 17. Local App Storage

V6 routes dashboard requests through FastAPI. Each analysis creates a run folder
under `outputs/runs/` containing the input text, structured JSON analysis,
Markdown brief, TXT brief, agent trace, and metadata. The dashboard history
panel retrieves saved runs through the API and download buttons use server
download endpoints.

### 18. Demo Case Library

V8 adds fictional educational demo inputs and generated artifacts under
`demo_cases/` and `demo_case_outputs/`. These cases make the product easier to
review because each example includes current-event context, issue extraction,
scenario classification, mechanisms, historical analogues, historical outcomes,
strategic lessons, evidence credibility, and downloadable artifacts.
