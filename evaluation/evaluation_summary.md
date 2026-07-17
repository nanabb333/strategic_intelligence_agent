# Evaluation Summary

## Overview

V5 preserves a deterministic regression and contract validation suite for the rules-based pipeline.

These synthetic cases test whether known rules and predetermined output contracts remain stable. They are not an independent research dataset and do not measure model accuracy, decision quality, or external validity.

## Methodology

- Each benchmark case defines expected scenario, mechanisms, lenses, and response categories.
- The evaluator converts the case title, document type, and notes into a compact source document.
- The existing issue extraction, classification, mechanism detection, lens analysis, and response retrieval modules are executed.
- Scores are deterministic coverage values between 0 and 1.

## Benchmark Cases

- Total cases: 25
- Earnings / Corporate Disclosure: 4
- Export Controls: 3
- Industrial Policy: 2
- Military / Security Shock: 1
- Other: 2
- Regulatory Action: 3
- Sanctions: 2
- Strategic Investment: 1
- Supply Chain Disruption: 4
- Trade Policy: 3

## Results

- Scenario contract match rate: 0.88
- Expected mechanism coverage rate: 0.72
- Fixed lens contract coverage: 1.0
- Fixed response contract coverage: 1.0
- No single overall score is reported because the components have different meanings and two are fixed contract checks.
- Detailed results: `evaluation/benchmark_results.csv`

## Research Evaluation Gap

- It does not prove factual correctness of all generated outputs.
- It does not prove legal, financial, or geopolitical accuracy.
- It does not replace human expert review.
- It does not evaluate live web retrieval.
- It does not evaluate LLM reasoning quality.
- The cases are not an independent held-out research dataset.
- External gold annotations and a human reviewer study have not been completed.

## Strengths

- Lens coverage is explicit and easy to verify because the system uses a fixed multi-lens framework.
- Scenario contract matching highlights where keyword-based classification changes against fixture expectations.
- Expected-mechanism coverage makes rule regressions visible without adding new analytical claims.

## Limitations

- Regression documents are compact synthetic cases derived from fixture metadata.
- Component values measure deterministic contract behavior, not real-world accuracy.
- Expected-mechanism coverage measures expected-name presence, not deeper semantic correctness.
- Lens coverage is fixed because all five lenses are always generated and expected.
- Response coverage is fixed because the current renderer and fixture expect one response pattern.

## Future Improvements

- Add benchmark cases based on longer primary-source documents.
- Add human review notes for ambiguous classifications.
- Expand response pattern categories while keeping language non-prescriptive.
- Add regression thresholds once the benchmark stabilizes.
