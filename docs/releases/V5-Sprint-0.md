# V5 Sprint 0 - Decision-First Information Architecture Migration

This document describes **V5 Sprint 0**, not a complete final Version 5 release.

## Version Position

- **V4.9:** stable V4 freeze baseline and enterprise design assessment.
- **V4.10:** reviewer workflow layout correction.
- **V5 Sprint 0:** decision-first information architecture migration.
- **Sprint 0 stabilization:** restoration of the stable enterprise workbench layout after the decision-first migration.

The dashboard and landing page report `V5 Sprint 0`. Application configuration and `GET /version` retain software version `5.0.0` and the compatibility label `Enterprise Product Release`; explicit `milestone: V5 Sprint 0` and `stage: sprint-0` fields define the current release phase. The compatibility label alone does not indicate a complete final V5 release.

## Sprint 0 Scope

Sprint 0 reorganized the current interface around:

```text
Decision Question
  -> Decision Context
  -> Supporting Evidence
  -> Decision Assessment
  -> Human Review
  -> Export
```

Project remains a secondary persistent container for related questions, evidence, assessments, timeline, delta, and review state.

## What Changed

- Made the decision question the primary entry point.
- Separated reviewer-authored Decision Context from Supporting Evidence.
- Renamed the primary review surface to Decision Assessment.
- Moved project selection into a secondary Current Project control.
- Aligned assessment, evidence, limitations, export, and recent-decision labels with the decision-first workflow.
- Preserved the existing local FastAPI, deterministic pipeline, project storage, and artifact behavior.

## What Sprint 0 Does Not Establish

Sprint 0 does not establish a final V5 release, production readiness, enterprise deployment readiness, compliance, benchmark leadership, or real-world accuracy. It does not add autonomous agents, autonomous research, background monitoring, forecasting, databases, cloud infrastructure, authentication, or final decision automation.

## Compatibility And Validation

The migration and layout stabilization retained the existing routes, storage schemas, and analysis behavior. Validate the current repository with:

```bash
ruff check .
python3 -m py_compile app.py src/*.py launch.py
python3 -m pytest
node --check dashboard/app.js
node --check dashboard/project.js
```

## Owner Action

- Capture a populated screenshot of the current Decision Assessment interface.
