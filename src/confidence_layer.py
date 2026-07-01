"""Qualitative confidence and assumption layer."""

from __future__ import annotations

from dataclasses import dataclass, field

from decision_case import DecisionCase
from evidence_ledger import EvidenceLedger


@dataclass
class ConfidenceAssessment:
    """Qualitative confidence record for one decision case."""

    confidence_level: str = "Low"
    key_assumptions: list[str] = field(default_factory=list)
    what_would_change_this_view: list[str] = field(default_factory=list)
    unknown_or_uncertain: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    rationale: str = ""


def assess_confidence(decision_case: DecisionCase, evidence_ledger: EvidenceLedger) -> ConfidenceAssessment:
    """Assess qualitative confidence without statistical claims."""
    evidence_count = len(evidence_ledger.items)
    high_confidence_items = sum(1 for item in evidence_ledger.items if item.confidence == "High")
    low_confidence_items = sum(1 for item in evidence_ledger.items if item.confidence == "Low")
    has_limitations = bool(decision_case.limitations)
    has_analogues = bool(decision_case.historical_analogues)

    if evidence_count >= 5 and high_confidence_items >= 2 and low_confidence_items == 0 and not has_limitations:
        level = "High"
    elif evidence_count >= 3 and has_analogues:
        level = "Moderate"
    else:
        level = "Low"

    if has_limitations and level == "High":
        level = "Moderate"

    unknowns = _unknowns(decision_case, evidence_ledger)
    limitations = decision_case.limitations or ["Evidence limits were not fully specified by the current pipeline."]
    rationale = _rationale(level, evidence_count, has_analogues, has_limitations)

    decision_case.confidence_level = level
    return ConfidenceAssessment(
        confidence_level=level,
        key_assumptions=decision_case.assumptions,
        what_would_change_this_view=decision_case.change_triggers,
        unknown_or_uncertain=unknowns,
        limitations=limitations,
        rationale=rationale,
    )


def render_evidence_confidence_section(
    *,
    evidence_ledger: EvidenceLedger,
    confidence_assessment: ConfidenceAssessment,
) -> str:
    """Render a concise Markdown evidence and confidence section."""
    support = _confidence_supporting_evidence(evidence_ledger)
    reducers = _confidence_reducers(evidence_ledger, confidence_assessment)
    improvers = _confidence_improvers(confidence_assessment)
    lines = [
        "## Evidence and Confidence",
        "",
        "### Confidence Assessment",
        "",
        f"**Overall Level:** {confidence_assessment.confidence_level}",
        "",
        f"**Reasoning:** {confidence_assessment.rationale}",
        "",
        "**Supporting Evidence**",
        "",
        *_bullets(support, "No supporting evidence was generated."),
        "",
        "**Confidence Reducers**",
        "",
        *_bullets(reducers, "No confidence reducers were generated."),
        "",
        "**Confidence Improvers**",
        "",
        *_bullets(improvers, "No confidence improvers were generated."),
        "",
        "### Evidence Ledger",
        "",
    ]
    for item in evidence_ledger.items:
        lines.extend(
            [
                f"- **{item.evidence_id} ({item.source_type})**",
                f"  - Reference: {_reference(item)}",
                f"  - Supporting Source: {_supporting_source(item)}",
                f"  - Evidence Type: {item.source_type}",
                f"  - Source Metadata: {_source_metadata(item)}",
                f"  - Observation: {item.observation}",
                f"  - Inference: {item.inference}",
                f"  - Supports: {item.claim_supported}",
                f"  - Why this evidence matters: {_why_evidence_matters(item)}",
                f"  - Relationship to recommendation: {_relationship_to_recommendation(item)}",
                f"  - Relevance: {item.relevance}; Confidence: {item.confidence}",
            ]
        )
        item_limitation = _item_specific_limitation(item.limitations)
        if item_limitation:
            lines.append(f"  - Item-specific limitation: {item_limitation}")

    lines.extend(["", "### Key Assumptions", ""])
    lines.extend(_bullets(confidence_assessment.key_assumptions, "No key assumptions were generated."))
    lines.extend(["", "### What Would Change This View", ""])
    lines.extend(_bullets(confidence_assessment.what_would_change_this_view, "No change triggers were generated."))
    lines.extend(["", "### What Is Unknown Or Uncertain", ""])
    lines.extend(_bullets(confidence_assessment.unknown_or_uncertain, "No uncertainty notes were generated."))
    lines.extend(["", "### Evidence Limitations", ""])
    lines.extend(
        _bullets(
            _consolidated_limitations(evidence_ledger, confidence_assessment),
            "No evidence limitations were generated.",
        )
    )
    return "\n".join(lines).strip() + "\n"


