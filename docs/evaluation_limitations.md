# Evaluation Limitations

The V5 benchmark improves portfolio credibility by making performance measurable, but it should be read conservatively.

## Why Benchmark Scores May Be High

- The benchmark cases are compact synthetic / curated test cases.
- Expected labels are aligned to the system's deterministic categories.
- Lens coverage is high because the system intentionally uses a fixed five-lens framework.
- Response retrieval coverage is high because the current response playbook has a narrow deterministic category.
- The benchmark measures consistency and coverage, not broad real-world correctness.

## Where Deterministic Rules Fail

- Ambiguous text can match the wrong scenario because keyword counts dominate context.
- Mixed documents can contain earnings, policy, sanctions, and supply chain signals at the same time.
- Vague articles with few entities may still trigger generic mechanisms.
- Non-English inputs are not fully supported by the English keyword rules.
- Exact-name mechanism scoring can miss partial or semantically related matches.

## What the Evaluation Does Not Prove

- It does not prove factual correctness of all generated outputs.
- It does not prove legal, financial, or geopolitical accuracy.
- It does not replace human expert review.
- It does not evaluate live web retrieval.
- It does not evaluate LLM reasoning quality.

## Future Human-Labeled Evaluation

A stronger evaluation would use independent human-labeled documents with reviewer notes for scenario, mechanism, evidence support, and acceptable uncertainty. Human review should include disagreement tracking for ambiguous cases.

## Future Source-Grounded Factual Evaluation

A future source-grounded benchmark should compare generated claims against primary-source excerpts, source dates, URLs, and explicitly marked evidence spans. That would test factual grounding rather than only category coverage.
