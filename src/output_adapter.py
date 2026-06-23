"""Output mode and deterministic localization adapter."""

from __future__ import annotations

from pathlib import Path


SUPPORTED_MODES = {"beginner", "analyst", "executive"}
SUPPORTED_LANGUAGES = {"en", "zh-CN", "zh-TW"}


LANGUAGE_NOTES = {
    "en": "English output mode.",
    "zh-CN": "简体中文模板化输出。核心分析由本地规则生成；未使用外部翻译 API。",
    "zh-TW": "繁體中文模板化輸出。核心分析由本地規則生成；未使用外部翻譯 API。",
}


MODE_TITLES = {
    "beginner": {"en": "Beginner Explanation", "zh-CN": "入门解释", "zh-TW": "入門解釋"},
    "analyst": {"en": "Analyst Reasoning Brief", "zh-CN": "分析师推理简报", "zh-TW": "分析師推理簡報"},
    "executive": {"en": "Executive Summary", "zh-CN": "高管摘要", "zh-TW": "高層摘要"},
}


DISCLAIMERS = {
    "en": "Decision-support only. No forecasts, probabilities, trading advice, or investment recommendations.",
    "zh-CN": "仅用于决策支持；不提供预测、概率、交易建议或投资建议。",
    "zh-TW": "僅用於決策支持；不提供預測、機率、交易建議或投資建議。",
}


def _extract_lines(markdown_text: str, limit: int) -> list[str]:
    lines = []
    for line in markdown_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            lines.append(stripped)
        elif stripped.startswith("**Core issue:**") or stripped.startswith("**Summary:**"):
            lines.append(f"- {stripped}")
        if len(lines) >= limit:
            break
    return lines


def adapt_output(markdown_text: str, mode: str = "analyst", language: str = "en") -> str:
    """Adapt a Markdown brief for a user mode and language.

    Localization is deterministic and template-based. It does not use external
    translation APIs and does not translate every source sentence.
    """
    if mode not in SUPPORTED_MODES:
        raise ValueError(f"Unsupported output mode: {mode}")
    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported language: {language}")

    title = MODE_TITLES[mode][language]
    disclaimer = DISCLAIMERS[language]
    note = LANGUAGE_NOTES[language]

    if mode == "analyst":
        return f"# {title}\n\n{disclaimer}\n\n> {note}\n\n{markdown_text.strip()}\n"

    line_limit = 8 if mode == "beginner" else 12
    selected_lines = _extract_lines(markdown_text, line_limit)
    if not selected_lines:
        selected_lines = ["- No structured findings were generated."]

    if language == "zh-CN":
        section_label = "重点内容"
        next_steps = "如何阅读：先看核心问题，再看证据来源和需要继续关注的事项。"
    elif language == "zh-TW":
        section_label = "重點內容"
        next_steps = "如何閱讀：先看核心問題，再看證據來源和需要繼續關注的事項。"
    else:
        section_label = "Key Points"
        next_steps = "How to read this: start with the core issue, then review evidence sources and monitoring considerations."

    return "\n".join(
        [
            f"# {title}",
            "",
            disclaimer,
            "",
            f"> {note}",
            "",
            f"## {section_label}",
            "",
            *selected_lines,
            "",
            f"## {next_steps}",
            "",
        ]
    )


def adapt_file(input_path: str | Path, output_path: str | Path, mode: str, language: str) -> Path:
    """Adapt an existing Markdown brief and write it to disk."""
    source = Path(input_path)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(adapt_output(source.read_text(encoding="utf-8"), mode, language), encoding="utf-8")
    return destination

