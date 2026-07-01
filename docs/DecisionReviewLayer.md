# Decision Review Layer

Version 4 Sprint 6 adds a reviewer-controlled Decision Review Layer.

The review layer records human review state around pathway drafts, comparison matrix cells, assumptions, unknowns, and decision triggers. It is auditable, project-scoped, and stored in local project JSON.

It does not approve, reject, select, rank, score, or recommend pathways.

## What Can Be Reviewed

Reviewers can record state for:

- pathway drafts
- comparison matrix cells
- assumptions
- unknowns
- decision triggers
- reviewer notes
- unresolved decision questions

Allowed review statuses:

- `not_reviewed`
- `reviewed`
- `accepted_for_consideration`
- `questioned`
- `needs_more_evidence`
- `needs_legal_or_compliance_review`
- `unresolved`

The model intentionally avoids:

- approved
- rejected
- selected
- recommended
- best

## Review Summary

The deterministic summary includes:

- reviewed pathways count
- unresolved issues count
- items needing more evidence
- items needing legal or compliance review
- unresolved decision questions
- latest reviewer note timestamp

No score, readiness upgrade, recommendation, or final decision is produced.

## Persistence

Review state is stored under:

```text
project["decision_review_state"]
```

This is backward-compatible with existing project JSON. Projects without review state return an empty default review state.

The review layer does not mutate:

- evidence acceptance state
- evidence lifecycle
- Decision Brief artifacts
- analysis runs
- pathway drafts

## API

Read current review state:

```text
GET /projects/{project_id}/decision/review
```

Update review state:

```text
PUT /projects/{project_id}/decision/review
```

The update endpoint accepts reviewer-controlled review status, notes, unresolved questions, and optional traceability metadata.

It does not retrieve evidence, run analysis, generate a Decision Brief, select a pathway, or modify accepted evidence.

## Dashboard

The dashboard includes a compact `Decision Review` panel in the active project workspace.

Reviewers can:

- mark an item as reviewed
- mark needs more evidence
- mark needs legal or compliance review
- add a reviewer note
- add an unresolved question

The UI avoids approval, rejection, selection, best-path, or recommendation language.

## Boundaries

The Decision Review Layer is not:

- an approval workflow
- a recommendation engine
- an investment advisor
- a legal advisor
- a final decision record
- autonomous research
- autonomous monitoring

The reviewer remains responsible for interpreting review state and making final decisions outside the system.
