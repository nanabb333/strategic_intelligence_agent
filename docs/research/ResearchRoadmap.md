# Research Roadmap

This document describes a realistic multi-year research evolution path for Strategic Intelligence Agent.

The roadmap does not add product commitments. It defines how the platform could mature from deterministic product-quality evaluation toward research-aware validation while remaining lightweight, local, and reviewable.

## Current Stage: Product Quality

The repository currently supports product quality through:

- Stable local FastAPI workflow.
- Reviewable Markdown, TXT, JSON, trace, and metadata artifacts.
- Decision Case Schema.
- Evidence Ledger.
- Confidence Assessment.
- Deterministic Decision Quality Evaluation.
- Case studies and documentation.
- Ruff, compile checks, pytest, and CI.

This stage answers whether the product is coherent, testable, maintainable, and reviewable.

It does not claim academic validation or real-world accuracy.

## Near-Term Stage: Research Validation

The next research stage should define small, reviewable validation protocols.

Possible work:

- Human-review rubrics for evidence use and analogue relevance.
- Failure-mode logging across curated cases.
- Reviewer disagreement notes.
- Structured comparison against generic unstructured responses.
- Case-level research memos that explain what the system handled well or poorly.

This stage should remain qualitative and transparent before adding more automation.

## Future Stage: Human Evaluation

A later stage could evaluate the system with human reviewers.

Possible work:

- Analyst review panels.
- Rubric-guided scoring.
- Inter-reviewer disagreement analysis.
- Localization review.
- Retrospective review of decision briefs.

This stage should not claim that the system replaces analysts. It should study whether the platform improves structure, reviewability, and decision conversation quality.

## Future Stage: Decision Intelligence Research Platform

A mature research platform could support reproducible studies of AI-assisted decision support.

Possible capabilities:

- Versioned research case sets.
- Structured annotation guidelines.
- Human-reviewed evidence and analogue labels.
- Failure-mode dashboards or reports.
- Carefully scoped baseline comparisons.
- Published methodology notes.

This stage would require stronger governance and clearer research protocols before any public claims.

## Sequencing Principle

Research maturity should follow this order:

1. Product quality.
2. Research validation design.
3. Human review protocols.
4. Carefully scoped comparative studies.
5. Research platform tooling.

The platform should not skip directly to benchmarks, leaderboards, or claims of superiority.

## Boundaries

The research roadmap should avoid:

- LLM judges without human review.
- Model leaderboards.
- Statistical claims without study design.
- Claims of prediction or real-world decision accuracy.
- Infrastructure expansion before methodology is clear.

Research value should come from better validation, not broader automation.
