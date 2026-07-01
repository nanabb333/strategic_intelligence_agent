"""Deterministic domain decision evaluation for reviewer workflows."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from decision_support_utils import latest_or_first_project_question, unique_refs
from evidence_intelligence import evidence_reference


@dataclass(frozen=True)
class DomainEvaluationDimension:
    """Evidence-backed evaluation dimension for a decision domain."""

    dimension_id: str
    label: str
    status: str
    evidence_refs: list[dict[str, str]] = field(default_factory=list)
    matched_terms: list[str] = field(default_factory=list)
    reviewer_note: str = ""


@dataclass(frozen=True)
class DomainRiskAssessment:
    """Domain risk exposure summary without scoring or ranking."""

    risk_category: str
    exposure_note: str
    evidence_refs: list[dict[str, str]] = field(default_factory=list)
    limitation_note: str = ""


@dataclass(frozen=True)
class AssetAllocationExposureMap:
    """Macro-sensitive asset allocation exposure map."""

    scenario: str
    exposure_dimensions: list[DomainEvaluationDimension] = field(default_factory=list)
    reviewer_note: str = "Potential asset-class sensitivity requires reviewer validation."


@dataclass(frozen=True)
class CreditRiskEvaluation:
    """Credit risk exposure map without assigning a credit rating."""

    credit_dimensions: list[DomainEvaluationDimension] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    reviewer_note: str = "Credit risk evaluation is evidence-backed and does not assign a credit rating."


@dataclass(frozen=True)
class InsuranceBusinessEvaluation:
    """Insurance business evaluation without investment or legal advice."""

    insurance_dimensions: list[DomainEvaluationDimension] = field(default_factory=list)
    missing_evidence: list[str] = field(default_factory=list)
    reviewer_note: str = "Insurance business evaluation supports reviewer analysis and is not investment or legal advice."


@dataclass(frozen=True)
class DomainEvaluationIssue:
    """Domain evaluation issue requiring reviewer attention."""

    issue_type: str
    domain: str
    explanation: str
    evidence_refs: list[dict[str, str]] = field(default_factory=list)
    reviewer_question: str = ""


@dataclass(frozen=True)
class DomainReviewerQuestion:
    """Domain-specific reviewer question."""

    question: str
    domain: str
    related_dimension: str = ""
    evidence_refs: list[dict[str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class DomainEvaluationFramework:
    """Reusable deterministic domain framework definition."""

    domain: str
    name: str
    description: str
    dimensions: list[str]
    trigger_terms: list[str]


@dataclass(frozen=True)
class DomainEvaluationResult:
    """Complete deterministic evaluation output for one domain."""

    domain: str
    applicable_frameworks: list[dict[str, str]]
    evaluation_dimensions: list[DomainEvaluationDimension]
    evidence_refs: list[dict[str, str]]
    risk_categories: list[str]
    constraints: list[str]
    assumptions: list[str]
    unknowns: list[str]
    reviewer_questions: list[DomainReviewerQuestion]
    limitation_notes: list[str]
    risk_assessments: list[DomainRiskAssessment] = field(default_factory=list)
    asset_allocation_exposure: AssetAllocationExposureMap | None = None
    credit_risk_evaluation: CreditRiskEvaluation | None = None
    insurance_business_evaluation: InsuranceBusinessEvaluation | None = None
    regulatory_suitability_flags: list[DomainEvaluationIssue] = field(default_factory=list)
    issues: list[DomainEvaluationIssue] = field(default_factory=list)


@dataclass(frozen=True)
class DomainEvaluationSet:
    """Serializable domain evaluation set for one decision context."""

    decision_question: str
    results: list[DomainEvaluationResult]
    reviewer_questions: list[DomainReviewerQuestion]
    limitation_notes: list[str] = field(default_factory=list)


INVESTMENT_DIMENSIONS = {
    "interest_rate_sensitivity": ["federal reserve", "fed", "rate hike", "rate cut", "interest rate", "利率", "加息", "降息"],
    "inflation_exposure": ["inflation", "cpi", "price pressure", "通胀", "物价"],
    "duration_risk": ["duration", "long-term bond", "yield curve", "久期", "收益率曲线"],
    "equity_valuation_risk": ["valuation", "equity multiple", "discount rate", "估值", "股票估值"],
    "earnings_sensitivity": ["earnings", "margin", "profit", "盈利", "利润率"],
    "liquidity_risk": ["liquidity", "liquidity tightening", "cash", "流动性"],
    "credit_spread_risk": ["credit spread", "spread widening", "利差"],
    "FX_exposure": ["fx", "foreign exchange", "currency", "美元", "汇率", "外汇"],
    "commodity_exposure": ["commodity", "oil", "gas", "metal", "大宗商品", "石油"],
    "policy_risk": ["policy", "tariff", "regulation", "政策", "关税"],
    "recession_sensitivity": ["recession", "slowdown", "hard landing", "衰退"],
    "market_sentiment": ["sentiment", "risk appetite", "market volatility", "市场情绪"],
    "portfolio_concentration": ["concentration", "overweight", "exposure", "集中度"],
    "downside_protection": ["downside", "hedge", "protection", "drawdown", "下行"],
}
CREDIT_DIMENSIONS = {
    "default_risk": ["default", "违约"],
    "leverage_risk": ["debt", "leverage", "杠杆", "债务"],
    "liquidity_risk": ["liquidity", "流动性"],
    "refinancing_risk": ["refinancing", "maturity wall", "再融资", "到期债务"],
    "interest_coverage": ["interest expense", "interest coverage", "利息支出"],
    "cash_flow_stability": ["cash flow", "free cash flow", "现金流"],
    "covenant_risk": ["covenant", "契约"],
    "counterparty_risk": ["counterparty", "交易对手"],
    "collateral_quality": ["collateral", "抵押"],
    "credit_spread_signal": ["credit spread", "spread", "利差"],
    "rating_action_risk": ["downgrade", "rating", "降级"],
    "sector_credit_pressure": ["sector pressure", "sector credit", "行业信用"],
}
INSURANCE_DIMENSIONS = {
    "underwriting_risk": ["underwriting", "承保"],
    "claims_risk": ["claims", "理赔"],
    "loss_ratio": ["loss ratio", "赔付率"],
    "combined_ratio": ["combined ratio", "综合成本率"],
    "reserve_adequacy": ["reserves", "reserve adequacy", "准备金"],
    "reinsurance_exposure": ["reinsurance", "再保险"],
    "catastrophe_exposure": ["catastrophe", "cat", "巨灾"],
    "premium_growth": ["premiums", "premium growth", "保费"],
    "policy_retention": ["retention", "renewal", "续保"],
    "investment_portfolio_sensitivity": ["investment portfolio", "portfolio yield", "投资组合"],
    "solvency_capital": ["solvency", "capital", "偿付能力"],
    "regulatory_capital_requirement": ["capital requirement", "regulatory capital", "资本要求"],
    "pricing_adequacy": ["pricing adequacy", "rate adequacy", "定价"],
    "fraud_risk": ["fraud", "欺诈"],
    "mortality_morbidity_risk": ["mortality", "morbidity", "死亡率", "发病率"],
}
REGULATORY_OVERLAY = {
    "investment_suitability": ["suitability", "client objective", "适当性"],
    "fiduciary_duty": ["fiduciary", "governance", "受托责任"],
    "securities_disclosure": ["disclosure", "sec", "10-k", "信息披露"],
    "capital_requirement": ["capital requirement", "资本要求"],
    "solvency_requirement": ["solvency", "偿付能力"],
    "insurance_regulation": ["insurance regulation", "regulator", "保险监管"],
    "risk_disclosure": ["risk disclosure", "风险披露"],
    "conflict_of_interest": ["conflict of interest", "利益冲突"],
    "jurisdiction_specific_review": ["jurisdiction", "cross-border", "管辖"],
}


FRAMEWORKS = [
    DomainEvaluationFramework(
        domain="investment_asset_allocation",
        name="Investment / Asset Allocation Evaluation",
        description="Evaluates macro-sensitive exposure dimensions without allocation recommendations.",
        dimensions=list(INVESTMENT_DIMENSIONS),
        trigger_terms=["investment", "asset allocation", "portfolio", "federal reserve", "fed", "inflation", "recession"],
    ),
    DomainEvaluationFramework(
        domain="credit_risk",
        name="Credit Risk Evaluation",
        description="Evaluates evidence-backed credit risk dimensions without assigning ratings.",
        dimensions=list(CREDIT_DIMENSIONS),
        trigger_terms=["credit", "debt", "leverage", "default", "downgrade", "refinancing", "covenant"],
    ),
    DomainEvaluationFramework(
        domain="insurance_business",
        name="Insurance Business Evaluation",
        description="Evaluates insurance operating and capital dimensions without investment or legal advice.",
        dimensions=list(INSURANCE_DIMENSIONS),
        trigger_terms=["insurance", "claims", "premiums", "underwriting", "loss ratio", "combined ratio", "solvency"],
    ),
]


def build_domain_evaluation(
    *,
    decision_question: str,
    decision_context: str = "",
    evidence_items: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return deterministic domain evaluations for a question and evidence set."""
    evidence = list(evidence_items or [])
    searchable = " ".join([decision_question or "", decision_context or "", *[_combined_text(item) for item in evidence]]).lower()
    frameworks = [framework for framework in FRAMEWORKS if _matches_any(searchable, framework.trigger_terms)]
    if not frameworks and evidence:
        frameworks = [FRAMEWORKS[0]]
    results = [_evaluate_framework(framework, evidence, searchable) for framework in frameworks]
    questions = _dedupe_questions([question for result in results for question in result.reviewer_questions])
    evaluation_set = DomainEvaluationSet(
        decision_question=(decision_question or "").strip(),
        results=results,
        reviewer_questions=questions,
        limitation_notes=[
            "Domain evaluation is deterministic and evidence-backed.",
            "No investment advice, credit rating, legal advice, ranking, or transaction recommendation is provided.",
        ],
    )
    return asdict(evaluation_set)


