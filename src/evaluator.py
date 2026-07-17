"""Deterministic benchmark evaluation for Strategic Intelligence Agent."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

from context_retriever import retrieve_current_context
from historical_retriever import retrieve_historical_analogues
from issue_extractor import extract_issues
from mechanism_detector import detect_mechanisms
from multi_lens_analyzer import analyze_lenses
from response_playbook_retriever import retrieve_response_patterns
from scenario_classifier import classify_scenarios


DEFAULT_EXPECTED_LENSES = [
    "Economics",
    "Political Economy",
    "International Relations",
    "Legislative / Regulatory",
    "Business Strategy",
]


@dataclass
class BenchmarkResult:
    """Regression-contract output for one synthetic case."""

    case_id: str
    scenario_expected: str
    scenario_actual: str
    scenario_match_score: float
    mechanisms_expected: list[str]
    mechanisms_actual: list[str]
    mechanism_match_score: float
    lenses_expected: list[str]
    lenses_actual: list[str]
    lens_coverage_score: float
    response_expected: list[str]
    response_actual: list[str]
    response_coverage_score: float
    comments: str


def _split_expected(value: str) -> list[str]:
    """Split semicolon-delimited expected values."""
    return [item.strip() for item in value.split(";") if item.strip()]


def _coverage_score(expected: list[str], actual: list[str]) -> float:
    """Return expected-item coverage as a deterministic score from 0 to 1."""
    if not expected:
        return 1.0
    actual_set = {item.lower() for item in actual}
    matched = sum(1 for item in expected if item.lower() in actual_set)
    return round(matched / len(expected), 3)


def _case_to_document(case: dict[str, str]) -> str:
    """Build a benchmark source document without including expected labels."""
    return (
        f"# {case['title']}\n\n"
        f"Document type: {case['document_type']}.\n\n"
        f"{case['notes']}\n\n"
        "Analyst task: classify the strategic issue, identify mechanisms, "
        "retrieve response patterns, and prepare evidence-aware reasoning."
    )


def evaluate_case(case: dict[str, str]) -> BenchmarkResult:
    """Evaluate one benchmark case against the existing deterministic pipeline."""
    document = _case_to_document(case)
    issues = extract_issues(document)
    classifications = classify_scenarios(issues)
    analogues = retrieve_historical_analogues(issues, classifications)
    contexts = retrieve_current_context(issues, classifications)
    mechanisms = detect_mechanisms(issues, classifications)
    interpretations = analyze_lenses(issues, classifications, mechanisms, analogues, contexts)
    responses = retrieve_response_patterns(analogues, mechanisms)

    issue_title = issues[0].title
    classification = classifications[0]
    actual_mechanisms = [item.mechanism_name for item in mechanisms.get(issue_title, [])]
    actual_lenses = [item.lens for item in interpretations.get(issue_title, [])]
    actual_responses = [item.pattern_name for item in responses.get(issue_title, [])]

    expected_mechanisms = _split_expected(case["expected_mechanisms"])
    expected_lenses = _split_expected(case["expected_lenses"]) or DEFAULT_EXPECTED_LENSES
    expected_responses = _split_expected(case["expected_response_categories"])

    scenario_score = 1.0 if classification.primary_scenario == case["expected_scenario"] else 0.0
    mechanism_score = _coverage_score(expected_mechanisms, actual_mechanisms)
    lens_score = _coverage_score(expected_lenses, actual_lenses)
    response_score = _coverage_score(expected_responses, actual_responses)
    comments = []
    if scenario_score < 1:
        comments.append(f"scenario mismatch: expected {case['expected_scenario']}, got {classification.primary_scenario}")
    missing_mechanisms = [
        item for item in expected_mechanisms if item.lower() not in {value.lower() for value in actual_mechanisms}
    ]
    if missing_mechanisms:
        comments.append(f"missing mechanisms: {', '.join(missing_mechanisms)}")
    if lens_score < 1:
        comments.append("not all expected lenses were generated")
    if response_score < 1:
        comments.append("expected response categories were not fully retrieved")
    if not comments:
        comments.append("all expected benchmark fields covered")

    return BenchmarkResult(
        case_id=case["case_id"],
        scenario_expected=case["expected_scenario"],
        scenario_actual=classification.primary_scenario,
        scenario_match_score=scenario_score,
        mechanisms_expected=expected_mechanisms,
        mechanisms_actual=actual_mechanisms,
        mechanism_match_score=mechanism_score,
        lenses_expected=expected_lenses,
        lenses_actual=actual_lenses,
        lens_coverage_score=lens_score,
        response_expected=expected_responses,
        response_actual=actual_responses,
        response_coverage_score=response_score,
        comments="; ".join(comments),
    )


def load_benchmark_cases(path: str | Path = "evaluation/benchmark_cases.csv") -> list[dict[str, str]]:
    """Load benchmark cases from CSV."""
    with Path(path).open(newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def evaluate_benchmark(
    cases_path: str | Path = "evaluation/benchmark_cases.csv",
    results_path: str | Path = "evaluation/benchmark_results.csv",
    summary_path: str | Path = "evaluation/evaluation_summary.md",
) -> list[BenchmarkResult]:
    """Run the benchmark and write results and summary artifacts."""
    cases = load_benchmark_cases(cases_path)
    results = [evaluate_case(case) for case in cases]
    write_results(results, results_path)
    write_summary(results, cases, summary_path, results_path)
    return results


def write_results(results: list[BenchmarkResult], path: str | Path) -> None:
    """Write benchmark results to CSV."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
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
    ]
    with destination.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "case_id": result.case_id,
                    "scenario_expected": result.scenario_expected,
                    "scenario_actual": result.scenario_actual,
                    "scenario_match_score": result.scenario_match_score,
                    "mechanisms_expected": "; ".join(result.mechanisms_expected),
                    "mechanisms_actual": "; ".join(result.mechanisms_actual),
                    "mechanism_match_score": result.mechanism_match_score,
                    "lenses_expected": "; ".join(result.lenses_expected),
                    "lenses_actual": "; ".join(result.lenses_actual),
                    "lens_coverage_score": result.lens_coverage_score,
                    "response_expected": "; ".join(result.response_expected),
                    "response_actual": "; ".join(result.response_actual),
                    "response_coverage_score": result.response_coverage_score,
                    "comments": result.comments,
                }
            )


