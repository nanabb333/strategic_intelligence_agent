"""RETIRED historical validator for the superseded V13.3 recommendation contract."""

from __future__ import annotations

from pathlib import Path
import re
import sys

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402


SAMPLE = (
    "New semiconductor export controls affect advanced chip supply chains and market access. "
    "Equipment suppliers are reviewing licensing requirements, customer eligibility, compliance documentation, "
    "supplier exposure, and margin impact."
)


CANONICAL_ORDER = [
    "snapshot",
    "question",
    "criteria",
    "paths",
    "ranking",
    "comparison",
    "preferred",
    "why_holds",
    "assumptions",
    "tradeoffs",
    "change",
    "actions",
    "monitoring",
    "history",
    "expectations",
    "evidence",
    "limitations",
]


HEADINGS = {
    "en": {
        "snapshot": "Decision Snapshot",
        "question": "Decision Question",
        "criteria": "Decision Criteria",
        "paths": "Decision Paths",
        "ranking": "Option Ranking",
        "comparison": "Option Comparison",
        "preferred": "Preferred Path",
        "why_holds": "Why This Reasoning Holds",
        "assumptions": "Assumptions",
        "tradeoffs": "Trade-offs",
        "change": "What Could Change This Recommendation",
        "actions": "Action Timeline",
        "monitoring": "What to Monitor",
        "history": "Historical Evidence",
        "expectations": "Market Expectations vs Actual Outcomes",
        "evidence": "Evidence Used",
        "limitations": "Limitations",
    },
    "zh-CN": {
        "snapshot": "决策快照",
        "question": "决策问题",
        "criteria": "最重要的判断因素",
        "paths": "可行方案",
        "ranking": "方案排序",
        "comparison": "方案对比",
        "preferred": "目前最佳方案",
        "why_holds": "为什么这个判断目前成立",
        "assumptions": "当前假设",
        "tradeoffs": "取舍：得到什么、放弃什么、风险还在哪里",
        "change": "哪些新证据会改变今天的判断",
        "actions": "行动时间表",
        "monitoring": "后续观察重点",
        "history": "历史证据",
        "expectations": "市场预期与实际结果",
        "evidence": "使用的证据",
        "limitations": "限制说明",
    },
    "zh-TW": {
        "snapshot": "決策快照",
        "question": "決策問題",
        "criteria": "最重要的判斷因素",
        "paths": "可行方案",
        "ranking": "方案排序",
        "comparison": "方案對比",
        "preferred": "目前最佳方案",
        "why_holds": "為什麼這個判斷目前成立",
        "assumptions": "目前假設",
        "tradeoffs": "取捨：得到什麼、放棄什麼、風險還在哪裡",
        "change": "哪些新證據會改變今天的判斷",
        "actions": "行動時間表",
        "monitoring": "後續觀察重點",
        "history": "歷史證據",
        "expectations": "市場預期與實際結果",
        "evidence": "使用的證據",
        "limitations": "限制說明",
    },
}


