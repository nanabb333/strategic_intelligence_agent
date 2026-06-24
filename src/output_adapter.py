"""Output mode and deterministic localization adapter."""

from __future__ import annotations

from pathlib import Path

from knowledge_localization import localize_knowledge_text
from localization import translate_text


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
    note = LANGUAGE_NOTES[language]

    localized_markdown = translate_text(localize_knowledge_text(markdown_text.strip(), language), language)

    if mode == "beginner":
        return _render_beginner_output(language)

    if language in {"zh-CN", "zh-TW"}:
        return _render_chinese_output(localized_markdown, mode, language)

    if mode == "analyst":
        return f"# {title}\n\n> {note}\n\n{localized_markdown}\n"

    line_limit = 8 if mode == "beginner" else 12
    selected_lines = _extract_lines(localized_markdown, line_limit)
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


def _render_beginner_output(language: str) -> str:
    """Render a plain-language beginner brief with practical next steps."""
    if language == "zh-CN":
        return "\n".join(
            [
                "# 入门解释",
                "",
                "## 这意味着什么",
                "",
                "- 这份文件描述的是一个可能影响组织决策、供应链、合规或市场准入的战略问题。",
                "- 关键不是预测结果，而是尽快确认哪些对象受影响、哪些流程需要调整、接下来应监测哪些信号。",
                "",
                "## 这件事为什么重要",
                "",
                "- 它可能改变企业与供应商、客户、监管机构或政府项目互动的方式。",
                "- 重点不在于预测结果，而在于帮助团队更快整理问题、比较历史案例并准备讨论。",
                "",
                "## 相似历史案例",
                "",
                "- 类似事件通常会被拿来与出口管制、制裁、产业政策、供应链中断或监管变化进行比较。",
                "- 历史案例只用于提供参考背景，不表示当前事件会重复过去结果。",
                "",
                "## 常见应对方式",
                "",
                "- 组织常见做法包括审查供应链、更新合规流程、准备内部简报、跟踪政策执行细节并确认关键依赖关系。",
                "",
                "## 后来通常发生什么",
                "",
                "- 类似案例中，影响通常不会只停留在新闻标题上，而会进入供应链、合规文件、客户沟通和管理层说明。",
                "- 如果缺少市场或用户结果证据，应明确说明本地数据不足，而不是推断收益或损失。",
                "",
                "## 接下来可以关注什么",
                "",
                "- 哪些供应商、客户或地区暴露度最高。",
                "- 是否需要新的合规文件、审批流程或内部记录。",
                "- 政府或监管机构是否发布实施时间表和细则。",
                "- 历史相似案例中哪些组织反应值得比较。",
                "",
                "## 限制说明",
                "",
                "- 仅用于教育和决策支持。",
                "- 不提供投资建议、交易建议、法律建议或预测。",
                "- 历史相似案例不能预测未来结果。",
                "- 建议由人工复核事实、来源和组织适用性。",
                "",
            ]
        )
    if language == "zh-TW":
        return "\n".join(
            [
                "# 入門解釋",
                "",
                "## 這意味著什麼",
                "",
                "- 這份文件描述的是一個可能影響組織決策、供應鏈、合規或市場准入的戰略問題。",
                "- 關鍵不是預測結果，而是盡快確認哪些對象受影響、哪些流程需要調整、接下來應監測哪些訊號。",
                "",
                "## 這件事為什麼重要",
                "",
                "- 它可能改變企業與供應商、客戶、監管機構或政府專案互動的方式。",
                "- 重點不在於預測結果，而在於幫助團隊更快整理問題、比較歷史案例並準備討論。",
                "",
                "## 相似歷史案例",
                "",
                "- 類似事件通常會被拿來與出口管制、制裁、產業政策、供應鏈中斷或監管變化進行比較。",
                "- 歷史案例只用於提供參考背景，不表示當前事件會重複過去結果。",
                "",
                "## 常見應對方式",
                "",
                "- 組織常見做法包括檢視供應鏈、更新合規流程、準備內部簡報、追蹤政策執行細節並確認關鍵依賴關係。",
                "",
                "## 後來通常發生什麼",
                "",
                "- 類似案例中，影響通常不會只停留在新聞標題上，而會進入供應鏈、合規文件、客戶溝通和管理層說明。",
                "- 如果缺少市場或使用者結果證據，應明確說明本地資料不足，而不是推斷收益或損失。",
                "",
                "## 接下來可以關注什麼",
                "",
                "- 哪些供應商、客戶或地區暴露度最高。",
                "- 是否需要新的合規文件、審批流程或內部紀錄。",
                "- 政府或監管機構是否發布實施時間表和細則。",
                "- 歷史相似案例中哪些組織反應值得比較。",
                "",
                "## 限制說明",
                "",
                "- 僅用於教育和決策支持。",
                "- 不提供投資建議、交易建議、法律建議或預測。",
                "- 歷史相似案例不能預測未來結果。",
                "- 建議由人工複核事實、來源和組織適用性。",
                "",
            ]
        )

    return "\n".join(
            [
                "# Beginner Explanation",
                "",
            "## What This Means",
            "",
            "- This document describes a strategic issue that may affect decisions, supply chains, compliance, or market access.",
            "- The key issue is not to predict the outcome; it is to identify who is exposed, what processes may need adjustment, and which signals to monitor next.",
            "",
            "## Why this matters",
            "",
            "- It may change how an organization works with suppliers, customers, regulators, or government programs.",
            "- The goal is not to predict outcomes; it is to organize the issue, compare historical situations, and support discussion.",
            "",
            "## Similar Historical Cases",
            "",
            "- Similar issues are often compared with export controls, sanctions, industrial policy, supply chain disruption, or regulatory change.",
            "- Historical cases are context for comparison, not proof that the current event will repeat the past.",
            "",
                "## Common Responses",
            "",
            "- Organizations often review supply chains, update compliance processes, prepare internal briefs, monitor implementation details, and identify key dependencies.",
            "",
            "## What Happened After",
            "",
            "- In similar cases, effects often moved beyond the headline into supply chains, compliance files, customer communication, and management commentary.",
            "- If market or user outcome evidence is missing, the system should say the local dataset does not contain enough evidence rather than infer gains or losses.",
            "",
            "## What to monitor next",
            "",
            "- Which suppliers, customers, or regions are most exposed.",
            "- Whether new compliance documents, approvals, or internal records are needed.",
            "- Whether government or regulatory bodies publish timelines and implementation details.",
            "- Which similar historical cases are most useful for comparison.",
            "",
            "## Important Limitations",
            "",
            "- Educational use only.",
            "- Not investment advice, trading advice, legal advice, or a forecast.",
            "- Historical analogues do not predict future outcomes.",
            "- Human review is recommended for facts, sources, and organizational relevance.",
            "",
        ]
    )


