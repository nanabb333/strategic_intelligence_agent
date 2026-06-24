"""Validate V11.2 rescue sprint user-value fixes."""

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
            "text": "Semiconductor export controls affect suppliers, licensing, customer eligibility, and advanced chip market access.",
            "language": language,
            "output_mode": mode,
            "question_text": "Which historical events are similar? What happened? What should I watch?",
        },
    )
    require(response.status_code == 200, response.text)
    return response.json()


def validate_link_experience() -> None:
    index = read("dashboard/index.html")
    app_js = read("dashboard/app.js")
    app_py = read("app.py")
    require("Analyze Link" in index, "Dashboard should not show misleading Paste Link copy.")
    require("try to fetch readable webpage text" in index, "Dashboard missing clear link-fetch explanation.")
    require("_fetch_url_text" in app_py and "No readable article content was detected" in app_py, "Backend link fetching/blocking behavior missing.")
    require("Links are stored as source metadata" not in app_js, "Old fake-link metadata copy remains.")


def validate_output_order() -> None:
    brief = analyze("en", "analyst")["brief_markdown"]
    sections = [
        "## Direct Answer",
        "## Similar Cases",
        "## What Happened Then",
        "## How Organizations Responded",
        "## What Happened After",
        "## Market Expectations vs Actual Outcomes",
        "## What This Means Now",
        "## What To Watch Next",
        "## Evidence Used",
        "## Limitations",
    ]
    for section in sections:
        require(section in brief, f"Missing section: {section}.")
    positions = [brief.find(section) for section in sections]
    require(positions == sorted(positions), "Output sections are not in required order.")
    require("## Mechanisms" not in brief and "## Agent Execution Trace" not in brief, "Internal framework sections leaked into main brief.")
    require(brief.count("## Limitations") == 1, "Limitations must appear once.")


def validate_beginner_and_chinese() -> None:
    beginner = analyze("en", "beginner")["brief_markdown"]
    for forbidden in [
        "Economics",
        "Political Economy",
        "International Relations",
        "Business Strategy",
        "Mechanism",
        "Framework",
        "Substantial",
        "Evidence evaluator",
        "Agent router",
        "Execution trace",
        "Method details",
    ]:
        require(forbidden not in beginner, f"Beginner output leaked forbidden term: {forbidden}.")

    chinese = analyze("zh-TW", "analyst")["brief_markdown"]
    for phrase in [
        "直接回答",
        "相似案例",
        "當時發生什麼",
        "組織如何應對",
        "後來發生什麼",
        "市場預期與實際結果",
        "這對現在代表什麼",
        "接下來 30–90 天該看什麼",
        "使用的證據",
        "限制說明",
    ]:
        require(phrase in chinese, f"zh-TW output missing required phrase: {phrase}.")
    for english in ["Economics", "Political Economy", "International Relations", "Business Strategy", "Substantial"]:
        require(english not in chinese, f"Chinese output leaked English framework label: {english}.")


def validate_demo_outputs() -> None:
    demo_dir = ROOT / "demo_outputs" / "v11_2_rescue"
    files = sorted(demo_dir.glob("*.md"))
    require(len(files) >= 5, f"Expected at least 5 demo outputs, found {len(files)}.")
    for path in files:
        text = path.read_text(encoding="utf-8")
        for phrase in ["## Direct Answer", "## Market Expectations vs Actual Outcomes", "## What To Watch Next", "## Limitations"]:
            require(phrase in text, f"{path.name} missing {phrase}.")


def validate_no_bad_empty_state() -> None:
    for path in ["dashboard/app.js", "dashboard/index.html", "README.md"]:
        require("No current event context returned" not in read(path), f"Bad empty-state copy remains in {path}.")


def main() -> None:
    validate_link_experience()
    validate_output_order()
    validate_beginner_and_chinese()
    validate_demo_outputs()
    validate_no_bad_empty_state()
    print("V11.2 rescue validation passed.")


if __name__ == "__main__":
    main()
