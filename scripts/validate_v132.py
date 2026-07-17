"""RETIRED historical validator for the superseded V13.2 recommendation contract."""

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


SCENARIOS = {
    "semiconductor": (
        "New semiconductor export controls affect advanced chip supply chains and market access. "
        "Equipment suppliers are reviewing licensing requirements, customer eligibility, compliance documentation, "
        "supplier exposure, and margin impact."
    ),
    "taiwan_family": (
        "A Taiwan-based family holds most assets in Taiwan real estate and local equities while future education "
        "and business cash flows may require USD liquidity. The family is considering whether to diversify toward "
        "US and Singapore assets without selling existing holdings immediately."
    ),
    "usd_insurance": (
        "A bank relationship manager is promoting a USD-denominated insurance savings product. The client wants "
        "to compare the product with USD deposits, Treasuries, and bond ETFs, and understand surrender costs, "
        "FX exposure, liquidity limits, and suitability risks."
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def analyze(text: str, *, language: str = "en", mode: str = "analyst") -> str:
    response = TestClient(app).post(
        "/analyze",
        json={
            "text": text,
            "language": language,
            "output_mode": mode,
            "question_text": "What should determine the decision, and why is the recommended option currently preferred?",
        },
    )
    require(response.status_code == 200, response.text)
    return response.json()["brief_markdown"]


def section(text: str, title: str, next_title: str) -> str:
    start = text.find(title)
    end = text.find(next_title)
    require(start >= 0 and end > start, f"Could not locate {title} before {next_title}.")
    return text[start:end]


def criteria_names(criteria_section: str) -> set[str]:
    return set(re.findall(r"- \*\*([^*]+)\*\* — \*\*Importance:", criteria_section))


def validate_weighted_criteria() -> None:
    brief = analyze(SCENARIOS["semiconductor"])
    criteria = section(brief, "## Decision Criteria", "## Decision Paths")
    require("Importance: High" in criteria, "Decision criteria must include at least one High importance label.")
    require("Importance: Medium" in criteria, "Decision criteria should include prioritized, not flat, criteria.")
    for phrase in ["Customer exposure", "Licensing uncertainty", "Margin impact"]:
        require(phrase in criteria, f"Semiconductor criteria missing {phrase}.")


def validate_criteria_vary() -> None:
    extracted = {}
    for name, text in SCENARIOS.items():
        brief = analyze(text)
        extracted[name] = criteria_names(section(brief, "## Decision Criteria", "## Decision Paths"))
    require(len({tuple(sorted(values)) for values in extracted.values()}) == 3, "Criteria should vary across three scenario types.")
    require("Jurisdiction concentration" in extracted["taiwan_family"], "Taiwan family criteria missing jurisdiction concentration.")
    require("Product suitability evidence" in extracted["usd_insurance"], "USD insurance criteria missing suitability evidence.")


def validate_option_fit_ranking_and_preferred_path() -> None:
    brief = analyze(SCENARIOS["semiconductor"])
    paths = section(brief, "## Decision Paths", "## Option Ranking")
    ranking = section(brief, "## Option Ranking", "## Option Comparison")
    preferred = section(brief, "## Preferred Path", "## Why This Reasoning Holds")
    require("**Criteria Fit**" in paths, "Option cards must include Criteria Fit.")
    require("Strong on Customer exposure, Licensing uncertainty, Margin impact" in paths, "Recommended option fit should reference high-importance criteria.")
    require("highest-importance criteria are Customer exposure, Licensing uncertainty, Margin impact" in ranking, "Ranking must reference weighted criteria.")
    require("Ranks second" in ranking and "Ranks third" in ranking, "Ranking must explain #2 and #3 positions.")
    require("Top criteria driving the recommendation: Customer exposure, Licensing uncertainty, Margin impact" in preferred, "Preferred path must name top criteria.")
    require("Why Option A does not rank first" in preferred, "Preferred path must explain rejected Option A.")
    require("Why Option C does not rank first" in preferred, "Preferred path must explain rejected Option C.")
    require("What would change the ranking" in preferred, "Preferred path must explain what could change the answer.")


def validate_tradeoffs_change_triggers_and_history() -> None:
    brief = analyze(SCENARIOS["semiconductor"])
    tradeoffs = section(brief, "## Trade-offs", "## What Could Change This Recommendation")
    for phrase in ["Benefits gained", "Costs accepted", "Opportunities sacrificed", "Risks still unresolved"]:
        require(phrase in tradeoffs, f"Trade-offs missing {phrase}.")
    change = section(brief, "## What Could Change This Recommendation", "## Action Timeline")
    for phrase in ["Option A becomes more reasonable", "Option C becomes more reasonable"]:
        require(phrase in change, f"Change trigger missing {phrase}.")
    require(brief.find("## Historical Evidence") > brief.find("## What to Monitor"), "Historical Evidence should remain below decision content.")
    historical = section(brief, "## Historical Evidence", "## Market Expectations")
    for phrase in ["**Why it supports the recommendation:**", "**Key limitation:**", "**Decision lesson:**", "**Why this case does not fully apply:**"]:
        require(phrase in historical, f"Historical evidence missing decision-evidence field {phrase}.")


def validate_beginner_and_chinese_outputs() -> None:
    beginner = analyze(SCENARIOS["semiconductor"], mode="beginner")
    require("## What matters most" in beginner, "Beginner mode must include plain-language criteria.")
    require("Importance:" not in beginner, "Beginner mode should not expose criteria weighting labels.")
    for forbidden in ["mechanism engine", "scoring model", "internal framework", "Agent Router", "Tool Registry"]:
        require(forbidden.lower() not in beginner.lower(), f"Beginner mode leaked internal label: {forbidden}")

    zh_cn = analyze(SCENARIOS["semiconductor"], language="zh-CN")
    for phrase in ["## 最重要的判断因素", "## 方案排序", "## 取舍：得到什么、放弃什么、风险还在哪里", "## 当前假设", "## 哪些新证据会改变今天的判断", "## 后续观察重点"]:
        require(phrase in zh_cn, f"zh-CN output missing localized heading: {phrase}")
    zh_tw = analyze(SCENARIOS["semiconductor"], language="zh-TW")
    for phrase in ["## 最重要的判斷因素", "## 方案排序", "## 取捨：得到什麼、放棄什麼、風險還在哪裡", "## 目前假設", "## 哪些新證據會改變今天的判斷", "## 後續觀察重點"]:
        require(phrase in zh_tw, f"zh-TW output missing localized heading: {phrase}")


def validate_dashboard_support() -> None:
    app_js = (ROOT / "dashboard/app.js").read_text(encoding="utf-8")
    styles = (ROOT / "dashboard/styles.css").read_text(encoding="utf-8")
    for phrase in ["Decision Criteria", "Criteria Fit", "Importance: High"]:
        require(phrase in app_js, f"Dashboard renderer missing {phrase}.")
    for selector in [".criteria-card", ".importance.high", ".criteria-fit-label", ".tradeoff-card", ".change-card"]:
        require(selector in styles, f"Dashboard styles missing {selector}.")


def main() -> None:
    validate_weighted_criteria()
    validate_criteria_vary()
    validate_option_fit_ranking_and_preferred_path()
    validate_tradeoffs_change_triggers_and_history()
    validate_beginner_and_chinese_outputs()
    validate_dashboard_support()
    print("V13.2 criteria-driven reasoning consolidation validation passed.")


if __name__ == "__main__":
    raise SystemExit("RETIRED: validates the superseded V13.2 ranking contract; not a current V5 validator.")
