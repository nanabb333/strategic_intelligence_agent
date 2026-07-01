# Pathway Comparison Matrix

Version 4 Sprint 5 adds a deterministic Pathway Comparison Matrix.

The matrix compares generated decision pathway drafts side by side. It helps reviewers compare evidence support, risks, constraints, domain concerns, assumptions, unknowns, timing, reversibility, and limitations.

It does not choose a pathway.

## What It Produces

The core output is a `PathwayComparisonMatrix`.

Each pathway comparison row includes:

- pathway ID
- pathway title
- pathway family
- evidence support summary
- supporting evidence references
- risk exposure summary
- regulatory constraint summary
- domain evaluation summary
- assumptions summary
- unknowns summary
- historical support summary
- execution complexity
- reversibility
- time sensitivity
- decision triggers
- reviewer questions
- limitation notes
- categorical dimension buckets

## Comparison Dimensions

The matrix uses these dimensions:

- evidence support
- risk exposure
- regulatory constraints
- domain-specific risks
- historical support
- assumptions required
- unknowns remaining
- execution complexity
- reversibility
- timing sensitivity
- evidence quality concerns

Buckets are categorical only:

- `low`
- `medium`
- `high`
- `mixed`
- `unknown`
- `not_applicable`

No numeric scores are produced.

## Deterministic Rules

The matrix uses deterministic inputs from:

- Decision Pathway Drafts
- Decision Readiness
- Domain Decision Evaluation
- Evidence Intelligence

Examples:

- many unresolved unknowns produce a high unknowns bucket
- regulatory uncertainty produces a high regulatory-constraint bucket
- stale or source-concentrated evidence produces medium or high evidence quality concern
- staged commitment and contingency preparation preserve higher reversibility
- accelerate / expand or reduce exposure can increase execution complexity
- sparse historical support produces low or unknown historical support

All summaries are explainable and traceable to evidence references where evidence exists.

## API

The read-only endpoint is:

```text
GET /projects/{project_id}/decision/pathway-comparison
```

It reads project data and reuses pathway drafts, readiness, domain evaluation, and evidence intelligence.

It does not:

- mutate project state
- retrieve evidence
- generate a Decision Brief
- select a pathway
- rank pathways
- assign probabilities
- provide investment advice
- provide legal advice

## Dashboard Panel

The dashboard includes a compact read-only `Pathway Comparison Matrix` panel.

It shows:

- side-by-side categorical matrix
- evidence support
- key risks
- regulatory constraints
- domain-specific concerns
- historical support
- assumptions
- unknowns
- execution complexity
- reversibility
- timing sensitivity
- decision triggers
- reviewer questions

The panel is for reviewer comparison only.

## Boundaries

The Pathway Comparison Matrix is not:

- a recommendation
- a ranking
- a scorecard
- a forecast
- investment advice
- legal advice
- a best-option selector
- autonomous research
- autonomous monitoring

The reviewer remains responsible for interpreting the matrix, verifying evidence, resolving constraints, and making decisions.
