# Version 4 Architecture

Version 4 evolves the platform from a one-time analysis tool into a structured Decision Intelligence Workspace.

This document defines the Version 4 workspace architecture and the boundaries implementation should respect. V4 adds local project workspace behavior, but it does not add live retrieval, storage infrastructure, or autonomous agents.

## Product Direction

Version 4 should preserve the product identity:

- Decision Intelligence Platform, not chatbot.
- Structured decision workspace, not conversational assistant.
- Evidence-backed recommendations, not autonomous research.
- Human-controlled workflows, not background monitoring.

The platform should help users work on decisions over time while keeping evidence, reasoning, recommendations, and change history reviewable.

## Primary Objectives

Version 4 should improve four areas:

- Decision Workspace
- Evidence Intelligence
- Evidence Traceability
- Decision Evolution

Any proposed capability should strengthen at least one of these areas and remain consistent with the Decision Intelligence Constitution.

## Decision Workspace

A Project represents a long-running decision problem.

Examples:

- US Export Controls
- Taiwan Expansion
- AI Infrastructure Investment
- Supply Chain Relocation

A Project should contain:

- Questions
- Evidence Library
- Decision History
- Generated Briefs
- Decision Timeline

Questions remain independent analyses. Projects provide continuity across those analyses.

## Questions

A Question is a specific decision-support request inside a Project.

Each Question should generate:

- Decision Brief
- Evidence Chain
- Recommendation
- Confidence Assessment
- Historical Analogues

Questions should not overwrite prior analyses. Each analysis should remain reproducible from its evidence bundle, configuration, and generated artifacts.

## Evidence Bundle

Version 4 should replace isolated inputs with a unified Evidence Bundle concept.

Evidence may originate from:

- Uploaded documents
- URLs supplied by the user
- User notes
- Project evidence library items
- Optional user-triggered live retrieval

The reasoning engine should operate on an Evidence Bundle rather than treating each input type as a separate product path.

The bundle should preserve source identity, evidence type, extraction notes, verification status, and relationship to the decision question.

## Evidence Library

Each Project should maintain a reusable Evidence Library.

Examples:

- Government publications
- Annual reports
- SEC filings
- Company announcements
- News articles supplied by the user
- Internal documents
- Uploaded PDFs
- User notes

Evidence should be reusable across multiple Questions. Users should not need to repeatedly upload or paste the same material for related analyses.

## Optional Live Evidence

Live retrieval may be added only as a user-triggered capability.

The platform must not perform autonomous browsing, autonomous searches, autonomous monitoring, or background source collection.

The intended workflow is:

```text
Question
  |
  v
Optional User-Triggered Retrieval
  |
  v
Evidence Collection
  |
  v
Evidence Validation
  |
  v
Evidence Bundle
  |
  v
Existing Decision Engine
```

Retrieved evidence should supplement user-provided evidence and repository historical knowledge. It should not replace human source selection or imply completeness.

## Evidence Traceability

Every recommendation should be traceable through a visible chain:

```text
Recommendation
  |
  v
Reasoning Rule
  |
  v
Historical Analogue
  |
  v
Evidence Statement
  |
  v
Original Source
```

The trace should make it clear whether support comes from a user-provided source, repository knowledge, historical analogue, internal inference, or future external evidence.

## Evidence Status

Evidence status should describe evidence state without claiming objective certainty.

Supported status language should include:

- Verified
- Corroborated
- User Provided
- Single Source
- Conflicting
- Historical Only
- Outdated
- Unavailable

Status labels should affect confidence and explanation. They should not be used as decorative metadata.

## Evidence Ranking

Evidence ranking should be deterministic and explainable.

Ranking dimensions may include:

- Authority
- Freshness
- Specificity
- Corroboration
- Question Relevance

The system should explain why evidence was ranked as stronger or weaker. It should not hide ranking logic behind opaque scores.

## Conflict Detection

The platform should recognize when evidence disagrees.

Conflicts should:

- Lower confidence where they affect the recommendation.
- Identify which sources disagree.
- Explain why the disagreement matters.
- Name what additional evidence would resolve or narrow the conflict.

The system should not force a single confident conclusion when the evidence base is materially conflicted.

## Decision Evolution

A Project should remember previous recommendations and make change over time reviewable.

When new evidence is added, the platform should compare:

