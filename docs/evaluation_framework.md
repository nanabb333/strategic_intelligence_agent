# Deterministic Regression and Contract Validation Framework

V5 retains an engineering regression layer for the deterministic workflow without adding analytical features, external APIs, forecasts, probabilities, or advice.

The cases are compact synthetic contract fixtures. Component values test rule stability and expected coverage only. They are not model accuracy, research performance, decision quality, or external validity.

## Why Evaluation Matters

Strategic intelligence tools need reviewable claims. Evaluation helps show:

- Whether scenario classification matches benchmark expectations.
- Whether mechanism detection retrieves expected mechanisms.
- Whether the multi-lens framework covers the intended analytic lenses.
- Whether response playbook retrieval returns expected response categories.
- Where the system has gaps that need review.

## Metrics

### Scenario Contract Match Rate

Scenario Contract Match is the share of regression cases where the actual scenario exactly matches the fixture expectation.

### Expected Mechanism Coverage Rate

Expected Mechanism Coverage is calculated as:

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

### No Overall Score

No single overall score is reported. Lens and response coverage are fixed contract checks, while scenario and mechanism values have different meanings; averaging them would obscure those differences.

## Artifacts

- `evaluation/benchmark_cases.csv`
- `evaluation/benchmark_results.csv`
- `evaluation/evaluation_summary.md`
- `src/evaluator.py`
- `scripts/validate_v50.py`

## What the Evaluation Does Not Prove

- It does not prove factual correctness of all generated outputs.
- It does not prove legal, financial, or geopolitical accuracy.
- It does not replace human expert review.
- It does not evaluate live web retrieval.
- It does not evaluate LLM reasoning quality.
- It does not use an independent held-out research dataset, external gold annotations, or a completed human reviewer study.

## Current Limitations

- Benchmark cases are compact synthetic cases.
- Mechanism scoring uses exact expected names.
- Response retrieval currently returns a narrow deterministic pattern.
- Metrics support portfolio credibility; they are not claims of real-world accuracy.
