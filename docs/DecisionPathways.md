# Decision Pathway Drafts

Version 4 Sprint 3 adds deterministic Decision Pathway Drafts.

Pathway drafts are reviewer-facing scaffolds generated from the Decision Readiness Map. They help reviewers compare possible decision paths without selecting, ranking, scoring, or recommending any path.

## What It Produces

The core output is a `DecisionPathwayDraftSet`.

Each draft includes:

- `pathway_id`
- `title`
- `pathway_family`
- `description`
- `applicable_frameworks`
- `supporting_evidence_refs`
- `related_risk_categories`
- `related_constraints`
- `historical_support_refs`
- `assumptions`
- `unknowns`
- `tradeoffs`
- `decision_triggers`
- `reviewer_questions`
- `limitation_notes`

The output intentionally excludes:

- ranking
- probability
- score
- best pathway
- recommendation score

## Pathway Families

Supported pathway families:

- `maintain_current_course`
- `delay_or_wait`
- `accelerate_or_expand`
- `diversify_or_hedge`
- `reduce_exposure`
- `seek_regulatory_clarity`
- `staged_commitment`
- `contingency_preparation`
- `further_evidence_required`

The engine generates 2 to 4 drafts when readiness is sufficient or partially sufficient. If the readiness map is insufficient, it generates a limited `further_evidence_required` draft. If regulatory uncertainty blocks readiness, it includes `seek_regulatory_clarity`.

## Inputs

The pathway drafting engine consumes:

- decision question
- optional decision context
- Decision Readiness Map
- applicable frameworks
- accepted evidence references
- Evidence Intelligence signals when available

It does not retrieve evidence, accept evidence, monitor sources, call an LLM, or generate a Decision Brief.

## Deterministic Rules

Draft families are selected from readiness state, mapped risks, mapped constraints, readiness issues, and evidence support.

Examples:

- insufficient evidence maps to `further_evidence_required`
- regulatory uncertainty maps to `seek_regulatory_clarity`
- market, financial, supply chain, or geopolitical risk can add `diversify_or_hedge`
- financial, counterparty, or sanctions/export-control risk can add `reduce_exposure`
- weak freshness or source diversity adds limitation notes
- unresolved conflicts add limitation notes and reviewer questions

No pathway is labeled as preferred.

## API

The read-only endpoint is:

```text
GET /projects/{project_id}/decision/pathways
```

It reads project data, builds or reuses Decision Readiness, and returns pathway drafts.

It does not:

- mutate project state
- generate a Decision Brief
- retrieve evidence
- accept evidence
- dismiss evidence
- rank pathways
- assign probabilities

## Dashboard Panel

The dashboard includes a compact read-only `Decision Pathway Drafts` panel in the active Project Workspace.

The panel displays:

- pathway title
- family
- description
- supporting evidence references
- risks and constraints
- assumptions
- unknowns
- decision triggers
- reviewer questions
- limitation notes

The panel is for reviewer comparison only.

## Boundaries

Decision Pathway Drafts are not:

- recommendations
- investment advice
- legal advice
- forecasts
- final decisions
- autonomous research
- autonomous monitoring

The reviewer remains responsible for source verification, legal/compliance review, investment judgment, and final decision-making.
