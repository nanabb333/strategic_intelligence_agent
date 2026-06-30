# V4 Workspace Demo

This folder is a release-validation demo for the Version 4 Decision Workspace workflow.

## Workflow

Project -> Questions -> Evidence Library -> Analysis Runs -> Decision Timeline -> Decision Delta

## Files

- `project.json`: sample project workspace with linked questions, evidence library, and decision history.
- `evidence_library.json`: standalone evidence library sample.
- `decision_history.json`: completed project decision timeline entries.
- `decision_delta.json`: deterministic latest-vs-previous decision comparison.
- `question_1_q_export_controls_immediate/`: generated Markdown, TXT, JSON, trace, metadata, and input artifacts for the first project question.
- `question_2_q_export_controls_update/`: generated Markdown, TXT, JSON, trace, metadata, and input artifacts for the second project question.

## Score Display

Reviewer-facing project and delta summaries use explicit score scales such as `9.7 / 10`. Raw `analysis.json` files preserve internal normalized values for machine-readable regression and API compatibility.

## Product Boundary

This demo uses local supplied text and deterministic repository logic. It does not perform autonomous browsing, background monitoring, live retrieval, multi-agent orchestration, or external evidence collection.
