"""Deterministic decision framework architecture for future pathway work."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


CONFIDENCE_BUCKETS = {"High", "Medium", "Low"}


@dataclass(frozen=True)
class DecisionFramework:
    """Reusable framework definition for one decision type."""

    framework_id: str
    name: str
    description: str
    applicable_decision_types: list[str]
    required_evidence_categories: list[str]
    required_risk_categories: list[str]
    required_constraints: list[str]
    historical_dimensions: list[str]
    pathway_dimensions: list[str]
    reviewer_questions: list[str]


@dataclass(frozen=True)
class DecisionClassification:
    """Deterministic classification output for a decision question."""

    decision_type: str
    applicable_frameworks: list[DecisionFramework]
    confidence_bucket: str
    matched_keywords: list[str] = field(default_factory=list)
    matched_metadata: list[str] = field(default_factory=list)
    rationale: str = ""


@dataclass(frozen=True)
class DecisionPathway:
    """Reviewable pathway structure without ranking, probabilities, or recommendations."""

    pathway_id: str
    title: str
    description: str
    supporting_evidence_refs: list[dict[str, str]] = field(default_factory=list)
    historical_analogue_refs: list[dict[str, str]] = field(default_factory=list)
    risk_categories: list[str] = field(default_factory=list)
    regulatory_constraints: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    decision_triggers: list[str] = field(default_factory=list)
    tradeoffs: list[str] = field(default_factory=list)
    reviewer_notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DecisionComparison:
    """Container for comparing pathways without calculating a preferred path."""

    pathways: list[DecisionPathway] = field(default_factory=list)
    comparison_dimensions: list[str] = field(default_factory=list)
    evidence_matrix: dict[str, Any] = field(default_factory=dict)
    risk_matrix: dict[str, Any] = field(default_factory=dict)
    constraint_matrix: dict[str, Any] = field(default_factory=dict)
    historical_matrix: dict[str, Any] = field(default_factory=dict)
    unknown_matrix: dict[str, Any] = field(default_factory=dict)


FRAMEWORK_DEFINITIONS: tuple[DecisionFramework, ...] = (
    DecisionFramework(
        framework_id="investment_decision",
        name="Investment Decision",
        description="Reviews capital exposure, market conditions, financial risks, and evidence sufficiency.",
        applicable_decision_types=["investment", "portfolio", "asset allocation"],
        required_evidence_categories=["financial_market", "company_ir", "sec_filing", "major_news"],
        required_risk_categories=["market_risk", "financial_risk", "counterparty_risk", "uncertainty_unknowns"],
        required_constraints=["securities_disclosure", "fiduciary_governance"],
        historical_dimensions=["market repricing", "earnings revision", "policy shock"],
        pathway_dimensions=["hold posture", "stage exposure", "reduce exposure", "defer decision"],
        reviewer_questions=[
            "What evidence supports the exposure thesis?",
            "What evidence challenges current assumptions?",
            "Which triggers would change the decision posture?",
        ],
    ),
    DecisionFramework(
        framework_id="corporate_strategy",
        name="Corporate Strategy",
        description="Reviews strategic options, competitive position, execution constraints, and timing.",
        applicable_decision_types=["strategy", "corporate strategy", "competitive positioning"],
        required_evidence_categories=["company_ir", "industry_analysis", "major_news"],
        required_risk_categories=["operational_execution_risk", "financial_risk", "reputational_risk"],
        required_constraints=["fiduciary_governance", "antitrust_competition"],
        historical_dimensions=["corporate strategy shift", "demand shock", "competitive response"],
        pathway_dimensions=["continue current strategy", "pivot strategy", "partner", "delay"],
        reviewer_questions=[
            "Which strategic assumptions are most exposed?",
            "What execution burden would each option create?",
            "What evidence would invalidate the current strategic frame?",
        ],
    ),
    DecisionFramework(
        framework_id="supply_chain",
        name="Supply Chain",
        description="Reviews supplier exposure, logistics disruption, inventory, and continuity options.",
        applicable_decision_types=["supply chain", "procurement", "logistics", "supplier"],
        required_evidence_categories=["industry_analysis", "official_government", "major_news"],
        required_risk_categories=["supply_chain_risk", "operational_execution_risk", "geopolitical_risk"],
        required_constraints=["licensing_approval", "sanctions_export_controls"],
        historical_dimensions=["supply chain reconfiguration", "demand shock", "geopolitical escalation"],
        pathway_dimensions=["dual source", "increase inventory", "reroute", "pause dependent activity"],
        reviewer_questions=[
            "Which suppliers or regions create concentration risk?",
            "What constraints affect substitution timing?",
            "What evidence supports continuity versus disruption?",
        ],
    ),
    DecisionFramework(
        framework_id="regulatory_compliance",
        name="Regulatory / Compliance",
        description="Reviews regulatory exposure, approval requirements, and compliance review needs.",
        applicable_decision_types=["regulatory", "compliance", "approval", "licensing"],
        required_evidence_categories=["regulator", "official_government", "legal_regulatory"],
        required_risk_categories=["regulatory_risk", "legal_compliance_risk", "uncertainty_unknowns"],
        required_constraints=["licensing_approval", "litigation_enforcement", "unknown_regulatory_exposure"],
        historical_dimensions=["regulatory escalation", "policy relief", "delayed resolution"],
        pathway_dimensions=["seek review", "defer action", "adjust controls", "prepare disclosure"],
        reviewer_questions=[
            "Which jurisdiction or authority is implicated?",
            "What evidence indicates approval or enforcement exposure?",
            "What must legal or compliance reviewers verify?",
        ],
    ),
    DecisionFramework(
        framework_id="export_control",
        name="Export Control",
        description="Reviews restricted-party, licensing, jurisdiction, and cross-border transfer exposure.",
        applicable_decision_types=["export control", "sanctions", "restricted party", "entity list"],
        required_evidence_categories=["official_government", "regulator", "legal_regulatory"],
        required_risk_categories=["sanctions_export_control_risk", "regulatory_risk", "geopolitical_risk"],
        required_constraints=["sanctions_export_controls", "licensing_approval"],
        historical_dimensions=["geopolitical escalation", "regulatory escalation", "policy relief"],
        pathway_dimensions=["screen counterparties", "seek license review", "pause transfer", "adjust scope"],
        reviewer_questions=[
            "Which product, party, or geography is implicated?",
            "What source establishes the restriction or licensing issue?",
            "What jurisdiction and applicability checks are required?",
        ],
    ),
    DecisionFramework(
        framework_id="market_entry",
        name="Market Entry",
        description="Reviews geography, demand, policy, competition, and operating constraints for entry decisions.",
        applicable_decision_types=["market entry", "geographic expansion", "new market"],
        required_evidence_categories=["industry_analysis", "official_government", "major_news"],
        required_risk_categories=["market_risk", "policy_risk", "operational_execution_risk", "geopolitical_risk"],
        required_constraints=["licensing_approval", "consumer_protection", "data_privacy"],
        historical_dimensions=["market repricing", "policy relief", "demand shock"],
        pathway_dimensions=["enter now", "pilot entry", "partner locally", "defer entry"],
        reviewer_questions=[
            "What evidence supports market demand?",
            "Which constraints affect entry timing?",
            "What would make a staged entry more defensible?",
        ],
    ),
    DecisionFramework(
        framework_id="strategic_partnership",
        name="Strategic Partnership",
        description="Reviews partner fit, counterparty exposure, competitive constraints, and governance.",
        applicable_decision_types=["partnership", "joint venture", "alliance", "counterparty"],
        required_evidence_categories=["company_ir", "major_news", "legal_regulatory"],
        required_risk_categories=["counterparty_risk", "antitrust_competition_risk", "reputational_risk"],
        required_constraints=["antitrust_competition", "fiduciary_governance", "sanctions_export_controls"],
        historical_dimensions=["corporate strategy shift", "litigation or enforcement path", "geopolitical escalation"],
        pathway_dimensions=["proceed with conditions", "narrow scope", "defer", "decline partnership"],
        reviewer_questions=[
            "What evidence supports partner reliability?",
            "Which constraints could affect deal structure?",
            "What governance safeguards are required?",
        ],
    ),
    DecisionFramework(
        framework_id="capital_allocation",
        name="Capital Allocation",
        description="Reviews allocation tradeoffs, financial resilience, timing, and governance.",
        applicable_decision_types=["capital allocation", "capex", "buyback", "dividend", "budget"],
        required_evidence_categories=["company_ir", "sec_filing", "financial_market"],
        required_risk_categories=["financial_risk", "market_risk", "operational_execution_risk"],
        required_constraints=["fiduciary_governance", "securities_disclosure"],
        historical_dimensions=["earnings revision", "market repricing", "corporate strategy shift"],
        pathway_dimensions=["allocate now", "stage allocation", "preserve liquidity", "defer"],
        reviewer_questions=[
            "Which evidence supports capital priority?",
            "What financial constraints affect timing?",
            "Which assumptions would change allocation posture?",
        ],
    ),
    DecisionFramework(
        framework_id="technology_strategy",
        name="Technology Strategy",
        description="Reviews technology roadmap, security, data, supplier, and adoption constraints.",
        applicable_decision_types=["technology", "platform", "cybersecurity", "data", "ai"],
        required_evidence_categories=["industry_analysis", "company_ir", "legal_regulatory"],
        required_risk_categories=["data_privacy_security_risk", "operational_execution_risk", "supply_chain_risk"],
        required_constraints=["data_privacy", "licensing_approval", "consumer_protection"],
        historical_dimensions=["corporate strategy shift", "supply chain reconfiguration", "regulatory escalation"],
        pathway_dimensions=["adopt", "pilot", "harden controls", "defer rollout"],
        reviewer_questions=[
            "What evidence supports technical readiness?",
            "Which security or data constraints require review?",
            "What operational dependencies affect rollout?",
        ],
    ),
    DecisionFramework(
        framework_id="board_executive_decision",
        name="Board / Executive Decision",
        description="Reviews governance, enterprise risk, stakeholder exposure, and escalation triggers.",
        applicable_decision_types=["board", "executive", "governance", "enterprise risk"],
        required_evidence_categories=["company_ir", "sec_filing", "legal_regulatory", "major_news"],
        required_risk_categories=["reputational_risk", "financial_risk", "legal_compliance_risk", "uncertainty_unknowns"],
        required_constraints=["fiduciary_governance", "securities_disclosure", "litigation_enforcement"],
        historical_dimensions=["delayed resolution", "litigation or enforcement path", "corporate strategy shift"],
        pathway_dimensions=["escalate", "approve with controls", "request more evidence", "defer"],
        reviewer_questions=[
            "What requires executive or board-level judgment?",
            "Which evidence is sufficient for governance review?",
            "What unknowns should be escalated before action?",
        ],
    ),
)


CLASSIFICATION_KEYWORDS: dict[str, list[str]] = {
    "investment_decision": ["invest", "investment", "portfolio", "asset", "market exposure", "buyback"],
    "corporate_strategy": ["strategy", "strategic", "competitive", "positioning", "business model"],
    "supply_chain": ["supply chain", "supplier", "procurement", "logistics", "inventory", "shortage"],
    "regulatory_compliance": ["regulatory", "regulation", "compliance", "approval", "license", "licensing"],
    "export_control": ["export control", "sanctions", "entity list", "restricted party", "export license"],
    "market_entry": ["market entry", "new market", "expand into", "geographic expansion", "launch in"],
    "strategic_partnership": ["partnership", "partner", "joint venture", "alliance", "counterparty"],
    "capital_allocation": ["capital allocation", "capex", "budget", "dividend", "cash", "liquidity"],
    "technology_strategy": ["technology", "platform", "cybersecurity", "data privacy", "ai", "software"],
    "board_executive_decision": ["board", "executive", "governance", "enterprise risk", "fiduciary"],
}


def load_decision_frameworks() -> list[DecisionFramework]:
    """Return the deterministic framework library."""
    return list(FRAMEWORK_DEFINITIONS)


def framework_registry() -> dict[str, DecisionFramework]:
    """Return framework definitions keyed by framework_id."""
    return {framework.framework_id: framework for framework in FRAMEWORK_DEFINITIONS}


def get_decision_framework(framework_id: str) -> DecisionFramework | None:
    """Look up a framework by stable ID."""
    return framework_registry().get(framework_id)


def validate_framework(framework: DecisionFramework) -> list[str]:
    """Return validation warnings for incomplete framework definitions."""
    warnings = []
    required_string_fields = ["framework_id", "name", "description"]
    for field_name in required_string_fields:
        if not getattr(framework, field_name).strip():
            warnings.append(f"{field_name} is required")

    required_list_fields = [
        "applicable_decision_types",
        "required_evidence_categories",
        "required_risk_categories",
        "required_constraints",
        "historical_dimensions",
        "pathway_dimensions",
        "reviewer_questions",
    ]
    for field_name in required_list_fields:
        if not getattr(framework, field_name):
            warnings.append(f"{field_name} must include at least one entry")
    return warnings


def classify_decision_question(
    decision_question: str,
    decision_context: str = "",
    evidence_metadata: list[dict[str, Any]] | None = None,
) -> DecisionClassification:
    """Classify a decision question with deterministic keyword and metadata rules."""
    searchable = _searchable_text(decision_question, decision_context, evidence_metadata or [])
    framework_scores: list[tuple[str, int, list[str], list[str]]] = []

    for framework_id, keywords in CLASSIFICATION_KEYWORDS.items():
        keyword_matches = [keyword for keyword in keywords if keyword in searchable]
        metadata_matches = _metadata_matches(framework_id, evidence_metadata or [])
        score = len(keyword_matches) + len(metadata_matches)
        if score:
            framework_scores.append((framework_id, score, keyword_matches, metadata_matches))

    if not framework_scores:
        fallback = get_decision_framework("board_executive_decision")
        frameworks = [fallback] if fallback else []
        return DecisionClassification(
            decision_type="Unclassified Decision",
            applicable_frameworks=frameworks,
            confidence_bucket="Low",
            matched_keywords=[],
            matched_metadata=[],
            rationale="No strong deterministic rule matched; defaulting to governance review structure.",
        )

    framework_scores.sort(key=lambda item: (-item[1], item[0]))
    top_score = framework_scores[0][1]
    selected_ids = [framework_id for framework_id, score, _, _ in framework_scores if score == top_score or score >= 2]
    registry = framework_registry()
    frameworks = [registry[framework_id] for framework_id in selected_ids if framework_id in registry]
    matched_keywords = _unique([match for framework_id, _, matches, _ in framework_scores if framework_id in selected_ids for match in matches])
    matched_metadata = _unique([match for framework_id, _, _, matches in framework_scores if framework_id in selected_ids for match in matches])
    primary_framework = frameworks[0] if frameworks else registry["board_executive_decision"]

    return DecisionClassification(
        decision_type=primary_framework.name,
        applicable_frameworks=frameworks,
        confidence_bucket=_confidence_bucket(top_score),
        matched_keywords=matched_keywords,
        matched_metadata=matched_metadata,
        rationale="Decision question classified with deterministic keyword and evidence metadata rules only.",
    )


def _searchable_text(decision_question: str, decision_context: str, evidence_metadata: list[dict[str, Any]]) -> str:
    metadata_parts: list[str] = []
    for item in evidence_metadata:
        metadata_parts.extend(
            str(item.get(key, ""))
            for key in ("title", "source_type", "source_name", "source_url", "risk_category", "constraint_category")
        )
        for key in ("risk_categories", "regulatory_constraints", "matched_terms", "triggering_terms"):
            value = item.get(key, [])
            if isinstance(value, list):
                metadata_parts.extend(str(entry) for entry in value)
            elif value:
                metadata_parts.append(str(value))
    return " ".join([decision_question or "", decision_context or "", *metadata_parts]).lower()


def _metadata_matches(framework_id: str, evidence_metadata: list[dict[str, Any]]) -> list[str]:
    framework = get_decision_framework(framework_id)
    if not framework:
        return []
    matches = []
    required_values = {
        *framework.required_evidence_categories,
        *framework.required_risk_categories,
        *framework.required_constraints,
    }
    for item in evidence_metadata:
        values = _metadata_values(item)
        matches.extend(sorted(required_values & values))
    return _unique(matches)


def _metadata_values(item: dict[str, Any]) -> set[str]:
    values: set[str] = set()
    for key in ("source_type", "risk_category", "constraint_category"):
        if item.get(key):
            values.add(str(item[key]).strip().lower().replace(" ", "_"))
    for key in ("risk_categories", "regulatory_constraints", "evidence_categories"):
        value = item.get(key, [])
        if isinstance(value, list):
            values.update(str(entry).strip().lower().replace(" ", "_") for entry in value if entry)
        elif value:
            values.add(str(value).strip().lower().replace(" ", "_"))
    return values


def _confidence_bucket(score: int) -> str:
    if score >= 3:
        return "High"
    if score >= 2:
        return "Medium"
    return "Low"


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        clean = value.strip()
        if clean and clean not in seen:
            seen.add(clean)
            output.append(clean)
    return output