```text
Previous Recommendation
  |
  v
New Evidence
  |
  v
What Changed
  |
  v
Updated Recommendation
```

Decision history should live in the Project. It should not be hidden inside transient conversations or overwritten by later analyses.

## Implemented Runtime Shape

Version 4 is implemented as a local workspace layer around the existing deterministic decision engine.

```text
Dashboard Project Workspace
  |
  v
FastAPI Project Routes
  |
  v
Local JSON Project Storage
  |
  v
Existing Analysis Pipeline
  |
  v
Run Artifacts + Project Timeline + Decision Delta
```

Key files:

- `app.py`: exposes `/projects`, `/projects/{project_id}`, `/projects/{project_id}/questions`, `/projects/{project_id}/evidence`, `/projects/{project_id}/delta`, and project-aware `/analyze` linking.
- `src/project_workspace.py`: creates and updates local project JSON files, stores questions, evidence notes, decision history, and deterministic decision delta.
- `src/evidence_retrieval.py`: provides the Version 4.5 user-triggered retrieval interface, deterministic source tiering, and a small provider abstraction that can later be swapped without changing the workspace contract.
- `dashboard/project.js`: controls project creation, active project state, selected project question, evidence note entry, timeline rendering, and delta rendering.
- `data/projects/`: local JSON project storage for runtime project state.
- `outputs/runs/`: local generated run artifacts for analysis output.
- `demo_case_outputs/v4_workspace/`: bundled release-validation demo with sample project, linked questions, evidence library, decision history, delta, and generated artifacts.

This remains a workspace, not a chatbot. There is no conversational memory thread, autonomous browsing, background monitoring, multi-agent orchestration, external retrieval loop, database service, or cloud dependency. A user explicitly creates projects, adds evidence notes, selects questions, and runs analyses.

## Version 4.5 Evidence Retrieval Candidate

Version 4.5 adds a bounded retrieval candidate workflow:

```text
User Clicks Search Current Evidence
  |
  v
Retrieve Evidence Candidates
  |
  v
Evidence Review Queue
  |
  v
User Accepts Selected Items
  |
  v
Project Evidence Library
  |
  v
Existing Decision Engine
```

Retrieval creates reviewable evidence items only. It must not directly update recommendations, call analysis, schedule follow-up searches, or monitor sources in the background.

The backend route `/retrieve-evidence` returns candidate items with:

- title
- source name
- source URL
- source type
- published date when available
- retrieved date
- excerpt
- status
- credibility tier
- freshness note

The project route `/projects/{project_id}/evidence/accept` saves selected retrieved items into the project evidence library after user review.

Source tiering is deterministic:

- Tier 1 Official: government, regulator, court, central bank, SEC, official statistics.
- Tier 2 Company: annual report, 10-K, 10-Q, investor relations, press release.
- Tier 3 Reputable News: Reuters, AP, FT, WSJ, Bloomberg.
- Tier 4 Research: academic, IMF, World Bank, OECD, NBER.
- Tier 5 Other: blogs, social, forums.

Tier 1-3 are included by default. Tier 5 is excluded unless explicitly allowed.

## Deployment Boundary

Version 4 should preserve local-first architecture.

The application should continue functioning locally. Future cloud deployment should remain possible, but the reasoning engine should stay deployment-independent.

Live retrieval, if added, should be optional and bounded. The core platform should still work with uploaded documents, pasted text, local repository knowledge, and project evidence.

## Implementation Priorities

Implementation should proceed incrementally:

1. Project Workspace model.
2. Evidence Bundle model.
3. Project Evidence Library.
4. Evidence traceability improvements.
5. Decision evolution and comparison.
6. Optional user-triggered live retrieval.

Each step should reuse existing modules where possible and avoid broad rewrites of the stable pipeline.

## Explicit Non-Goals

Version 4 should not introduce:

- Autonomous agents.
- Autonomous web research.
- Autonomous monitoring.
- Multi-agent orchestration.
- Chat-first workflows.
- Unbounded source crawling.
- New infrastructure without clear product value.
- Claims of prediction, legal advice, investment advice, trading advice, or benchmark superiority.

## Architecture Standard

Every V4 change should improve at least one of:

- Decision Quality
- Evidence Quality
- Trust
- Explainability
- Traceability
- Reviewer Experience
- Maintainability
- Portfolio Quality

If a proposal does not clearly improve one of these dimensions, it should normally be rejected.
