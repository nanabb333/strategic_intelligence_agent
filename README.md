# Strategic Intelligence Agent

A local strategic intelligence decision-support application that turns documents, policy texts, articles, earnings excerpts, and operational updates into structured executive intelligence briefs.

![Strategic Intelligence Agent workbench](docs/screenshots/dashboard_workbench.svg)

## Example Analysis

**Sample input document**

```text
The government announced new export controls affecting advanced semiconductor manufacturing equipment and high-performance AI chips. Several chipmakers and equipment suppliers said they are reviewing licensing requirements and customer exposure. The measures may limit access to advanced-node production tools for firms tied to restricted end users. Executives are preparing internal briefings on supply chain exposure, compliance burden, and market access implications.
```

**What the system identifies**

| Field | Example system output |
| --- | --- |
| Event type | Export control policy update |
| Key actors | Government regulators, semiconductor manufacturers, equipment suppliers, restricted end users |
| Affected sector | Semiconductors and advanced chip supply chains |
| Scenario category | Export Controls |
| Mechanisms | Technology Containment, Market Access Restriction, Compliance Burden, Supply Chain Reconfiguration |
| Historical analogues | Prior semiconductor equipment controls, entity-list restrictions, industrial policy responses |
| Historical outcomes | Licensing reviews, supplier exposure mapping, customer segmentation, compliance process expansion |
| Strategic lessons | Export-control shocks often require entity screening, supplier review, customer-risk mapping, and management reporting routines |
| Evidence credibility note | Based on local curated historical summaries; source status and confidence labels are reported separately; findings require human review |

This example is intentionally practical: the app does not merely restate the document. It classifies the strategic issue, connects it to mechanisms and historical patterns, and produces a reviewable brief.

## Sample Output Preview

The example below is an illustrative preview of the local deterministic workflow output. It is not a forecast, investment recommendation, legal opinion, or claim of future accuracy.

```text
Current Event Context:
New semiconductor export controls appear to affect advanced chip supply chains,
equipment access, licensing exposure, and customer review processes.

Scenario:
Export Controls

Mechanisms:
- Technology Containment
- Market Access Restriction
- Compliance Burden
- Supply Chain Reconfiguration

Historical Analogues:
- Semiconductor equipment export-control episodes
- Entity-list restrictions affecting technology suppliers
- Industrial policy responses around strategic chip capacity

Historical Outcomes:
- Firms reviewed customer exposure and licensing obligations.
- Suppliers adjusted compliance screening and reporting workflows.
- Some organizations reassessed geographic concentration and critical dependencies.

Strategic Lessons:
- Supply chain mapping frequently appears after export-control shocks.
- Compliance operations become part of strategic planning, not only legal review.
- Historical analogues are useful for framing questions, not predicting outcomes.

Decision Considerations:
- Which products, customers, or suppliers require review?
- Which internal teams need a shared view of exposure?
- What evidence is strong enough for executive discussion, and what remains uncertain?

Evidence Credibility:
Historical outcomes are simplified educational summaries from a local knowledge base.
Confidence labels reflect internal evidence coding, not real-world predictive accuracy.
Source URLs are not fabricated; unavailable sources remain marked as pending.
```

## Why This Matters

Strategic analysis is often blocked by messy source material. A policy note, earnings excerpt, or disruption update may contain useful signals, but analysts still need to identify the issue type, assess operating mechanisms, compare similar cases, and communicate implications clearly.

Strategic Intelligence Agent turns that workflow into a repeatable local product:

- It accepts pasted text or uploaded `.md` / `.txt` files.
- It structures the issue, actors, sector, and scenario.
- It retrieves local historical analogues and simplified historical outcomes.
- It surfaces mechanisms and strategic lessons without making predictions.
- It creates Markdown, TXT, and JSON artifacts for review.
- It reports evidence limitations instead of hiding uncertainty.

## Why This Is Not Just a Summarizer

A generic summarizer tells the user what the document says. Strategic Intelligence Agent helps the user understand what kind of strategic issue the document represents and how to reason about it.

| Generic Summarizer | Strategic Intelligence Agent |
| --- | --- |
| Condenses the source text | Extracts the issue, actors, sector, and scenario |
| Produces a shorter version of the document | Classifies the strategic situation |
| Usually stays inside the document | Connects the issue to local historical analogues |
| May miss operating mechanisms | Detects mechanisms such as export controls, sanctions, compliance burden, or supply chain reconfiguration |
| Does not explain historical patterns | Retrieves simplified observed outcomes from comparable cases |
| Rarely states evidence limits clearly | Reports confidence distribution, source status, and limitations |
| Produces prose | Produces a brief plus structured JSON artifacts for further analysis |

## What The System Does

The workflow moves from unstructured input to a reviewable intelligence artifact:

```text
Document
-> Issue Extraction
-> Scenario Classification
-> Mechanism Detection
-> Historical Analogues
-> Historical Outcomes
-> Strategic Lessons
-> Evidence Credibility
-> Executive Brief
-> Downloadable Artifacts
```

Core analytical components:

