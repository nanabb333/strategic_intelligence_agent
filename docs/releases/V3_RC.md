# Version 3 Release Candidate

## Summary

Version 3 Release Candidate marks the repository as a stable AI Decision Intelligence Platform for external review. The release candidate preserves the local deterministic product while adding a research validation documentation layer for future work.

This release does not claim scientific proof, benchmark superiority, real-world accuracy, forecasting ability, investment advice, legal advice, or trading advice.

## Highlights

- Stable local FastAPI decision-support workflow.
- Thin `app.py` with service and pipeline separation.
- Reviewable run artifacts: Markdown, TXT, JSON, trace, metadata, and input text.
- Decision Intelligence Framework and Constitution.
- Evidence Architecture and V2 evidence-aware artifact fields.
- Deterministic Decision Quality Evaluation Harness.
- V2 case studies demonstrating evidence, confidence, and evaluation.
- V3 research documentation for future validation work.

## Major Architectural Milestones

- **Product architecture:** Local decision-support workbench with deterministic modules and downloadable artifacts.
- **Decision architecture:** Seven-layer Decision Intelligence Framework.
- **Governance:** Decision Intelligence Constitution for future change control.
- **Evidence architecture:** Explicit separation of evidence, observation, inference, and recommendation.
- **Artifact architecture:** Additive JSON fields for decision quality and reviewability.
- **Research architecture:** Separate documentation layer for research validation, benchmark strategy, failure modes, and research roadmap.

## V2 Trust Improvements

Version 2 introduced the first evidence-aware decision-quality foundation:

- `decision_case`: structured decision case summary.
- `evidence_ledger`: reviewable evidence items with observations, inferences, supported claims, relevance, confidence, limitations, and section usage.
- `confidence_assessment`: qualitative confidence, assumptions, change triggers, unknowns, limitations, and rationale.
- `decision_quality_evaluation`: deterministic product-quality evaluation across direct answer quality, historical analogue relevance, evidence use, option clarity, risk identification, change trigger quality, localization quality, and overconfidence control.

These fields are additive. They do not remove existing outputs or change the core user flow.

## V3 Research Direction

Version 3 establishes the research validation foundation:

- [Research Agenda](../research/ResearchAgenda.md)
- [Benchmark Strategy](../research/BenchmarkStrategy.md)
- [Failure Modes](../research/FailureModes.md)
- [Research Roadmap](../research/ResearchRoadmap.md)

The research layer separates product QA from future research validation and academic benchmarking. The current repository implements product QA and deterministic product-quality evaluation only.

## Known Limitations

- The app is local and single-user.
- Outputs require human review before executive, operational, legal, financial, or geopolitical use.
- The system does not perform autonomous internet research or live monitoring.
- Historical analogues support comparison, not prediction.
- Confidence labels are qualitative and are not statistical probabilities.
- Deterministic evaluation scores are product-quality review aids, not scientific validation.
- Demo artifacts are fictionalized educational examples and are not claims about real events.
- Source URLs are not fabricated; missing source links remain marked transparently.

## Future Work

- Human-review rubrics for evidence use and analogue relevance.
- Reviewer disagreement tracking.
- Research validation protocols.
- Failure-mode logging across curated cases.
- Localization review for V2 evidence and confidence structures.
- Carefully scoped baseline comparisons after methodology is defined.

Future work should preserve the platform's boundaries: local execution, reviewable artifacts, explicit limitations, and human-controlled judgment.

## Validation

Release-candidate validation should pass:

```bash
python3 -m ruff check .
python3 -m compileall app.py src tests
python3 -m pytest
```
