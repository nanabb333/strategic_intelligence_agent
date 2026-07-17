"""Validate Strategic Intelligence Agent V5 evaluation framework."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from evaluator import evaluate_benchmark, metric_summary  # noqa: E402


REQUIRED_CASE_COLUMNS = {
    "case_id",
    "title",
    "document_type",
    "expected_scenario",
    "expected_mechanisms",
    "expected_lenses",
    "expected_response_categories",
    "difficulty",
    "notes",
}

REQUIRED_RESULT_COLUMNS = {
    "case_id",
    "scenario_expected",
    "scenario_actual",
    "scenario_match_score",
    "mechanisms_expected",
    "mechanisms_actual",
    "mechanism_match_score",
    "lenses_expected",
    "lenses_actual",
    "lens_coverage_score",
    "response_expected",
    "response_actual",
    "response_coverage_score",
    "comments",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def validate_dataset() -> None:
    cases_path = ROOT / "evaluation/benchmark_cases.csv"
    if not cases_path.exists():
        raise AssertionError("benchmark_cases.csv is missing.")
    rows = read_csv(cases_path)
    if len(rows) < 20:
        raise AssertionError("Expected at least 20 benchmark cases.")
    if set(rows[0]) != REQUIRED_CASE_COLUMNS:
        raise AssertionError("Benchmark case columns do not match V5 schema.")

    expected_scenarios = {row["expected_scenario"] for row in rows}
    required_scenarios = {
        "Export Controls",
        "Industrial Policy",
        "Supply Chain Disruption",
        "Earnings / Corporate Disclosure",
        "Trade Policy",
        "Sanctions",
        "Regulatory Action",
    }
    missing = required_scenarios - expected_scenarios
    if missing:
        raise AssertionError(f"Benchmark dataset missing scenario coverage: {sorted(missing)}")


def validate_results_and_summary() -> None:
    results = evaluate_benchmark(
        ROOT / "evaluation/benchmark_cases.csv",
        ROOT / "evaluation/benchmark_results.csv",
        ROOT / "evaluation/evaluation_summary.md",
    )
    metrics = metric_summary(results)
    if int(metrics["benchmark_case_count"]) < 20:
        raise AssertionError("Metrics did not include all benchmark cases.")

    results_path = ROOT / "evaluation/benchmark_results.csv"
    result_rows = read_csv(results_path)
    if set(result_rows[0]) != REQUIRED_RESULT_COLUMNS:
        raise AssertionError("Benchmark result columns do not match V5 schema.")

    metric_names = [
        "mechanism_expected_coverage_rate",
        "scenario_contract_match_rate",
        "lens_coverage_rate",
        "response_retrieval_coverage",
    ]
    for metric_name in metric_names:
        metric_value = metrics[metric_name]
        if not 0 <= metric_value <= 1:
            raise AssertionError(f"Metric out of range: {metric_name}={metric_value}")

    summary = (ROOT / "evaluation/evaluation_summary.md").read_text(encoding="utf-8")
    for heading in ["## Overview", "## Methodology", "## Benchmark Cases", "## Results", "## Strengths", "## Limitations", "## Future Improvements"]:
        if heading not in summary:
            raise AssertionError(f"Evaluation summary missing {heading}")


def validate_dashboard_and_docs() -> None:
    dashboard = (ROOT / "dashboard/index.html").read_text(encoding="utf-8")
    if "evaluation-tab" not in dashboard or "Deterministic regression and contract snapshot" not in dashboard:
        raise AssertionError("Dashboard regression validation tab is missing.")
    for path in [
        "docs/evaluation_framework.md",
        "docs/benchmark_design.md",
        "evaluation/evaluation_summary.md",
    ]:
        if not (ROOT / path).exists():
            raise AssertionError(f"Missing V5 document: {path}")


def main() -> None:
    validate_dataset()
    validate_results_and_summary()
    validate_dashboard_and_docs()
    print("V5.0 validation passed.")


if __name__ == "__main__":
    main()
