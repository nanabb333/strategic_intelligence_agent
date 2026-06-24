"""Deterministic event-family understanding for product-facing analysis.

This layer keeps historical comparison relevant by identifying the event
family before the brief turns to analogues and outcomes. It is intentionally
rule-based and local.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EventUnderstanding:
    """Product-facing event interpretation used to constrain comparisons."""

    event_type: str
    event_family: str
    rationale: str
    relevant_families: list[str] = field(default_factory=list)
    comparison_guardrail: str = ""


EVENT_RULES = [
    {
        "event_type": "Corporate restructuring / layoff event",
        "event_family": "Corporate Restructuring",
        "keywords": ["layoff", "layoffs", "job cuts", "headcount", "workforce reduction", "restructuring", "cost cuts"],
        "families": ["Corporate Restructuring", "Earnings / Corporate Disclosure", "Corporate Strategic Response"],
        "guardrail": "Compare with restructuring, cost-control, and corporate disclosure cases unless the source text clearly links the layoffs to trade policy or sanctions.",
    },
    {
        "event_type": "Earnings shock or guidance event",
        "event_family": "Earnings Shock",
        "keywords": ["earnings miss", "missed earnings", "guidance", "margin pressure", "revenue decline", "forecast cut", "profit warning"],
        "families": ["Earnings / Corporate Disclosure", "Financial / Earnings Geopolitical Exposure", "Corporate Strategic Response"],
        "guardrail": "Compare with disclosure, demand-visibility, margin-pressure, and management-communication cases.",
    },
    {
        "event_type": "Export control policy event",
        "event_family": "Trade Restriction",
        "keywords": ["export control", "export controls", "entity list", "licensing requirement", "end-use", "end user", "advanced chips", "advanced semiconductor"],
        "families": ["Export Controls", "Trade Policy", "Technology Competition", "Corporate Strategic Response"],
        "guardrail": "Compare with technology-control, licensing, market-access, and supply-chain exposure cases.",
    },
    {
        "event_type": "Sanctions or restricted-counterparty event",
        "event_family": "Economic Coercion",
        "keywords": ["sanction", "sanctions", "ofac", "restricted counterparty", "blocked party", "asset freeze"],
        "families": ["Sanctions", "Financial / Earnings Geopolitical Exposure", "Corporate Strategic Response"],
        "guardrail": "Compare with sanctions, payments, counterparty-screening, and compliance-operation cases.",
    },
    {
        "event_type": "Bank product or customer-risk event",
        "event_family": "Financial Product Risk",
        "keywords": ["high-yield product", "yield product", "structured product", "deposit product", "new bank product", "bank promotion", "wealth product"],
        "families": ["Regulatory Action", "Financial / Earnings Geopolitical Exposure", "Corporate Strategic Response"],
        "guardrail": "Compare with banking supervision, customer-risk, liquidity-disclosure, and product-governance cases.",
    },
    {
        "event_type": "Industrial subsidy or state-support event",
        "event_family": "State Support",
        "keywords": ["subsidy", "subsidies", "tax credit", "industrial policy", "state support", "incentive", "domestic content", "chips act"],
        "families": ["Industrial Policy", "Trade Policy", "Corporate Strategic Response"],
        "guardrail": "Compare with subsidy implementation, eligibility, localization, and capacity-planning cases.",
    },
    {
        "event_type": "Supply chain disruption event",
        "event_family": "Supply Chain Disruption",
        "keywords": ["supply chain", "shipping", "logistics", "red sea", "route disruption", "port", "chokepoint", "supplier disruption"],
        "families": ["Supply Chain Disruption", "Geopolitical Escalation", "Corporate Strategic Response"],
        "guardrail": "Compare with logistics, supplier concentration, chokepoint, and continuity-planning cases.",
    },
]


def detect_event_understanding(text: str, question: str = "") -> EventUnderstanding:
    """Identify the most relevant event family from the input and question."""
    searchable = f"{text} {question}".lower()
    best_rule = None
    best_score = 0
    for rule in EVENT_RULES:
        score = sum(1 for keyword in rule["keywords"] if keyword in searchable)
        if score > best_score:
            best_rule = rule
            best_score = score

    if not best_rule:
        return EventUnderstanding(
            event_type="Strategic event requiring classification",
            event_family="Strategic Event",
            rationale="No narrow event-family rule dominated, so the system keeps comparison broad and evidence-limited.",
            relevant_families=[
                "Export Controls",
                "Sanctions",
                "Industrial Policy",
                "Supply Chain Disruption",
                "Regulatory Action",
                "Earnings / Corporate Disclosure",
                "Corporate Strategic Response",
            ],
            comparison_guardrail="Use broad comparisons only when the input lacks enough detail for a narrower event-family match.",
        )

    matched_keywords = [keyword for keyword in best_rule["keywords"] if keyword in searchable]
    return EventUnderstanding(
        event_type=best_rule["event_type"],
        event_family=best_rule["event_family"],
        rationale=f"Matched event signals: {', '.join(matched_keywords)}.",
        relevant_families=list(best_rule["families"]),
        comparison_guardrail=best_rule["guardrail"],
    )
