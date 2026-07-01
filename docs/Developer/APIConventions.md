# API Conventions

Repo 5 keeps existing routes backward-compatible. Future routes should follow these conventions unless there is a compatibility reason not to.

## Route Families

| Area | Preferred Pattern | Current Examples |
| --- | --- | --- |
| Health and release | top-level noun | `GET /health`, `GET /version`, `GET /diagnostics` |
| Runs | `/runs`, `/run/{run_id}` | `GET /runs`, `GET /run/{run_id}`, `GET /run/{run_id}/download/{artifact}` |
| Projects | `/projects`, `/projects/{project_id}` | `GET /projects`, `POST /projects`, `GET /projects/{project_id}` |
| Project questions | `/projects/{project_id}/questions` | `POST /projects/{project_id}/questions` |
| Project evidence | `/projects/{project_id}/evidence` | `GET /projects/{project_id}/evidence`, `POST /projects/{project_id}/evidence`, `POST /projects/{project_id}/evidence/accept` |
| Evidence retrieval | `/retrieve-evidence` | `POST /retrieve-evidence` |
| Decision views | `/projects/{project_id}/decision/{view}` | `readiness`, `pathways`, `domain-evaluation`, `pathway-comparison`, `review` |

## Naming Standard

- Use nouns for durable resources: `projects`, `evidence`, `runs`.
- Use explicit decision-view names under `/decision/`.
- Keep retrieval user-triggered and separate from evidence acceptance.
- Prefer read-only `GET` for derived reviewer support panels.
- Use `POST` or `PUT` only when reviewer-controlled state changes.

## Compatibility Notes

`/analyze` remains the stable standalone and project-aware analysis route. It is acceptable for `/analyze` to accept optional project context because existing clients already use it. A dedicated project analysis route can be considered later only if `/analyze` becomes hard to reason about.

## Boundaries

Routes must not imply autonomous behavior. Avoid names like `/agent`, `/autopilot`, `/monitor`, `/watch`, `/decide`, `/approve`, or `/recommend-best`.