- **Issue extraction:** Converts source text into structured fields.
- **Scenario classification:** Frames the document as export controls, sanctions, supply chain disruption, industrial policy, regulatory action, earnings disclosure, or another strategic scenario.
- **Mechanism detection:** Identifies recurring mechanisms such as technology containment, strategic dependency, compliance burden, market access restriction, and supply chain reconfiguration.
- **Historical analogue retrieval:** Finds structurally similar historical cases from local curated records.
- **Historical outcome retrieval:** Connects analogues to simplified observed outcomes and strategic responses.
- **Strategic lesson generation:** Uses rule-based logic to surface recurring lessons across outcomes.
- **Multi-lens analysis:** Reviews the issue through economics, political economy, international relations, regulatory, and business strategy lenses.
- **Evidence credibility:** Reports confidence distribution, source status distribution, limitations, and reviewer notes.

## Product Features

- Local FastAPI backend.
- Browser dashboard for non-technical users.
- Paste-input and file-upload workflows.
- Guided questions for common analyst tasks.
- Beginner, analyst, and executive output modes.
- Bilingual UX support.
- Run history saved under `outputs/runs/`.
- Markdown, TXT, and JSON downloads.
- Deterministic local knowledge bases for context, mechanisms, analogues, outcomes, and playbooks.
- Validation scripts for targeted regression checks.

## What Users Can Do With The Output

Users can use the generated artifacts to:

- Prepare an executive briefing.
- Compare a current issue with historical analogues.
- Identify strategic mechanisms behind a policy, market, or operational event.
- Structure risk and strategy discussions.
- Generate decision-support notes for analyst review.
- Export JSON artifacts for further analysis or portfolio demonstration.
- Preserve a run history with input text, metadata, trace, brief, and structured analysis.

The output is designed to support thinking and communication. It does not replace human judgment.

## Demo Preview

The repository includes a dashboard preview:

- [Dashboard screenshot](docs/screenshots/dashboard_workbench.svg)

To try the local app, start the FastAPI server and open the dashboard at:

```text
http://127.0.0.1:8000/dashboard/
```

Additional screenshots can be added after running the local app with representative cases.

## Evidence & Limitations

This project is a decision-support workflow, not a prediction system.

It is not:

- A trading system.
- A forecasting system.
- Investment advice.
- Legal advice.
- A geopolitical prediction engine.
- A live web-monitoring product.
- A production SaaS deployment.

Historical outcome records are simplified educational summaries. Source URLs are not fabricated; unavailable URLs remain marked through source status fields such as `source pending`. Confidence labels reflect internal evidence coding for this portfolio project, not real-world predictive accuracy.

The system does not prove factual correctness, legal accuracy, financial accuracy, geopolitical accuracy, or future outcomes. Human expert review is required before executive use.

## How To Run Locally

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Start the local server:

```bash
python3 -m uvicorn app:app --reload
```

Open the dashboard:

```text
http://127.0.0.1:8000/dashboard/
```

Each analysis creates a local run folder under `outputs/runs/` containing:

- `input.txt`
- `analysis.json`
- `brief.md`
- `brief.txt`
- `agent_trace.json`
- `metadata.json`

See [docs/local_app_setup.md](docs/local_app_setup.md), [docs/run_management_design.md](docs/run_management_design.md), and [docs/json_artifact_design.md](docs/json_artifact_design.md).

## Repository Structure

```text
app.py                         Local FastAPI backend.
dashboard/                     Browser dashboard for non-technical users.
docs/                          Architecture, portfolio, product, and case-study docs.
examples/                      Source examples and demo inputs.
knowledge_base/                Local analogue, outcome, mechanism, and context records.
outputs/                       Generated briefs and local run artifacts.
scripts/                       Validation scripts.
src/                           Deterministic analysis pipeline.
evaluation/                    Benchmark cases, generated results, and evaluation summary.
legacy/financial_rubric_agent/ Preserved earlier project history.
```

## Portfolio Positioning

This repository is strongest as a demonstration of AI product architecture, business analytics workflow design, and strategic intelligence judgment.

It shows:

- Agent-style workflow orchestration without unnecessary autonomy.
- Deterministic tool use and traceability.
- Local FastAPI productization.
- Bilingual guided UX for non-technical users.
- Historical analogue and outcome reasoning.
- Evidence credibility and limitation reporting.
- Scope control around non-forecasting decision support.

Primary portfolio docs:

- [docs/repo5_case_study.md](docs/repo5_case_study.md)
- [docs/product_walkthrough.md](docs/product_walkthrough.md)
- [docs/product_requirements.md](docs/product_requirements.md)
- [docs/interview_story.md](docs/interview_story.md)
- [docs/resume_bullets.md](docs/resume_bullets.md)
- [docs/evaluation_framework.md](docs/evaluation_framework.md)
- [docs/evaluation_limitations.md](docs/evaluation_limitations.md)
- [docs/business_analytics_relevance.md](docs/business_analytics_relevance.md)

## Project Status

The current project is a local usable application with a deterministic document-to-brief pipeline, dashboard, run history, downloadable artifacts, historical outcomes, strategic lessons, and evidence credibility reporting.

Current targeted validation:

```bash
python3 -m compileall src
```

Older validators are retained for regression checks, but they should only be run when older-version files are directly modified, targeted validation fails, or a regression is suspected.

Remaining limitations:

- Deterministic keyword and rule-based methods can miss nuance.
- Historical outcomes are simplified summaries, not source-grounded claims.
- The app is local and single-user.
- No live web retrieval is performed.
- No RAG infrastructure or LLM reasoning benchmark is included.
- No forecasts, probabilities, investment advice, legal advice, or trading recommendations are generated.
