"""Validate Strategic Intelligence Agent V4.5 non-AI user layer."""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from output_adapter import adapt_file  # noqa: E402
from run_agent import run_agent  # noqa: E402


LOCALE_KEYS = {
    "appTitle",
    "uploadInstructions",
    "pasteInstructions",
    "helperText",
    "questionTypeLabel",
    "outputModeLabel",
    "languageLabel",
    "runAnalysis",
    "exportMarkdown",
    "exportTxt",
    "documentSummary",
    "scenarioClassification",
    "historicalAnalogues",
    "currentContext",
    "implications",
    "disclaimer",
    "errorEmptyInput",
    "examplePrompt",
}

EXAMPLES = [
    (
        "examples/non_ai_user_examples/beginner_export_controls_zh_TW.md",
        "outputs/beginner_export_controls_zh_TW.md",
        "beginner",
        "zh-TW",
    ),
    (
        "examples/non_ai_user_examples/beginner_supply_chain_zh_CN.md",
        "outputs/beginner_supply_chain_zh_CN.md",
        "beginner",
        "zh-CN",
    ),
    (
        "examples/non_ai_user_examples/beginner_business_policy_en.md",
        "outputs/beginner_business_policy_en.md",
        "beginner",
        "en",
    ),
]

FORBIDDEN = [
    "buy",
    "sell",
    "hold",
    "price target",
    "expected return",
    "should invest",
    "will happen",
    "decision-makers should",
    "trading recommendation",
    "investment recommendation",
]


def assert_exists(path: str) -> Path:
    candidate = ROOT / path
    if not candidate.exists():
        raise AssertionError(f"Missing required file: {path}")
    return candidate


def validate_locales() -> None:
    for locale in ["en", "zh-CN", "zh-TW"]:
        path = assert_exists(f"locales/{locale}.json")
        data = json.loads(path.read_text(encoding="utf-8"))
        missing = LOCALE_KEYS - set(data)
        if missing:
            raise AssertionError(f"{path} missing locale keys: {sorted(missing)}")

    zh_cn = json.loads((ROOT / "locales/zh-CN.json").read_text(encoding="utf-8"))
    zh_tw = json.loads((ROOT / "locales/zh-TW.json").read_text(encoding="utf-8"))
    if "不用会写提示词" not in zh_cn["helperText"]:
        raise AssertionError("Simplified Chinese helper text is missing.")
    if "不用會寫提示詞" not in zh_tw["helperText"]:
        raise AssertionError("Traditional Chinese helper text is missing.")


def validate_guided_questions() -> None:
    path = assert_exists("knowledge_base/guided_questions.csv")
    rows = list(csv.DictReader(path.read_text(encoding="utf-8").splitlines()))
    required_columns = {
        "question_id",
        "language",
        "user_facing_question",
        "internal_analysis_goal",
        "recommended_tools",
        "output_focus",
    }
    if set(rows[0]) != required_columns:
        raise AssertionError("Guided question CSV columns do not match V4.5 schema.")

    languages = {row["language"] for row in rows}
    if languages != {"en", "zh-CN", "zh-TW"}:
        raise AssertionError(f"Unexpected guided question languages: {languages}")

    question_ids = {row["question_id"] for row in rows}
    for language in languages:
        language_rows = [row for row in rows if row["language"] == language]
        if len(language_rows) != 8:
            raise AssertionError(f"{language} should contain 8 guided questions.")
    if len(question_ids) != 8:
        raise AssertionError("Expected 8 unique guided question ids.")


def validate_dashboard() -> None:
    index = assert_exists("dashboard/index.html").read_text(encoding="utf-8")
    app = assert_exists("dashboard/app.js").read_text(encoding="utf-8")
    assert_exists("dashboard/styles.css")

    for marker in ["language-select", "question-select", "mode-select", "guided-question-buttons"]:
        if marker not in index:
            raise AssertionError(f"Dashboard missing {marker}")
    for marker in ["guidedQuestions", "zh-CN", "zh-TW", "applyLocale", "adaptDashboardOutput"]:
        if marker not in app:
            raise AssertionError(f"Dashboard app missing {marker}")


def validate_docs() -> None:
    for path in [
        "docs/non_ai_user_guide.md",
        "docs/non_ai_user_guide_zh_CN.md",
        "docs/non_ai_user_guide_zh_TW.md",
        "docs/localization_design.md",
        "docs/guided_question_design.md",
        "docs/archive/v45_non_ai_user_layer.md",
    ]:
        assert_exists(path)


def generate_outputs() -> None:
    tmp_dir = Path("/private/tmp/strategic_intelligence_agent_v45")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    for input_file, output_file, mode, language in EXAMPLES:
        base_output = tmp_dir / (Path(output_file).stem + "_base.md")
        run_agent(ROOT / input_file, base_output)
        adapt_file(base_output, ROOT / output_file, mode=mode, language=language)
        assert_exists(output_file)


def validate_forbidden_language() -> None:
    for _, output_file, _, _ in EXAMPLES:
        text = (ROOT / output_file).read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN:
            if re.search(r"\b" + re.escape(phrase) + r"\b", text):
                raise AssertionError(f"Forbidden language found in {output_file}: {phrase}")


def main() -> None:
    assert_exists("src/output_adapter.py")
    validate_locales()
    validate_guided_questions()
    validate_dashboard()
    validate_docs()
    generate_outputs()
    validate_forbidden_language()
    print("V4.5 validation passed.")


if __name__ == "__main__":
    main()
