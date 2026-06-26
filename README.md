# Strategic Intelligence Agent

A local **Strategic Intelligence Assistant** that helps users ask plain-language questions about business, policy, market-access, supply-chain, and geopolitical events, then turns source material into structured decision-support briefs.

![Strategic Intelligence Agent workbench](docs/screenshots/v12_assistant_workbench.svg)

## Engineering Documentation

For reviewers interested in the software architecture:

- [Engineering Architecture](docs/EngineeringArchitecture.md)
- [Analysis Pipeline](docs/Pipeline.md)
- [Testing](docs/Testing.md)
- [Folder Structure](docs/FolderStructure.md)

## Normal User Vision

The intended product path is:

```text
Download -> Open App -> Ask Question
```

A non-technical user should be able to open the local app, type a question or paste source material, click Analyze, and download Markdown, TXT, or JSON results. The current repository still runs as a developer-started local FastAPI app, but the product direction is a normal-user desktop experience rather than a notebook, prompt demo, or engineering-only workflow.

## What A User Can Ask

The dashboard is built around one ChatGPT-style input area. A user can:

- Ask a question with no article attached: “What should I monitor over the next 90 days?”
- Paste an article, policy excerpt, earnings note, supply-chain update, or internal memo.
- Paste a readable webpage URL and let the local backend attempt text extraction.
- Upload `.txt`, `.md`, `.markdown`, or text-based `.pdf` files.

If URL extraction fails, the app stops and asks for pasted text or a file. It does not generate filler from an unreadable link.

## What Every Output Answers

Every useful brief is organized around practical strategic questions:

- What happened?
- Why does it matter?
- What similar cases existed?
- What did organizations do?
- What happened afterwards?
- What did markets or users appear to expect?
- What actually happened in comparable historical cases?
- What can be learned?
- What should the user monitor next?

The default output does not lead with mechanisms, agent routing, political-economy labels, or evidence machinery. Those details remain available for analyst review, but Beginner Mode keeps the product focused on plain-language decision support.

## Product Improvements From Real User Testing

Recent user testing showed that the project needed more practical depth and a simpler user experience. The current product upgrade responds to that feedback directly:

- **Knowledge depth:** the historical outcome dataset expanded from 20 to 105 educational cases across export controls, sanctions, industrial policy, supply chain disruption, technology competition, regulatory action, geopolitical escalation, corporate response, and financial exposure.
- **Localization:** output localization is centralized in `src/localization.py` so section headings, evidence labels, confidence labels, and recurring dashboard/result labels are more consistently rendered in English, Simplified Chinese, and Traditional Chinese.
- **Free-form questions:** the old artificial question-type dropdown is replaced with an “Ask a Question” box, routed deterministically by `src/question_router.py`.
- **UX simplification:** the dashboard now shows the executive brief and strategic lessons before methodology-heavy sections.
- **Input clarity:** the paste area is larger, visually emphasized, labeled clearly, and supports upload or drag-and-drop for `.txt`, `.md`, `.markdown`, and text-based `.pdf` files.

## Product Evolution Through User Testing

The current product direction is shaped by real usability feedback:

- **Larger knowledge base:** more historical outcome cases make analogue and outcome retrieval feel less thin during portfolio demos.
- **Fuller localization:** major knowledge-base labels such as Strategic Dependency, Supply Chain Reconfiguration, Industrial Subsidy, and Alliance Coordination are localized for Chinese modes.
- **Simplified workflow:** the dashboard now uses one assistant-style input area for questions, pasted documents, URLs, and uploaded files.
- **Value-first output design:** results prioritize a direct answer, similar cases, what happened then, how organizations responded, what happened after, market expectations vs actual outcomes, what to watch next, evidence used, and limitations.

The product remains local and deterministic. These changes improve usability and credibility without adding live web search, RAG, autonomous agents, forecasting, legal advice, or investment advice.

## Supported Inputs

The local app supports four input patterns through one input area:

- **Question-only:** ask from the local knowledge base and historical cases.
- **Pasted source:** paste a document, article, policy excerpt, earnings note, or memo.
- **Uploaded file:** upload `.txt`, `.md`, `.markdown`, or text-based `.pdf` files.
- **URL included:** paste a webpage URL and the local app will try to fetch readable article text for analysis.

PDF support uses local text extraction and does not perform OCR. Scanned image PDFs are not supported.

Link analysis is intentionally plain: if the local app can read webpage text, it analyzes that text and preserves the source URL. If the page blocks access, returns too little readable text, or is not a text page, the app asks the user to paste article text or upload a file instead.

## Demo Case Library

Reviewers can inspect five fictional educational cases that show the product working across realistic strategic intelligence scenarios:

- Semiconductor export controls affecting advanced chip supply chains and market access.
- Industrial policy subsidies for domestic battery, semiconductor, or clean-tech production.
- Geopolitical escalation affecting shipping routes and supply chain planning.
- Financial earnings pressure linked to geopolitical exposure and sanctions compliance costs.
- Digital market regulation affecting platforms, data governance, and market access.

Start here: [docs/demo_case_library.md](docs/demo_case_library.md)

Each case includes an input file in `demo_cases/`, generated artifacts in `demo_case_outputs/`, and a walkthrough in `docs/demo_case_walkthroughs/`.

## Event Understanding Layer

The system does not just summarize an input document. It first identifies the event family so comparisons stay relevant:

- Layoff -> Corporate Restructuring
- Earnings Miss -> Earnings Shock
- Export Controls -> Trade Restriction
- Sanctions -> Economic Coercion
- New Bank Product -> Financial Product Risk
- Industrial Subsidy -> State Support
- Supply Chain Disruption -> Supply Chain Disruption

