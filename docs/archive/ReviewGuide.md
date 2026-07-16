# Review Guide

This guide is for reviewers who want to understand Strategic Intelligence Decision Companion quickly without reading every document in the repository.

## Recommended Reading Order

1. [README](../../README.md): product summary, setup, demo walkthrough, and limitations.
2. [Product Overview](../ProductOverview.md): users, supported inputs, outputs, workflow, and limitations.
3. [Decision Intelligence Framework](../DecisionIntelligenceFramework.md): conceptual layers behind the product.
4. [Evidence Architecture](../EvidenceArchitecture.md): how evidence, observations, inferences, recommendations, confidence, and evaluation relate.
5. [Demo Scenarios](DemoScenarios.md): realistic portfolio demo cases.
6. [Engineering Architecture](../EngineeringArchitecture.md): FastAPI, service layer, pipeline, artifacts, and storage.
7. [Testing](../Testing.md): test scope, CI checks, and validation commands.
8. [Repository Trust Audit](../RepositoryTrustAudit.md): scientific, engineering, product, and UX credibility review.
9. [Version 4 Architecture](Version4Architecture.md): project workspace, evidence library, timeline, delta, and non-agent boundaries.

For V2 evidence-aware examples, review:

- [Semiconductor Export Controls](../case_studies/semiconductor_export_controls.md)
- [Red Sea Shipping Disruption](../case_studies/red_sea_shipping_disruption.md)
- [Industrial Subsidy Strategy](../case_studies/industrial_subsidy_strategy.md)

## How To Run Locally

### Option A: One-Click Local Launch

For non-technical reviewers on macOS:

1. Double-click `start.command` in the repository folder.
2. If macOS blocks it, right-click `start.command`, then choose **Open**.
3. Keep the terminal window open while reviewing.
4. The browser opens the dashboard at:

```text
http://127.0.0.1:8000/dashboard/
```

### Option B: Manual Terminal Launch

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Start the local app:

```bash
python3 -m uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000/dashboard/
```

## How To Test

Run:

```bash
python3 -m ruff check .
python3 -m compileall app.py src tests
python3 -m pytest
```

These checks validate linting, import/compile health, and the lightweight helper/API test suite.

## How To Test V4 Locally

Version 4 should be reviewed as a structured Decision Intelligence Workspace, not as a chat interface.

1. Start the local FastAPI app:

```bash
python3 -m uvicorn app:app --reload
```

2. Open the dashboard:

```text
http://127.0.0.1:8000/dashboard/
```

3. In **Projects**, create a new project.
4. Add a project question and keep it selected.
5. Paste source material into the decision input box.
6. Click **Build decision brief**.
7. Confirm the saved question now shows a linked run.
8. Add a manual Evidence Library note.
9. Select one or more Evidence Library items before running the next analysis.
10. Confirm the generated run JSON metadata includes `project_id`, `project_question_id`, and selected `evidence_ids`.
11. Confirm the analysis JSON includes an `evidence_bundle` and that selected evidence IDs appear in the Evidence Ledger.
12. Add a second project question and run another analysis.
13. Confirm the Decision Timeline has two entries.
14. Confirm Decision Delta appears and shows previous/current recommendation, confidence, Decision Quality on a `/ 10` scale, and durable project evidence ID changes when available.
15. Use **Search Current Evidence** only as a user-triggered candidate workflow; confirm retrieved items still require review and acceptance before they can be selected into an Evidence Bundle.
16. Use the browser print dialog to print or save PDF. The print view should focus on generated results, not the sidebar controls.

Standalone analysis should still work when no project is active.

## V4.5 Decision Context Before Retrieval

Decision Context is the required foundation for live retrieval:

```text
Project -> Question -> Selected Evidence IDs -> Evidence Bundle -> Analysis Run -> Timeline / Delta
```

Project-aware runs should be traceable to the project, project question, selected evidence IDs, and Evidence Bundle. Accepted evidence follows a simple lifecycle: Retrieved, Reviewed, Accepted, Used, Archived.

Live retrieval remains user-triggered and review-first. Retrieved items do not make decisions and do not automatically enter analysis. They are candidates for reviewer inspection before acceptance into the Evidence Library and explicit selection into an Evidence Bundle.

Default source ranking prefers:

- Tier 1 Official: government, regulator, court, central bank, SEC, official statistics.
- Tier 2 Company: annual report, 10-K, 10-Q, investor relations, press release.
- Tier 3 Reputable News: Reuters, AP, FT, WSJ, Bloomberg.

Tier 4 Research can be explicitly allowed for research context. Tier 5 Other is excluded by default and should only be allowed intentionally. This is not autonomous browsing, autonomous monitoring, or an tool-routing workflow.

## Suggested Demo Scenario

Use this decision question:

```text
What should management consider after new semiconductor export controls affect customer eligibility and advanced chip supply chains?
```

Use this supporting material:

```text
New semiconductor export controls affect advanced chip supply chains and market access. Equipment suppliers are reviewing licensing requirements, customer eligibility, and compliance documentation. Executives want to understand similar historical cases, observed outcomes, and what to monitor next.
```

Then click **Build decision brief**.

## V4 Workspace Demo Artifacts

The release-validation demo is stored in:

```text
demo_case_outputs/v4_workspace/
```

Review these files:

- `project.json`: sample V4 project with linked questions, evidence library, and decision history.
- `decision_delta.json`: deterministic latest-vs-previous comparison.
- `question_1_q_export_controls_immediate/brief.md`: first generated decision brief.
- `question_2_q_export_controls_update/brief.md`: second generated decision brief.
- `analysis.json` files: structured run artifacts for reviewer inspection.

## How To Interpret Outputs

The brief is designed as decision support, not a prediction.

Review the output in this order:

1. **Decision Snapshot:** current recommendation, confidence language, rationale, and review window.
2. **Decision Criteria:** factors that should drive the decision.
3. **Decision Paths:** available options and why one path is currently preferred.
4. **Historical Evidence:** cases that may resemble the current situation.
5. **Evidence and Confidence:** evidence items, qualitative confidence, assumptions, uncertainty, change triggers, and limitations.
6. **Trade-offs and Assumptions:** what is gained, accepted, sacrificed, or unresolved.
7. **Monitoring Signals:** evidence that could change the current recommendation.
8. **Limitations:** where human review remains necessary.

## Downloaded Artifacts

Each run creates:

- `input.txt`: source material used for the run.
- `brief.md`: Markdown decision brief.
- `brief.txt`: plain text decision brief.
- `analysis.json`: structured analysis object.
- `agent_trace.json`: local route and tool trace.
- `metadata.json`: run metadata.

Runtime folders are written under `outputs/runs/` and ignored by git.

The structured analysis JSON includes additive V2 fields: `decision_case`, `evidence_ledger`, `confidence_assessment`, and `decision_quality_evaluation`.

V4 project state is local JSON. The FastAPI app exposes project routes in `app.py`, workspace persistence lives in `src/project_workspace.py`, and dashboard workspace behavior lives in `dashboard/project.js`.

## What This Project Does Not Claim

The project does not claim:

- real-world predictive accuracy
- investment advice
- trading recommendations
- legal advice
- live web monitoring
- autonomous internet research
- production SaaS deployment

It should be evaluated as a local AI decision-support product and portfolio artifact.

## Screenshots

Existing dashboard preview files are stored in [docs/screenshots](../screenshots/).
