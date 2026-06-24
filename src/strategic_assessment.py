"""Deterministic strategic assessment layer for V11.

This module turns retrieved historical outcomes into decision-support
summaries: patterns, observed outcome distributions, expectation gaps, and
monitoring priorities. It does not forecast or assign probabilities.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field

from issue_extractor import ExtractedIssue
from outcome_retriever import HistoricalOutcome
from scenario_classifier import ScenarioClassification


@dataclass
class HistoricalPattern:
    """Recurring organizational response across retrieved cases."""

    pattern: str
    frequency_percent: int
    supporting_cases: list[str] = field(default_factory=list)
    interpretation: str = ""


@dataclass
class OutcomeDistributionItem:
    """Observed outcome category frequency across retrieved cases."""

    outcome_type: str
    frequency_percent: int
    case_count: int
    interpretation: str = ""


@dataclass
class ExpectationGap:
    """Simplified expectation-vs-reality comparison for one historical case."""

    event: str
    consensus_expectation: str
    observed_outcome: str
    expectation_gap: str
    strategic_lesson: str


@dataclass
class RoleBasedMonitoring:
    """Monitoring priorities by user role."""

    investor_view: list[str] = field(default_factory=list)
    corporate_strategy_view: list[str] = field(default_factory=list)
    supply_chain_view: list[str] = field(default_factory=list)


@dataclass
class StrategicAssessment:
    """Top-level V11 strategic assessment."""

    direct_answer: str
    historical_patterns: list[HistoricalPattern] = field(default_factory=list)
    outcome_distribution: list[OutcomeDistributionItem] = field(default_factory=list)
    expectation_vs_reality: list[ExpectationGap] = field(default_factory=list)
    strategic_watchlist: list[str] = field(default_factory=list)
    role_based_monitoring: RoleBasedMonitoring = field(default_factory=RoleBasedMonitoring)
    important_limitations: list[str] = field(default_factory=list)


PATTERN_RULES = [
    (
        "Reviewed supplier concentration or diversified supply options",
        ["supplier", "source", "sourcing", "route", "inventory", "qualification", "alternative"],
        "Similar cases often pushed organizations to reduce dependence on a narrow set of suppliers, routes, or inputs.",
    ),
    (
        "Expanded compliance monitoring and documentation",
        ["compliance", "screening", "license", "documentation", "restricted", "legal", "eligibility"],
        "Organizations often added documentation, screening, or approval routines when rules became more restrictive.",
    ),
    (
        "Adjusted capital planning or localization strategy",
        ["site", "domestic", "local", "capacity", "investment", "incentive", "tax credit"],
        "Industrial-policy cases often shifted attention toward eligibility, localization, and sequencing of investment decisions.",
    ),
    (
        "Increased executive communication and guidance monitoring",
        ["guidance", "communication", "uncertainty", "visibility", "customer", "management"],
        "Uncertain events often made management communication and stakeholder updates more important.",
    ),
    (
        "Reviewed continuity plans and operational exposure",
        ["continuity", "exposure", "security", "conflict", "chokepoint", "logistics", "delivery"],
        "Operationally exposed cases often led teams to review contingency plans, routes, and concentration risks.",
    ),
]


EXPECTATION_TEMPLATES = {
    "Export Controls": (
        "Observers often focus first on immediate licensing or shipment disruption.",
        "The larger gap is that operational adaptation, supplier screening, and product planning can become ongoing management work.",
        "Do not stop at the restriction itself; monitor how firms redesign compliance and supply relationships.",
    ),
    "Sanctions": (
        "Observers often expect a narrow restriction on named counterparties.",
        "The practical effect can spread into payments, contracts, screening, and relationship reviews.",
        "Track second-order compliance and counterparty effects, not only the initial sanctions list.",
    ),
    "Industrial Policy": (
        "Observers often expect direct benefits from subsidies or incentives.",
        "Implementation details, eligibility rules, and capacity constraints can shape who can actually use the policy.",
        "Watch implementation guidance and execution requirements before assuming strategic value.",
    ),
    "Supply Chain Disruption": (
        "Observers often focus on near-term delays.",
        "The durable lesson is usually exposure mapping, inventory policy, and alternate supplier qualification.",
        "Separate short-term disruption from longer-term operating model changes.",
    ),
    "Trade Policy": (
        "Observers often expect tariff or customs effects to be the main issue.",
        "The broader effect can include documentation burden, sourcing changes, and cross-border operating complexity.",
        "Monitor implementation details and how firms adjust cross-border workflows.",
    ),
    "Geopolitical Escalation": (
        "Observers often focus on headline political risk.",
        "The practical gap is exposure concentration across routes, suppliers, customers, and operating geography.",
        "Watch continuity planning, insurance, routing, and management commentary.",
    ),
}


def generate_strategic_assessments(
    issues: list[ExtractedIssue],
    classifications: list[ScenarioClassification],
    historical_outcomes: dict[str, list[HistoricalOutcome]],
) -> dict[str, StrategicAssessment]:
    """Generate V11 strategic assessments for each issue."""
    classification_by_issue = {item.issue_title: item for item in classifications}
    results: dict[str, StrategicAssessment] = {}
    for issue in issues:
        classification = classification_by_issue.get(issue.title)
        scenario = classification.primary_scenario if classification else "Other"
        outcomes = historical_outcomes.get(issue.title, [])
        results[issue.title] = StrategicAssessment(
            direct_answer=_direct_answer(issue, scenario, outcomes),
            historical_patterns=_historical_patterns(outcomes),
            outcome_distribution=_outcome_distribution(outcomes),
            expectation_vs_reality=_expectation_gaps(outcomes),
            strategic_watchlist=_strategic_watchlist(scenario, issue),
            role_based_monitoring=_role_based_monitoring(),
            important_limitations=[
                "Historical patterns describe retrieved educational cases; they are not forecasts.",
                "Outcome frequencies are counts within the local curated dataset, not real-world probabilities.",
                "The system does not use live web retrieval or source verification.",
                "Human review is required before operational, legal, financial, or executive use.",
            ],
        )
    return results


def _direct_answer(issue: ExtractedIssue, scenario: str, outcomes: list[HistoricalOutcome]) -> str:
    sector = ", ".join(issue.industries[:2]) or "the affected sector"
    if not outcomes:
        return (
            f"This appears to be a {scenario} issue affecting {sector}. The immediate value is to map exposure, "
            "identify affected stakeholders, and monitor implementation details before drawing conclusions."
        )
    top_patterns = _historical_patterns(outcomes)[:2]
    pattern_text = "; ".join(item.pattern.lower() for item in top_patterns) or "reviewed exposure and monitoring routines"
    return (
        f"This appears to be a {scenario} issue affecting {sector}. Across similar historical cases, organizations most often "
        f"{pattern_text}. The practical next step is to identify exposure, compare similar cases, and monitor concrete implementation signals."
    )


def _historical_patterns(outcomes: list[HistoricalOutcome]) -> list[HistoricalPattern]:
    if not outcomes:
        return []
    pattern_cases: dict[str, list[str]] = defaultdict(list)
    pattern_notes: dict[str, str] = {}
    for outcome in outcomes:
        searchable = f"{outcome.observed_outcome} {outcome.strategic_response} {outcome.sector}".lower()
        for pattern, keywords, interpretation in PATTERN_RULES:
            if any(keyword in searchable for keyword in keywords):
                pattern_cases[pattern].append(f"{outcome.case_name} ({outcome.year})")
                pattern_notes[pattern] = interpretation
    total = len(outcomes)
    patterns = [
        HistoricalPattern(
            pattern=pattern,
            frequency_percent=round(len(cases) / total * 100),
            supporting_cases=cases[:5],
            interpretation=pattern_notes[pattern],
        )
        for pattern, cases in pattern_cases.items()
    ]
    return sorted(patterns, key=lambda item: item.frequency_percent, reverse=True)[:5]


def _outcome_distribution(outcomes: list[HistoricalOutcome]) -> list[OutcomeDistributionItem]:
    if not outcomes:
        return []
    categories = [_classify_outcome(outcome) for outcome in outcomes]
    counts = Counter(categories)
    total = len(outcomes)
    return [
        OutcomeDistributionItem(
            outcome_type=category,
            frequency_percent=round(count / total * 100),
            case_count=count,
            interpretation=_outcome_interpretation(category),
        )
        for category, count in counts.most_common()
    ]


def _classify_outcome(outcome: HistoricalOutcome) -> str:
    text = f"{outcome.observed_outcome} {outcome.strategic_response}".lower()
    if any(token in text for token in ["disrupted", "delayed", "restricted", "shortage", "chokepoint"]):
        return "Partial Disruption"
    if any(token in text for token in ["reviewed", "monitored", "evaluated", "adjusted", "prepared"]):
        return "Adaptation"
    if any(token in text for token in ["severe", "withdraw", "conflict", "crisis"]):
        return "Severe Impact"
    return "Strategic Reassessment"


def _outcome_interpretation(category: str) -> str:
    return {
        "Adaptation": "Cases in this group show organizations adjusting processes, monitoring, or planning rather than stopping operations entirely.",
        "Partial Disruption": "Cases in this group show meaningful constraints, delays, or access limits that required operational response.",
        "Severe Impact": "Cases in this group show broad disruption or sharp uncertainty requiring senior-level attention.",
        "Strategic Reassessment": "Cases in this group show planning reviews or strategic repositioning without a single dominant disruption pattern.",
    }.get(category, "Observed outcome category from retrieved cases.")


def _expectation_gaps(outcomes: list[HistoricalOutcome]) -> list[ExpectationGap]:
    gaps: list[ExpectationGap] = []
    for outcome in outcomes[:5]:
        expectation, gap, lesson = EXPECTATION_TEMPLATES.get(
            outcome.event_family,
            (
                "Observers often focus first on the headline event.",
                "The practical impact can appear in operating routines, stakeholder behavior, and implementation details.",
                "Translate the headline into concrete exposure, process, and monitoring questions.",
            ),
        )
        gaps.append(
            ExpectationGap(
                event=f"{outcome.case_name} ({outcome.year})",
                consensus_expectation=expectation,
                observed_outcome=outcome.observed_outcome,
                expectation_gap=gap,
                strategic_lesson=lesson,
            )
        )
    return gaps


def _strategic_watchlist(scenario: str, issue: ExtractedIssue) -> list[str]:
    watchlist = [
        "Regulatory clarification, implementation dates, exemptions, or licensing guidance.",
        "Management commentary about customer exposure, supplier exposure, or operational constraints.",
        "Supplier diversification announcements, qualification updates, or inventory adjustments.",
        "Capex, localization, or sourcing changes tied to the event.",
        "Evidence that affected organizations are revising contracts, compliance workflows, or customer terms.",
    ]
    if "Earnings" in scenario or issue.document_type_guess.lower().startswith("earnings"):
        watchlist.insert(1, "Revenue exposure, margin commentary, and guidance revisions in future management updates.")
    return watchlist[:6]


def _role_based_monitoring() -> RoleBasedMonitoring:
    return RoleBasedMonitoring(
        investor_view=[
            "Monitor revenue exposure, margin pressure, management guidance, and customer concentration commentary.",
            "Separate operational disruption signals from ordinary quarterly volatility.",
            "Do not treat this output as investment advice or a buy/sell recommendation.",
        ],
        corporate_strategy_view=[
            "Monitor localization requirements, policy implementation details, supplier concentration, and eligibility rules.",
            "Identify which business units need updated exposure maps or decision memos.",
            "Prepare executive discussion notes that separate known facts from unresolved questions.",
        ],
        supply_chain_view=[
            "Monitor inventory coverage, logistics routes, alternative suppliers, and qualification timelines.",
            "Check whether single-source inputs or chokepoints require contingency planning.",
            "Track customer communication needs if delivery timing or input availability changes.",
        ],
    )
