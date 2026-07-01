# Version 5.0 Release Notes

Version 5.0 is the Enterprise Product Release of Repo 5: Strategic Intelligence Decision Companion.

This release focuses on product quality, release readiness, documentation clarity, reviewer workflow, and enterprise consistency. It does not add a new reasoning layer, autonomous agent behavior, autonomous browsing, monitoring, or external infrastructure.

## Release Positioning

Repo 5 is an Enterprise Decision Intelligence Platform. It helps reviewers structure strategic decisions through evidence, historical analogues, confidence assessment, decision quality checks, project workspaces, evidence lifecycle controls, and local artifacts.

Repo 5 is not a chatbot, autonomous research platform, autonomous decision maker, or monitoring system.

## What Is Included

- Deterministic Decision Intelligence pipeline.
- Project Workspace with questions, evidence library, decision timeline, and decision delta.
- Decision Context linking runs to project ID, question ID, selected evidence IDs, and Evidence Bundle.
- Evidence lifecycle and decision lifecycle governance metadata.
- Evidence Ledger and audit-oriented project evidence records.
- Enterprise configuration defaults in `config/defaults.json`.
- Diagnostics endpoint at `GET /diagnostics`.
- Release metadata endpoint at `GET /version`.
- Local JSON storage for projects and run artifacts.
- Lavender-grey enterprise dashboard identity.
- V4 workspace demo artifacts under `demo_case_outputs/v4_workspace/`.

## Compatibility

Version 5.0 is compatible with Version 4 and Version 4.5 local project JSON workspaces. New metadata is additive. Existing projects without archive, lifecycle, or release metadata should continue to load.

## Local Validation

Run:

```bash
python3 -m pytest
```

Optional API checks after starting FastAPI:

```text
GET http://127.0.0.1:8000/health
GET http://127.0.0.1:8000/version
GET http://127.0.0.1:8000/diagnostics
```

## Boundaries

Version 5.0 intentionally does not add:

- autonomous agents
- autonomous browsing
- background monitoring
- new LLM workflows
- external search providers
- databases
- microservices
- cloud dependencies
- authentication

These boundaries keep the product local-first, deterministic, reviewer-first, and maintainable.
