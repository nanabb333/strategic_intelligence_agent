# Strategic Intelligence Agent

A local strategic intelligence decision-support application that turns documents, articles, policy texts, earnings excerpts, and operational updates into structured executive intelligence briefs.

![Strategic Intelligence Agent workbench](docs/screenshots/dashboard_workbench.svg)

## What This Project Is

Strategic Intelligence Agent is a portfolio-grade AI product architecture project focused on analyst productivity, business analytics, and strategic intelligence workflows.

The application helps a user move from unstructured text to a reviewable intelligence artifact:

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

It runs locally through a FastAPI backend and browser dashboard. The system uses deterministic Python modules and local knowledge bases; it does not depend on live web search, cloud deployment, or paid LLM APIs.

## Why It Matters

Strategic analysis is often blocked by messy source material. Analysts need to identify the issue, classify the scenario, compare it with historical patterns, understand what happened in similar cases, and communicate implications clearly.

This project demonstrates how an AI-style workflow can become a usable product:

- It structures unstructured source text.
- It retrieves historical analogues and simplified historical outcomes.
- It surfaces mechanisms and multi-lens interpretations.
- It generates strategic lessons without making predictions.
- It creates Markdown, TXT, and JSON artifacts for review.
- It reports evidence credibility and limitations instead of hiding uncertainty.

## Who It Is For

The target user is a non-technical analyst, strategy student, business analytics candidate, policy researcher, or portfolio reviewer who wants a guided local tool rather than a prompt-writing exercise.

The dashboard is designed so a user can:

1. Open the browser.
2. Paste text or upload a `.md` / `.txt` file.
3. Choose a guided question.
4. Click Analyze.
5. Download Markdown, TXT, or JSON results.

## What Problem It Solves

The project addresses a practical analyst workflow problem: turning long or ambiguous strategic source material into a structured, evidence-aware brief.

It is useful for reviewing:

- Export control updates.
- Industrial policy texts.
- Sanctions or trade policy excerpts.
- Supply chain disruption notes.
- Earnings announcements with strategic uncertainty.
- Geopolitical or regulatory operating-risk summaries.

## Local App Usage

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

## Example Use Case

A user pastes a short article about new semiconductor export controls.

The system can:

- Extract the policy issue and relevant industry terms.
- Classify the scenario as export controls.
- Detect mechanisms such as technology containment and compliance burden.
- Retrieve historical analogues such as prior entity-list or equipment-control cases.
- Retrieve simplified historical outcomes from related cases.
- Generate strategic lessons about supplier review, licensing exposure, and monitoring routines.
- Provide an evidence credibility note explaining confidence distribution, source status, and limitations.
- Produce an executive brief for review.

## Strategic Intelligence Framework

The project is organized around decision support, not prediction.

Core analytical components:

- **Issue extraction:** Converts source text into structured fields.
- **Scenario classification:** Frames the document as export controls, sanctions, supply chain disruption, industrial policy, regulatory action, earnings disclosure, or another scenario.
- **Mechanism detection:** Identifies recurring mechanisms such as technology containment, strategic dependency, compliance burden, market access restriction, and supply chain reconfiguration.
- **Historical analogue retrieval:** Finds structurally similar historical cases from local curated records.
- **Historical outcome retrieval:** Connects analogues to simplified observed outcomes and strategic responses.
- **Strategic lesson generation:** Uses rule-based logic to surface recurring lessons across outcomes.
- **Multi-lens analysis:** Reviews the issue through economics, political economy, international relations, regulatory, and business strategy lenses.
- **Evidence credibility:** Reports confidence distribution, source status distribution, limitations, and reviewer notes.

## What This Is Not

This project is not:

- A trading system.
- A forecasting system.
- Investment advice.
- Legal advice.
- A geopolitical prediction engine.
- A live web-monitoring product.
- A production SaaS deployment.

Outputs are decision-support artifacts for analyst review.

## Evidence & Limitations

The system is intentionally transparent about uncertainty.

Historical outcome records are simplified educational summaries. Source URLs are not fabricated; unavailable URLs remain marked through source status fields such as `source pending`. Confidence labels reflect internal evidence coding for this portfolio project, not real-world predictive accuracy.

The evidence credibility layer reports:

- Evidence summary.
- Confidence distribution.
- Source status distribution.
- Key limitations.
- Reviewer note.

The system does not prove factual correctness, legal accuracy, financial accuracy, geopolitical accuracy, or future outcomes. Human expert review is required before executive use.

## Business Analytics Relevance

This project demonstrates business analytics product thinking:

- Structured extraction from unstructured information.
- Deterministic retrieval and scoring.
- Workflow orchestration across modular tools.
- Local artifact generation for review and reuse.
- Validation scripts and benchmark-oriented credibility checks.
- Product UX for non-technical users.

See [docs/business_analytics_relevance.md](docs/business_analytics_relevance.md).

## Portfolio Positioning

This repository is strongest as a demonstration of AI product architecture and applied analytics judgment.

It shows:

- Agent-style workflow orchestration without unnecessary autonomy.
- Tool selection and traceability.
- Local FastAPI productization.
- Bilingual guided UX.
- Historical analogue and outcome reasoning.
- Evidence credibility and limitations.
- Portfolio-safe scope control.

Primary portfolio docs:

- [docs/repo5_case_study.md](docs/repo5_case_study.md)
- [docs/product_walkthrough.md](docs/product_walkthrough.md)
- [docs/product_requirements.md](docs/product_requirements.md)
- [docs/interview_story.md](docs/interview_story.md)
- [docs/resume_bullets.md](docs/resume_bullets.md)
- [docs/evaluation_framework.md](docs/evaluation_framework.md)
- [docs/evaluation_limitations.md](docs/evaluation_limitations.md)

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

## Validation

For current work, use targeted validation:

```bash
python3 -m compileall src
python3 scripts/validate_v75.py
```

When a V8 validator exists, use:

```bash
python3 scripts/validate_v80.py
```

Older validators are retained for regression checks, but they should only be run when older-version files are directly modified, targeted validation fails, or a regression is suspected.

## Short Milestone Summary

- Deterministic document-to-brief pipeline.
- Historical analogue, current-context, mechanism, and multi-lens reasoning.
- Local FastAPI app with dashboard, run history, and downloadable artifacts.
- Historical outcomes and strategic lessons.
- Evidence credibility and portfolio case study.

## Remaining Limitations

- Deterministic keyword and rule-based methods can miss nuance.
- Historical outcomes are simplified summaries, not source-grounded claims.
- The app is local and single-user.
- No live web retrieval is performed.
- No RAG infrastructure or LLM reasoning benchmark is included.
- No forecasts, probabilities, investment advice, legal advice, or trading recommendations are generated.