def _unknowns(decision_case: DecisionCase, evidence_ledger: EvidenceLedger) -> list[str]:
    unknowns = [
        "The current brief does not verify information outside the supplied input and local records.",
        "Organization-specific exposure, timing, and implementation constraints require human review.",
    ]
    if not decision_case.stakeholders or decision_case.stakeholders[0].startswith("Affected decision-makers"):
        unknowns.append("Stakeholders are not fully specified in the extracted material.")
    if any(item.confidence == "Low" for item in evidence_ledger.items):
        unknowns.append("At least one evidence item has low confidence and should be reviewed before use.")
    return unknowns


def _rationale(level: str, evidence_count: int, has_analogues: bool, has_limitations: bool) -> str:
    pieces = [f"{evidence_count} reviewable evidence items were recorded"]
    pieces.append("historical analogues are available" if has_analogues else "historical analogue support is limited")
    if has_limitations:
        pieces.append("limitations remain visible")
    return f"{level} confidence because " + ", ".join(pieces) + "."


def _bullets(items: list[str], fallback: str) -> list[str]:
    return [f"- {item}" for item in items] if items else [f"- {fallback}"]


def _supporting_source(item) -> str:
    if item.source_type == "User-provided readable URL or extracted page text":
        return "User-provided URL or extracted readable page text."
    if item.source_type == "User-provided input material":
        return "User-provided source material."
    if item.source_type.startswith("Local historical"):
        return f"{_clean_sentence(item.evidence_text)} Based on the repository's curated historical knowledge base."
    if item.source_type == "Deterministic mechanism detection":
        return "Repository mechanism framework and source-text cues."
    if item.source_type == "Evidence assessment":
        return "Internal evidence assessment derived from supplied material and deterministic interpretation checks."
    if item.source_type == "Local current-context record":
        return "Repository current-context knowledge base."
    return "Source type not specified."


def _reference(item) -> str:
    for value in (item.limitations, item.evidence_text):
        url = _extract_url(value)
        if url:
            label = _reference_label(item)
            return f"{label}. URL: {url}."
    return "No primary source link available."


def _reference_label(item) -> str:
    text = item.evidence_text.split(":", 1)[0].strip()
    if text and text.lower() not in {"source pending", "historical outcome record retrieved"}:
        return text
    return "Open source"


def _source_metadata(item) -> str:
    if item.source_type.startswith("Local historical") or item.source_type == "Local current-context record":
        return "Publisher: Repository knowledge base; Publication Date: not available; Verification Status: curated local record."
    if item.source_type.startswith("User-provided"):
        return "Publisher: user-provided material; Publication Date: not available; Verification Status: provided input, not independently verified."
    if item.source_type == "Evidence assessment":
        return "Publisher: internal deterministic assessment; Publication Date: analysis run; Verification Status: derived from available evidence."
    if item.source_type == "Deterministic mechanism detection":
        return "Publisher: internal mechanism framework; Publication Date: analysis run; Verification Status: deterministic classification support."
    return "Publisher: not specified; Publication Date: not available; Verification Status: not specified."


def _extract_url(value: str) -> str:
    for token in value.replace(")", " ").replace("(", " ").split():
        clean = token.strip(".,;")
        if clean.startswith(("http://", "https://")) and " " not in clean:
            return clean
    return ""