def build_project_domain_evaluation(project: dict[str, Any]) -> dict[str, Any]:
    """Build domain evaluation from a project without mutating project state."""
    question = latest_or_first_project_question(project)
    context = " ".join([str(project.get("name", "")), str(project.get("description", ""))]).strip()
    return build_domain_evaluation(
        decision_question=question.get("question", "") if question else "",
        decision_context=context,
        evidence_items=project.get("evidence_library", []),
    )


def _evaluate_framework(
    framework: DomainEvaluationFramework,
    evidence: list[dict[str, Any]],
    searchable: str,
) -> DomainEvaluationResult:
    term_map = _term_map_for_domain(framework.domain)
    dimensions = [_dimension(dimension, terms, evidence) for dimension, terms in term_map.items()]
    covered = [dimension for dimension in dimensions if dimension.status == "mapped"]
    missing = [dimension.dimension_id for dimension in dimensions if dimension.status == "missing"]
    refs = unique_refs([ref for dimension in covered for ref in dimension.evidence_refs])
    issues = [
        DomainEvaluationIssue(
            issue_type="missing_evidence",
            domain=framework.domain,
            explanation=f"Missing evidence for {dimension.replace('_', ' ')}.",
            reviewer_question=f"Which evidence supports {dimension.replace('_', ' ')}?",
        )
        for dimension in missing[:6]
    ]
    regulatory_flags = _regulatory_flags(evidence, framework.domain)
    questions = _reviewer_questions(framework.domain, dimensions, regulatory_flags)
    risks = [_risk_assessment(framework.domain, dimension) for dimension in covered[:8]]
    result_kwargs: dict[str, Any] = {}
    if framework.domain == "investment_asset_allocation":
        result_kwargs["asset_allocation_exposure"] = AssetAllocationExposureMap(
            scenario=_investment_scenario(searchable),
            exposure_dimensions=covered,
        )
    if framework.domain == "credit_risk":
        result_kwargs["credit_risk_evaluation"] = CreditRiskEvaluation(
            credit_dimensions=dimensions,
            missing_evidence=missing,
        )
    if framework.domain == "insurance_business":
        result_kwargs["insurance_business_evaluation"] = InsuranceBusinessEvaluation(
            insurance_dimensions=dimensions,
            missing_evidence=missing,
        )
    return DomainEvaluationResult(
        domain=framework.domain,
        applicable_frameworks=[_framework_summary(framework)],
        evaluation_dimensions=dimensions,
        evidence_refs=refs,
        risk_categories=[dimension.dimension_id for dimension in covered],
        constraints=[flag.issue_type for flag in regulatory_flags],
        assumptions=_assumptions_for_domain(framework.domain, covered),
        unknowns=[f"Missing evidence for {dimension.replace('_', ' ')}." for dimension in missing[:8]],
        reviewer_questions=questions,
        limitation_notes=_limitation_notes(framework.domain),
        risk_assessments=risks,
        regulatory_suitability_flags=regulatory_flags,
        issues=issues + regulatory_flags,
        **result_kwargs,
    )