OPTION_TERMS = {
    "en": {
        "option_a": "### Option A",
        "option_b": "### Option B (Recommended)",
        "option_c": "### Option C",
        "path": "**Path:**",
        "pros": "**Pros**",
        "cons": "**Cons**",
        "criteria_fit": "**Criteria Fit**",
        "importance_high": "Importance: High",
    },
    "zh-CN": {
        "option_a": "### 方案 A",
        "option_b": "### 方案 B（推荐）",
        "option_c": "### 方案 C",
        "path": "**路径：**",
        "pros": "**优点**",
        "cons": "**不足**",
        "criteria_fit": "**与判断因素的符合程度**",
        "importance_high": "重要性：高",
    },
    "zh-TW": {
        "option_a": "### 方案 A",
        "option_b": "### 方案 B（建議）",
        "option_c": "### 方案 C",
        "path": "**路徑：**",
        "pros": "**優點**",
        "cons": "**不足**",
        "criteria_fit": "**與判斷因素的符合程度**",
        "importance_high": "重要性：高",
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def analyze(language: str) -> str:
    response = TestClient(app).post(
        "/analyze",
        json={
            "text": SAMPLE,
            "language": language,
            "output_mode": "analyst",
            "question_text": "What should determine this decision?",
        },
    )
    require(response.status_code == 200, response.text)
    return response.json()["brief_markdown"]


def section_headings(markdown: str) -> list[str]:
    return [line.replace("## ", "", 1).strip() for line in markdown.splitlines() if line.startswith("## ")]


def section(markdown: str, heading: str, next_heading: str) -> str:
    start = markdown.find(f"## {heading}")
    end = markdown.find(f"## {next_heading}")
    require(start >= 0 and end > start, f"Could not locate section {heading} before {next_heading}.")
    return markdown[start:end]


def validate_same_section_architecture(outputs: dict[str, str]) -> None:
    for language, markdown in outputs.items():
        expected = [HEADINGS[language][key] for key in CANONICAL_ORDER]
        actual = section_headings(markdown)[: len(expected)]
        require(actual == expected, f"{language} section order differs.\nExpected: {expected}\nActual: {actual}")


def validate_option_cards(outputs: dict[str, str]) -> None:
    for language, markdown in outputs.items():
        terms = OPTION_TERMS[language]
        paths = section(markdown, HEADINGS[language]["paths"], HEADINGS[language]["ranking"])
        for key in ["option_a", "option_b", "option_c", "path", "pros", "cons", "criteria_fit"]:
            require(terms[key] in paths, f"{language} option cards missing {key}: {terms[key]}")
        require(paths.count(terms["path"]) >= 3, f"{language} should have Path field in all three option cards.")
        require(paths.count(terms["pros"]) >= 3, f"{language} should have Pros field in all three option cards.")
        require(paths.count(terms["cons"]) >= 3, f"{language} should have Cons field in all three option cards.")
        require(paths.count(terms["criteria_fit"]) >= 3, f"{language} should have Criteria Fit field in all three option cards.")


def validate_decision_criteria_and_hierarchy(outputs: dict[str, str]) -> None:
    for language, markdown in outputs.items():
        headings = HEADINGS[language]
        terms = OPTION_TERMS[language]
        criteria = section(markdown, headings["criteria"], headings["paths"])
        require(terms["importance_high"] in criteria, f"{language} criteria missing high-importance label.")
        positions = [markdown.find(f"## {headings[key]}") for key in CANONICAL_ORDER]
        require(all(position >= 0 for position in positions), f"{language} missing at least one required section.")
        require(positions == sorted(positions), f"{language} hierarchy is not decision-first.")
        require(markdown.find(f"## {headings['actions']}") < markdown.find(f"## {headings['history']}"), f"{language} actions should appear before historical evidence.")
        require(markdown.find(f"## {headings['monitoring']}") < markdown.find(f"## {headings['history']}"), f"{language} monitoring should appear before historical evidence.")


def validate_chinese_terminology(outputs: dict[str, str]) -> None:
    zh_cn = outputs["zh-CN"]
    zh_tw = outputs["zh-TW"]
    for phrase in ["可行方案", "目前最佳方案", "最重要的判断因素", "与判断因素的符合程度", "后续观察重点", "哪些新证据会改变今天的判断"]:
        require(phrase in zh_cn, f"zh-CN missing professional terminology: {phrase}")
    for phrase in ["可行方案", "目前最佳方案", "最重要的判斷因素", "與判斷因素的符合程度", "後續觀察重點", "哪些新證據會改變今天的判斷"]:
        require(phrase in zh_tw, f"zh-TW missing professional terminology: {phrase}")
    for stale in ["Decision Paths", "Preferred Path", "Decision Criteria", "Criteria Fit", "Trade-offs", "What to Monitor"]:
        require(stale not in zh_cn, f"zh-CN leaked English heading/label: {stale}")
        require(stale not in zh_tw, f"zh-TW leaked English heading/label: {stale}")


def validate_dashboard_localized_cards() -> None:
    app_js = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    styles = (ROOT / "dashboard/styles.css").read_text(encoding="utf-8")
    for phrase in ["决策快照", "決策快照", "最重要的判断因素", "最重要的判斷因素", "哪些新证据会改变今天的判断", "哪些新證據會改變今天的判斷"]:
        require(phrase in app_js, f"Dashboard missing localized section mapping: {phrase}")
    for selector in [".decision-card", ".criteria-card", ".choices-card", ".ranking-card", ".recommended-card", ".monitor-card", ".supporting-card"]:
        require(selector in styles, f"Dashboard missing card style: {selector}")


def validate_language_structure_counts(outputs: dict[str, str]) -> None:
    counts = {language: len(re.findall(r"^## ", markdown, flags=re.MULTILINE)) for language, markdown in outputs.items()}
    require(len(set(counts.values())) == 1, f"Languages should have identical section counts: {counts}")


def main() -> None:
    outputs = {language: analyze(language) for language in ["en", "zh-CN", "zh-TW"]}
    validate_same_section_architecture(outputs)
    validate_language_structure_counts(outputs)
    validate_option_cards(outputs)
    validate_decision_criteria_and_hierarchy(outputs)
    validate_chinese_terminology(outputs)
    validate_dashboard_localized_cards()
    print("V13.3 localization parity validation passed.")


if __name__ == "__main__":
    raise SystemExit("RETIRED: validates the superseded V13.3 localized recommendation contract; not a current V5 validator.")
