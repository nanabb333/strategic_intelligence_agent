# Review Guide

This guide is for reviewers who want to understand Strategic Intelligence Agent quickly without reading every document in the repository.

## Recommended Reading Order

1. [README](../README.md): product summary, setup, demo walkthrough, and limitations.
2. [Product Overview](ProductOverview.md): users, supported inputs, outputs, workflow, and limitations.
3. [Demo Scenarios](DemoScenarios.md): realistic portfolio demo cases.
4. [Engineering Architecture](EngineeringArchitecture.md): FastAPI, service layer, pipeline, artifacts, and storage.
5. [Testing](Testing.md): test scope, CI checks, and validation commands.
6. [Repository Trust Audit](RepositoryTrustAudit.md): scientific, engineering, product, and UX credibility review.

## How To Run Locally

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

## How To Interpret Outputs

The brief is designed as decision support, not a prediction.

Review the output in this order:

1. **Decision Snapshot:** current recommendation, confidence language, rationale, and review window.
2. **Decision Criteria:** factors that should drive the decision.
3. **Decision Paths:** available options and why one path is currently preferred.
4. **Historical Evidence:** cases that may resemble the current situation.
5. **Trade-offs and Assumptions:** what is gained, accepted, sacrificed, or unresolved.
6. **Monitoring Signals:** evidence that could change the current recommendation.
7. **Limitations:** where human review remains necessary.

## Downloaded Artifacts

Each run creates:

- `input.txt`: source material used for the run.
- `brief.md`: Markdown decision brief.
- `brief.txt`: plain text decision brief.
- `analysis.json`: structured analysis object.
- `agent_trace.json`: local route and tool trace.
- `metadata.json`: run metadata.

Runtime folders are written under `outputs/runs/` and ignored by git.

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

Existing dashboard preview files are stored in [docs/screenshots](screenshots/).

No new screenshot was fabricated for this final polish pass.
