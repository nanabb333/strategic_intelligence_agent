"""Localization for curated knowledge-base terms and artifacts."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


KNOWLEDGE_TERMS = {
    "zh-CN": {
        "Technology Containment": "技术遏制",
        "Strategic Dependency": "战略依赖",
        "Supply Chain Reconfiguration": "供应链重构",
        "Capital Constraint": "资本约束",
        "Market Access Restriction": "市场准入限制",
        "Industrial Subsidy": "产业补贴",
        "Security Escalation": "安全升级",
        "Regulatory Shock": "监管冲击",
        "Information Uncertainty": "信息不确定性",
        "Demand Shock": "需求冲击",
        "Financial Intermediation Stress": "金融中介压力",
        "Compliance Burden": "合规负担",
        "Alliance Coordination": "联盟协调",
        "Chokepoint Exposure": "瓶颈暴露",
        "Policy Signaling": "政策信号",
        "Operational Resilience": "运营韧性",
        "Counterparty Risk": "交易对手风险",
        "Legislative Implementation Gap": "立法实施缺口",
        "Reputational Sensitivity": "声誉敏感性",
        "Input Cost Pressure": "投入成本压力",
        "Monitoring and contingency planning": "监测与应急规划",
        "Historical Outcomes Database": "历史结果数据库",
        "Mechanism Framework": "机制框架",
        "Response Playbook": "应对手册",
        "Mechanism framework entry": "机制框架条目",
        "Deterministic response pattern": "确定性应对模式",
    },
    "zh-TW": {
        "Technology Containment": "技術遏制",
        "Strategic Dependency": "戰略依賴",
        "Supply Chain Reconfiguration": "供應鏈重構",
        "Capital Constraint": "資本約束",
        "Market Access Restriction": "市場准入限制",
        "Industrial Subsidy": "產業補貼",
        "Security Escalation": "安全升級",
        "Regulatory Shock": "監管衝擊",
        "Information Uncertainty": "資訊不確定性",
        "Demand Shock": "需求衝擊",
        "Financial Intermediation Stress": "金融中介壓力",
        "Compliance Burden": "合規負擔",
        "Alliance Coordination": "聯盟協調",
        "Chokepoint Exposure": "瓶頸暴露",
        "Policy Signaling": "政策信號",
        "Operational Resilience": "營運韌性",
        "Counterparty Risk": "交易對手風險",
        "Legislative Implementation Gap": "立法實施缺口",
        "Reputational Sensitivity": "聲譽敏感性",
        "Input Cost Pressure": "投入成本壓力",
        "Monitoring and contingency planning": "監測與應急規劃",
        "Historical Outcomes Database": "歷史結果資料庫",
        "Mechanism Framework": "機制框架",
        "Response Playbook": "應對手冊",
        "Mechanism framework entry": "機制框架條目",
        "Deterministic response pattern": "確定性應對模式",
    },
}


def localize_knowledge_text(text: str, language: str) -> str:
    """Translate curated knowledge-base terms while preserving source text."""
    if language == "en":
        return text
    localized = text
    for source, target in KNOWLEDGE_TERMS.get(language, {}).items():
        localized = localized.replace(source, target)
    return localized


def localize_analysis_payload(payload: dict[str, Any], language: str) -> dict[str, Any]:
    """Localize major knowledge-base fields in analysis artifacts."""
    if language == "en":
        return payload
    cloned = deepcopy(payload)
    _walk_and_localize(cloned, language)
    return cloned


def _walk_and_localize(value: Any, language: str) -> None:
    if isinstance(value, dict):
        for key, item in list(value.items()):
            if isinstance(item, str):
                value[key] = localize_knowledge_text(item, language)
            else:
                _walk_and_localize(item, language)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            if isinstance(item, str):
                value[index] = localize_knowledge_text(item, language)
            else:
                _walk_and_localize(item, language)
