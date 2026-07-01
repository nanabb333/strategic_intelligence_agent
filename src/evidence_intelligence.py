"""Deterministic evidence-set intelligence for reviewer workflows."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from hashlib import sha1
from itertools import combinations
import re
from typing import Any
from urllib.parse import urlparse


CONFLICT_MARKERS = {
    "denied",
    "disputed",
    "contradicts",
    "contradict",
    "reversed",
    "no final decision",
    "not confirmed",
    "rumor",
    "unverified",
}
OPPOSING_MARKERS = [
    ("sanctions lifted", "sanctions imposed"),
    ("approved", "blocked"),
    ("approval", "blocked"),
    ("permitted", "prohibited"),
    ("confirmed", "not confirmed"),
]
LOW_CREDIBILITY_TIERS = {"Tier 5 Other", "Unknown"}
STALE_DAYS = 365
CURRENT_DAYS = 180
COVERAGE_CATEGORIES = [
    "official_government",
    "regulator",
    "company_ir",
    "sec_filing",
    "major_news",
    "industry_analysis",
    "academic",
    "legal_regulatory",
    "financial_market",
    "unknown",
]
STOPWORDS = {
    "about",
    "after",
    "again",
    "also",
    "and",
    "are",
    "because",
    "been",
    "before",
    "being",
    "between",
    "from",
    "has",
    "have",
    "into",
    "not",
    "that",
    "the",
    "their",
    "this",
    "with",
    "would",
}
RISK_CATEGORY_TERMS = {
    "market_risk": ["market", "volatility", "repricing", "demand shock", "价格波动", "市场风险", "需求冲击"],
    "financial_risk": ["earnings", "revenue", "margin", "debt", "liquidity", "cash flow", "财务风险", "收入", "利润率", "流动性"],
    "policy_risk": ["policy", "tariff", "subsidy", "central bank", "fiscal", "monetary", "政策风险", "关税", "补贴"],
    "regulatory_risk": ["regulator", "regulatory", "approval", "license", "licensing", "监管风险", "监管", "审批", "许可"],
    "legal_compliance_risk": ["legal", "compliance", "court", "lawsuit", "settlement", "法律风险", "合规", "诉讼"],
    "sanctions_export_control_risk": ["sanctions", "export control", "export controls", "restricted entity", "entity list", "制裁", "出口管制", "实体清单"],
    "antitrust_competition_risk": ["antitrust", "competition", "monopoly", "merger review", "反垄断", "竞争", "垄断"],
    "disclosure_reporting_risk": ["disclosure", "10-k", "10-q", "sec filing", "reporting", "披露", "报告", "信息披露"],
    "supply_chain_risk": ["supply chain", "supplier", "logistics", "inventory", "生产中断", "供应链", "供应商", "库存"],
    "operational_execution_risk": ["execution", "operational", "delay", "implementation", "capacity", "运营风险", "执行", "延迟"],
    "geopolitical_risk": ["geopolitical", "taiwan", "china", "war", "conflict", "diplomatic", "地缘政治", "冲突", "外交"],
    "reputational_risk": ["reputation", "brand", "public backlash", "consumer trust", "声誉风险", "品牌", "公众反应"],
    "data_privacy_security_risk": ["data privacy", "cybersecurity", "breach", "personal data", "数据隐私", "网络安全", "数据泄露"],
    "counterparty_risk": ["counterparty", "customer concentration", "vendor", "default", "交易对手", "客户集中", "违约"],
    "uncertainty_unknowns": ["uncertain", "unknown", "unverified", "not confirmed", "uncertainty", "不确定", "未知", "未确认"],
}
REGULATORY_CONSTRAINT_TERMS = {
    "securities_disclosure": ["sec", "10-k", "10-q", "disclosure", "material information", "securities", "证券披露", "信息披露"],
    "sanctions_export_controls": ["sanctions", "export control", "entity list", "restricted party", "license", "制裁", "出口管制", "实体清单"],
    "antitrust_competition": ["antitrust", "competition authority", "monopoly", "merger review", "反垄断", "竞争监管"],
    "data_privacy": ["data privacy", "personal data", "gdpr", "cybersecurity", "数据隐私", "个人信息", "网络安全"],
    "licensing_approval": ["license", "licensing", "approval", "permit", "authorization", "许可", "审批", "授权"],
    "litigation_enforcement": ["litigation", "lawsuit", "court", "enforcement", "settlement", "诉讼", "执法", "和解"],
    "fiduciary_governance": ["fiduciary", "board", "governance", "proxy", "shareholder", "受托责任", "治理", "董事会"],
    "labor_employment": ["labor", "employment", "union", "worker", "workforce", "劳动", "就业", "工会"],
    "environmental_regulation": ["environmental", "emissions", "climate", "pollution", "环境监管", "排放", "污染"],
    "consumer_protection": ["consumer protection", "consumer", "pricing practice", "product safety", "消费者保护", "产品安全"],
    "unknown_regulatory_exposure": ["regulatory uncertainty", "unclear jurisdiction", "unknown exposure", "监管不确定", "管辖不明"],
}
HISTORICAL_PATHWAY_TERMS = {
    "base_case_continuity": ["continued", "unchanged", "stable", "maintained", "持续", "稳定", "维持"],
    "market_repricing": ["repricing", "selloff", "rally", "volatility", "valuation", "重新定价", "波动", "估值"],
    "regulatory_escalation": ["investigation", "enforcement", "new rule", "stricter", "监管升级", "调查", "执法"],
    "policy_relief": ["relief", "waiver", "exemption", "eased", "政策缓和", "豁免", "放松"],
    "supply_chain_reconfiguration": ["reshoring", "supplier shift", "supply chain", "inventory build", "供应链重组", "转移供应商"],
    "corporate_strategy_shift": ["strategy", "restructuring", "divest", "acquisition", "战略调整", "重组", "收购"],
    "litigation_or_enforcement_path": ["lawsuit", "court", "settlement", "enforcement", "litigation", "诉讼", "执法"],
    "geopolitical_escalation": ["escalation", "sanctions imposed", "diplomatic", "military", "地缘升级", "制裁升级"],
    "demand_shock": ["demand shock", "order decline", "consumer demand", "需求冲击", "订单下降"],
    "earnings_revision": ["earnings revision", "guidance", "forecast", "profit warning", "盈利修正", "业绩指引"],
    "delayed_resolution": ["delayed", "postponed", "no final decision", "pending", "延迟", "推迟", "待定"],
}
PATHWAY_RISK_LINKS = {
    "market_repricing": ["market_risk", "financial_risk"],
    "regulatory_escalation": ["regulatory_risk", "legal_compliance_risk"],
    "policy_relief": ["policy_risk", "regulatory_risk"],
    "supply_chain_reconfiguration": ["supply_chain_risk", "operational_execution_risk"],
    "corporate_strategy_shift": ["operational_execution_risk", "financial_risk"],
    "litigation_or_enforcement_path": ["legal_compliance_risk", "regulatory_risk"],
    "geopolitical_escalation": ["geopolitical_risk", "sanctions_export_control_risk"],
    "demand_shock": ["market_risk", "financial_risk"],
    "earnings_revision": ["financial_risk", "disclosure_reporting_risk"],
    "delayed_resolution": ["uncertainty_unknowns", "operational_execution_risk"],
}


def build_evidence_intelligence(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Return deterministic reviewer intelligence for an evidence set."""
    evidence = [_normalize_record(item) for item in items]
    duplicates = detect_duplicate_groups(evidence)
    relationships = analyze_evidence_relationships(evidence)
    freshness = analyze_freshness(evidence)
    coverage = analyze_coverage(evidence)
    attention = reviewer_attention_queue(evidence, duplicates, relationships, freshness)
    novelty = analyze_novelty(evidence)
    risk_signals = classify_decision_risk_evidence(evidence)
    regulatory_flags = flag_regulatory_constraints(evidence)
    pathway_signals = generate_historical_pathway_signals(evidence, risk_signals)
    return {
        "summary": summarize_evidence_set(evidence, attention),
        "duplicate_groups": duplicates,
        "relationships": relationships,
        "novelty": novelty,
        "coverage": coverage,
        "freshness": freshness,
        "attention_items": attention,
        "traceable_signals": build_traceable_signals(evidence, duplicates, relationships, novelty, attention),
        "decision_risk_evidence_map": risk_signals,
        "regulatory_constraint_flags": regulatory_flags,
        "historical_pathway_signals": pathway_signals,
    }


