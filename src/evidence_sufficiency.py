"""Deterministic evidence sufficiency tiers for reviewer workflow support."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from decision_assessment import NeutralDecisionAssessment
from evidence_ledger import EvidenceLedger


TIERS = {"Insufficient", "Limited", "Reviewable", "Evidence-rich"}


@dataclass(frozen=True)
class EvidenceSufficiencyAssessment:
    """Explain whether the recorded evidence is sufficient for structured review."""

    tier: str
    rationale: str
    rule_explanation: str
    evidence_item_count: int
    source_based_item_count: int
    low_support_item_count: int
    duplicate_item_count: int = 0
    missing_evidence: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    interpretation_boundary: str = (
        "Structural assessment only. This tier does not validate source quality, source independence beyond "
        "detectable identifiers, claim-level support, analogue relevance, factual validity, or probability of correctness."
    )


def assess_evidence_sufficiency(
    assessment: NeutralDecisionAssessment,
    evidence_ledger: EvidenceLedger,
) -> EvidenceSufficiencyAssessment:
    """Assign an explicit tier from count, source, and limitation rules."""
    items = _deduplicated_items(evidence_ledger.items)
    evidence_count = len(items)
    source_identities = {
        item.source_identity.strip().lower()
        for item in items
        if _counts_as_detectable_source(item)
    }
    source_based = len(source_identities)
    low_support = sum(1 for item in items if item.confidence == "Low")
    has_pathways = bool(assessment.pathways_for_review)

    if evidence_count < 2 or not has_pathways:
        tier = "Insufficient"
        rule = "Fewer than two ledger items are available, or no neutral pathway can be formed."
    elif evidence_count < 4 or source_based < 1:
        tier = "Limited"
        rule = "At least two items exist, but fewer than four items or no source-based item limits review."
    elif low_support == 0 and evidence_count >= 7 and source_based >= 3:
        tier = "Evidence-rich"
        rule = "At least seven unique records, three detectable source identities, and no low-support item are recorded; this remains a structural status only."
    else:
        tier = "Reviewable"
        rule = "At least four items and one source-based item support structured review; limitations may remain."

    missing = list(assessment.unknowns)
    if source_based == 0:
        missing.append("At least one traceable source-based evidence item is required.")
    if low_support:
        missing.append(f"{low_support} low-support evidence item(s) require reviewer verification.")
    if not assessment.pathways_for_review:
        missing.append("Additional evidence is required before multiple pathways can be compared.")

    return EvidenceSufficiencyAssessment(
        tier=tier,
        rationale=(
            f"{tier}: {evidence_count} unique ledger item(s), {source_based} detectable source identity/identities, "
            f"and {low_support} low-support item(s) were recorded."
        ),
        rule_explanation=rule,
        evidence_item_count=evidence_count,
        source_based_item_count=source_based,
        low_support_item_count=low_support,
        duplicate_item_count=max(0, len(evidence_ledger.items) - evidence_count),
        missing_evidence=_unique(missing),
        limitations=_unique(assessment.limitations),
    )


def normalize_stored_evidence_sufficiency(analysis: dict[str, Any]) -> dict[str, Any]:
    """Return current sufficiency data or an explicitly legacy read-only view."""
    current = analysis.get("evidence_sufficiency")
    if isinstance(current, dict) and current:
        return current
    legacy = analysis.get("confidence_assessment")
    if not isinstance(legacy, dict) or not legacy:
        return {}
    legacy_level = str(legacy.get("confidence_level") or "").strip()
    tier = {"Low": "Limited", "Moderate": "Reviewable", "High": "Reviewable"}.get(legacy_level, "Limited")
    return {
        "tier": tier,
        "rationale": "Legacy qualitative confidence was normalized for display only.",
        "rule_explanation": "The original artifact predates the evidence sufficiency contract.",
        "missing_evidence": list(legacy.get("unknown_or_uncertain") or []),
        "limitations": list(legacy.get("limitations") or []),
        "interpretation_boundary": (
            "Structural assessment only. Legacy confidence is not treated as calibrated confidence, source-quality "
            "validation, claim-level support, factual validity, or a probability of correctness."
        ),
        "legacy_compatibility": {"read_only": True, "legacy_confidence_level": legacy_level},
    }


def render_evidence_sufficiency_section(
    assessment: EvidenceSufficiencyAssessment,
    evidence_ledger: EvidenceLedger,
) -> str:
    """Render evidence sufficiency and a compact, inspectable ledger."""
    lines = [
        "## Evidence Sufficiency",
        "",
        f"**Tier:** {assessment.tier} — Structural assessment only",
        "",
        f"**Why this tier:** {assessment.rationale}",
        "",
        f"**Deterministic rule:** {assessment.rule_explanation}",
        "",
        assessment.interpretation_boundary,
        "",
        "### Missing or Unresolved Evidence",
        "",
        *(_bullets(assessment.missing_evidence) or ["- No additional missing-evidence item was generated."]),
        "",
        "### Evidence Ledger",
        "",
    ]
    for item in evidence_ledger.items:
        lines.extend(
            [
                f"- **{item.evidence_id} ({item.source_type})**",
                f"  - Observation: {item.observation}",
                f"  - Inference: {item.inference}",
                f"  - Supports: {item.claim_supported}",
                f"  - Relevance: {item.relevance}; Support level: {item.confidence}",
                f"  - Limitation: {item.limitations}",
            ]
        )
    return "\n".join(lines).strip() + "\n"


def _bullets(values: list[str]) -> list[str]:
    return [f"- {value}" for value in values]


def _unique(values: list[str]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        clean = str(value).strip()
        if clean and clean not in seen:
            seen.add(clean)
            output.append(clean)
    return output


def _deduplicated_items(items: list[Any]) -> list[Any]:
    output: list[Any] = []
    seen: set[str] = set()
    for item in items:
        identity = _evidence_identity(item)
        if identity in seen:
            continue
        seen.add(identity)
        output.append(item)
    return output


def _evidence_identity(item: Any) -> str:
    evidence_id = str(getattr(item, "evidence_id", "") or "").strip().lower()
    if evidence_id:
        return f"evidence:{evidence_id}"
    source_identity = str(getattr(item, "source_identity", "") or "").strip().lower()
    text = str(getattr(item, "evidence_text", "") or "").strip().lower()
    return f"source:{source_identity}|text:{text}"


def _counts_as_detectable_source(item: Any) -> bool:
    identity = str(getattr(item, "source_identity", "") or "").strip().lower()
    status = str(getattr(item, "source_status", "") or "").strip().lower()
    combined = " ".join(
        [
            identity,
            status,
            str(getattr(item, "source_type", "") or "").lower(),
            str(getattr(item, "evidence_text", "") or "").lower(),
            str(getattr(item, "limitations", "") or "").lower(),
        ]
    )
    return bool(
        getattr(item, "externally_sourced", False)
        and identity
        and "source pending" not in combined
        and "unverified analogue" not in combined
        and "local-analogue:" not in identity
    )