def metric_summary(results: list[BenchmarkResult]) -> dict[str, float]:
    """Calculate separate deterministic regression-contract metrics."""
    if not results:
        return {
            "benchmark_case_count": 0.0,
            "mechanism_expected_coverage_rate": 0.0,
            "scenario_contract_match_rate": 0.0,
            "lens_coverage_rate": 0.0,
            "response_retrieval_coverage": 0.0,
        }
    return {
        "benchmark_case_count": float(len(results)),
        "mechanism_expected_coverage_rate": round(mean(item.mechanism_match_score for item in results), 3),
        "scenario_contract_match_rate": round(mean(item.scenario_match_score for item in results), 3),
        "lens_coverage_rate": round(mean(item.lens_coverage_score for item in results), 3),
        "response_retrieval_coverage": round(mean(item.response_coverage_score for item in results), 3),
    }


def write_summary(
    results: list[BenchmarkResult],
    cases: list[dict[str, str]],
    path: str | Path,
    results_path: str | Path,
) -> None:
    """Write a Markdown benchmark report from generated results."""
    metrics = metric_summary(results)
    result_display_path = _display_path(results_path)
    scenario_counts: dict[str, int] = {}
    for case in cases:
        scenario_counts[case["expected_scenario"]] = scenario_counts.get(case["expected_scenario"], 0) + 1

    strengths = [
        "Lens coverage is explicit and easy to verify because the system uses a fixed multi-lens framework.",
        "Scenario contract matching highlights where keyword-based classification changes against fixture expectations.",
        "Expected-mechanism coverage makes rule regressions visible without adding new analytical claims.",
    ]
    limitations = [
        "Regression documents are compact synthetic cases derived from fixture metadata.",
        "Component values measure deterministic contract behavior, not real-world accuracy.",
        "Expected-mechanism coverage measures expected-name presence, not deeper semantic correctness.",
        "Lens coverage is fixed because all five lenses are always generated and expected.",
        "Response coverage is fixed because the current renderer and fixture expect one response pattern.",
    ]

    lines = [
        "# Evaluation Summary",
        "",
        "## Overview",
        "",
        "V5 preserves a deterministic regression and contract validation suite for the rules-based pipeline.",
        "",
        "These synthetic cases test whether known rules and predetermined output contracts remain stable. They are not an independent research dataset and do not measure model accuracy, decision quality, or external validity.",
        "",
        "## Methodology",
        "",
        "- Each benchmark case defines expected scenario, mechanisms, lenses, and response categories.",
        "- The evaluator converts the case title, document type, and notes into a compact source document.",
        "- The existing issue extraction, classification, mechanism detection, lens analysis, and response retrieval modules are executed.",
        "- Scores are deterministic coverage values between 0 and 1.",
        "",
        "## Benchmark Cases",
        "",
        f"- Total cases: {int(metrics['benchmark_case_count'])}",
    ]
    for scenario, count in sorted(scenario_counts.items()):
        lines.append(f"- {scenario}: {count}")

    lines.extend(
        [
            "",
            "## Results",
            "",
            f"- Scenario contract match rate: {metrics['scenario_contract_match_rate']}",
            f"- Expected mechanism coverage rate: {metrics['mechanism_expected_coverage_rate']}",
            f"- Fixed lens contract coverage: {metrics['lens_coverage_rate']}",
            f"- Fixed response contract coverage: {metrics['response_retrieval_coverage']}",
            "- No single overall score is reported because the components have different meanings and two are fixed contract checks.",
            f"- Detailed results: `{result_display_path}`",
            "",
            "## Research Evaluation Gap",
            "",
            "- It does not prove factual correctness of all generated outputs.",
            "- It does not prove legal, financial, or geopolitical accuracy.",
            "- It does not replace human expert review.",
            "- It does not evaluate live web retrieval.",
            "- It does not evaluate LLM reasoning quality.",
            "- The cases are not an independent held-out research dataset.",
            "- External gold annotations and a human reviewer study have not been completed.",
            "",
            "## Strengths",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in strengths)
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in limitations)
    lines.extend(
        [
            "",
            "## Future Improvements",
            "",
            "- Add benchmark cases based on longer primary-source documents.",
            "- Add human review notes for ambiguous classifications.",
            "- Expand response pattern categories while keeping language non-prescriptive.",
            "- Add regression thresholds once the benchmark stabilizes.",
        ]
    )
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _display_path(path: str | Path) -> str:
    """Return a stable repository-relative path when possible."""
    candidate = Path(path)
    try:
        return candidate.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def main() -> None:
    """Run benchmark evaluation from the command line."""
    results = evaluate_benchmark()
    metrics = metric_summary(results)
    print("V5 deterministic regression and contract validation completed.")
    print(f"Regression cases: {int(metrics['benchmark_case_count'])}")
    print(f"Scenario contract match rate: {metrics['scenario_contract_match_rate']}")
    print(f"Expected mechanism coverage rate: {metrics['mechanism_expected_coverage_rate']}")
    print(f"Fixed lens contract coverage: {metrics['lens_coverage_rate']}")
    print(f"Fixed response contract coverage: {metrics['response_retrieval_coverage']}")


if __name__ == "__main__":
    main()
