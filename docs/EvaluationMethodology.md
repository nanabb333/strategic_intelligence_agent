# Regression Validation Methodology

This document describes the current deterministic regression and contract validation approach. It does not claim model accuracy, decision quality, or real-world usefulness. Planned research evaluation is defined in [Research Evaluation Plan](research/EvaluationPlan.md).

## Current Evaluation Scope

The repository includes a deterministic benchmark framework with:

- `evaluation/benchmark_cases.csv`
- `evaluation/benchmark_results.csv`
- `evaluation/evaluation_summary.md`
- `src/evaluator.py`
- `scripts/validate_v50.py`

The benchmark cases are compact synthetic / curated cases. They are designed to test consistency, coverage, and regression behavior.

## What Is Measured

The current benchmark measures:

- Scenario classification match.
- Expected mechanism coverage.
- Expected lens coverage.
- Expected response retrieval coverage.
- Separate contract-match and expected-coverage component results. No single overall score is reported.

## What Is Not Measured

The current benchmark does not measure:

- Real-world accuracy.
- Factual correctness of all generated text.
- Legal, financial, geopolitical, or operational correctness.
- Live web retrieval quality.
- LLM reasoning quality.
- Human judgment about pathway usefulness, evidence clarity, and decision support.
- Long-document robustness.

## Reproducibility

To reproduce the current evaluation artifacts, inspect:

```bash
python3 scripts/validate_v50.py
```

For general repository validation, run:

```bash
python3 -m ruff check .
python3 -m compileall app.py src tests
python3 -m pytest
```

## Interpreting Scores

Scores should be read as internal signals:

- High component values mean the current deterministic rules reproduced predetermined synthetic-case contracts.
- Low scores expose mismatch or missing coverage.
- Scores do not prove the app is accurate in the real world.

## Future Evaluation Direction

A stronger evidence-driven evaluation program would add:

- Human-labeled benchmark documents.
- Longer primary-source examples.
- Reviewer disagreement notes.
- Source-grounded factual checks.
- Golden output fixtures for regression.
- Explicit failure-case tracking.

## Related Docs

- [Evaluation Framework](evaluation_framework.md)
- [Evaluation Limitations](evaluation_limitations.md)
- [Golden Output Philosophy](GoldenOutputPhilosophy.md)
- [Future Engineering Recommendations](FutureEngineeringRecommendations.md)
