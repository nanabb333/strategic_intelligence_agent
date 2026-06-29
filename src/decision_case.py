"""Decision case schema for evidence-aware analysis artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DecisionCase:
    """Reviewable decision case summary for one primary issue."""

    decision_question: str = ""
    source_summary: str = ""
    situation: str = ""
    stakeholders: list[str] = field(default_factory=list)
    decision_criteria: list[str] = field(default_factory=list)
    decision_options: list[str] = field(default_factory=list)
    evidence_items: list[str] = field(default_factory=list)
    historical_analogues: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    recommended_path: str = ""
    confidence_level: str = "Low"
    change_triggers: list[str] = field(default_factory=list)
    monitoring_signals: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)


def build_decision_case(
    *,
    issue: Any | None,
    classification: Any | None,
    analogues: list[Any],
    mechanisms: list[Any],
    strategic_assessment: Any | None,
    evidence_ids: list[str],
    question_text: str,
) -> DecisionCase:
    """Build a lightweight decision case from existing deterministic outputs."""
    if issue is None:
        return DecisionCase(
            decision_question=question_text or "What decision does this material raise?",
            source_summary="No issue summary was generated from the supplied material.",
            situation="No structured situation was extracted.",
            evidence_items=evidence_ids,
            limitations=["The pipeline did not extract a primary issue from the input."],
        )

    scenario = getattr(classification, "primary_scenario", "") if classification else ""
    event_type = getattr(strategic_assessment, "event_type", "") if strategic_assessment else ""
    criteria = _decision_criteria_for_issue(issue, scenario)
    options = [
        "Option A: wait for more complete information before changing posture.",
        "Option B: map exposure, preserve flexibility, and prepare staged response options.",
        "Option C: move immediately to a more defensive posture.",
    ]
    limitations = list(getattr(strategic_assessment, "important_limitations", []) or [])
    if not limitations:
        limitations = ["Available evidence is limited to the supplied material and local deterministic records."]

    return DecisionCase(
        decision_question=question_text or _fallback_question(event_type, scenario),
        source_summary=getattr(issue, "summary", "") or "No source summary generated.",
        situation=getattr(issue, "core_issue", "") or getattr(issue, "title", "Untitled issue"),
        stakeholders=_stakeholders(issue),
        decision_criteria=criteria,
        decision_options=options,
        evidence_items=evidence_ids,
        historical_analogues=[_analogue_label(item) for item in analogues],
        assumptions=_assumptions(issue, scenario, mechanisms),
        risks=_risks(issue, scenario),
        recommended_path="Option B: map exposure, preserve flexibility, and prepare staged response options.",
        confidence_level="Low",
        change_triggers=_change_triggers(scenario),
        monitoring_signals=_monitoring_signals(issue, scenario),
        limitations=limitations,
    )


def _fallback_question(event_type: str, scenario: str) -> str:
    context = event_type or scenario or "this situation"
    return f"What should decision-makers consider in response to {context}?"


def _stakeholders(issue: Any) -> list[str]:
    values: list[str] = []
    for attr in ("actors", "companies", "countries_or_regions", "industries"):
        values.extend(str(item) for item in getattr(issue, attr, []) or [] if item)
    return _unique(values) or ["Affected decision-makers and stakeholders were not specified in detail."]


def _decision_criteria_for_issue(issue: Any, scenario: str) -> list[str]:
    base = ["Evidence quality", "Exposure", "Reversibility", "Execution burden", "Monitoring value"]
    industries = getattr(issue, "industries", []) or []
    if industries:
        base.insert(1, f"Impact on {industries[0]}")
    if scenario:
        base.append(f"Scenario fit: {scenario}")
    return _unique(base)


def _assumptions(issue: Any, scenario: str, mechanisms: list[Any]) -> list[str]:
    assumptions = [
        "The supplied material is sufficient for an initial decision-support brief.",
        "Human review will verify source details before operational use.",
    ]
    if scenario:
        assumptions.append(f"The {scenario} frame is an appropriate starting point for analysis.")
    if mechanisms:
        names = ", ".join(getattr(item, "mechanism_name", "identified mechanism") for item in mechanisms[:3])
        assumptions.append(f"The identified mechanisms remain relevant to the decision context: {names}.")
    if getattr(issue, "industries", None):
        assumptions.append("Sector exposure should be validated against organization-specific data.")
    return assumptions


def _risks(issue: Any, scenario: str) -> list[str]:
    risks = [
        "The source material may omit operational details needed for final action.",
        "Historical similarity may not transfer cleanly to the current context.",
        "New evidence may change the preferred path.",
    ]
    if scenario:
        risks.append(f"The {scenario} classification may be incomplete if the input is brief or ambiguous.")
    if not getattr(issue, "actors", []):
        risks.append("Stakeholder detail is limited in the extracted issue.")
    return risks


def _change_triggers(scenario: str) -> list[str]:
    triggers = [
        "New primary source material changes the factual basis.",
        "Stakeholder responses differ from the assumptions in the brief.",
        "Implementation details create materially different constraints.",
    ]
    if scenario:
        triggers.append(f"Evidence shows the situation no longer fits the {scenario} frame.")
    return triggers


def _monitoring_signals(issue: Any, scenario: str) -> list[str]:
    signals = ["Source updates", "Stakeholder responses", "Implementation details", "Evidence gaps"]
    if scenario:
        signals.append(f"{scenario} indicators")
    industries = getattr(issue, "industries", []) or []
    if industries:
        signals.append(f"{industries[0]} exposure changes")
    return _unique(signals)


def _analogue_label(item: Any) -> str:
    title = getattr(item, "case_title", "") or getattr(item, "case_name", "") or "Historical analogue"
    year = getattr(item, "year", "")
    return f"{title} ({year})" if year else title


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        clean = value.strip()
        if clean and clean not in seen:
            seen.add(clean)
            result.append(clean)
    return result