def _item_specific_limitation(value: str) -> str:
    text = value.strip()
    if not text:
        return ""
    generic_fragments = [
        "no primary supporting source",
        "source pending",
        "historical analogues support comparison",
        "historical similarity supports comparison",
        "mechanism detection is deterministic",
        "current-context records are local references",
        "source detail depends on the supplied material",
    ]
    if any(fragment in text.lower() for fragment in generic_fragments):
        return ""
    return text


def _consolidated_limitations(
    evidence_ledger: EvidenceLedger,
    confidence_assessment: ConfidenceAssessment,
) -> list[str]:
    limitations = [
        "Some evidence is derived from user-provided material rather than independently verified primary sources.",
        "Some historical analogues are based on curated repository knowledge rather than linked source documents.",
        "Analogue transferability depends on whether the current case shares comparable mechanisms and constraints.",
        "Organization-specific exposure, timing, cost, and implementation data may be missing.",
    ]
    limitations.extend(confidence_assessment.limitations)
    limitations.extend(
        item_specific
        for item in evidence_ledger.items
        if (item_specific := _item_specific_limitation(item.limitations))
    )
    return _unique(limitations)


def _confidence_supporting_evidence(evidence_ledger: EvidenceLedger) -> list[str]:
    values: list[str] = []
    if any(item.source_type.startswith("User-provided") for item in evidence_ledger.items):
        values.append("User-provided evidence defines the decision frame.")
    historical_count = sum(1 for item in evidence_ledger.items if item.source_type.startswith("Local historical"))
    if historical_count:
        values.append(f"{historical_count} repository historical records support analogue reasoning.")
    if any(item.source_type == "Evidence assessment" and item.confidence == "High" for item in evidence_ledger.items):
        values.append("Evidence assessment includes high-confidence support for parts of the recommendation.")
    if any(item.source_type == "Deterministic mechanism detection" for item in evidence_ledger.items):
        values.append("Mechanism detection links the issue to operational or strategic pressure points.")
    return values


def _confidence_reducers(
    evidence_ledger: EvidenceLedger,
    confidence_assessment: ConfidenceAssessment,
) -> list[str]:
    reducers: list[str] = []
    if any("No primary source link" in _reference(item) for item in evidence_ledger.items):
        reducers.append("Some evidence records do not include primary source links.")
    if any(item.confidence == "Low" for item in evidence_ledger.items):
        reducers.append("At least one evidence item is low confidence.")
    if confidence_assessment.unknown_or_uncertain:
        reducers.extend(confidence_assessment.unknown_or_uncertain[:2])
    return _unique(reducers)


def _confidence_improvers(confidence_assessment: ConfidenceAssessment) -> list[str]:
    values = [
        trigger
        for trigger in confidence_assessment.what_would_change_this_view
        if trigger and "new primary source" in trigger.lower()
    ]
    values.extend(
        [
            "Organization-specific exposure mapping.",
            "Updated financial, customer, supplier, or compliance evidence.",
            "Clear regulatory, contractual, or operating-owner confirmation.",
        ]
    )
    return _unique(values[:5])


def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        clean = item.strip()
        key = clean.lower()
        if clean and key not in seen:
            seen.add(key)
            result.append(clean)
    return result


def _why_evidence_matters(item) -> str:
    claim = item.claim_supported.rstrip(".")
    return f"It supports {claim.lower()} and clarifies whether the recommendation rests on source material, historical comparison, or remaining uncertainty."


def _relationship_to_recommendation(item) -> str:
    section = item.used_in_section.lower()
    if "decision snapshot" in section or "decision criteria" in section:
        return "It frames the decision and the criteria used to compare options."
    if "historical" in section:
        return "It supports the recommendation by showing a comparable response pattern, while preserving transferability limits."
    if "mechanism" in section:
        return "It explains how the issue could create operational or strategic pressure."
    if "monitor" in section or "context" in section:
        return "It identifies observable signals that could confirm or change today's recommendation."
    if "evidence" in section:
        return "It identifies support, uncertainty, or missing evidence that should constrain confidence."
    return "It provides reviewable support for the decision brief."


def _clean_sentence(value: str) -> str:
    text = value.strip()
    if not text:
        return ""
    return text if text.endswith((".", "!", "?")) else f"{text}."
