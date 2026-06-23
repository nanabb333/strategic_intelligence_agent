"""Deterministic current-event context extraction."""

from __future__ import annotations

from dataclasses import dataclass, field
import re


EVENT_TYPE_KEYWORDS = {
    "Export Controls": ["export control", "export controls", "entity list", "license", "licensing", "restricted end user"],
    "Sanctions": ["sanctions", "sanctioned", "asset freeze", "restricted party", "embargo"],
    "Industrial Policy": ["industrial policy", "subsidy", "subsidies", "tax credit", "domestic production", "incentive"],
    "Regulatory Action": ["regulator", "regulatory", "regulation", "rule", "enforcement", "compliance"],
    "Geopolitical Escalation": ["geopolitical", "escalation", "security", "conflict", "military", "regional tension"],
    "Supply Chain Disruption": ["supply chain", "shipping", "logistics", "disruption", "rerouting", "shortage"],
    "Corporate Strategic Shift": ["strategic shift", "restructuring", "partnership", "joint venture", "facility", "capex"],
    "Technology Competition": ["technology competition", "AI chips", "advanced chip", "platform", "digital", "semiconductor"],
    "Legislative Action": ["lawmakers", "legislation", "bill", "act", "parliament", "congress"],
    "Trade Restriction": ["tariff", "trade restriction", "import", "customs", "export ban"],
    "Financial / Earnings Risk": ["earnings", "margin", "revenue", "provision", "credit", "exposure"],
    "Market Access Restriction": ["market access", "restricted access", "customer exposure", "access to", "foreign market"],
}

SECTOR_KEYWORDS = {
    "Semiconductors": ["semiconductor", "chip", "chips", "AI chips", "fabrication", "advanced-node"],
    "Banking / Financial Services": ["bank", "banking", "financial institution", "credit", "lending", "earnings"],
    "Supply Chain / Logistics": ["supply chain", "shipping", "logistics", "port", "freight", "rerouting"],
    "Energy": ["energy", "oil", "gas", "electricity", "grid", "renewable"],
    "Clean Technology": ["battery", "batteries", "clean-tech", "clean technology", "solar"],
    "Digital Platforms": ["digital platform", "platform", "data governance", "app store", "online marketplace"],
    "Manufacturing": ["manufacturing", "factory", "production", "facility", "supplier"],
    "Technology": ["technology", "software", "cloud", "AI", "data"],
}

REGION_KEYWORDS = [
    "United States",
    "U.S.",
    "US",
    "China",
    "Taiwan",
    "European Union",
    "EU",
    "Japan",
    "South Korea",
    "Middle East",
    "Red Sea",
    "Russia",
    "Ukraine",
    "Southeast Asia",
    "Europe",
]

ACTOR_PATTERNS = {
    "Government regulators": ["government", "regulator", "agency", "ministry", "officials"],
    "Lawmakers": ["lawmakers", "congress", "parliament", "legislators"],
    "Corporate executives": ["executives", "management", "board", "chief executive"],
    "Suppliers": ["suppliers", "vendors", "equipment suppliers"],
    "Customers": ["customers", "end users", "buyers"],
    "Financial institutions": ["bank", "financial institution", "lender"],
    "Digital platforms": ["platform", "digital platform", "marketplace"],
}

POLICY_DOMAIN_KEYWORDS = {
    "Technology and national security": ["export control", "AI chips", "semiconductor", "technology competition"],
    "Industrial strategy": ["industrial policy", "subsidy", "domestic production", "incentive"],
    "Trade and market access": ["tariff", "trade", "market access", "import", "export ban"],
    "Financial stability and compliance": ["earnings", "bank", "sanctions compliance", "credit", "exposure"],
    "Competition and data governance": ["digital platform", "data governance", "competition", "market access"],
    "Geopolitical operating risk": ["geopolitical", "shipping", "security", "regional tension", "escalation"],
}