def _render_chinese_output(localized_markdown: str, mode: str, language: str) -> str:
    """Render a strict Chinese brief from localized deterministic sections.

    This renderer intentionally avoids carrying over long English analytical
    paragraphs from the base brief. Proper nouns in extracted case names may
    remain in English, but generated explanation text is Chinese.
    """
    if language == "zh-CN":
        title = MODE_TITLES[mode][language]
        note = LANGUAGE_NOTES[language]
        labels = {
            "direct": "直接回答",
            "similar": "相似案例",
            "then": "当时发生什么",
            "response": "组织如何应对",
            "after": "后来发生什么",
            "market": "市场预期与实际结果",
            "now": "这对现在代表什么",
            "watch": "接下来 30–90 天该看什么",
            "evidence": "使用的证据",
            "limits": "限制说明",
        }
        bullets = {
            "direct": [
                "该事件应被理解为一个需要梳理暴露度、比较历史案例并持续监测执行信号的战略问题。",
                "系统的核心判断是：先确认谁受影响、哪些流程可能需要调整，再观察政策、供应链和管理层沟通的后续变化。",
            ],
            "similar": ["可比较出口管制、制裁、产业政策、供应链中断或监管变化等本地历史案例。"],
            "then": ["类似案例中，最初影响通常出现在客户准入、合规文件、供应链路径或管理层说明。"],
            "response": ["组织常见做法包括复核供应商、更新合规流程、准备内部简报和监测执行细节。"],
            "after": ["后来影响通常进入运营调整阶段，而不是只停留在标题事件本身。"],
            "market": ["如果本地数据缺少市场或用户结果证据，系统会说明证据不足，而不是推断收益或损失。"],
            "now": ["当前最有用的问题是：谁暴露最多、哪些流程会变、下一条可观察信号是什么。"],
            "watch": ["接下来 30–90 天可关注监管细则、供应商公告、管理层指引、资本开支调整和客户沟通变化。"],
            "evidence": [
                "使用输入文本、本地历史相似案例和本地历史结果记录。",
            ],
            "limits": [
                "仅用于教育和决策支持；不提供投资建议、法律建议或预测。",
                "历史相似案例不能预测未来结果；严肃决策需要人工复核。",
            ],
        }
    else:
        title = MODE_TITLES[mode][language]
        note = LANGUAGE_NOTES[language]
        labels = {
            "direct": "直接回答",
            "similar": "相似案例",
            "then": "當時發生什麼",
            "response": "組織如何應對",
            "after": "後來發生什麼",
            "market": "市場預期與實際結果",
            "now": "這對現在代表什麼",
            "watch": "接下來 30–90 天該看什麼",
            "evidence": "使用的證據",
            "limits": "限制說明",
        }
        bullets = {
            "direct": [
                "該事件應被理解為一個需要梳理暴露度、比較歷史案例並持續監測執行訊號的戰略問題。",
                "系統的核心判斷是：先確認誰受影響、哪些流程可能需要調整，再觀察政策、供應鏈和管理層溝通的後續變化。",
            ],
            "similar": ["可比較出口管制、制裁、產業政策、供應鏈中斷或監管變化等本地歷史案例。"],
            "then": ["類似案例中，最初影響通常出現在客戶准入、合規文件、供應鏈路徑或管理層說明。"],
            "response": ["組織常見做法包括複核供應商、更新合規流程、準備內部簡報和監測執行細節。"],
            "after": ["後來影響通常進入營運調整階段，而不是只停留在標題事件本身。"],
            "market": ["如果本地資料缺少市場或使用者結果證據，系統會說明證據不足，而不是推斷收益或損失。"],
            "now": ["當前最有用的問題是：誰暴露最多、哪些流程會變、下一條可觀察訊號是什麼。"],
            "watch": ["接下來 30–90 天可關注監管細則、供應商公告、管理層指引、資本開支調整和客戶溝通變化。"],
            "evidence": [
                "使用輸入文字、本地歷史相似案例和本地歷史結果記錄。",
            ],
            "limits": [
                "僅用於教育和決策支持；不提供投資建議、法律建議或預測。",
                "歷史相似案例不能預測未來結果；嚴肅決策需要人工複核。",
            ],
        }

    lines = [f"# {title}", "", f"> {note}", ""]
    for key in [
        "direct",
        "similar",
        "then",
        "response",
        "after",
        "market",
        "now",
        "watch",
        "evidence",
        "limits",
    ]:
        lines.extend([f"## {labels[key]}", ""])
        lines.extend(f"- {item}" for item in bullets[key])
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def adapt_file(input_path: str | Path, output_path: str | Path, mode: str, language: str) -> Path:
    """Adapt an existing Markdown brief and write it to disk."""
    source = Path(input_path)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(adapt_output(source.read_text(encoding="utf-8"), mode, language), encoding="utf-8")
    return destination
