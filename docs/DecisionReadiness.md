# Decision Readiness

Version 4 Sprint 2 adds a deterministic Decision Readiness layer.

Decision Readiness is the bridge between Evidence Intelligence and future Decision Pathways. It answers a reviewer workflow question:

```text
Is the current decision question and accepted evidence set ready for pathway analysis?
```

It does not decide what to do.

## What It Produces

The core output is a `DecisionReadinessMap` with:

- decision question
- applicable frameworks
- primary framework
- framework evidence maps
- risk coverage
- constraint coverage
- historical support
- assumption map
- unknowns map
- evidence gaps
- over-concentration flags
- conflict flags
- freshness flags
- source diversity flags
- reviewer questions
- readiness issues
- readiness summary

All mapped signals include evidence references when evidence exists.

## Framework Evidence Mapping

For each applicable `DecisionFramework`, the readiness layer maps accepted project evidence into:

- required evidence categories
- required risk categories
- required constraints
- historical dimensions
- pathway dimensions
- reviewer questions

Coverage buckets are categorical:

- `covered`
- `partially_covered`
- `missing`
- `over_concentrated`
- `unknown`

The layer does not calculate a recommendation score, ranking, probability, or preferred pathway.

## Evidence Intelligence Integration

Decision Readiness consumes Evidence Intelligence outputs when available:

- decision risk evidence map
- regulatory / legal constraint flags
- historical pathway signals
- duplicate / support / conflict relationships
- freshness
- source diversity

It adapts these signals into framework-aware readiness. It does not duplicate retrieval, validation, ranking, or Decision Brief logic.

## Readiness States

Readiness states are workflow statuses:

- `ready_for_pathway_analysis`
- `partially_ready`
- `not_ready_insufficient_evidence`
- `blocked_by_conflicts`
- `blocked_by_regulatory_uncertainty`
- `stale_or_low_diversity_evidence`
- `unknown`

These states do not instruct the reviewer to proceed, stop, buy, sell, approve, reject, or take any legal position.

## Assumptions And Unknowns

The readiness layer maps deterministic assumptions such as:

- market continuity
- regulatory stability
- supply availability
- demand resilience
- execution capacity
- financing availability
- stakeholder alignment
- legal clearance
- data security
- geopolitical stability

It also surfaces unknown categories such as:

- missing market data
- missing financial impact
- missing regulatory status
- missing legal review
- missing supplier data
- missing customer demand
- missing timeline
- missing counterparty position
- missing historical outcome
- missing source diversity
- unresolved conflict

Each assumption or unknown includes an explanation, related framework dimensions where applicable, evidence references when available, and a reviewer question.

## API

The read-only endpoint is:

```text
GET /projects/{project_id}/decision/readiness
```

It reads:

- project questions
- project description/name as context
- accepted project evidence

It returns a `DecisionReadinessMap`.

It does not:

- mutate project state
- retrieve evidence
- accept or dismiss evidence
- generate a Decision Brief
- generate final pathways
- rank options

## Dashboard Panel

The dashboard shows a compact read-only `Decision Readiness` panel in the active Project Workspace, near Evidence Intelligence.

The panel displays:

- readiness summary
- applicable frameworks
- evidence coverage by framework
- key evidence gaps
- risk / constraint coverage
- historical support
- assumptions and unknowns
- reviewer questions
- readiness issues

The panel uses cautious reviewer-first language and does not provide a recommended action.

## Boundaries

Decision Readiness is not:

- investment advice
- legal advice
- a forecast
- autonomous research
- autonomous monitoring
- a chatbot
- a pathway generator
- a ranking engine

The reviewer remains responsible for all decisions, legal/compliance review, source verification, and final pathway interpretation.
