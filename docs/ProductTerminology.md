# Product Terminology

Current-facing documentation uses one official English vocabulary. Historical documents, code symbols, generated artifact fields, and compatibility routes may retain older wording when changing them would alter behavior or historical accuracy.

## Product Identity

- **Official product name:** Strategic Intelligence Decision Companion
- **Official category:** Deterministic, auditable, reviewer-first strategic decision-support system
- **Operating principles:** reviewer-first, local-first, deterministic, non-prescriptive

## Current Workflow Terms

| Term | Definition |
| --- | --- |
| Decision Question | The decision that requires reviewer judgment. |
| Decision Context | Reviewer-authored background, objectives, constraints, or criteria; not evidence. |
| Supporting Evidence | Material supplied or accepted for use in the assessment. |
| Neutral Decision Assessment | The structured review artifact; pathways are not ranked or selected by the system. |
| Human Review | Reviewer inspection, notes, unresolved questions, and judgment. |
| Export | Local Markdown, TXT, JSON, trace, or metadata artifacts. |
| Current Project | Optional persistent container for related questions, evidence, assessments, timeline, delta, and review state. |

## Supporting Capability Terms

| Term | Definition |
| --- | --- |
| Evidence Retrieval | User-triggered retrieval of reviewable evidence candidates. |
| Evidence Intelligence | Deterministic support for duplicate, conflict, freshness, coverage, novelty, and source-diversity review. |
| Decision Readiness | Deterministic map of evidence coverage, gaps, assumptions, unknowns, and reviewer questions. |
| Decision Pathway Draft | Deterministic reusable pathway archetype populated with case-derived references, risks, constraints, assumptions, and unknowns; not fully evidence-derived and not a recommendation. |
| Pathway Comparison Matrix | Categorical side-by-side comparison without preferred-option selection. |
| Decision Review | Reviewer-controlled status, notes, unresolved questions, and review summary. |
| Evidence Sufficiency | Structural review-workflow tier; does not validate source quality, source independence beyond detectable identifiers, claim-level support, analogue relevance, factual validity, or probability of correctness. |
| Artifact Completeness | Passed and missing field-presence/review-structure checks; not a `/10` score, factual validation, or decision-quality evaluation. |
| Tool Router | Rules-based orchestration and tool selection; not an autonomous agent. |

## Avoid In Current-Facing Copy

The formal product description is: "a deterministic, auditable, reviewer-first strategic decision-support system."

Do not present the product or primary workflow as an AI Agent, autonomous agent, Agent Router, LLM-powered system, trained machine-learning model, Workspace Management, Decision Workspace, Decision Snapshot, preferred-option selector, autonomous recommendation system, chatbot, autonomous researcher, monitoring system, forecasting engine, legal or investment advisor, compliance automation system, generic RAG demo, or autonomous decision maker. Historical internal class names may remain for compatibility; current UI and documentation use Tool Router or deterministic orchestration.

Older code symbols and compatibility artifacts should not be renamed solely for copy consistency.
