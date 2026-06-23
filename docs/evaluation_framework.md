# Evaluation Framework

V5 adds a credibility layer for Strategic Intelligence Agent. It measures the existing deterministic workflow without adding analytical features, external APIs, forecasts, probabilities, or advice.

## Why Evaluation Matters

Strategic intelligence tools need reviewable claims. Evaluation helps show:

- Whether scenario classification matches benchmark expectations.
- Whether mechanism detection retrieves expected mechanisms.
- Whether the multi-lens framework covers the intended analytic lenses.
- Whether response playbook retrieval returns expected response categories.
- Where the system has gaps that need review.

## Metrics

### Scenario Accuracy

Scenario Accuracy is the share of benchmark cases where the actual scenario exactly matches the expected scenario.

### Mechanism Accuracy

Mechanism Accuracy is expected mechanism coverage:

```text
matched expected mechanisms / total expected mechanisms
```

This measures expected-name coverage, not deep semantic correctness.

### Lens Coverage Rate

Lens Coverage Rate is expected analytic-lens coverage:

```text
matched expected lenses / total expected lenses
```

The current framework expects Economics, Political Economy, International Relations, Legislative / Regulatory, and Business Strategy.

### Response Retrieval Coverage

Response Retrieval Coverage is expected response-category coverage:

```text
matched expected response categories / total expected response categories
```

### Overall Benchmark Score

Overall Benchmark Score is the average of scenario accuracy, mechanism accuracy, lens coverage, and response retrieval coverage for each case, then averaged across cases.

## Artifacts

- `evaluation/benchmark_cases.csv`
- `evaluation/benchmark_results.csv`
- `evaluation/evaluation_summary.md`
- `src/evaluator.py`
- `scripts/validate_v50.py`

## Current Limitations

- Benchmark cases are compact synthetic cases.
- Mechanism scoring uses exact expected names.
- Response retrieval currently returns a narrow deterministic pattern.
- Metrics support portfolio credibility; they are not claims of real-world accuracy.