This prevents weak comparisons such as treating a semiconductor export-control case as directly comparable to a corporate layoff unless the input text clearly explains the link. The layer is deterministic and local: it does not use live web search, external news APIs, RAG, or LLM calls.

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
Decision Snapshot:
Current Position: Monitor closely and prepare staged response options
Confidence: Medium
Why: Historical cases suggest the first headline is rarely the full impact; the
real risk usually appears through implementation details, exposure mapping,
compliance burden, customer eligibility, margins, or management reaction.
Next 30-90 Days: Track management guidance, supplier/customer exposure,
implementation details, margin pressure, and whether the issue remains temporary
or becomes structural.

Decision Question:
The key question is not only what happened, but whether this event creates a
temporary adjustment problem or a deeper structural risk.

Decision Criteria:
- Customer exposure — Importance: High. Restricted end-user exposure determines
  whether market access is actually constrained.
- Licensing uncertainty — Importance: High. Approval timing and denial patterns
  determine whether the issue becomes an operating bottleneck.
- Margin impact — Importance: High. Costs matter if they flow through to
  revenue, pricing, or profitability.
- Compliance burden — Importance: Medium. Documentation and staffing costs can
  become durable operating work.

Decision Paths:
- Option A: Wait for final rule detail before changing operations.
  Criteria Fit: low disruption, but weak if customer exposure or licensing
  uncertainty becomes binding.
- Option B: Map exposure and prepare staged adjustments. Recommended.
  Criteria Fit: strongest fit against customer exposure, licensing uncertainty,
  and margin impact while preserving flexibility.
- Option C: Immediately reduce exposed customers, suppliers, or product lines.
  Criteria Fit: stronger protection, but higher execution cost if details remain
  uncertain.

Option Ranking:
1. Option B ranks first because the highest-importance criteria are customer
   exposure, licensing uncertainty, and margin impact. It improves readiness
   without creating the execution burden of Option C or the underpreparedness
   of Option A.
2. Option A ranks second because it has lower cost, but can leave the team
   underprepared if exposure grows.
3. Option C ranks third because it is protective but costly unless restrictions
   are already binding.

Preferred Path:
Option B currently ranks first because it performs best on the criteria that
matter most for this decision. The recommendation accepts monitoring and
coordination costs, but avoids premature irreversible action.

Trade-offs:
- Benefits gained: exposure mapping, readiness, and reversibility.
- Costs accepted: monitoring cadence, internal ownership, and compliance review.
- Opportunities sacrificed: the lowest-effort posture of Option A and the
  maximum immediate protection of Option C.
- Risks still unresolved: future rule details, license denials, customer
  eligibility changes, and margin pressure.

What Could Change This Recommendation:
- License denials become binding.
- Customer eligibility materially worsens.
- Margin damage becomes structural.
- Management guidance shifts from temporary disruption to durable impairment.

Historical Evidence:
- Case: Prior semiconductor equipment controls.
  Why it supports the recommendation: licensing and equipment access became
  operational work, not only policy headlines.
  Key limitation: current rule scope, actor exposure, and timing may differ.
  Decision lesson: map exposure before making irreversible operating changes.

What to Monitor:
- Management guidance and operating commentary.
- Supplier and customer exposure.
- Implementation details, licensing rules, exemptions, or timelines.
- Margin pressure, cost absorption, or working-capital strain.

Action Timeline:
- Immediate: review supplier exposure and list products/customers requiring
  license or eligibility review.
- Next 30 Days: track compliance costs and management commentary.
- Next Quarter: reassess whether evidence still supports Option B or whether
  Option A or Option C has become more appropriate.
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
Document or readable webpage
-> Similar Case Retrieval
-> Historical Outcome Review
-> Market Expectations vs Actual Outcomes
-> Direct Answer
-> What To Watch Next
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
- Free-form analyst questions with deterministic intent routing.
- Beginner, analyst, and executive output modes.
- English, Simplified Chinese, and Traditional Chinese localization for key output structure and labels.
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
- A live web-search or monitoring product.
- A production SaaS deployment.

Historical outcome records are simplified educational summaries. Source URLs are not fabricated; unavailable URLs remain marked through source status fields such as `source pending`. Confidence labels reflect internal evidence coding for this portfolio project, not real-world predictive accuracy.

The system does not prove factual correctness, legal accuracy, financial accuracy, geopolitical accuracy, or future outcomes. Human expert review is required before executive use.

## Local App Readiness

The intended normal-user product path remains:

```text
Download -> Open App -> Ask Question
```

That desktop wrapper is not built yet. The current repository is a working local product demo and portfolio implementation, but it still requires a developer-style setup to run the FastAPI server.

**Normal User Vision**

- Planned experience: no Python, Git, VS Code, terminal commands, or local server setup.
- Current limitation: the no-code desktop app packaging is not implemented yet.
- Product goal: type a question, paste content or URL, upload a file if needed, click Analyze, and download results.

**V12 Desktop App Roadmap**

- Mac `.app`
- Windows `.exe`
- Download -> double click -> use
- No Python required
- No Git required
- No VS Code required

**For Developers**

- Use Python, Git, and a local FastAPI server.
- Run the dashboard locally for testing and portfolio review.
- Inspect generated Markdown, TXT, and JSON artifacts under `outputs/runs/`.

## Developer Setup

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

Run engineering checks:

```bash
python3 -m ruff check .
python3 -m compileall app.py src tests
python3 -m pytest
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
- No live web search, external news monitoring, or source-grounded web research is performed. URL mode only attempts to fetch readable text from a user-provided page.
- No RAG infrastructure or LLM reasoning benchmark is included.
- No forecasts, probabilities, investment advice, legal advice, or trading recommendations are generated.
