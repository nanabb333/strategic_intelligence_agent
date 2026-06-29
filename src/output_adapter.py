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

    source_markdown = markdown_text.strip()
    localized_markdown = translate_text(localize_knowledge_text(source_markdown, language), language)

    if mode == "beginner":
        return _render_beginner_output(language, localized_markdown)

    if mode == "executive":
        return _render_executive_output(localized_markdown, language)

    if language in {"zh-CN", "zh-TW"}:
        return _render_chinese_output(source_markdown, mode, language)

    return localized_markdown.strip() + "\n"


def _section_map(markdown_text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_title = ""
    current_lines: list[str] = []
    for line in markdown_text.splitlines():
        if line.startswith("## "):
            if current_title:
                sections[current_title] = "\n".join(current_lines).strip()
            current_title = line.replace("## ", "", 1).strip()
            current_lines = []
        elif current_title:
            current_lines.append(line)
    if current_title:
        sections[current_title] = "\n".join(current_lines).strip()
    return sections


def _beginner_criteria(criteria_text: str) -> str:
    if not criteria_text:
        return "- The most important factors are exposure, reversibility, execution burden, and what new information the next review will produce."
    simplified: list[str] = []
    for line in criteria_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        stripped = stripped.replace("- **", "- ").replace("**", "")
        if " — " in stripped:
            name, rest = stripped.split(" — ", 1)
            reason = rest.split(". ", 1)[1] if ". " in rest else rest
            simplified.append(f"{name}: {reason}")
        else:
            simplified.append(stripped)
    return "\n".join(simplified[:6]) or criteria_text


def _render_executive_output(markdown_text: str, language: str) -> str:
    sections = _section_map(markdown_text)
    if language == "zh-CN":
        title = "高管摘要"
        preferred = "Preferred Path"
        monitor = "What to Monitor"
        actions = "Action Timeline"
        limitations = "Limitations"
    elif language == "zh-TW":
        title = "高層摘要"
        preferred = "Preferred Path"
        monitor = "What to Monitor"
        actions = "Action Timeline"
        limitations = "Limitations"
    else:
        title = "Executive Summary"
        preferred = "Preferred Path"
        monitor = "What to Monitor"
        actions = "Action Timeline"
        limitations = "Limitations"

    lines = [f"# {title}", ""]
    for section in ["Decision Snapshot", "Decision Criteria", preferred, "Assumptions", "Trade-offs", "Failure Modes", "What Could Change This Recommendation", monitor, actions, limitations]:
        body = sections.get(section)
        if body:
            lines.extend([f"## {section}", "", body, ""])
    if len(lines) <= 2:
        return markdown_text.strip() + "\n"
    return "\n".join(lines).strip() + "\n"


def _render_beginner_from_sections(markdown_text: str) -> str:
    sections = _section_map(markdown_text)
    snapshot = sections.get("Decision Snapshot", "").strip()
    question = sections.get("Decision Question", "").strip()
    criteria = sections.get("Decision Criteria", "").strip()
    paths = sections.get("Decision Paths", "").strip()
    preferred = sections.get("Preferred Path", "").strip()
    reasoning = sections.get("Why This Reasoning Holds", "").strip()
    assumptions = sections.get("Assumptions", "").strip()
    tradeoffs = sections.get("Trade-offs", "").strip()
    failure_modes = sections.get("Failure Modes", "").strip()
    change_section = sections.get("What Could Change This Recommendation", "").strip()
    monitor = sections.get("What to Monitor", "").strip()
    actions = sections.get("Action Timeline", "").strip() or sections.get("Actions / Next Steps", "").strip()
    limitations = sections.get("Limitations", "").strip()
    change_lines = [
        line
        for line in reasoning.splitlines()
        if "make it wrong" in line.lower() or "would make" in line.lower()
    ]
    return "\n".join(
        [
            "# Beginner Explanation",
            "",
            "## Decision Snapshot",
            "",
            snapshot or "**Current Position:** Gradual monitoring and staged adjustment",
            "",
            "## What this means",
            "",
            question or "- The issue should be treated as a decision question, not only a news summary.",
            "",
            "## Why it matters",
            "",
            "- The useful decision is whether to wait, prepare gradually, or act defensively now.",
            "- The answer depends on exposure, costs, reversibility, and whether stronger evidence appears.",
            "",
            "## What matters most",
            "",
            _beginner_criteria(criteria),
            "",
            "## Your choices",
            "",
            paths or "- Option A: wait.\\n- Option B: prepare gradually.\\n- Option C: act defensively now.",
            "",
            "## Best current path",
            "",
            preferred or "- Option B is usually the better starting point when evidence is meaningful but still incomplete.",
            "",
            "## What to watch next",
            "",
            monitor or "- Watch for evidence that the issue is becoming more costly, less reversible, or more structural.",
            "",
            "## What could change this answer",
            "",
            change_section or "\n".join(change_lines) or "- Clear evidence of severe exposure, binding constraints, customer loss, or persistent cost pressure could change the answer.",
            "",
            "## Assumptions behind this answer",
            "",
            assumptions or "- The current evidence remains incomplete but meaningful enough to justify staged preparation.",
            "",
            "## Trade-offs",
            "",
            tradeoffs or "- The recommended path keeps flexibility, but it requires active monitoring and does not remove all risk immediately.",
            "",
            "## How this could fail",
            "",
            failure_modes or "- The recommendation could fail if exposure worsens faster than the review cadence or if the historical comparison does not fit the current case.",
            "",
            "## Action Timeline",
            "",
            actions or "- Build an exposure map and define trigger points for changing the decision path.",
            "",
            "## Limitations",
            "",
            limitations or "- Educational decision-support only. Not investment, legal, trading, or forecasting advice.",
            "",
        ]
    )


def _render_beginner_output(language: str, markdown_text: str = "") -> str:
    """Render a plain-language beginner brief with practical next steps."""
    if language == "en" and markdown_text:
        return _render_beginner_from_sections(markdown_text)
    if language == "zh-CN":
        return "\n".join(
            [
                "# 入门解释",
                "",
                "## 当前判断",
                "",
                "**Current Position:** 逐步监测并准备阶段性调整",
                "**Confidence:** Medium",
                "**Why:** 类似历史案例显示，最初新闻标题通常不是全部影响，真正问题常出现在执行细节、暴露度、客户或供应商反应中。",
                "**Next 30-90 Days:** 关注管理层说明、供应商和客户暴露、政策细节、成本压力，以及问题是否从短期调整变成结构性风险。",
                "",
                "## 这意味着什么",
                "",
                "- 这份文件描述的是一个可能影响组织决策、供应链、合规或市场准入的战略问题。",
                "- 关键不是预测结果，而是尽快确认哪些对象受影响、哪些流程需要调整、接下来应监测哪些信号。",
                "",
                "## 为什么重要",
                "",
                "- 它可能改变企业与供应商、客户、监管机构或政府项目互动的方式。",
                "- 重点不在于预测结果，而在于帮助团队更快整理问题、比较历史案例并准备讨论。",
                "",
                "## 最重要的判断因素",
                "",
                "- 暴露度是否已经具体到客户、供应商、地区或产品。",
                "- 行动是否可逆，以及现在行动会不会造成不必要成本。",
                "- 是否有足够信息支持立即行动，还是更适合先建立监测和准备机制。",
                "",
                "## 可能路径",
                "",
                "- Option A: 维持现状，等待更多证据。",
                "- Option B: 逐步调整，边监测边准备。",
                "- Option C: 立即采取防御性行动。",
                "",
                "## 当前较好的路径",
                "",
                "- Option B 当前更合适，因为它保留灵活性，同时降低以后被迫仓促反应的风险。",
                "- 其他路径暂不优先：Option A 可能准备不足，Option C 可能在证据不足时带来过高成本。",
                "",
                "## 放弃了什么",
                "",
                "- 放弃了完全不行动的低成本。",
                "- 也放弃了立即防御行动带来的最大保护。",
                "- 换取的是更清楚的暴露度、后续调整空间和较低的仓促决策风险。",
                "",
                "## 接下来可以关注什么",
                "",
                "- 哪些供应商、客户或地区暴露度最高。",
                "- 是否需要新的合规文件、审批流程或内部记录。",
                "- 政府或监管机构是否发布实施时间表和细则。",
                "- 历史相似案例中哪些组织反应值得比较。",
                "",
                "## 什么可能改变答案",
                "",
                "- 如果出现明确的客户损失、强制性规则、严重成本压力或管理层指引变化，可能需要转向更防御性的行动。",
                "",
                "## 当前假设",
                "",
                "- 当前信息足以开始准备，但还不足以证明必须立即采取最防御性的行动。",
                "- 历史案例只能用于比较，不能当作预测。",
                "",
                "## 限制",
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
                "## 目前判斷",
                "",
                "**Current Position:** 逐步監測並準備階段性調整",
                "**Confidence:** Medium",
                "**Why:** 類似歷史案例顯示，最初新聞標題通常不是全部影響，真正問題常出現在執行細節、暴露度、客戶或供應商反應中。",
                "**Next 30-90 Days:** 關注管理層說明、供應商和客戶暴露、政策細節、成本壓力，以及問題是否從短期調整變成結構性風險。",
                "",
                "## 這意味著什麼",
                "",
                "- 這份文件描述的是一個可能影響組織決策、供應鏈、合規或市場准入的戰略問題。",
                "- 關鍵不是預測結果，而是盡快確認哪些對象受影響、哪些流程需要調整、接下來應監測哪些訊號。",
                "",
                "## 為什麼重要",
                "",
                "- 它可能改變企業與供應商、客戶、監管機構或政府專案互動的方式。",
                "- 重點不在於預測結果，而在於幫助團隊更快整理問題、比較歷史案例並準備討論。",
                "",
                "## 最重要的判斷因素",
                "",
                "- 暴露度是否已經具體到客戶、供應商、地區或產品。",
                "- 行動是否可逆，以及現在行動會不會造成不必要成本。",
                "- 是否有足夠資訊支持立即行動，還是更適合先建立監測和準備機制。",
                "",
                "## 可能路徑",
                "",
                "- Option A: 維持現狀，等待更多證據。",
                "- Option B: 逐步調整，邊監測邊準備。",
                "- Option C: 立即採取防禦性行動。",
                "",
                "## 目前較好的路徑",
                "",
                "- Option B 目前更合適，因為它保留靈活性，同時降低以後被迫倉促反應的風險。",
                "- 其他路徑暫不優先：Option A 可能準備不足，Option C 可能在證據不足時帶來過高成本。",
                "",
                "## 放棄了什麼",
                "",
                "- 放棄了完全不行動的低成本。",
                "- 也放棄了立即防禦行動帶來的最大保護。",
                "- 換取的是更清楚的暴露度、後續調整空間和較低的倉促決策風險。",
                "",
                "## 接下來可以關注什麼",
                "",
                "- 哪些供應商、客戶或地區暴露度最高。",
                "- 是否需要新的合規文件、審批流程或內部紀錄。",
                "- 政府或監管機構是否發布實施時間表和細則。",
                "- 歷史相似案例中哪些組織反應值得比較。",
                "",
                "## 什麼可能改變答案",
                "",
                "- 如果出現明確的客戶流失、強制性規則、嚴重成本壓力或管理層指引變化，可能需要轉向更防禦性的行動。",
                "",
                "## 目前假設",
                "",
                "- 目前資訊足以開始準備，但還不足以證明必須立即採取最防禦性的行動。",
                "- 歷史案例只能用於比較，不能當作預測。",
                "",
                "## 限制",
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
            "## Decision Snapshot",
            "",
            "**Current Position:** Gradual monitoring and staged adjustment",
            "**Confidence:** Medium",
            "**Why:** Similar historical cases suggest the first headline is rarely the full impact; the real issue usually appears through implementation details, exposure, customer or supplier reaction, and management guidance.",
            "**Next 30-90 Days:** Track management guidance, supplier/customer exposure, policy details, cost pressure, and whether the issue remains temporary or becomes structural.",
            "",
            "## What this means",
            "",
            "- This document describes a strategic issue that may affect decisions, supply chains, compliance, or market access.",
            "- The key issue is not to predict the outcome; it is to identify who is exposed, what processes may need adjustment, and which signals to monitor next.",
            "",
            "## Why it matters",
            "",
            "- It may change how an organization works with suppliers, customers, regulators, or government programs.",
            "- The goal is not to predict outcomes; it is to organize the issue, compare historical situations, and support discussion.",
            "",
            "## Possible paths",
            "",
            "- Option A: Keep the current position and wait for more evidence.",
            "- Option B: Make gradual adjustments while monitoring the issue.",
            "- Option C: Take immediate defensive action.",
            "",
            "## Best current path",
            "",
            "- Option B is currently the better path because it keeps flexibility while reducing the risk of reacting later under worse conditions.",
            "",
            "## What to watch next",
            "",
            "- Which suppliers, customers, or regions are most exposed.",
            "- Whether new compliance documents, approvals, or internal records are needed.",
            "- Whether government or regulatory bodies publish timelines and implementation details.",
            "- Which similar historical cases are most useful for comparison.",
            "",
            "## What could change the answer",
            "",
            "- Clear customer loss, binding rules, severe cost pressure, or changed management guidance could make a more defensive path more appropriate.",
            "",
            "## Limitations",
            "",
            "- Educational use only.",
            "- Not investment advice, trading advice, legal advice, or a forecast.",
            "- Historical analogues do not predict future outcomes.",
            "- Human review is recommended for facts, sources, and organizational relevance.",
            "",
        ]
    )


CHINESE_SECTION_HEADINGS = {
    "zh-CN": {
        "Decision Snapshot": "决策快照",
        "Decision Question": "决策问题",
        "Decision Criteria": "最重要的判断因素",
        "Decision Paths": "可行方案",
        "Option Ranking": "方案排序",
        "Option Comparison": "方案对比",
        "Preferred Path": "目前最佳方案",
        "Why This Reasoning Holds": "为什么这个判断目前成立",
        "Assumptions": "当前假设",
        "Trade-offs": "取舍：得到什么、放弃什么、风险还在哪里",
        "Failure Modes": "可能失效的情况",
        "What Could Change This Recommendation": "哪些新证据会改变今天的判断",
        "Action Timeline": "行动时间表",
        "What to Monitor": "后续观察重点",
        "Historical Evidence": "历史证据",
        "Market Expectations vs Actual Outcomes": "市场预期与实际结果",
        "Evidence Used": "使用的证据",
        "Limitations": "限制说明",
    },
    "zh-TW": {
        "Decision Snapshot": "決策快照",
        "Decision Question": "決策問題",
        "Decision Criteria": "最重要的判斷因素",
        "Decision Paths": "可行方案",
        "Option Ranking": "方案排序",
        "Option Comparison": "方案對比",
        "Preferred Path": "目前最佳方案",
        "Why This Reasoning Holds": "為什麼這個判斷目前成立",
        "Assumptions": "目前假設",
        "Trade-offs": "取捨：得到什麼、放棄什麼、風險還在哪裡",
        "Failure Modes": "可能失效的情況",
        "What Could Change This Recommendation": "哪些新證據會改變今天的判斷",
        "Action Timeline": "行動時間表",
        "What to Monitor": "後續觀察重點",
        "Historical Evidence": "歷史證據",
        "Market Expectations vs Actual Outcomes": "市場預期與實際結果",
        "Evidence Used": "使用的證據",
        "Limitations": "限制說明",
    },
}


CHINESE_ORDER = [
    "Decision Snapshot",
    "Decision Question",
    "Decision Criteria",
    "Decision Paths",
    "Option Ranking",
    "Option Comparison",
    "Preferred Path",
    "Why This Reasoning Holds",
    "Assumptions",
    "Trade-offs",
    "Failure Modes",
    "What Could Change This Recommendation",
    "Action Timeline",
    "What to Monitor",
    "Historical Evidence",
    "Market Expectations vs Actual Outcomes",
    "Evidence Used",
    "Limitations",
]


def _chinese_replacements(language: str) -> dict[str, str]:
    if language == "zh-CN":
        return {
            "**Current Position:**": "**当前建议：**",
            "**Confidence:**": "**信心等级：**",
            "**Why:**": "**判断依据：**",
            "**Next 30-90 Days:**": "**未来 30-90 天：**",
            "**Path:**": "**路径：**",
            "**Pros**": "**优点**",
            "**Cons**": "**不足**",
            "**Criteria Fit**": "**与判断因素的符合程度**",
            "**Case:**": "**案例：**",
            "**Why it supports the recommendation:**": "**为什么支持当前建议：**",
            "**Key limitation:**": "**关键限制：**",
            "**Decision lesson:**": "**决策启示：**",
            "**Why this case does not fully apply:**": "**为什么不能直接套用：**",
            "**Initial / mainstream expectation:**": "**最初 / 主流预期：**",
            "**Market or user behavior:**": "**市场或用户行为：**",
            "**Actual observed outcome:**": "**实际观察结果：**",
            "**Expectation gap:**": "**预期差：**",
            "**Lesson:**": "**启示：**",
            "### Option A": "### 方案 A",
            "### Option B (Recommended)": "### 方案 B（推荐）",
            "### Option C": "### 方案 C",
            "Wait for final rule detail before changing operations": "等待最终规则细节，再决定是否调整运营",
            "Map exposure and prepare staged adjustments": "梳理暴露度，并准备阶段性调整",
            "Immediately reduce exposed customers, suppliers, or product lines": "立即减少受影响的客户、供应商或产品线",
            "Lowest immediate effort.": "短期投入最低。",
            "Preserves current posture while more evidence arrives.": "在更多证据出现前保留现有安排。",
            "Risk can accumulate if exposure is already material.": "如果暴露度已经较高，风险可能继续累积。",
            "May delay preparation if the issue moves quickly.": "如果事件发展很快，准备工作可能滞后。",
            "Best balance between preparation and flexibility.": "在提前准备和保留灵活性之间较平衡。",
            "Creates useful information before irreversible action.": "在采取不可逆行动前，先形成有用的信息基础。",
            "Requires active monitoring and ownership.": "需要明确负责人，并持续跟踪。",
            "Does not eliminate exposure immediately.": "不能立即消除全部暴露。",
            "Highest immediate risk reduction.": "短期风险降低幅度最大。",
            "Useful if exposure is already severe or binding.": "如果暴露已经严重或约束已经生效，这一路径更有用。",
            "Highest opportunity cost and execution burden.": "机会成本和执行负担最高。",
            "Hardest to reverse if the issue proves temporary.": "如果问题后来被证明只是短期扰动，这一路径最难撤回。",
            "Strong on low execution burden and near-term opportunity cost.": "在降低执行负担和短期机会成本方面表现较强。",
            "Strong on": "在",
            "Weak on": "在以下方面较弱：",
            "if current exposure is already material.": "如果当前暴露已经实质化。",
            "Fails high-importance criteria when": "如果",
            "cannot be assessed quickly.": "无法快速评估，就难以满足高重要性判断因素。",
            "because it converts uncertainty into an exposure map and review cadence.": "因为它把不确定性转化为暴露度清单和复盘节奏。",
            "Medium on immediate protection because it prepares response options before using them.": "即时保护程度中等，因为它先准备应对方案，再决定是否启用。",
            "Best overall fit when high-importance criteria are serious but not yet fully resolved.": "当高重要性因素已经值得重视、但尚未完全明朗时，它的整体匹配度最高。",
            "Strong on immediate protection if": "如果",
            "is already severe.": "已经严重，则即时保护效果较强。",
            "Weak on execution complexity, reversibility, and sacrificed upside.": "在执行复杂度、可逆性和放弃的上行空间方面较弱。",
            "Only fits the high-importance criteria better than Option B if evidence shows": "只有当证据显示",
            "Only fits the high-importance criteria better than 方案 B if evidence shows": "只有当证据显示",
            "is binding or worsening.": "已经形成约束或继续恶化时，才比方案 B 更符合高重要性判断因素。",
            "Ranks first because the highest-importance criteria are": "排名第一，因为最高重要性的判断因素是",
            "It improves readiness on those criteria without creating the execution burden of Option C or the underpreparedness of Option A.": "它能提升这些维度上的准备度，同时避免方案 C 的执行负担和方案 A 的准备不足。",
            "It improves readiness on those criteria without creating the execution burden of 方案 C or the underpreparedness of 方案 A.": "它能提升这些维度上的准备度，同时避免方案 C 的执行负担和方案 A 的准备不足。",
            "Ranks second because it has lower cost and disruption than Option C, but it is weaker than Option B on": "排名第二，因为它比方案 C 成本和扰动更低，但在以下因素上弱于方案 B：",
            "Ranks second because it has lower cost and disruption than 方案 C, but it is weaker than 方案 B on": "排名第二，因为它比方案 C 成本和扰动更低，但在以下因素上弱于方案 B：",
            "if exposure grows.": "如果暴露度上升。",
            "Ranks third because it offers more protection, but it is weaker on reversibility, opportunity cost, and execution burden unless": "排名第三，因为它保护力度更强，但除非",
            "Option B currently ranks first": "方案 B 目前排名第一",
            "It ranks first because": "它排名第一，是因为",
            "Top criteria driving the recommendation:": "推动当前建议的核心判断因素：",
            "Why 方案 B ranks first:": "为什么方案 B 排名第一：",
            "it performs best on the criteria that matter most for this decision, especially": "它在本次决策最重要的因素上表现最好，尤其是",
            "while preserving flexibility.": "同时保留灵活性。",
            "Costs accepted:": "接受的成本：",
            "requires monitoring, ownership, and delayed full protection rather than a one-step defensive move.": "需要持续监测、明确负责人，并接受保护不会一步到位，而不是立即采取全面防御行动。",
            "Why 方案 A does not rank first:": "为什么方案 A 不是首选：",
            "keeps costs low, but it can leave the user underprepared on": "成本较低，但可能让使用者在以下因素上准备不足：",
            "Why 方案 C does not rank first:": "为什么方案 C 不是首选：",
            "offers more protection, but it can impose high opportunity cost before evidence on": "保护力度更高，但在以下证据足够明确前，可能带来过高机会成本：",
            "is strong enough.": "已经足够强。",
            "What would change the ranking: stronger evidence that the high-importance criteria are either clearly immaterial or clearly severe.": "什么会改变排序：如果更强证据表明高重要性因素要么明显不重要、要么已经明显严重，就应重新排序。",
            "1. Option B": "1. 方案 B",
            "2. Option A": "2. 方案 A",
            "3. Option C": "3. 方案 C",
            "Option A": "方案 A",
            "Option B": "方案 B",
            "Option C": "方案 C",
            "These are the dimensions driving today's decision:": "以下因素决定今天应如何判断：",
            "Importance: High": "重要性：高",
            "Importance: Medium": "重要性：中",
            "Importance: Low": "重要性：低",
            "Customer exposure": "客户暴露度",
            "customer exposure": "客户暴露度",
            "Licensing uncertainty": "许可不确定性",
            "licensing uncertainty": "许可不确定性",
            "Compliance burden": "合规负担",
            "compliance burden": "合规负担",
            "Margin impact": "利润率影响",
            "margin impact": "利润率影响",
            "Supply chain resilience": "供应链韧性",
            "supply chain resilience": "供应链韧性",
            "Jurisdiction concentration": "司法辖区集中度",
            "Liquidity": "流动性",
            "Opportunity cost": "机会成本",
            "Execution complexity": "执行复杂度",
            "Flexibility": "灵活性",
            "Review discipline": "复盘纪律",
            "Net return after costs": "扣除成本后的净回报",
            "FX exposure": "汇率暴露",
            "Alternative simplicity": "替代方案简洁度",
            "Product suitability evidence": "产品适配性证据",
            "Benefits gained": "得到什么",
            "Costs accepted": "接受什么成本",
            "Opportunities sacrificed": "放弃什么机会",
            "Risks still unresolved": "尚未解决的风险",
            "Immediate": "立即",
            "Next 30 Days": "未来 30 天",
            "Next Quarter": "下一季度",
            "Investor": "投资者",
            "Corporate Strategy": "企业战略",
            "Supply Chain": "供应链",
            "Policy": "政策",
            "Input document or question text.": "输入文档或用户问题。",
            "Local historical analogue records.": "本地历史相似案例记录。",
            "Local historical outcome records.": "本地历史结果记录。",
            "Deterministic event-family understanding rules.": "确定性的事件类型识别规则。",
            "在以下方面较弱： 客户暴露度, 许可不确定性, 利润率影响 如果当前暴露已经实质化。": "如果当前暴露已经实质化，它在客户暴露度、许可不确定性和利润率影响方面较弱。",
            "在 客户暴露度, 许可不确定性, 利润率影响 因为它把不确定性转化为暴露度清单和复盘节奏。": "在客户暴露度、许可不确定性和利润率影响方面表现较强，因为它把不确定性转化为暴露度清单和复盘节奏。",
            "在 immediate protection if 客户暴露度 已经严重，则即时保护效果较强。": "如果客户暴露度已经严重，它的即时保护效果较强。",
            "在以下方面较弱： execution complexity, reversibility, and sacrificed upside.": "在执行复杂度、可逆性和放弃的上行空间方面较弱。",
            "如果 客户暴露度 无法快速评估，就难以满足高重要性判断因素。": "如果客户暴露度无法快速评估，就难以满足高重要性判断因素。",
            "只有当证据显示 客户暴露度 已经形成约束或继续恶化时，才比方案 B 更符合高重要性判断因素。": "只有当证据显示客户暴露度已经形成约束或继续恶化时，才比方案 B 更符合高重要性判断因素。",
        }
    return {
        "**Current Position:**": "**目前建議：**",
        "**Confidence:**": "**信心等級：**",
        "**Why:**": "**判斷依據：**",
        "**Next 30-90 Days:**": "**未來 30-90 天：**",
        "**Path:**": "**路徑：**",
        "**Pros**": "**優點**",
        "**Cons**": "**不足**",
        "**Criteria Fit**": "**與判斷因素的符合程度**",
        "**Case:**": "**案例：**",
        "**Why it supports the recommendation:**": "**為什麼支持目前建議：**",
        "**Key limitation:**": "**關鍵限制：**",
        "**Decision lesson:**": "**決策啟示：**",
        "**Why this case does not fully apply:**": "**為什麼不能直接套用：**",
        "**Initial / mainstream expectation:**": "**最初 / 主流預期：**",
        "**Market or user behavior:**": "**市場或使用者行為：**",
        "**Actual observed outcome:**": "**實際觀察結果：**",
        "**Expectation gap:**": "**預期差：**",
        "**Lesson:**": "**啟示：**",
            "### Option A": "### 方案 A",
            "### Option B (Recommended)": "### 方案 B（建議）",
            "### Option C": "### 方案 C",
            "Wait for final rule detail before changing operations": "等待最終規則細節，再決定是否調整營運",
            "Map exposure and prepare staged adjustments": "梳理暴露度，並準備階段性調整",
            "Immediately reduce exposed customers, suppliers, or product lines": "立即減少受影響的客戶、供應商或產品線",
            "Lowest immediate effort.": "短期投入最低。",
            "Preserves current posture while more evidence arrives.": "在更多證據出現前保留現有安排。",
            "Risk can accumulate if exposure is already material.": "如果暴露度已經較高，風險可能繼續累積。",
            "May delay preparation if the issue moves quickly.": "如果事件發展很快，準備工作可能滯後。",
            "Best balance between preparation and flexibility.": "在提前準備和保留靈活性之間較平衡。",
            "Creates useful information before irreversible action.": "在採取不可逆行動前，先形成有用的資訊基礎。",
            "Requires active monitoring and ownership.": "需要明確負責人，並持續追蹤。",
            "Does not eliminate exposure immediately.": "不能立即消除全部暴露。",
            "Highest immediate risk reduction.": "短期風險降低幅度最大。",
            "Useful if exposure is already severe or binding.": "如果暴露已經嚴重或約束已經生效，這一路徑更有用。",
            "Highest opportunity cost and execution burden.": "機會成本和執行負擔最高。",
            "Hardest to reverse if the issue proves temporary.": "如果問題後來被證明只是短期擾動，這一路徑最難撤回。",
            "Strong on low execution burden and near-term opportunity cost.": "在降低執行負擔和短期機會成本方面表現較強。",
            "Strong on": "在",
            "Weak on": "在以下方面較弱：",
            "if current exposure is already material.": "如果目前暴露已經實質化。",
            "Fails high-importance criteria when": "如果",
            "cannot be assessed quickly.": "無法快速評估，就難以滿足高重要性判斷因素。",
            "because it converts uncertainty into an exposure map and review cadence.": "因為它把不確定性轉化為暴露度清單和複盤節奏。",
            "Medium on immediate protection because it prepares response options before using them.": "即時保護程度中等，因為它先準備應對方案，再決定是否啟用。",
            "Best overall fit when high-importance criteria are serious but not yet fully resolved.": "當高重要性因素已經值得重視、但尚未完全明朗時，它的整體匹配度最高。",
            "Strong on immediate protection if": "如果",
            "is already severe.": "已經嚴重，則即時保護效果較強。",
            "Weak on execution complexity, reversibility, and sacrificed upside.": "在執行複雜度、可逆性和放棄的上行空間方面較弱。",
            "Only fits the high-importance criteria better than Option B if evidence shows": "只有當證據顯示",
            "Only fits the high-importance criteria better than 方案 B if evidence shows": "只有當證據顯示",
            "is binding or worsening.": "已經形成約束或繼續惡化時，才比方案 B 更符合高重要性判斷因素。",
            "Ranks first because the highest-importance criteria are": "排名第一，因為最高重要性的判斷因素是",
            "It improves readiness on those criteria without creating the execution burden of Option C or the underpreparedness of Option A.": "它能提升這些維度上的準備度，同時避免方案 C 的執行負擔和方案 A 的準備不足。",
            "It improves readiness on those criteria without creating the execution burden of 方案 C or the underpreparedness of 方案 A.": "它能提升這些維度上的準備度，同時避免方案 C 的執行負擔和方案 A 的準備不足。",
            "Ranks second because it has lower cost and disruption than Option C, but it is weaker than Option B on": "排名第二，因為它比方案 C 成本和擾動更低，但在以下因素上弱於方案 B：",
            "Ranks second because it has lower cost and disruption than 方案 C, but it is weaker than 方案 B on": "排名第二，因為它比方案 C 成本和擾動更低，但在以下因素上弱於方案 B：",
            "if exposure grows.": "如果暴露度上升。",
            "Ranks third because it offers more protection, but it is weaker on reversibility, opportunity cost, and execution burden unless": "排名第三，因為它保護力度更強，但除非",
            "Option B currently ranks first": "方案 B 目前排名第一",
            "It ranks first because": "它排名第一，是因為",
            "Top criteria driving the recommendation:": "推動目前建議的核心判斷因素：",
            "Why 方案 B ranks first:": "為什麼方案 B 排名第一：",
            "it performs best on the criteria that matter most for this decision, especially": "它在本次決策最重要的因素上表現最好，尤其是",
            "while preserving flexibility.": "同時保留靈活性。",
            "Costs accepted:": "接受的成本：",
            "requires monitoring, ownership, and delayed full protection rather than a one-step defensive move.": "需要持續監測、明確負責人，並接受保護不會一步到位，而不是立即採取全面防禦行動。",
            "Why 方案 A does not rank first:": "為什麼方案 A 不是首選：",
            "keeps costs low, but it can leave the user underprepared on": "成本較低，但可能讓使用者在以下因素上準備不足：",
            "Why 方案 C does not rank first:": "為什麼方案 C 不是首選：",
            "offers more protection, but it can impose high opportunity cost before evidence on": "保護力度更高，但在以下證據足夠明確前，可能帶來過高機會成本：",
            "is strong enough.": "已經足夠強。",
            "What would change the ranking: stronger evidence that the high-importance criteria are either clearly immaterial or clearly severe.": "什麼會改變排序：如果更強證據表明高重要性因素要麼明顯不重要、要麼已經明顯嚴重，就應重新排序。",
            "1. Option B": "1. 方案 B",
        "2. Option A": "2. 方案 A",
        "3. Option C": "3. 方案 C",
        "Option A": "方案 A",
        "Option B": "方案 B",
        "Option C": "方案 C",
        "These are the dimensions driving today's decision:": "以下因素決定今天應如何判斷：",
        "Importance: High": "重要性：高",
        "Importance: Medium": "重要性：中",
        "Importance: Low": "重要性：低",
            "Customer exposure": "客戶暴露度",
            "customer exposure": "客戶暴露度",
            "Licensing uncertainty": "許可不確定性",
            "licensing uncertainty": "許可不確定性",
            "Compliance burden": "合規負擔",
            "compliance burden": "合規負擔",
            "Margin impact": "利潤率影響",
            "margin impact": "利潤率影響",
            "Supply chain resilience": "供應鏈韌性",
            "supply chain resilience": "供應鏈韌性",
        "Jurisdiction concentration": "司法轄區集中度",
        "Liquidity": "流動性",
        "Opportunity cost": "機會成本",
        "Execution complexity": "執行複雜度",
        "Flexibility": "靈活性",
        "Review discipline": "複盤紀律",
        "Net return after costs": "扣除成本後的淨回報",
        "FX exposure": "匯率暴露",
        "Alternative simplicity": "替代方案簡潔度",
        "Product suitability evidence": "產品適配性證據",
        "Benefits gained": "得到什麼",
        "Costs accepted": "接受什麼成本",
        "Opportunities sacrificed": "放棄什麼機會",
        "Risks still unresolved": "尚未解決的風險",
        "Immediate": "立即",
        "Next 30 Days": "未來 30 天",
        "Next Quarter": "下一季",
        "Investor": "投資者",
        "Corporate Strategy": "企業策略",
        "Supply Chain": "供應鏈",
        "Policy": "政策",
        "Input document or question text.": "輸入文件或使用者問題。",
        "Local historical analogue records.": "本地歷史相似案例紀錄。",
        "Local historical outcome records.": "本地歷史結果紀錄。",
            "Deterministic event-family understanding rules.": "確定性的事件類型識別規則。",
            "在以下方面較弱： 客戶暴露度, 許可不確定性, 利潤率影響 如果目前暴露已經實質化。": "如果目前暴露已經實質化，它在客戶暴露度、許可不確定性和利潤率影響方面較弱。",
            "在 客戶暴露度, 許可不確定性, 利潤率影響 因為它把不確定性轉化為暴露度清單和複盤節奏。": "在客戶暴露度、許可不確定性和利潤率影響方面表現較強，因為它把不確定性轉化為暴露度清單和複盤節奏。",
            "在 immediate protection if 客戶暴露度 已經嚴重，則即時保護效果較強。": "如果客戶暴露度已經嚴重，它的即時保護效果較強。",
            "在以下方面較弱： execution complexity, reversibility, and sacrificed upside.": "在執行複雜度、可逆性和放棄的上行空間方面較弱。",
            "如果 客戶暴露度 無法快速評估，就難以滿足高重要性判斷因素。": "如果客戶暴露度無法快速評估，就難以滿足高重要性判斷因素。",
            "只有當證據顯示 客戶暴露度 已經形成約束或繼續惡化時，才比方案 B 更符合高重要性判斷因素。": "只有當證據顯示客戶暴露度已經形成約束或繼續惡化時，才比方案 B 更符合高重要性判斷因素。",
        }


def _localize_chinese_body(text: str, language: str) -> str:
    localized = text
    for source, target in _chinese_replacements(language).items():
        localized = localized.replace(source, target)
    return localized


def _render_chinese_output(markdown_text: str, mode: str, language: str) -> str:
    """Render the same decision architecture in Chinese.

    The section order and card structure mirror the English analyst output. Only
    headings and recurring decision terms are localized.
    """
    sections = _section_map(markdown_text)
    headings = CHINESE_SECTION_HEADINGS[language]
    lines = [f"# {MODE_TITLES[mode][language]}", "", f"> {LANGUAGE_NOTES[language]}", ""]
    for section in CHINESE_ORDER:
        body = sections.get(section)
        if not body:
            continue
        lines.extend([f"## {headings[section]}", ""])
        lines.append(_localize_chinese_body(body, language))
        lines.append("")
    if len(lines) <= 4:
        return translate_text(localize_knowledge_text(markdown_text.strip(), language), language).strip() + "\n"
    return "\n".join(lines).strip() + "\n"


def adapt_file(input_path: str | Path, output_path: str | Path, mode: str, language: str) -> Path:
    """Adapt an existing Markdown brief and write it to disk."""
    source = Path(input_path)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(adapt_output(source.read_text(encoding="utf-8"), mode, language), encoding="utf-8")
    return destination
