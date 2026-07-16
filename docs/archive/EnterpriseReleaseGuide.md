# Enterprise Release Guide

This guide describes how to review Repo 5 as an enterprise-ready local Decision Intelligence product.

## Release Identity

- Product: Strategic Intelligence Decision Companion
- Release: Version 5.0 Enterprise Product Release
- Runtime: local FastAPI application with vanilla HTML, CSS, and JavaScript dashboard
- Storage: local JSON project files and local run artifact folders
- Boundary: deterministic decision-support platform, not an autonomous agent

## Reviewer Flow

1. Start the local app:

```bash
python3 -m uvicorn app:app --reload
```

2. Open:

```text
http://127.0.0.1:8000/dashboard/
```

3. Create a project.
4. Add a project question.
5. Add or accept evidence into the project evidence library.
6. Select evidence for the run.
7. Build the decision brief.
8. Review the Decision Snapshot, Evidence and Confidence, Decision Timeline, and Decision Delta.
9. Download Markdown, TXT, or JSON artifacts.
10. Check release metadata and diagnostics:

```text
http://127.0.0.1:8000/version
http://127.0.0.1:8000/diagnostics
```

## Release Checks

Use this checklist before portfolio presentation or external review:

- `python3 -m pytest` passes.
- Dashboard loads at `/dashboard/`.
- `/health` returns status `ok`.
- `/version` returns Version 5.0 release metadata.
- `/diagnostics` reports project and run storage state.
- A standalone analysis run still works.
- A project-aware analysis run links `project_id`, `project_question_id`, and selected `evidence_ids`.
- Download links for Markdown, TXT, and JSON work.
- Existing Version 4 workspace demo artifacts remain available.

## Recovery Model

Repo 5 is local-first. Recovery is based on visible local files:

- Projects live under `data/projects/`.
- Runs live under `outputs/runs/`.
- Demo artifacts live under `demo_case_outputs/`.
- Configuration defaults live under `config/defaults.json`.

Malformed project files should appear as diagnostics warnings rather than crash project listing. Diagnostics do not delete data or mutate workspace state.

## Deployment Notes

Version 5.0 is intended for local demonstrations and code review. Docker, hosted auth, user accounts, centralized databases, telemetry, and cloud deployment are future product decisions, not release requirements.
