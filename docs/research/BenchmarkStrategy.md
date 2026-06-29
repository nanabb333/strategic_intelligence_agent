# Benchmark Strategy

This document explains how future benchmarking should be approached for Strategic Intelligence Agent.

Benchmarking should support research validation without overstating what the repository currently proves. The platform currently implements product QA and deterministic product-quality evaluation. It does not currently implement academic benchmarking, model leaderboards, LLM-judge evaluation, or statistical claims.

## Evaluation Categories

### Product QA

Product QA checks whether the product behaves reliably and remains internally coherent.

Examples:

- Unit and API tests pass.
- Markdown and JSON artifacts are generated.
- Required output sections are present.
- V2 fields remain additive and backward-compatible.
- Deterministic Decision Quality Evaluation runs without external services.

The repository currently implements this category.

### Research Validation

Research validation asks whether the system's decision-support outputs are useful, reviewable, appropriately cautious, and meaningfully better structured than weaker baselines.

Examples:

- Human reviewers assess evidence use and analogue relevance.
- Outputs are reviewed against structured rubrics.
- Failure modes are tracked across cases.
- Confidence language is compared with evidence quality.
- Historical decision replay is used carefully as a retrospective exercise.

The repository defines the foundation for this category but does not yet implement it.

### Academic Benchmarking

Academic benchmarking requires formal experimental design. It may include shared datasets, baseline systems, controlled evaluation protocols, inter-reviewer agreement, statistical analysis, and reproducible reports.

The repository does not currently implement academic benchmarking.

## Possible Future Comparisons

### Human Analyst Review

Human analysts could review generated briefs using a structured rubric. The goal would be to identify strengths, weaknesses, ambiguity, and disagreement, not to declare absolute correctness.

### Baseline LLM Comparison

Future work could compare the platform against a generic LLM response to the same input. The comparison should focus on structure, evidence transparency, analogue handling, assumptions, risks, and revisability. It should not become a model leaderboard.

### Historical Decision Replay

Historical decision replay could test whether the framework would have surfaced relevant evidence, options, risks, and change triggers at an earlier point in time. Replay should avoid hindsight bias and should not claim that the system would have predicted actual outcomes.

### Structured Rubric Review

Reviewers could score outputs against dimensions such as direct answer quality, evidence use, analogue relevance, option clarity, risk identification, change-trigger quality, localization quality, and overconfidence control.

## Benchmark Design Principles

- Use transparent rubrics.
- Separate structure quality from factual accuracy.
- Record reviewer disagreement.
- Preserve source boundaries.
- Avoid hidden LLM judges.
- Avoid claims of benchmark superiority unless the protocol supports them.
- Treat scores as review signals, not proof of real-world accuracy.

## Current Repository Position

The current repository implements:

- Product QA through tests, compile checks, linting, and API smoke tests.
- Deterministic product-quality evaluation through `decision_quality_evaluation`.
- Documentation and case studies that make evidence, confidence, and evaluation visible.

It does not implement:

- Human evaluation studies.
- Baseline LLM comparisons.
- Academic benchmark datasets.
- Statistical validation.
- Real-world accuracy claims.

Future benchmarking should begin with small, reviewable protocols before adding automation.
