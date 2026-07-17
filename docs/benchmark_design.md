# Regression Fixture Design

The V5 synthetic fixture suite checks the existing deterministic pipeline against predetermined engineering contracts.

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
- Results remain separate; no overall score is calculated or presented as research performance.

## Credibility Principle

The suite is designed for regression detection. Because fixture wording and expected labels were created alongside the rules, results cannot establish external validity. Current component results are written to `evaluation/benchmark_results.csv` and summarized in `evaluation/evaluation_summary.md`.
