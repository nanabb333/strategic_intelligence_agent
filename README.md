# Strategic Intelligence Agent

An analyst workbench that converts documents, articles, policy texts, and earnings excerpts into structured executive intelligence briefs.

![Strategic Intelligence Agent workbench](docs/screenshots/dashboard_workbench.svg)

## Project Overview

Strategic Intelligence Agent is a portfolio-grade decision-support product for strategic intelligence and business analytics. It combines deterministic issue extraction, scenario classification, historical analogue retrieval, current context retrieval, implication analysis, evidence traceability, and executive brief generation.

V2 adds a local Analyst Workbench in `dashboard/` so reviewers can paste source text, upload Markdown or text files, inspect collapsible analysis sections, review source evidence, and export an executive brief.

## What This Is / Is Not

This is:

- A decision-support workflow.
- A strategic intelligence workbench.
- An analyst productivity product.
- A business analytics portfolio project.
- A demonstration of agent-style workflow orchestration.

This is not:

- A trading platform.
- A forecasting system.
- Investment advice.
- A source of trading recommendations, price targets, expected returns, or portfolio allocation guidance.

## Architecture

```text
Input Document
-> Issue Extraction
-> Scenario Classification
-> Historical Analogue Retrieval
-> Current Context Retrieval
-> Implication Analysis
-> Executive Brief
-> Analyst Workbench Display / Export
```

See [docs/architecture_diagram.md](docs/architecture_diagram.md) and [docs/system_architecture.md](docs/system_architecture.md) for more detail.

## Workflow

1. The analyst pastes or uploads a document.
2. The system extracts issue fields such as actors, industries, policy terms, and document type.
3. The scenario classifier assigns a deterministic scenario label.
4. The historical retriever finds relevant analogue cases.
5. The context retriever finds domain context from local knowledge-base files.
6. The synthesis layer separates observed similarities, differences, business considerations, operational considerations, geopolitical considerations, and strategic questions.
7. The workbench displays collapsible sections with evidence labels.
8. The executive brief can be exported as Markdown or TXT.

## Business Value

Analysts often lose time turning messy source material into executive-ready intelligence. This project demonstrates how an analytics product can make that process repeatable:

- Information extraction structures unstructured text.
- Retrieval adds historical and current context.
- Evidence traceability makes output reviewable.
- Workflow design turns a one-off analysis task into a repeatable product.
- Executive brief generation creates a usable decision-support artifact.

See [docs/business_analytics_relevance.md](docs/business_analytics_relevance.md).

## Repository Structure

```text
dashboard/                     Local browser analyst workbench.
docs/                          Portfolio, architecture, product, and interview docs.
examples/                      Source examples and demo inputs.
knowledge_base/                Historical analogue records.
knowledge_base/current_context/ Local context KB files by domain.
outputs/                       Generated executive intelligence briefs.
demo_outputs/                  Generated portfolio demo briefs.
scripts/                       Validation scripts.
src/                           Deterministic analysis pipeline.
legacy/financial_rubric_agent/ Preserved earlier project history.
```

## Run The Workbench

Open this file in a browser:

```text
dashboard/index.html
```

The dashboard is static and local. It supports paste input, `.md` and `.txt` uploads, collapsible results, evidence labels, and Markdown/TXT export.

## Run The Pipeline

```bash
python3 src/run_agent.py examples/chips_act_example.md --output outputs/chips_act_brief.md
python3 src/run_agent.py examples/banking_earnings_example.md --output outputs/banking_earnings_brief.md
python3 src/run_agent.py examples/red_sea_shipping_example.md --output outputs/red_sea_shipping_brief.md
```

## Demo Outputs

V2 demo inputs live in `examples/demo_inputs/`. Validation generates matching briefs in `demo_outputs/`:

- `demo_outputs/semiconductor_policy_brief.md`
- `demo_outputs/bank_earnings_brief.md`
- `demo_outputs/supply_chain_disruption_brief.md`
- `demo_outputs/red_sea_shipping_brief.md`

## Validation

```bash
python3 -m compileall src
python3 scripts/validate_v05.py
python3 scripts/validate_v10.py
python3 scripts/validate_v20.py
```

The V2 validator checks that the dashboard loads, outputs generate, exports are written to `outputs/`, and evidence traces exist.

## Portfolio Value

This project demonstrates:

- AI product architecture without overclaiming model intelligence.
- Agent workflow decomposition.
- Deterministic retrieval and synthesis.
- Business analytics product thinking.
- Evidence-aware executive communication.
- Frontend product packaging for a GitHub portfolio.

Supporting docs:

- [docs/product_walkthrough.md](docs/product_walkthrough.md)
- [docs/product_requirements.md](docs/product_requirements.md)
- [docs/interview_story.md](docs/interview_story.md)
- [docs/resume_bullets.md](docs/resume_bullets.md)
- [docs/portfolio_case_study.md](docs/portfolio_case_study.md)

## Future Roadmap

- Add optional LLM provider support behind the existing deterministic interfaces.
- Add richer source metadata with dates and URLs.
- Add structured JSON intermediate artifacts.
- Add tests for retrieval scoring edge cases.
- Add a lightweight local server for direct dashboard-to-`outputs/` saving.
- Add user-selectable knowledge-base filters and evidence review controls.

## Limitations

- V2 remains deterministic and keyword-based.
- The dashboard is a local static interface.
- Browser exports download files; the validation script writes repository export artifacts into `outputs/`.
- No live web retrieval is performed.
- No forecasts, probabilities, investment advice, or trading recommendations are generated.

