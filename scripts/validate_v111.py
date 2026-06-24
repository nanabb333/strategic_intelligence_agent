"""Validate V11.1 product quality fixes."""

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


def analyze(language: str, mode: str, question: str) -> dict:
    client = TestClient(app)
    response = client.post(
        "/analyze",
        json={
            "text": (
                "New semiconductor export controls affect advanced chip suppliers, "
                "licensing requirements, customer eligibility, compliance documentation, "
                "and market access for AI chip supply chains."
            ),
            "language": language,
            "output_mode": mode,
            "question_text": question,
        },
    )
    require(response.status_code == 200, f"{language}/{mode} analyze failed: {response.text}")
    return response.json()


def validate_theme() -> None:
    styles = read("dashboard/styles.css")
    for color in ["#B8A7E8", "#F7F4FF", "#EFEAFB", "#DDD6F7", "#7C6AA6"]:
        require(color in styles, f"Soft lavender-grey theme missing {color}.")
    for loud in ["#8B5CF6", "#A78BFA", "#7C3AED", "#6D28D9", "#1f5eff", "#1241b2"]:
        require(loud not in styles, f"Loud or old purple/blue color remains: {loud}.")


def validate_direct_answer_and_market_section() -> None:
    payload = analyze("en", "analyst", "Which historical events are similar? How did organizations respond?")
    brief = payload["brief_markdown"]
    first_section = brief.find("## Direct Answer")
    require(first_section != -1, "Direct Answer section missing.")
    require(first_section < brief.find("## Similar Cases"), "Direct Answer is not the first substantive section.")
    for phrase in [
        "Similar cases",
        "What Happened Then",
        "How Organizations Responded",
        "What Happened After",
        "What To Watch Next",
        "The key pattern is",
        "The main risk is",
        "The next signal to watch is",
    ]:
        require(phrase in brief, f"Direct answer missing practical phrase: {phrase}.")
    for phrase in [
        "## Market Expectations vs Actual Outcomes",
        "Initial / mainstream expectation",
        "Market or user behavior",
        "Actual observed outcome",
        "Expectation gap",
        "Local dataset does not contain enough market-outcome evidence for this claim.",
    ]:
        require(phrase in brief, f"Market expectation section missing phrase: {phrase}.")
    require(brief.count("## Limitations") == 1, "Limitations should appear exactly once.")
    require(brief.rfind("## Limitations") > brief.find("## Market Expectations vs Actual Outcomes"), "Limitations should appear after analysis sections.")
    require(brief.count("investment advice") == 1, "Investment-advice disclaimer should appear only in final limitations.")


def validate_beginner_plain_language() -> None:
    payload = analyze("en", "beginner", "What does this mean?")
    brief = payload["brief_markdown"]
    for section in [
        "## What This Means",
        "## Why this matters",
        "## Similar Historical Cases",
        "## Common Responses",
        "## What Happened After",
        "## What to monitor next",
        "## Important Limitations",
    ]:
        require(section in brief, f"Beginner brief missing section: {section}.")
    for jargon in [
        "Mechanism",
        "Multi-Lens",
        "Political Economy",
        "International Relations",
        "Tool Registry",
        "Agent Router",
        "source pending",
    ]:
        require(jargon not in brief, f"Beginner brief leaked analyst jargon: {jargon}.")


def validate_chinese_localization() -> None:
    simplified = analyze("zh-CN", "analyst", "哪些历史事件相似？组织如何应对？")["brief_markdown"]
    for phrase in ["直接回答", "相似案例", "当时发生什么", "组织如何应对", "后来发生什么", "市场预期与实际结果", "这对现在代表什么", "接下来 30–90 天该看什么", "使用的证据", "限制说明"]:
        require(phrase in simplified, f"zh-CN analyst output missing label: {phrase}.")
    for english in ["Economics", "Political Economy", "International Relations", "Business Strategy", "Direct Answer", "Historical Patterns"]:
        require(english not in simplified, f"zh-CN output leaked English framework label: {english}.")

    traditional = analyze("zh-TW", "beginner", "這代表什麼？")["brief_markdown"]
    for phrase in ["這意味著什麼", "相似歷史案例", "常見應對方式", "後來通常發生什麼", "接下來可以關注什麼", "限制說明"]:
        require(phrase in traditional, f"zh-TW beginner output missing label: {phrase}.")
    for english in ["Economics", "Political Economy", "International Relations", "Business Strategy", "Direct Answer"]:
        require(english not in traditional, f"zh-TW output leaked English framework label: {english}.")


def validate_desktop_readiness_docs() -> None:
    readme = read("README.md")
    for phrase in [
        "Desktop App Readiness",
        "For Normal Users",
        "For Developers",
        "Download",
        "Double click",
        "no Python, Git, VS Code, terminal commands, or local server setup",
    ]:
        require(phrase in readme, f"README missing desktop-readiness phrase: {phrase}.")


def main() -> None:
    validate_theme()
    validate_direct_answer_and_market_section()
    validate_beginner_plain_language()
    validate_chinese_localization()
    validate_desktop_readiness_docs()
    print("V11.1 validation passed.")


if __name__ == "__main__":
    main()