def _dimension(dimension_id: str, terms: list[str], evidence: list[dict[str, Any]]) -> DomainEvaluationDimension:
    matched_items = [item for item in evidence if _matched_terms(_combined_text(item), terms)]
    matched_terms = sorted({term for item in matched_items for term in _matched_terms(_combined_text(item), terms)}, key=str.lower)
    refs = [evidence_reference(item) for item in matched_items]
    status = "mapped" if refs else "missing"
    return DomainEvaluationDimension(
        dimension_id=dimension_id,
        label=dimension_id.replace("_", " "),
        status=status,
        evidence_refs=refs,
        matched_terms=matched_terms,
        reviewer_note=(
            f"Evidence suggests this dimension may matter: {dimension_id.replace('_', ' ')}."
            if refs
            else f"Reviewer should evaluate whether {dimension_id.replace('_', ' ')} evidence is needed."
        ),
    )


def _regulatory_flags(evidence: list[dict[str, Any]], domain: str) -> list[DomainEvaluationIssue]:
    flags = []
    for flag, terms in REGULATORY_OVERLAY.items():
        matched_items = [item for item in evidence if _matched_terms(_combined_text(item), terms)]
        if not matched_items:
            continue
        flags.append(
            DomainEvaluationIssue(
                issue_type=flag,
                domain=domain,
                explanation="Potential suitability or disclosure consideration. May require compliance review. Reviewer should verify jurisdiction and applicability.",
                evidence_refs=[evidence_reference(item) for item in matched_items],
                reviewer_question="Which compliance, suitability, or disclosure review is required?",
            )
        )
    return flags