@dataclass
class EventContext:
    """Structured current-event context extracted from source text."""

    event_type: str
    primary_actor: str
    secondary_actor: str
    affected_sectors: list[str] = field(default_factory=list)
    affected_regions: list[str] = field(default_factory=list)
    policy_domain: str = "General strategic context"
    strategic_significance: str = ""
    event_summary: str = ""
    confidence: str = "Low"
    context_limitations: list[str] = field(default_factory=list)


def extract_event_context(document_text: str) -> EventContext:
    """Extract transparent current-event context without external calls."""
    text = document_text.strip()
    lowered = text.lower()
    event_type, event_matches = _best_match(lowered, EVENT_TYPE_KEYWORDS, "General Strategic Event")
    sectors = _find_categories(lowered, SECTOR_KEYWORDS) or ["General business operations"]
    regions = _find_terms(text, REGION_KEYWORDS) or ["Region not specified"]
    actors = _find_categories(lowered, ACTOR_PATTERNS)
    primary_actor = actors[0] if actors else "Primary actor not specified"
    secondary_actor = actors[1] if len(actors) > 1 else "Secondary actor not specified"
    policy_domain, domain_matches = _best_match(lowered, POLICY_DOMAIN_KEYWORDS, "General strategic context")
    confidence = _confidence_label(len(event_matches), sectors, regions, actors)
    summary = _first_sentences(text, limit=2)
    significance = _strategic_significance(event_type, sectors, policy_domain)
    limitations = [
        "Current-event context is extracted from the submitted document only.",
        "No live web retrieval, external news API, or source verification is performed.",
        "Actor, sector, and region labels use deterministic keyword rules and may miss nuance.",
    ]
    if not event_matches:
        limitations.append("No strong event-type keyword pattern was detected.")
    if not domain_matches:
        limitations.append("Policy-domain classification is based on limited source cues.")

    return EventContext(
        event_type=event_type,
        primary_actor=primary_actor,
        secondary_actor=secondary_actor,
        affected_sectors=sectors,
        affected_regions=regions,
        policy_domain=policy_domain,
        strategic_significance=significance,
        event_summary=summary,
        confidence=confidence,
        context_limitations=limitations,
    )


def _best_match(lowered_text: str, mapping: dict[str, list[str]], default: str) -> tuple[str, list[str]]:
    best_label = default
    best_matches: list[str] = []
    for label, keywords in mapping.items():
        matches = [keyword for keyword in keywords if keyword.lower() in lowered_text]
        if len(matches) > len(best_matches):
            best_label = label
            best_matches = matches
    return best_label, best_matches


def _find_categories(lowered_text: str, mapping: dict[str, list[str]]) -> list[str]:
    results: list[str] = []
    for label, keywords in mapping.items():
        if any(keyword.lower() in lowered_text for keyword in keywords):
            results.append(label)
    return results


def _find_terms(text: str, terms: list[str]) -> list[str]:
    found: list[str] = []
    for term in terms:
        escaped = re.escape(term)
        if term[0].isalnum():
            escaped = r"\b" + escaped
        if term[-1].isalnum():
            escaped = escaped + r"\b"
        if re.search(escaped, text, flags=re.IGNORECASE) and term not in found:
            found.append(term)
    return found


def _first_sentences(text: str, limit: int) -> str:
    sentences = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", text) if sentence.strip()]
    return " ".join(sentences[:limit])[:700] or "No event summary available."


def _confidence_label(match_count: int, sectors: list[str], regions: list[str], actors: list[str]) -> str:
    score = match_count
    if sectors and sectors != ["General business operations"]:
        score += 1
    if regions and regions != ["Region not specified"]:
        score += 1
    if actors:
        score += 1
    if score >= 5:
        return "High"
    if score >= 2:
        return "Medium"
    return "Low"


def _strategic_significance(event_type: str, sectors: list[str], policy_domain: str) -> str:
    sector_text = ", ".join(sectors[:3])
    return (
        f"This {event_type.lower()} context matters because it may affect {sector_text} through "
        f"{policy_domain.lower()} considerations. The layer frames what kind of event the input describes "
        "before the system retrieves analogues, outcomes, and lessons."
    )
