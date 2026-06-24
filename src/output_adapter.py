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
    disclaimer = DISCLAIMERS[language]
    note = LANGUAGE_NOTES[language]

    localized_markdown = translate_text(localize_knowledge_text(markdown_text.strip(), language), language)

    if mode == "beginner":
        return _render_beginner_output(language)

    if language in {"zh-CN", "zh-TW"}:
        return _render_chinese_output(localized_markdown, mode, language)

    if mode == "analyst":
        return f"# {title}\n\n{disclaimer}\n\n> {note}\n\n{localized_markdown}\n"

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


def _render_beginner_output(language: str) -> str:
    """Render a plain-language beginner brief with practical next steps."""
    if language == "zh-CN":
        return "\n".join(
            [
                "# 入门解释",
                "",
                DISCLAIMERS[language],
                "",
                "## 一句话解释",
                "",
                "- 这份文件描述的是一个可能影响组织决策、供应链、合规或市场准入的战略问题。",
                "",
                "## 这件事为什么重要",
                "",
                "- 它可能改变企业与供应商、客户、监管机构或政府项目互动的方式。",
                "- 重点不在于预测结果，而在于帮助团队更快整理问题、比较历史案例并准备讨论。",
                "",
                "## 可能受到影响的对象",
                "",
                "- 供应商、客户、合规团队、运营团队、管理层和需要跟踪政策变化的业务部门。",
                "",
                "## 历史上类似情况",
                "",
                "- 类似事件通常会被拿来与出口管制、制裁、产业政策、供应链中断或监管变化进行比较。",
                "- 历史案例只用于提供参考背景，不表示当前事件会重复过去结果。",
                "",
                "## 常见应对方式",
                "",
                "- 组织常见做法包括审查供应链、更新合规流程、准备内部简报、跟踪政策执行细节并确认关键依赖关系。",
                "",
                "## 接下来可以关注什么",
                "",
                "- 哪些供应商、客户或地区暴露度最高。",
                "- 是否需要新的合规文件、审批流程或内部记录。",
                "- 政府或监管机构是否发布实施时间表和细则。",
                "- 历史相似案例中哪些组织反应值得比较。",
                "",
                "## 建议下一步",
                "",
                "- 列出受影响的供应商、客户、地区和业务流程。",
                "- 检查是否需要补充合规文件或内部审批。",
                "- 监测政策实施时间表、监管说明和行业反馈。",
                "- 将当前问题与相似历史案例进行一页式比较。",
                "- 准备一份内部讨论简报，明确已知事实、未知信息和需要跟进的问题。",
                "",
                "## 需要小心的地方",
                "",
                "- 本系统不进行实时网页检索，也不提供预测、法律意见、投资建议或交易建议。",
                "- 输出应由人工分析者复核，尤其是事实、来源和组织适用性。",
                "",
                "## 分析透明度",
                "",
                "- 本系统使用规则式分析流程，将输入文件连接到历史案例、常见机制与战略经验。结果应由人工分析者复核。",
                "",
            ]
        )
    if language == "zh-TW":
        return "\n".join(
            [
                "# 入門解釋",
                "",
                DISCLAIMERS[language],
                "",
                "## 一句話解釋",
                "",
                "- 這份文件描述的是一個可能影響組織決策、供應鏈、合規或市場准入的戰略問題。",
                "",
                "## 這件事為什麼重要",
                "",
                "- 它可能改變企業與供應商、客戶、監管機構或政府專案互動的方式。",
                "- 重點不在於預測結果，而在於幫助團隊更快整理問題、比較歷史案例並準備討論。",
                "",
                "## 可能受到影響的對象",
                "",
                "- 供應商、客戶、合規團隊、營運團隊、管理層和需要追蹤政策變化的業務部門。",
                "",
                "## 歷史上類似情況",
                "",
                "- 類似事件通常會被拿來與出口管制、制裁、產業政策、供應鏈中斷或監管變化進行比較。",
                "- 歷史案例只用於提供參考背景，不表示當前事件會重複過去結果。",
                "",
                "## 常見應對方式",
                "",
                "- 組織常見做法包括檢視供應鏈、更新合規流程、準備內部簡報、追蹤政策執行細節並確認關鍵依賴關係。",
                "",
                "## 接下來可以關注什麼",
                "",
                "- 哪些供應商、客戶或地區暴露度最高。",
                "- 是否需要新的合規文件、審批流程或內部紀錄。",
                "- 政府或監管機構是否發布實施時間表和細則。",
                "- 歷史相似案例中哪些組織反應值得比較。",
                "",
                "## 建議下一步",
                "",
                "- 列出受影響的供應商、客戶、地區和業務流程。",
                "- 檢查是否需要補充合規文件或內部審批。",
                "- 監測政策實施時間表、監管說明和產業反饋。",
                "- 將當前問題與相似歷史案例進行一頁式比較。",
                "- 準備一份內部討論簡報，明確已知事實、未知資訊和需要跟進的問題。",
                "",
                "## 需要小心的地方",
                "",
                "- 本系統不進行即時網頁檢索，也不提供預測、法律意見、投資建議或交易建議。",
                "- 輸出應由人工分析者複核，尤其是事實、來源和組織適用性。",
                "",
                "## 分析透明度",
                "",
                "- 本系統使用規則式分析流程，將輸入文件連結到歷史案例、常見機制與策略經驗。結果應由人工分析者複核。",
                "",
            ]
        )

    return "\n".join(
        [
            "# Beginner Explanation",
            "",
            DISCLAIMERS[language],
            "",
            "## One-sentence explanation",
            "",
            "- This document describes a strategic issue that may affect decisions, supply chains, compliance, or market access.",
            "",
            "## Why this matters",
            "",
            "- It may change how an organization works with suppliers, customers, regulators, or government programs.",
            "- The goal is not to predict outcomes; it is to organize the issue, compare historical situations, and support discussion.",
            "",
            "## Who may be affected",
            "",
            "- Suppliers, customers, compliance teams, operations teams, leadership, and business teams tracking policy changes.",
            "",
            "## Similar historical situations",
            "",
            "- Similar issues are often compared with export controls, sanctions, industrial policy, supply chain disruption, or regulatory change.",
            "- Historical cases are context for comparison, not proof that the current event will repeat the past.",
            "",
            "## Common responses",
            "",
            "- Organizations often review supply chains, update compliance processes, prepare internal briefs, monitor implementation details, and identify key dependencies.",
            "",
            "## What to monitor next",
            "",
            "- Which suppliers, customers, or regions are most exposed.",
            "- Whether new compliance documents, approvals, or internal records are needed.",
            "- Whether government or regulatory bodies publish timelines and implementation details.",
            "- Which similar historical cases are most useful for comparison.",
            "",
            "## Suggested Next Steps",
            "",
            "- Identify which suppliers, customers, regions, and workflows are most exposed.",
            "- Check whether new compliance documentation or internal approval is required.",
            "- Monitor government implementation timelines, regulatory guidance, and industry responses.",
            "- Compare the issue with similar historical cases in a short one-page note.",
            "- Prepare a short internal briefing that separates known facts, unknowns, and follow-up questions.",
            "",
            "## Important limitations",
            "",
            "- The system does not use live web retrieval and does not provide forecasts, legal advice, investment advice, or trading recommendations.",
            "- A human analyst should review the output, especially facts, sources, and organizational relevance.",
            "",
            "## Analysis Transparency",
            "",
            "- This system uses a rules-based workflow to connect the input document with historical cases, common mechanisms, and strategic lessons. A human analyst should review the result.",
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
        disclaimer = DISCLAIMERS[language]
        note = LANGUAGE_NOTES[language]
        labels = {
            "summary": "高管摘要",
            "context": "当前事件背景",
            "scenario": "情境分类",
            "lessons": "战略经验",
            "outcomes": "历史结果",
            "analogues": "历史相似案例",
            "mechanisms": "机制",
            "evidence": "证据审查",
            "limits": "局限性",
        }
        bullets = {
            "summary": [
                "系统已根据输入文本生成本地、确定性的战略情报简报。",
                "本输出用于决策支持和分析师效率提升，不提供预测、法律意见、投资建议或交易建议。",
                "历史案例、机制和证据说明用于帮助组织问题，而不是断言未来结果。",
            ],
            "context": [
                "当前事件背景由输入文档中的关键词、行业、参与者和政策线索生成。",
                "系统不会执行实时网页检索，也不会自动核验外部来源。",
            ],
            "scenario": [
                "情境分类用于说明该事件更接近出口管制、制裁、产业政策、供应链中断、监管行动或其他战略场景。",
                "置信标签描述内部分类线索强弱，不代表概率。",
            ],
            "lessons": [
                "战略经验来自检索到的历史结果模式。",
                "常见经验包括供应链多元化、合规流程扩展、交易对手审查、管理层沟通和持续监测。",
            ],
            "outcomes": [
                "历史结果用于展示类似事件中曾经出现过的组织反应和运营后果。",
                "这些结果是教育性摘要，需要人工复核，不能直接套用为当前事件结论。",
            ],
            "analogues": [
                "历史相似案例用于结构化比较，帮助分析当前事件可能涉及哪些机制和利益相关者。",
                "相似案例不代表当前事件会重复过去结果。",
            ],
            "mechanisms": [
                "机制用于说明事件背后的作用路径，例如技术遏制、战略依赖、供应链重构、产业补贴、市场准入限制和合规负担。",
            ],
            "evidence": [
                "证据审查会区分输入文档、本地历史数据库、机制框架和证据可信度说明。",
                "来源待补充表示该教育性数据尚未附加可核验链接。",
            ],
            "limits": [
                "中文输出只本地化系统生成的分析内容，不声称翻译用户上传的完整原文。",
                "系统不提供实时新闻检索、RAG、预测、法律建议或投资建议。",
            ],
        }
    else:
        title = MODE_TITLES[mode][language]
        disclaimer = DISCLAIMERS[language]
        note = LANGUAGE_NOTES[language]
        labels = {
            "summary": "高階主管摘要",
            "context": "當前事件背景",
            "scenario": "情境分類",
            "lessons": "策略經驗",
            "outcomes": "歷史結果",
            "analogues": "歷史相似案例",
            "mechanisms": "機制",
            "evidence": "證據審查",
            "limits": "限制",
        }
        bullets = {
            "summary": [
                "系統已根據輸入文字生成本地、確定性的戰略情報簡報。",
                "本輸出用於決策支持和分析師效率提升，不提供預測、法律意見、投資建議或交易建議。",
                "歷史案例、機制和證據說明用於幫助組織問題，而不是斷言未來結果。",
            ],
            "context": [
                "當前事件背景由輸入文件中的關鍵字、產業、參與者和政策線索生成。",
                "系統不會執行即時網頁檢索，也不會自動核驗外部來源。",
            ],
            "scenario": [
                "情境分類用於說明該事件更接近出口管制、制裁、產業政策、供應鏈中斷、監管行動或其他戰略場景。",
                "信心標籤描述內部分類線索強弱，不代表機率。",
            ],
            "lessons": [
                "策略經驗來自檢索到的歷史結果模式。",
                "常見經驗包括供應鏈多元化、合規流程擴展、交易對手審查、管理層溝通和持續監測。",
            ],
            "outcomes": [
                "歷史結果用於展示類似事件中曾經出現過的組織反應和營運後果。",
                "這些結果是教育性摘要，需要人工複核，不能直接套用為當前事件結論。",
            ],
            "analogues": [
                "歷史相似案例用於結構化比較，幫助分析當前事件可能涉及哪些機制和利害關係人。",
                "相似案例不代表當前事件會重複過去結果。",
            ],
            "mechanisms": [
                "機制用於說明事件背後的作用路徑，例如技術遏制、戰略依賴、供應鏈重構、產業補貼、市場准入限制和合規負擔。",
            ],
            "evidence": [
                "證據審查會區分輸入文件、本地歷史資料庫、機制框架和證據可信度說明。",
                "來源待補充表示該教育性資料尚未附加可核驗連結。",
            ],
            "limits": [
                "中文輸出只本地化系統生成的分析內容，不聲稱翻譯使用者上傳的完整原文。",
                "系統不提供即時新聞檢索、RAG、預測、法律建議或投資建議。",
            ],
        }

    lines = [f"# {title}", "", disclaimer, "", f"> {note}", ""]
    for key in ["summary", "context", "scenario", "lessons", "outcomes", "analogues", "mechanisms", "evidence", "limits"]:
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