def _risk_assessment(domain: str, dimension: DomainEvaluationDimension) -> DomainRiskAssessment:
    return DomainRiskAssessment(
        risk_category=dimension.dimension_id,
        exposure_note=f"Exposure consideration: {dimension.label}. Reviewer should evaluate evidence coverage.",
        evidence_refs=dimension.evidence_refs,
        limitation_note=f"{domain.replace('_', ' ')} output is a reviewer aid, not a recommendation.",
    )


def _reviewer_questions(
    domain: str,
    dimensions: list[DomainEvaluationDimension],
    regulatory_flags: list[DomainEvaluationIssue],
) -> list[DomainReviewerQuestion]:
    questions = []
    for dimension in dimensions:
        if dimension.status == "mapped":
            question = f"How material is the evidence-backed {dimension.label} exposure consideration?"
        else:
            question = f"What evidence is needed to evaluate {dimension.label}?"
        questions.append(
            DomainReviewerQuestion(
                question=question,
                domain=domain,
                related_dimension=dimension.dimension_id,
                evidence_refs=dimension.evidence_refs,
            )
        )
    for flag in regulatory_flags:
        questions.append(
            DomainReviewerQuestion(
                question=flag.reviewer_question,
                domain=domain,
                related_dimension=flag.issue_type,
                evidence_refs=flag.evidence_refs,
            )
        )
    return _dedupe_questions(questions)[:12]


def _term_map_for_domain(domain: str) -> dict[str, list[str]]:
    if domain == "credit_risk":
        return CREDIT_DIMENSIONS
    if domain == "insurance_business":
        return INSURANCE_DIMENSIONS
    return INVESTMENT_DIMENSIONS


def _investment_scenario(searchable: str) -> str:
    if _matches_any(searchable, ["rate hike", "hikes", "加息"]):
        return "Federal Reserve rate hikes"
    if _matches_any(searchable, ["rate cut", "cuts", "降息"]):
        return "Federal Reserve rate cuts"
    if _matches_any(searchable, ["inflation shock", "通胀"]):
        return "inflation shock"
    if _matches_any(searchable, ["recession", "衰退"]):
        return "recession risk"
    if _matches_any(searchable, ["liquidity tightening", "流动性"]):
        return "liquidity tightening"
    if _matches_any(searchable, ["policy uncertainty", "政策"]):
        return "policy uncertainty"
    return "macro-sensitive investment review"


def _assumptions_for_domain(domain: str, dimensions: list[DomainEvaluationDimension]) -> list[str]:
    if domain == "credit_risk":
        return ["Reviewer validates external credit evidence before using the exposure map."]
    if domain == "insurance_business":
        return ["Reviewer validates reported insurance metrics and regulatory capital context."]
    return ["Reviewer validates asset-class sensitivity and portfolio context before using the exposure map."]


def _limitation_notes(domain: str) -> list[str]:
    common = [
        "This output is deterministic and evidence-backed.",
        "No rankings, transaction instructions, market probabilities, or personalized financial advice are provided.",
    ]
    if domain == "credit_risk":
        return common + ["Credit risk evaluation is not a credit rating."]
    if domain == "insurance_business":
        return common + ["Insurance business evaluation is not investment or legal advice."]
    return common + ["Investment / asset allocation evaluation is not investment advice."]


def _framework_summary(framework: DomainEvaluationFramework) -> dict[str, str]:
    return {"domain": framework.domain, "name": framework.name, "description": framework.description}


def _combined_text(item: dict[str, Any]) -> str:
    return " ".join(str(item.get(key, "")) for key in ("title", "summary", "excerpt", "text_excerpt", "source_type", "source_name"))


def _matches_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def _matched_terms(text: str, terms: list[str]) -> list[str]:
    lowered = text.lower()
    return [term for term in terms if term.lower() in lowered]


def _dedupe_questions(questions: list[DomainReviewerQuestion]) -> list[DomainReviewerQuestion]:
    output = []
    seen = set()
    for question in questions:
        if question.question not in seen:
            seen.add(question.question)
            output.append(question)
    return output
