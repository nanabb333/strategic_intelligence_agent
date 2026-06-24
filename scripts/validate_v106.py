"""Validate V10.6 beginner readability and actionable output upgrade."""

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


def analyze(language: str, mode: str) -> dict:
    client = TestClient(app)
    response = client.post(
        "/analyze",
        json={
            "text": (
                "New semiconductor export controls affect advanced chip suppliers, "
                "customer access, compliance documentation, and supply chain planning."
            ),
            "language": language,
            "output_mode": mode,
            "question_text": "What does this issue mean and what should I monitor next?",
        },
    )
    require(response.status_code == 200, f"{language}/{mode} analyze failed: {response.text}")
    return response.json()


def validate_beginner_brief() -> None:
    payload = analyze("en", "beginner")
    brief = payload["brief_markdown"]
    for phrase in [
        "One-sentence explanation",
        "Why this matters",
        "Who may be affected",
        "Similar historical situations",
        "Common responses",
        "What to monitor next",
        "Suggested Next Steps",
        "Important limitations",
        "Analysis Transparency",
    ]:
        require(phrase in brief, f"Beginner brief missing section: {phrase}.")
    for phrase in ["Benchmark results", "Tool Registry", "Agent Router", "Mechanism framework entry", "source pending"]:
        require(phrase not in brief, f"Beginner brief leaked internal phrase: {phrase}.")


def validate_chinese_beginner_brief() -> None:
    payload = analyze("zh-TW", "beginner")
    brief = payload["brief_markdown"]
    for phrase in [
        "一句話解釋",
        "這件事為什麼重要",
        "可能受到影響的對象",
        "歷史上類似情況",
        "常見應對方式",
        "接下來可以關注什麼",
        "建議下一步",
        "需要小心的地方",
        "分析透明度",
    ]:
        require(phrase in brief, f"zh-TW beginner brief missing heading: {phrase}.")
    forbidden = [
        "One-sentence explanation",
        "Why this matters",
        "Suggested Next Steps",
        "This system uses",
        "Benchmark results",
        "Tool Registry",
        "Agent Router",
        "source pending",
        "forecast",
        "investment advice",
    ]
    for phrase in forbidden:
        require(phrase not in brief, f"zh-TW beginner brief leaked English/internal phrase: {phrase}.")


def validate_dashboard_beginner_mode() -> None:
    index = read("dashboard/index.html")
    app_js = read("dashboard/app.js")
    require("beginner-only" in index, "Dashboard missing beginner-only transparency section.")
    require("internal-detail" in index, "Dashboard does not mark internal sections for hiding.")
    require("applyOutputModeVisibility" in app_js, "Dashboard missing output-mode visibility controller.")
    require("beginner-mode" in app_js, "Dashboard does not toggle beginner-mode class.")
    for phrase in ["Benchmark results", "Execution Trace", "Analysis Path", "Selected Tools", "Tool Registry", "Agent Router"]:
        require(phrase in index, f"Analyst detail phrase missing entirely: {phrase}.")


def validate_theme() -> None:
    styles = read("dashboard/styles.css")
    for color in ["#A78BFA", "#C4B5FD", "#F5F3FF", "#EDE9FE", "#7C3AED"]:
        require(color in styles, f"Softer lavender color missing: {color}.")
    for color in ["#8B5CF6", "#6D28D9", "#1f5eff", "#1241b2"]:
        require(color not in styles, f"Over-saturated or old theme color remains: {color}.")


def validate_analyst_detail_preserved() -> None:
    payload = analyze("en", "analyst")
    brief = payload["brief_markdown"]
    for phrase in ["Mechanisms", "Evidence", "Agent Execution Trace"]:
        require(phrase in brief, f"Analyst brief lost detailed section: {phrase}.")


def main() -> None:
    validate_beginner_brief()
    validate_chinese_beginner_brief()
    validate_dashboard_beginner_mode()
    validate_theme()
    validate_analyst_detail_preserved()
    print("V10.6 validation passed.")


if __name__ == "__main__":
    main()
