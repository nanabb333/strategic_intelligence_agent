"""Validate V10.5 Chinese rendering and lavender UI redesign."""

from __future__ import annotations

from pathlib import Path
import sys

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_chinese_api_output() -> None:
    client = TestClient(app)
    response = client.post(
        "/analyze",
        json={
            "text": (
                "New export controls affect semiconductor suppliers, strategic dependency, "
                "supply chain reconfiguration, compliance burden, and market access."
            ),
            "language": "zh-TW",
            "output_mode": "analyst",
            "question_text": "這和哪些歷史事件相似？",
        },
    )
    require(response.status_code == 200, f"zh-TW analyze failed: {response.text}")
    payload = response.json()
    brief = payload["brief_markdown"]
    mechanisms = str(payload["analysis"].get("mechanisms", []))

    for phrase in ["策略經驗", "歷史結果", "歷史相似案例", "當前事件背景", "機制", "證據審查"]:
        require(phrase in brief, f"Chinese brief missing required section: {phrase}.")

    forbidden = [
        "The issue may indicate",
        "Historical and context evidence should be used",
        "Supply chain diversification frequently appears",
        "Strategic Dependency",
        "Supply Chain Reconfiguration",
        "Market Access Restriction",
        "Source:",
        "ImplicationAnalyzer",
    ]
    for phrase in forbidden:
        require(phrase not in brief, f"Chinese brief leaked English phrase: {phrase}.")
        require(phrase not in mechanisms, f"Chinese analysis leaked English mechanism phrase: {phrase}.")


def validate_dashboard_order_and_labels() -> None:
    index = read("dashboard/index.html")
    app_js = read("dashboard/app.js")
    styles = read("dashboard/styles.css")

    language = index.find("language-select")
    mode = index.find("mode-select")
    question = index.find("question-input")
    input_tabs = index.find("input-mode-tabs")
    require(-1 not in [language, mode, question, input_tabs], "Dashboard input controls missing.")
    require(language < mode < question < input_tabs, "Dashboard first-screen order is not language, mode, question, input.")

    for phrase in [
        "工具註冊表",
        "智能路由",
        "多維分析",
        "綜合分析",
        "機制框架",
        "歷史資料庫",
        "輸入文件",
        "來源待補充",
    ]:
        require(phrase in app_js, f"Dashboard missing localized label: {phrase}.")

    for phrase in ["Source:", "ImplicationAnalyzer"]:
        require(phrase not in app_js, f"Dashboard renderer still contains hardcoded English label: {phrase}.")

    for color in ["#A78BFA", "#EDE9FE", "#7C3AED"]:
        require(color in styles, f"Lavender theme missing color: {color}.")
    for old_color in ["#1f5eff", "#1241b2", "#8B5CF6"]:
        require(old_color not in styles, f"Old blue theme color still present: {old_color}.")


def validate_output_adapter() -> None:
    from output_adapter import adapt_output

    markdown = """
# Executive Intelligence Brief

## Strategic Lessons
- Supply chain diversification frequently appears after export-control or disruption shocks.

## Mechanisms Detected
- Strategic Dependency
"""
    rendered = adapt_output(markdown, mode="analyst", language="zh-CN")
    for phrase in ["战略经验", "历史结果", "历史相似案例", "证据审查"]:
        require(phrase in rendered, f"Strict Chinese renderer missing section: {phrase}.")
    for phrase in ["Supply chain diversification frequently appears", "Strategic Dependency", "Source:"]:
        require(phrase not in rendered, f"Strict Chinese renderer leaked English phrase: {phrase}.")


def main() -> None:
    validate_chinese_api_output()
    validate_dashboard_order_and_labels()
    validate_output_adapter()
    print("V10.5 validation passed.")


if __name__ == "__main__":
    main()
