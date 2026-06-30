# Evaluation Summary

## Overview

V5 adds a deterministic benchmark framework for measuring credibility of the existing Strategic Intelligence Agent pipeline. It does not add new analytical features, forecasting, LLM APIs, or investment advice.

These benchmark scores measure internal deterministic benchmark performance only. The cases are compact synthetic / curated test cases intended to test consistency, coverage, and regression behavior. They do not represent real-world accuracy.

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

- Scenario Accuracy: 88%
- Mechanism Accuracy: 72%
- Lens Coverage Rate: 100%
- Response Retrieval Coverage: 100%
- Overall Benchmark Score: 90%
- Detailed results: `evaluation/benchmark_results.csv`

## What the Evaluation Does Not Prove

- It does not prove factual correctness of all generated outputs.
- It does not prove legal, financial, or geopolitical accuracy.
- It does not replace human expert review.
- It does not evaluate live web retrieval.
- It does not evaluate LLM reasoning quality.

## Strengths

- Lens coverage is explicit and easy to verify because the system uses a fixed multi-lens framework.
- Scenario scoring highlights where keyword-based classification is aligned or misaligned with benchmark expectations.
- Mechanism scoring makes retrieval gaps visible without adding new analytical claims.

## Limitations

- Benchmark documents are compact synthetic cases derived from the benchmark metadata.
- Scores measure internal deterministic benchmark performance, not real-world accuracy.
- Mechanism scoring measures expected-name coverage, not deeper semantic correctness.
- Response playbook retrieval currently exposes a narrow deterministic response pattern.
- Metrics are evaluation aids, not claims of real-world accuracy.

## Future Improvements

- Add benchmark cases based on longer primary-source documents.
- Add human review notes for ambiguous classifications.
- Expand response pattern categories while keeping language non-prescriptive.
- Add regression thresholds once the benchmark stabilizes.
