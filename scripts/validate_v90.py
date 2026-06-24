"""Validate V9 product and intelligence upgrade."""

from __future__ import annotations

import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from localization import translate_text  # noqa: E402
from output_adapter import adapt_output  # noqa: E402
from question_router import route_question  # noqa: E402


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_dataset() -> None:
    path = ROOT / "knowledge_base" / "historical_outcomes.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    require(len(rows) >= 50, f"Expected at least 50 historical outcome cases, found {len(rows)}.")
    require(not any(row.get(None) for row in rows), "historical_outcomes.csv contains malformed CSV rows.")
    families = {row["event_family"] for row in rows}
    for family in [
        "Export Controls",
        "Sanctions",
        "Industrial Policy",
        "Supply Chain Disruption",
        "Technology Competition",
        "Regulatory Action",
        "Geopolitical Escalation",
        "Corporate Strategic Response",
        "Financial / Earnings Geopolitical Exposure",
    ]:
        require(family in families, f"Dataset missing event family: {family}.")


def validate_docs() -> None:
    taxonomy = ROOT / "docs" / "intelligence_case_taxonomy.md"
    audit = ROOT / "docs" / "intelligence_dataset_audit.md"
    require(taxonomy.exists(), "docs/intelligence_case_taxonomy.md missing.")
    require(audit.exists(), "docs/intelligence_dataset_audit.md missing.")
    audit_text = audit.read_text(encoding="utf-8")
    require("Current case count:** 55" in audit_text, "Dataset audit missing current case count.")
    require("Mechanism Distribution" in audit_text, "Dataset audit missing mechanism distribution.")


def validate_localization() -> None:
    require((ROOT / "src" / "localization.py").exists(), "src/localization.py missing.")
    sample = "# Executive Intelligence Brief\n\n## Current Event Context\n\n- **Confidence:** Medium"
    simplified = translate_text(sample, "zh-CN")
    traditional = translate_text(sample, "zh-TW")
    require("当前事件背景" in simplified and "中等" in simplified, "Simplified Chinese localization incomplete.")
    require("當前事件背景" in traditional and "中等（繁體）" in traditional, "Traditional Chinese localization incomplete.")
    adapted = adapt_output(sample, mode="analyst", language="zh-CN")
    require("分析师推理简报" in adapted and "当前事件背景" in adapted, "Output adapter is not using localization layer.")


def validate_question_router() -> None:
    require((ROOT / "src" / "question_router.py").exists(), "src/question_router.py missing.")
    route = route_question("What historical events resemble this?")
    require(route.intent == "Historical Comparison", "Question router failed historical-comparison intent.")
    route = route_question("What evidence is missing?")
    require(route.intent == "Evidence Review", "Question router failed evidence-review intent.")


def validate_dashboard() -> None:
    index = read("dashboard/index.html")
    app_js = read("dashboard/app.js")
    styles = read("dashboard/styles.css")
    require('id="question-input"' in index, "Free-form question input missing.")
    require("Ask a Question" in index, "Ask a Question label missing.")
    require("question-select" not in index, "Old question type dropdown still present.")
    require("question_id: \"freeform\"" in app_js, "Dashboard is not sending free-form question id.")
    require("questionPlaceholder" in app_js, "Dashboard missing question placeholder localization.")
    require("dragover" in app_js and "drop" in app_js, "Dashboard missing drag-and-drop handlers.")
    require(".document-dropzone" in styles, "Input area visual emphasis missing.")

    executive_index = index.find("executiveBrief")
    lessons_index = index.find("strategicLessons")
    outcomes_index = index.find("historicalOutcomes")
    analogues_index = index.find("historicalAnalogues")
    detailed_index = index.find("detailedAnalysis")
    trace_index = index.find("executionTrace")
    require(
        executive_index < lessons_index < outcomes_index < analogues_index < detailed_index < trace_index,
        "Dashboard layout order does not match V9 value-first sequence.",
    )


def validate_readme() -> None:
    readme = read("README.md")
    require("Product Improvements From Real User Testing" in readme, "README missing user-testing improvements section.")
    require("Free-form analyst questions" in readme, "README missing free-form question positioning.")
    require("55 educational cases" in readme, "README missing expanded dataset count.")


def main() -> None:
    validate_dataset()
    validate_docs()
    validate_localization()
    validate_question_router()
    validate_dashboard()
    validate_readme()
    print("V9.0 validation passed.")


if __name__ == "__main__":
    main()
