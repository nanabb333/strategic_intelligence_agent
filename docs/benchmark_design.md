# Benchmark Design

The V5 benchmark evaluates the existing Strategic Intelligence Agent pipeline against a curated set of strategic intelligence cases.

## Case Selection

The benchmark covers 20 cases across:

- Export Controls
- Industrial Policy
- Supply Chain Disruption
- Banking Stress
- Earnings Announcements
- Trade Policy
- Sanctions
- Technology Competition
- Regulatory Change

Cases were selected to exercise the existing deterministic classifier, mechanism detector, multi-lens analyzer, and response playbook retriever.

## Dataset Schema

`evaluation/benchmark_cases.csv` contains:

- `case_id`
- `title`
- `document_type`
- `expected_scenario`
- `expected_mechanisms`
- `expected_lenses`
- `expected_response_categories`
- `difficulty`
- `notes`

The evaluator uses title, document type, and notes as the benchmark document. It does not inject expected labels into the source document.

## Scoring Design

The benchmark uses deterministic scoring:

- Scenario classification is exact match.
- Mechanism detection is expected-item coverage.
- Lens coverage is expected-item coverage.
- Response retrieval coverage is expected-item coverage.
- Overall score is the average of those four measures.

## Credibility Principle

The benchmark is intentionally modest. It is designed to reveal strengths and gaps, not to inflate performance claims. Current results are written to `evaluation/benchmark_results.csv` and summarized in `evaluation/evaluation_summary.md`.