def summarize_evidence_set(items: list[dict[str, Any]], attention_items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Summarize source, credibility, freshness, validation, and review state."""
    freshness = analyze_freshness(items)
    return {
        "total_evidence_count": len(items),
        "source_type_counts": dict(Counter(_value(item, "source_type", "Unknown") for item in items)),
        "credibility_tier_counts": dict(Counter(_value(item, "credibility_tier", "Unknown") for item in items)),
        "freshness_summary": {
            "current_count": len(freshness["current_items"]),
            "stale_count": len(freshness["stale_items"]),
            "missing_date_count": len(freshness["missing_date_items"]),
            "freshness_risk": freshness["freshness_risk"],
        },
        "validation_status_counts": dict(Counter(_value(item, "validation_status", "Unknown") for item in items)),
        "reviewer_status_counts": dict(Counter(_reviewer_status(item) for item in items)),
        "attention_items": attention_items or [],
    }


def detect_duplicate_groups(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Detect deterministic duplicate and near-duplicate evidence groups."""
    groups: list[dict[str, Any]] = []
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in items:
        for key in _duplicate_keys(item):
            grouped.setdefault(key, []).append(item)

    used_ids: set[str] = set()
    for key, group_items in grouped.items():
        ids = [_evidence_id(item) for item in group_items]
        unique_ids = list(dict.fromkeys(ids))
        if len(unique_ids) < 2 or set(unique_ids) <= used_ids:
            continue
        used_ids.update(unique_ids)
        groups.append(
            {
                "duplicate_reason": key[0],
                "primary_evidence_id": unique_ids[0],
                "duplicate_evidence_ids": unique_ids[1:],
                "primary_evidence_ref": evidence_reference(group_items[0]),
                "duplicate_evidence_refs": [evidence_reference(item) for item in group_items[1:]],
                "evidence_refs": [evidence_reference(item) for item in group_items],
            }
        )

    for left, right in combinations(items, 2):
        left_id = _evidence_id(left)
        right_id = _evidence_id(right)
        if left_id in used_ids and right_id in used_ids:
            continue
        similarity = _token_overlap(_text_for_similarity(left), _text_for_similarity(right))
        if similarity >= 0.82:
            used_ids.update({left_id, right_id})
            groups.append(
                {
                    "duplicate_reason": f"similar excerpt overlap {similarity:.2f}",
                    "primary_evidence_id": left_id,
                    "duplicate_evidence_ids": [right_id],
                    "primary_evidence_ref": evidence_reference(left),
                    "duplicate_evidence_refs": [evidence_reference(right)],
                    "evidence_refs": [evidence_reference(left), evidence_reference(right)],
                }
            )
    return groups


def analyze_evidence_relationships(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return conservative support/conflict/insufficient relationship labels."""
    relationships = []
    for left, right in combinations(items, 2):
        label, rationale = _relationship_label(left, right)
        relationships.append(
            {
                "evidence_ids": [_evidence_id(left), _evidence_id(right)],
                "evidence_refs": [evidence_reference(left), evidence_reference(right)],
                "relationship": label,
                "rationale": rationale,
            }
        )
    return relationships


def analyze_novelty(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Score whether each item adds new source, date, category, keywords, geography, or actor signals."""
    seen_sources: set[str] = set()
    seen_dates: set[str] = set()
    seen_source_types: set[str] = set()
    seen_keywords: set[str] = set()
    seen_geographies: set[str] = set()
    seen_actors: set[str] = set()
    output = []
    for item in items:
        reasons = []
        source = _source_key(item)
        date = _date_key(item)
        source_type = source_category(item)
        keywords = _claim_keywords(item)
        geographies = _geography_mentions(item)
        actors = _actor_mentions(item)

        if source and source not in seen_sources:
            reasons.append("new source")
        if date and date not in seen_dates:
            reasons.append("new date")
        if source_type and source_type not in seen_source_types:
            reasons.append("new source type")
        if keywords - seen_keywords:
            reasons.append("new claim keywords")
        if geographies - seen_geographies:
            reasons.append("new geography")
        if actors - seen_actors:
            reasons.append("new company / regulator / actor mention")

        score = round(min(1.0, len(reasons) / 6), 3)
        output.append(
            {
                "evidence_id": _evidence_id(item),
                "evidence_ref": evidence_reference(item),
                "novelty_score": score,
                "novelty_reasons": reasons or ["No substantial novelty detected."],
            }
        )
        seen_sources.add(source)
        seen_dates.add(date)
        seen_source_types.add(source_type)
        seen_keywords.update(keywords)
        seen_geographies.update(geographies)
        seen_actors.update(actors)
    return output


def analyze_coverage(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize deterministic source-category coverage without searching for gaps."""
    covered = sorted({source_category(item) for item in items if source_category(item) != "unknown"})
    missing = [category for category in COVERAGE_CATEGORIES if category != "unknown" and category not in covered]
    score = round(len(covered) / (len(COVERAGE_CATEGORIES) - 1), 3)
    if score >= 0.5:
        recommendation = "Coverage is broad enough for reviewer comparison; verify source quality and conflicts."
    elif covered:
        recommendation = "Coverage is partial; reviewer should note missing source categories before relying on the evidence set."
    else:
        recommendation = "Coverage is weak; reviewer should treat the evidence set as incomplete."
    return {
        "covered_categories": covered or ["unknown"],
        "missing_categories": missing,
        "coverage_score": score,
        "reviewer_recommendation": recommendation,
    }


def analyze_freshness(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Classify evidence as current, stale, or missing date using published/retrieved dates."""
    stale = []
    current = []
    missing = []
    for item in items:
        evidence_id = _evidence_id(item)
        age = _age_days(item)
        if age is None:
            missing.append(evidence_id)
        elif age > STALE_DAYS:
            stale.append(evidence_id)
        elif age <= CURRENT_DAYS:
            current.append(evidence_id)
    total = max(len(items), 1)
    if len(stale) / total >= 0.4:
        risk = "High"
    elif stale or len(missing) / total >= 0.4:
        risk = "Moderate"
    else:
        risk = "Low"
    return {
        "stale_items": stale,
        "current_items": current,
        "missing_date_items": missing,
        "stale_evidence_refs": [evidence_reference(item) for item in items if _evidence_id(item) in stale],
        "current_evidence_refs": [evidence_reference(item) for item in items if _evidence_id(item) in current],
        "missing_date_evidence_refs": [evidence_reference(item) for item in items if _evidence_id(item) in missing],
        "freshness_risk": risk,
    }


def reviewer_attention_queue(
    items: list[dict[str, Any]],
    duplicate_groups: list[dict[str, Any]] | None = None,
    relationships: list[dict[str, Any]] | None = None,
    freshness: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return deterministic evidence items needing reviewer attention."""
    duplicate_ids = {
        evidence_id
        for group in duplicate_groups or []
        for evidence_id in group.get("duplicate_evidence_ids", [])
    }
    conflict_ids = {
        evidence_id
        for relationship in relationships or []
        if relationship.get("relationship") == "potential_conflict"
        for evidence_id in relationship.get("evidence_ids", [])
    }
    stale_ids = set((freshness or analyze_freshness(items)).get("stale_items", []))
    attention = []
    for item in items:
        evidence_id = _evidence_id(item)
        reasons = []
        if evidence_id in duplicate_ids:
            reasons.append("duplicate")
        if not _value(item, "source_name") and not _value(item, "source_url"):
            reasons.append("missing source")
        if not _value(item, "published_at"):
            reasons.append("missing date")
        if _value(item, "validation_status") in {"Weak Metadata", "Needs Review"}:
            reasons.append("weak metadata")
        if "unsupported" in " ".join(_list_value(item, "validation_notes")).lower():
            reasons.append("unsupported source type")
        if evidence_id in conflict_ids or _value(item, "conflict_status") not in {"", "No Conflict"}:
            reasons.append("potential conflict")
        if evidence_id in stale_ids:
            reasons.append("stale evidence")
        if _value(item, "credibility_tier", "Unknown") in LOW_CREDIBILITY_TIERS:
            reasons.append("low credibility")
        if not (_value(item, "excerpt") or _value(item, "text_excerpt")):
            reasons.append("empty excerpt")
        if reasons:
            attention.append({"evidence_id": evidence_id, "evidence_ref": evidence_reference(item), "reasons": sorted(set(reasons))})
    return attention


def build_traceable_signals(
    items: list[dict[str, Any]],
    duplicate_groups: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
    novelty: list[dict[str, Any]],
    attention: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Create compact traceable evidence signals for reviewer dashboards."""
    signals: list[dict[str, Any]] = []
    for group in duplicate_groups:
        signals.append(
            {
                "signal_type": "possible_duplicate",
                "label": "Possible duplicate",
                "evidence_refs": group.get("evidence_refs", []),
                "reviewer_note": group.get("duplicate_reason", "Duplicate review recommended."),
            }
        )
    for relationship in relationships:
        if relationship.get("relationship") not in {"potential_conflict", "supports"}:
            continue
        signals.append(
            {
                "signal_type": relationship.get("relationship"),
                "label": "Potential conflict" if relationship.get("relationship") == "potential_conflict" else "May support",
                "evidence_refs": relationship.get("evidence_refs", []),
                "reviewer_note": relationship.get("rationale", "Reviewer should inspect related evidence."),
            }
        )
    novelty_by_id = {entry.get("evidence_id"): entry for entry in novelty}
    attention_ids = {entry.get("evidence_id") for entry in attention}
    for item in items:
        evidence_id = _evidence_id(item)
        novelty_entry = novelty_by_id.get(evidence_id, {})
        if evidence_id in attention_ids or float(novelty_entry.get("novelty_score", 0) or 0) > 0:
            signals.append(
                {
                    "signal_type": "review_attention",
                    "label": "Review recommended",
                    "evidence_refs": [evidence_reference(item)],
                    "reviewer_note": ", ".join(novelty_entry.get("novelty_reasons", [])) or "Reviewer attention recommended.",
                }
            )
    return signals


def classify_decision_risk_evidence(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Classify deterministic risk exposure signals from evidence text."""
    signals = []
    for category, terms in RISK_CATEGORY_TERMS.items():
        matched_items = _items_matching_terms(items, terms)
        if not matched_items:
            continue
        matched_terms = sorted({term for item in matched_items for term in _matched_terms(item, terms)}, key=str.lower)
        signals.append(
            {
                "risk_category": category,
                "evidence_refs": [evidence_reference(item) for item in matched_items],
                "matched_terms": matched_terms,
                "reviewer_explanation": _risk_explanation(category, matched_terms),
                "confidence_bucket": _confidence_bucket(matched_items, matched_terms),
                "limitation_note": _limitation_note(matched_items, matched_terms),
            }
        )
    return signals


def flag_regulatory_constraints(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Surface cautious regulatory or legal review flags without legal conclusions."""
    flags = []
    for category, terms in REGULATORY_CONSTRAINT_TERMS.items():
        matched_items = _items_matching_terms(items, terms)
        if not matched_items:
            continue
        triggering_terms = sorted({term for item in matched_items for term in _matched_terms(item, terms)}, key=str.lower)
        flags.append(
            {
                "constraint_category": category,
                "evidence_refs": [evidence_reference(item) for item in matched_items],
                "triggering_terms": triggering_terms,
                "reviewer_note": (
                    "May require legal / compliance review. Reviewer should verify jurisdiction and applicability. "
                    "Not legal advice."
                ),
                "limitation_note": _limitation_note(matched_items, triggering_terms),
            }
        )
    return flags


def generate_historical_pathway_signals(
    items: list[dict[str, Any]], risk_signals: list[dict[str, Any]] | None = None
) -> list[dict[str, Any]]:
    """Identify deterministic historical pathway families without probabilities."""
    risk_categories = {signal.get("risk_category") for signal in risk_signals or []}
    signals = []
    for pathway, terms in HISTORICAL_PATHWAY_TERMS.items():
        matched_items = _items_matching_terms(items, terms)
        if not matched_items:
            continue
        triggering_terms = sorted({term for item in matched_items for term in _matched_terms(item, terms)}, key=str.lower)
        linked_risks = [risk for risk in PATHWAY_RISK_LINKS.get(pathway, []) if risk in risk_categories]
        signals.append(
            {
                "pathway_family": pathway,
                "evidence_refs": [evidence_reference(item) for item in matched_items],
                "triggering_terms": triggering_terms,
                "related_risk_categories": linked_risks,
                "reviewer_explanation": f"Evidence terms may resemble the {pathway.replace('_', ' ')} pathway.",
                "historical_analogue_hint": _historical_analogue_hint(pathway),
                "limitation_note": "No probability is assigned; reviewer should compare facts, timing, and source quality.",
            }
        )
    return signals


def evidence_reference(item: dict[str, Any]) -> dict[str, str]:
    """Return a deterministic, reviewer-friendly evidence reference."""
    url = _value(item, "source_url") or _value(item, "canonical_url") or _nested_metadata_value(item, "canonical_url")
    source = _value(item, "source_name") or _domain(url) or _value(item, "source_type") or "Unknown source"
    date = (_value(item, "published_at") or _value(item, "retrieved_at") or _value(item, "created_at"))[:10]
    return {
        "evidence_id": _evidence_id(item),
        "title": _value(item, "title") or "Untitled evidence",
        "source": source,
        "source_url": url,
        "date": date,
    }


def source_category(item: dict[str, Any]) -> str:
    """Map evidence metadata into deterministic coverage categories."""
    value = " ".join(
        [
            _value(item, "source_type"),
            _value(item, "source_name"),
            _value(item, "source_url"),
            _value(item, "title"),
        ]
    ).lower()
    if "sec.gov" in value or "10-k" in value or "10-q" in value or "sec filing" in value:
        return "sec_filing"
    if "investor relations" in value or "press release" in value or "company" in value:
        return "company_ir"
    if ".gov" in value or "government" in value or "official" in value:
        return "official_government"
    if "regulator" in value or "court" in value or "central bank" in value:
        return "regulator"
    if any(marker in value for marker in ["reuters", "associated press", "bloomberg", "wsj", "financial times", "major news"]):
        return "major_news"
    if "industry" in value or "analysis" in value:
        return "industry_analysis"
    if any(marker in value for marker in ["academic", "journal", "university", "nber", "oecd", "world bank", "imf"]):
        return "academic"
    if "legal" in value or "law" in value or "regulatory" in value:
        return "legal_regulatory"
    if "market" in value or "financial" in value or "earnings" in value:
        return "financial_market"
    return "unknown"


def _relationship_label(left: dict[str, Any], right: dict[str, Any]) -> tuple[str, str]:
    left_text = _combined_text(left)
    right_text = _combined_text(right)
    if _has_conflict_signal(left_text, right_text):
        return "potential_conflict", "Conflict markers or opposing claims appear across the evidence pair."
    overlap = _token_overlap(left_text, right_text)
    same_category = source_category(left) == source_category(right) and source_category(left) != "unknown"
    close_dates = _date_proximity_days(left, right)
    if overlap >= 0.35 and (same_category or close_dates is not None and close_dates <= 30):
        return "supports", "Evidence pair has overlapping topic terms and compatible source category or date proximity."
    return "insufficient_information", "Evidence pair does not have enough deterministic overlap to infer support or conflict."


def _has_conflict_signal(left_text: str, right_text: str) -> bool:
    combined = f"{left_text} {right_text}".lower()
    if any(marker in combined for marker in CONFLICT_MARKERS):
        return True
    return any(first in combined and second in combined for first, second in OPPOSING_MARKERS)


def _duplicate_keys(item: dict[str, Any]) -> list[tuple[str, str]]:
    keys = []
    source_url = _normalized_url(_value(item, "source_url"))
    canonical_url = _normalized_url(_value(item, "canonical_url") or _nested_metadata_value(item, "canonical_url"))
    title = _normalize_phrase(_value(item, "title"))
    if source_url:
        keys.append(("same URL", source_url))
    if canonical_url:
        keys.append(("same canonical URL", canonical_url))
    if title:
        keys.append(("same normalized title", title))
    return keys


def _combined_text(item: dict[str, Any]) -> str:
    return " ".join(
        [
            _value(item, "title"),
            _value(item, "excerpt"),
            _value(item, "summary"),
            _value(item, "text_excerpt"),
        ]
    )


def _text_for_similarity(item: dict[str, Any]) -> str:
    return " ".join([_value(item, "excerpt"), _value(item, "summary"), _value(item, "text_excerpt")])


def _token_overlap(left: str, right: str) -> float:
    left_tokens = _tokens(left)
    right_tokens = _tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return round(len(left_tokens & right_tokens) / min(len(left_tokens), len(right_tokens)), 3)


def _claim_keywords(item: dict[str, Any]) -> set[str]:
    return {token for token in _tokens(_combined_text(item)) if len(token) >= 5}


def _geography_mentions(item: dict[str, Any]) -> set[str]:
    text = _combined_text(item).lower()
    geographies = {"us", "u.s", "united states", "china", "europe", "eu", "taiwan", "japan", "uk", "india"}
    return {geo for geo in geographies if geo in text}


def _actor_mentions(item: dict[str, Any]) -> set[str]:
    text = _combined_text(item)
    actors = set(re.findall(r"\b[A-Z][A-Za-z0-9&.-]{2,}(?:\s+[A-Z][A-Za-z0-9&.-]{2,})?\b", text))
    source_name = _value(item, "source_name")
    if source_name:
        actors.add(source_name)
    return actors


def _date_proximity_days(left: dict[str, Any], right: dict[str, Any]) -> int | None:
    left_date = _parse_date(_value(left, "published_at"))
    right_date = _parse_date(_value(right, "published_at"))
    if not left_date or not right_date:
        return None
    return abs((left_date - right_date).days)


def _age_days(item: dict[str, Any]) -> int | None:
    published = _parse_date(_value(item, "published_at"))
    retrieved = _parse_date(_value(item, "retrieved_at")) or datetime.now()
    if not published:
        return None
    return max((retrieved - published).days, 0)


def _parse_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value[:10])
    except ValueError:
        return None


def _normalize_record(item: dict[str, Any]) -> dict[str, Any]:
    return dict(item or {})


def _evidence_id(item: dict[str, Any]) -> str:
    stable_id = _value(item, "id") or _value(item, "evidence_id") or _value(item, "trace_id")
    if stable_id:
        return stable_id
    title = _normalize_phrase(_value(item, "title"))
    url = _normalized_url(
        _value(item, "source_url") or _value(item, "canonical_url") or _nested_metadata_value(item, "canonical_url")
    )
    source = _normalize_phrase(_value(item, "source_name") or _value(item, "source_type"))
    created = (_value(item, "created_at") or _value(item, "retrieved_at"))[:19]
    fingerprint = "|".join([title, url, source, created])
    digest = sha1(fingerprint.encode("utf-8")).hexdigest()[:12]
    return f"evref_{digest}"


def _items_matching_terms(items: list[dict[str, Any]], terms: list[str]) -> list[dict[str, Any]]:
    return [item for item in items if _matched_terms(item, terms)]


def _matched_terms(item: dict[str, Any], terms: list[str]) -> list[str]:
    text = _combined_text(item).lower()
    metadata_text = " ".join(
        [
            _value(item, "source_type"),
            _value(item, "source_name"),
            _value(item, "source_url"),
            _value(item, "credibility_tier"),
            _value(item, "validation_status"),
        ]
    ).lower()
    searchable = f"{text} {metadata_text}"
    return [term for term in terms if term.lower() in searchable]


def _risk_explanation(category: str, matched_terms: list[str]) -> str:
    term_text = ", ".join(matched_terms[:5]) if matched_terms else "risk-related terms"
    return f"Evidence contains terms associated with {category.replace('_', ' ')}: {term_text}."


def _confidence_bucket(items: list[dict[str, Any]], matched_terms: list[str]) -> str:
    if len(items) >= 2 or len(matched_terms) >= 3:
        return "high"
    if len(matched_terms) >= 2:
        return "medium"
    return "low"


def _limitation_note(items: list[dict[str, Any]], matched_terms: list[str]) -> str:
    if len(items) <= 1 or len(matched_terms) <= 1:
        return "Based on sparse evidence; reviewer should corroborate before using this signal."
    return "Deterministic text signal only; reviewer should verify context and source quality."


def _historical_analogue_hint(pathway: str) -> str:
    hints = {
        "market_repricing": "Compare with prior market repricing episodes after policy, earnings, or demand shocks.",
        "regulatory_escalation": "Compare with prior regulatory investigations or rulemaking escalation sequences.",
        "policy_relief": "Compare with prior waiver, exemption, or policy relaxation episodes.",
        "supply_chain_reconfiguration": "Compare with prior supplier shift, inventory build, or reshoring episodes.",
        "geopolitical_escalation": "Compare with prior sanctions, diplomatic escalation, or cross-border restriction episodes.",
        "delayed_resolution": "Compare with prior pending-review or postponed-decision timelines.",
    }
    return hints.get(pathway, "Compare with prior episodes sharing similar actors, timing, and evidence sequence.")


def _domain(value: str) -> str:
    if not value:
        return ""
    parsed = urlparse(value if "://" in value else f"https://{value}")
    return parsed.netloc.lower()


def _source_key(item: dict[str, Any]) -> str:
    return _normalized_url(_value(item, "source_url")) or _normalize_phrase(_value(item, "source_name"))


def _date_key(item: dict[str, Any]) -> str:
    return _value(item, "published_at")[:10]


def _reviewer_status(item: dict[str, Any]) -> str:
    return _value(item, "reviewer_status") or _value(item, "status", "Unknown")


def _nested_metadata_value(item: dict[str, Any], key: str) -> str:
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    return _value(metadata, key)


def _value(item: dict[str, Any], key: str, default: str = "") -> str:
    value = item.get(key, default)
    if value is None:
        return default
    return str(value).strip()


def _list_value(item: dict[str, Any], key: str) -> list[str]:
    value = item.get(key, [])
    if isinstance(value, list):
        return [str(entry) for entry in value]
    return [str(value)] if value else []


def _normalized_url(value: str) -> str:
    clean = value.strip().lower()
    if clean.endswith("/"):
        clean = clean[:-1]
    return clean


def _normalize_phrase(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", value.lower()).split())


def _tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) > 2 and token not in STOPWORDS
    }
