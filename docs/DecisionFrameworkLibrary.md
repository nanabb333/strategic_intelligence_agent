# Decision Framework Library

Version 4 Decision Intelligence begins with reusable architecture, not recommendations.

This layer defines deterministic decision frameworks, question classification, and structural pathway models that future Decision Intelligence features can build on. It does not change the Decision Brief, Evidence Retrieval, Evidence Acceptance, Evidence Intelligence, Dashboard, or API behavior.

## Purpose

The Decision Framework Library helps the platform identify what kind of decision a reviewer is working on and which dimensions should be considered. It is designed for explainability, maintainability, reviewer workflow, and auditability.

It is not:

- an autonomous agent
- a chatbot
- a forecasting engine
- an investment advisor
- a legal advisor
- a recommendation engine

The reviewer remains responsible for all decisions.

## Module

The implementation lives in:

```text
src/decision_frameworks.py
```

The module is intentionally isolated. It does not import the FastAPI app, dashboard code, retrieval code, or Decision Brief generation pipeline.

## Framework Library

Each `DecisionFramework` defines:

- `framework_id`
- `name`
- `description`
- `applicable_decision_types`
- `required_evidence_categories`
- `required_risk_categories`
- `required_constraints`
- `historical_dimensions`
- `pathway_dimensions`
- `reviewer_questions`

Initial frameworks:

- Investment Decision
- Corporate Strategy
- Supply Chain
- Regulatory / Compliance
- Export Control
- Market Entry
- Strategic Partnership
- Capital Allocation
- Technology Strategy
- Board / Executive Decision

These frameworks describe dimensions that matter for review. They do not select a preferred action.

## Decision Question Classification

`classify_decision_question()` accepts:

- decision question
- optional decision context
- optional evidence metadata

It returns:

- decision type
- applicable framework definitions
- confidence bucket: `High`, `Medium`, or `Low`
- matched keywords
- matched metadata
- rationale

Classification uses deterministic keyword and metadata rules only. There is no ML, embedding search, LLM call, or external retrieval.

Confidence reflects rule coverage only. It is not a probability of correctness, investment confidence, legal confidence, or forecast confidence.

## Decision Pathway Model

`DecisionPathway` is a reusable data structure for future pathway work.

Fields:

- `pathway_id`
- `title`
- `description`
- `supporting_evidence_refs`
- `historical_analogue_refs`
- `risk_categories`
- `regulatory_constraints`
- `assumptions`
- `unknowns`
- `decision_triggers`
- `tradeoffs`
- `reviewer_notes`

The model intentionally excludes:

- recommendation score
- AI confidence score
- ranking
- probability
- best pathway

## Decision Comparison Model

`DecisionComparison` is a structural container for future side-by-side pathway review.

Fields:

- `pathways`
- `comparison_dimensions`
- `evidence_matrix`
- `risk_matrix`
- `constraint_matrix`
- `historical_matrix`
- `unknown_matrix`

It does not calculate a preferred pathway.

## Future Build Path

Future versions can use this architecture to:

1. classify a decision question
2. select relevant frameworks
3. map accepted evidence into framework dimensions
4. create reviewer-defined pathways
5. compare pathways across evidence, risk, constraints, history, and unknowns

The current sprint stops before pathway generation. It establishes the reusable foundation only.

## Boundaries

This layer must not:

- make recommendations
- provide investment advice
- provide legal advice
- rank pathways
- assign probabilities
- trigger retrieval
- mutate project evidence
- change the Decision Brief
- change dashboard or API behavior

Any future feature that uses this module should preserve reviewer control and deterministic traceability.
