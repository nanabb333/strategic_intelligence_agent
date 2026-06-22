"""Deterministic issue extraction for Strategic Intelligence Agent."""

from dataclasses import dataclass, field
import re


COUNTRY_REGION_KEYWORDS = [
    "United States",
    "U.S.",
    "US",
    "China",
    "Taiwan",
    "Russia",
    "Ukraine",
    "European Union",
    "EU",
    "Japan",
    "South Korea",
    "Korea",
    "Netherlands",
    "Middle East",
    "Red Sea",
    "United Kingdom",
    "UK",
]

INDUSTRY_KEYWORDS = [
    "semiconductor",
    "semiconductors",
    "chip",
    "chips",
    "AI",
    "cloud",
    "automotive",
    "shipping",
    "energy",
    "manufacturing",
    "technology",
    "battery",
    "batteries",
    "logistics",
    "retail",
    "software",
]

POLICY_TERMS = [
    "export control",
    "export controls",
    "sanctions",
    "tariff",
    "tariffs",
    "subsidy",
    "subsidies",
    "industrial policy",
    "regulation",
    "regulatory",
    "entity list",
    "license",
    "licensing",
    "compliance",
    "CHIPS Act",
    "Inflation Reduction Act",
    "IRA",
]

ACTOR_KEYWORDS = [
    "government",
    "regulator",
    "executives",
    "suppliers",
    "customers",
    "firms",
    "companies",
    "lawmakers",
    "military",
    "allies",
    "management",
    "board",
]

DOCUMENT_TYPE_KEYWORDS = {
    "Earnings / Corporate Disclosure": ["earnings", "guidance", "quarter", "revenue", "margin", "disclosure"],
    "Policy / Regulatory Text": ["policy", "act", "regulation", "rule", "export control", "sanctions"],
    "Operational Risk Note": ["supply chain", "logistics", "supplier", "shipping", "disruption"],
    "Security / Geopolitical Update": ["military", "security", "strait", "sanctions", "conflict"],
}


@dataclass
class ExtractedIssue:
    """Structured representation of an issue found in a document."""

    title: str
    summary: str
    core_issue: str
    actors: list[str] = field(default_factory=list)
    countries_or_regions: list[str] = field(default_factory=list)
    industries: list[str] = field(default_factory=list)
    policy_terms: list[str] = field(default_factory=list)
    companies: list[str] = field(default_factory=list)
    document_type_guess: str = "General Strategic Note"
    uncertainties: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)


def _find_terms(text: str, terms: list[str]) -> list[str]:
    """Find configured terms with case-insensitive word-boundary matching."""
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


def _extract_companies(text: str) -> list[str]:
    """Extract simple company-like names and known corporate names."""
    known_companies = [
        "Huawei",
        "ASML",
        "TSMC",
        "Samsung",
        "Apple",
        "Microsoft",
        "Nvidia",
        "Intel",
        "Tesla",
        "Toyota",
        "Maersk",
    ]
    companies = _find_terms(text, known_companies)
    pattern = re.compile(
        r"\b([A-Z][A-Za-z0-9&.-]+(?:\s+[A-Z][A-Za-z0-9&.-]+){0,3}\s+"
        r"(?:Inc\.|Corp\.|Corporation|Company|Ltd\.|Limited|LLC|PLC))\b"
    )
    for match in pattern.findall(text):
        candidate = match.strip()
        if candidate not in companies and len(companies) < 8:
            companies.append(candidate)
    return companies


def _guess_document_type(text: str) -> str:
    lowered = text.lower()
    best_type = "General Strategic Note"
    best_count = 0
    for document_type, keywords in DOCUMENT_TYPE_KEYWORDS.items():
        count = sum(1 for keyword in keywords if keyword.lower() in lowered)
        if count > best_count:
            best_type = document_type
            best_count = count
    return best_type


def _extract_uncertainties(text: str) -> list[str]:
    uncertainty_terms = ["uncertain", "uncertainty", "uncertainties", "unknown", "unclear", "monitor"]
    sentences = re.split(r"(?<=[.!?])\s+", text)
    results = [
        sentence.strip()
        for sentence in sentences
        if any(term in sentence.lower() for term in uncertainty_terms)
    ]
    return results[:5]


def extract_issues(document_text: str) -> list[ExtractedIssue]:
    """Extract strategic issue fields from document text without external APIs."""
    text = document_text.strip()
    if not text:
        return []

    lines = text.splitlines()
    first_line = lines[0].strip().lstrip("#").strip()
    title = first_line[:80] or "Untitled issue"
    body = "\n".join(lines[1:]).strip() or text
    summary = body[:500].strip()
    if len(body) > 500:
        summary = f"{summary}..."
    core_issue = re.split(r"(?<=[.!?])\s+", body)[0].strip() or title

    return [
        ExtractedIssue(
            title=title,
            summary=summary,
            core_issue=core_issue,
            actors=_find_terms(text, ACTOR_KEYWORDS),
            countries_or_regions=_find_terms(text, COUNTRY_REGION_KEYWORDS),
            industries=_find_terms(text, INDUSTRY_KEYWORDS),
            policy_terms=_find_terms(text, POLICY_TERMS),
            companies=_extract_companies(text),
            document_type_guess=_guess_document_type(text),
            uncertainties=_extract_uncertainties(text),
            evidence=[summary],
        )
    ]
