const localeText = {
  en: {
    appTitle: "Strategic Intelligence Agent",
    workbenchLabel: "Analyst Workbench",
    uploadInstructions: "Upload .md/.txt",
    pasteInstructions: "Paste document text",
    helperText: "No prompt writing needed. Choose a question and paste your text.",
    documentTextLabel: "Document text",
    questionTypeLabel: "Question type",
    outputModeLabel: "Output mode",
    languageLabel: "Language",
    beginnerMode: "Beginner",
    analystMode: "Analyst",
    executiveMode: "Executive",
    runAnalysis: "Run Analysis",
    exportMarkdown: "Export Markdown",
    exportTxt: "Export TXT",
    exportNote: "Exports download locally. For repository demos, save exported files into outputs/.",
    documentSummary: "Document Summary",
    scenarioClassification: "Scenario Classification",
    historicalAnalogues: "Historical Analogues",
    currentContext: "Current Context",
    implications: "Implications",
    mechanisms: "Mechanisms",
    interpretations: "Interpretations",
    historicalResponses: "Historical Responses",
    evidenceAssessment: "Evidence Assessment",
    executiveBrief: "Executive Brief",
    limitations: "Limitations",
    selectedTools: "Selected Tools",
    executionTrace: "Execution Trace",
    analysisPath: "Analysis Path",
    disclaimer: "Decision-support only. No forecasts, probabilities, trading advice, or investment recommendations.",
    errorEmptyInput: "Paste or upload a document to analyze.",
  },
  "zh-CN": {
    appTitle: "战略情报代理",
    workbenchLabel: "分析工作台",
    uploadInstructions: "上传 .md/.txt",
    pasteInstructions: "粘贴文档文本",
    helperText: "不用会写提示词。选择一个问题，然后贴上文字。",
    documentTextLabel: "文档文本",
    questionTypeLabel: "问题类型",
    outputModeLabel: "输出模式",
    languageLabel: "语言",
    beginnerMode: "入门",
    analystMode: "分析师",
    executiveMode: "高管",
    runAnalysis: "开始分析",
    exportMarkdown: "导出 Markdown",
    exportTxt: "导出 TXT",
    exportNote: "导出文件会下载到本地。用于仓库演示时，可保存到 outputs/。",
    documentSummary: "文档摘要",
    scenarioClassification: "情境分类",
    historicalAnalogues: "历史类比",
    currentContext: "当前背景",
    implications: "影响分析",
    mechanisms: "机制",
    interpretations: "多种解释",
    historicalResponses: "历史应对模式",
    evidenceAssessment: "证据评估",
    executiveBrief: "高管情报简报",
    limitations: "限制",
    selectedTools: "已选择工具",
    executionTrace: "执行轨迹",
    analysisPath: "分析路径",
    disclaimer: "仅用于决策支持。不提供预测、概率、交易建议或投资建议。",
    errorEmptyInput: "请粘贴或上传需要分析的文档。",
  },
  "zh-TW": {
    appTitle: "策略情報代理",
    workbenchLabel: "分析工作台",
    uploadInstructions: "上傳 .md/.txt",
    pasteInstructions: "貼上文件文字",
    helperText: "不用會寫提示詞。選擇一個問題，然後貼上文字。",
    documentTextLabel: "文件文字",
    questionTypeLabel: "問題類型",
    outputModeLabel: "輸出模式",
    languageLabel: "語言",
    beginnerMode: "入門",
    analystMode: "分析師",
    executiveMode: "高階主管",
    runAnalysis: "開始分析",
    exportMarkdown: "匯出 Markdown",
    exportTxt: "匯出 TXT",
    exportNote: "匯出檔案會下載到本機。用於儲存庫展示時，可保存到 outputs/。",
    documentSummary: "文件摘要",
    scenarioClassification: "情境分類",
    historicalAnalogues: "歷史類比",
    currentContext: "當前背景",
    implications: "影響分析",
    mechanisms: "機制",
    interpretations: "多種解釋",
    historicalResponses: "歷史應對模式",
    evidenceAssessment: "證據評估",
    executiveBrief: "高階主管情報簡報",
    limitations: "限制",
    selectedTools: "已選工具",
    executionTrace: "執行軌跡",
    analysisPath: "分析路徑",
    disclaimer: "僅用於決策支援。不提供預測、機率、交易建議或投資建議。",
    errorEmptyInput: "請貼上或上傳需要分析的文件。",
  },
};

const guidedQuestions = [
  {
    id: "meaning",
    en: "What does this issue mean?",
    "zh-CN": "这件事是什么意思？",
    "zh-TW": "這件事是什麼意思？",
  },
  {
    id: "analogues",
    en: "What past events does this resemble?",
    "zh-CN": "这和过去哪些事件相似？",
    "zh-TW": "這和過去哪些事件相似？",
  },
  {
    id: "mechanisms",
    en: "What mechanisms may be operating?",
    "zh-CN": "可能有哪些机制在发挥作用？",
    "zh-TW": "可能有哪些機制在發揮作用？",
  },
  {
    id: "responses",
    en: "What have actors done in similar situations?",
    "zh-CN": "历史上相关参与者采取过哪些做法？",
    "zh-TW": "歷史上相關參與者採取過哪些做法？",
  },
  {
    id: "affected",
    en: "Who may be affected?",
    "zh-CN": "哪些主体可能受到影响？",
    "zh-TW": "哪些主體可能受到影響？",
  },
  {
    id: "monitor",
    en: "What should I monitor next?",
    "zh-CN": "我应该关注哪些后续变化？",
    "zh-TW": "我應該關注哪些後續變化？",
  },
  {
    id: "interpretations",
    en: "What are competing interpretations?",
    "zh-CN": "有哪些不同解释？",
    "zh-TW": "有哪些不同解釋？",
  },
  {
    id: "limitations",
    en: "What is missing from the evidence?",
    "zh-CN": "证据中还缺少什么？",
    "zh-TW": "證據中還缺少什麼？",
  },
];

const scenarioRules = {
  "Export Controls": ["export control", "entity list", "license", "licensing", "restricted access"],
  "Industrial Policy": ["chips act", "industrial policy", "subsidy", "domestic manufacturing", "incentive"],
  "Sanctions": ["sanctions", "asset freeze", "embargo"],
  "Supply Chain Disruption": ["supply chain", "shipping", "logistics", "shortage", "disruption", "rerouting"],
  "Regulatory Action": ["regulation", "regulatory", "compliance", "rule", "enforcement"],
  "Military / Security Shock": ["military", "security", "red sea", "strait", "conflict"],
  "Earnings / Corporate Disclosure": ["earnings", "guidance", "quarter", "margin", "revenue", "disclosure", "deposit"],
  "Strategic Investment": ["investment", "capex", "facility", "plant", "partnership"],
  "Trade Policy": ["tariff", "trade", "customs", "import"],
};

const historicalCases = [
  { title: "CHIPS and Science Act", source: "Historical Database", scenario: "Industrial Policy", relevance: "shares characteristics with subsidy-backed semiconductor capacity planning" },
  { title: "Huawei Entity List", source: "Historical Database", scenario: "Export Controls", relevance: "may resemble technology-access restrictions and compliance screening" },
  { title: "Russia Sanctions After Ukraine Invasion", source: "Historical Database", scenario: "Sanctions", relevance: "shares characteristics with sanctions-driven counterparty review" },
  { title: "COVID Supply Chain Disruption", source: "Historical Database", scenario: "Supply Chain Disruption", relevance: "may resemble supplier continuity and logistics stress" },
  { title: "Red Sea Shipping Disruption", source: "Historical Database", scenario: "Supply Chain Disruption", relevance: "shares characteristics with route disruption and delivery monitoring" },
  { title: "Major Earnings Guidance Withdrawal During COVID", source: "Historical Database", scenario: "Earnings / Corporate Disclosure", relevance: "may resemble disclosure under operational uncertainty" },
];

const contextFindings = [
  { industry: "Semiconductors", source: "Context Knowledge Base", keywords: ["semiconductor", "chips", "ai", "fabrication"], text: "Semiconductor strategy requires monitoring licensing, supplier concentration, fabrication capacity, and government incentive requirements." },
  { industry: "Banking", source: "Context Knowledge Base", keywords: ["bank", "deposit", "credit", "liquidity", "capital"], text: "Banking analysis often requires monitoring deposit trends, credit quality, liquidity planning, regulatory engagement, and capital levels." },
  { industry: "Supply Chain", source: "Context Knowledge Base", keywords: ["supply chain", "shipping", "logistics", "inventory", "supplier"], text: "Supply chain disruptions can affect routing, lead times, inventory planning, supplier communication, and customer commitments." },
  { industry: "Trade Policy", source: "Context Knowledge Base", keywords: ["trade", "tariff", "customs", "export control", "sanctions"], text: "Trade policy context requires monitoring customs rules, sanctions lists, control lists, eligibility rules, and compliance guidance." },
  { industry: "Energy", source: "Context Knowledge Base", keywords: ["energy", "oil", "gas", "battery", "grid"], text: "Energy context can involve sanctions, industrial incentives, shipping chokepoints, permitting, and equipment lead times." },
];

const mechanisms = [
  { name: "Technology Containment", keywords: ["export control", "chips", "semiconductor", "cloud"], observation: "sensitive technology access is being limited or reviewed" },
  { name: "Strategic Dependency", keywords: ["supplier", "semiconductor", "supply chain", "fabrication"], observation: "operating exposure depends on concentrated suppliers or jurisdictions" },
  { name: "Supply Chain Reconfiguration", keywords: ["supply chain", "shipping", "logistics", "rerouting"], observation: "routes, suppliers, or inventory planning may need review" },
  { name: "Capital Constraint", keywords: ["earnings", "margin", "deposit", "liquidity", "capital"], observation: "financial or operating flexibility is constrained" },
  { name: "Industrial Subsidy", keywords: ["chips act", "subsidy", "incentive", "domestic manufacturing"], observation: "public incentives shape business decisions" },
  { name: "Regulatory Shock", keywords: ["regulatory", "compliance", "rule", "enforcement"], observation: "compliance obligations or oversight are changing" },
];

let currentBrief = "";
let currentLanguage = "en";
let currentMode = "analyst";
let currentQuestion = guidedQuestions[0];

function textIncludes(text, keyword) {
  return text.toLowerCase().includes(keyword.toLowerCase());
}

function t(key) {
  return localeText[currentLanguage][key] || localeText.en[key] || key;
}

function populateGuidedQuestions() {
  const select = document.getElementById("question-select");
  const buttons = document.getElementById("guided-question-buttons");
  select.innerHTML = "";
  buttons.innerHTML = "";

  guidedQuestions.forEach((question) => {
    const option = document.createElement("option");
    option.value = question.id;
    option.textContent = question[currentLanguage];
    select.appendChild(option);

    const button = document.createElement("button");
    button.type = "button";
    button.className = question.id === currentQuestion.id ? "guided-button active" : "guided-button";
    button.textContent = question[currentLanguage];
    button.addEventListener("click", () => {
      currentQuestion = question;
      select.value = question.id;
      populateGuidedQuestions();
      runAnalysis();
    });
    buttons.appendChild(button);
  });
  select.value = currentQuestion.id;
}

function applyLocale() {
  document.documentElement.lang = currentLanguage;
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  document.getElementById("helper-text").textContent = t("helperText");
  populateGuidedQuestions();
}

function classifyScenario(text) {
  let best = { scenario: "Other", matches: [] };
  for (const [scenario, keywords] of Object.entries(scenarioRules)) {
    const matches = keywords.filter((keyword) => textIncludes(text, keyword));
    if (matches.length > best.matches.length) {
      best = { scenario, matches };
    }
  }
  const confidence = best.matches.length >= 3 ? "High" : best.matches.length >= 1 ? "Medium" : "Low";
  return { ...best, confidence };
}

function summarizeDocument(text) {
  const clean = text.trim().replace(/\s+/g, " ");
  return clean.slice(0, 420) + (clean.length > 420 ? "..." : "");
}

function extractEntities(text) {
  const industries = ["semiconductor", "banking", "supply chain", "shipping", "energy", "trade policy", "AI", "cloud"].filter((item) => textIncludes(text, item));
  const policyTerms = ["export control", "industrial policy", "sanctions", "CHIPS Act", "tariff", "regulatory", "compliance"].filter((item) => textIncludes(text, item));
  return { industries, policyTerms };
}

function retrieveAnalogues(classification) {
  const exact = historicalCases.filter((item) => item.scenario === classification.scenario);
  const fallback = historicalCases.filter((item) => item.scenario !== classification.scenario);
  return [...exact, ...fallback].slice(0, 3);
}

function retrieveContext(text) {
  const matches = contextFindings.filter((item) => item.keywords.some((keyword) => textIncludes(text, keyword)));
  return (matches.length ? matches : contextFindings).slice(0, 3);
}

function detectMechanisms(text) {
  const matches = mechanisms.filter((item) => item.keywords.some((keyword) => textIncludes(text, keyword)));
  return (matches.length ? matches : mechanisms.slice(0, 2)).slice(0, 4);
}

function buildInterpretations(classification, detectedMechanisms) {
  const mechanismText = detectedMechanisms.map((item) => item.name).join(", ") || "detected mechanisms";
  return [
    { lens: "Economics", hypothesis: `One possible interpretation is that the ${classification.scenario} issue reflects resource allocation constraints linked to ${mechanismText}.` },
    { lens: "Political Economy", hypothesis: `One possible interpretation is that public authority and business incentives are interacting through ${mechanismText}.` },
    { lens: "International Relations", hypothesis: "One possible interpretation is that cross-border strategic positioning is part of the event context." },
    { lens: "Legislative / Regulatory", hypothesis: "One possible interpretation is that implementation rules and compliance obligations are central to the event." },
    { lens: "Business Strategy", hypothesis: "One possible interpretation is that executives face a resilience and positioning question." },
  ];
}

function buildEvidenceAssessment(interpretations) {
  return interpretations.map((item) => ({
    lens: item.lens,
    confidence: "Moderate",
    supporting: "Source document, retrieved analogues, and context records provide partial support.",
    missing: "Primary-source details and stakeholder-specific exposure remain missing.",
  }));
}

function routeTools(text, classification, entities) {
  const selected = ["IssueExtractor", "ScenarioClassifier", "HistoricalRetriever"];
  const skipped = [];
  const isEarningsOnly = classification.scenario === "Earnings / Corporate Disclosure"
    && !["regulatory", "compliance", "supply chain", "export control", "sanctions"].some((keyword) => textIncludes(text, keyword));

  if (isEarningsOnly) {
    skipped.push("ContextRetriever");
  } else {
    selected.push("ContextRetriever");
  }
  selected.push("ImplicationAnalyzer", "BriefGenerator");

  const trace = [
    `Scenario detected: ${classification.scenario}`,
    `Document signals: ${entities.industries.join(", ") || "general strategic note"}`,
    "Tool selected: IssueExtractor because source text must be structured.",
    "Tool selected: ScenarioClassifier because retrieval needs a scenario frame.",
    "Tool selected: HistoricalRetriever because analogues support comparison.",
    skipped.includes("ContextRetriever")
      ? "Tool skipped: ContextRetriever because the route is focused on corporate disclosure interpretation."
      : "Tool selected: ContextRetriever because domain context is relevant.",
    "Tool selected: ImplicationAnalyzer because selected evidence must be synthesized.",
    "Tool selected: BriefGenerator because the deliverable is an executive brief.",
  ];

  const decisions = selected.map((tool) => ({ tool, decision: "Selected" }))
    .concat(skipped.map((tool) => ({ tool, decision: "Skipped" })));
  return { selected, skipped, trace, decisions };
}

function buildBrief(text, classification, entities, analogues, contexts, route, detectedMechanisms, interpretations, assessments) {
  const analogueLines = analogues.map((item) => `- ${item.title}: ${item.relevance} (Source: ${item.source})`).join("\n");
  const contextLines = contexts.map((item) => `- ${item.industry}: ${item.text} (Source: ${item.source})`).join("\n");
  const traceLines = route.trace.map((item, index) => `${index + 1}. ${item}`).join("\n");
  const decisionLines = route.decisions.map((item) => `- ${item.tool}: ${item.decision}`).join("\n");
  const mechanismLines = detectedMechanisms.map((item) => `- ${item.name}: ${item.observation}`).join("\n");
  const interpretationLines = interpretations.map((item) => `- ${item.lens}: ${item.hypothesis}`).join("\n");
  const assessmentLines = assessments.map((item) => `- ${item.lens}: ${item.confidence}. ${item.supporting}`).join("\n");
  return `# Executive Intelligence Brief

${t("disclaimer")}

## Guided Question

- Question: ${currentQuestion[currentLanguage]}
- Output mode: ${currentMode}
- Language: ${currentLanguage}
- Source: User selection

## Executive Summary

- The document describes a ${classification.scenario} issue.
- Historical analogues and current context are used for comparison, not prediction.
- Evidence references identify source origins.

## Agent Execution Trace

${traceLines}

## Tool Decisions

${decisionLines}

## Analysis Path

- Agent Router reviewed document type, scenario, industries, actors, and keywords.
- Tool Registry exposed available analysis tools.
- Selected tools executed before result synthesis.

## Key Issue

${summarizeDocument(text)}

Source: Input Document

## Scenario Classification

- Primary scenario: ${classification.scenario}
- Matched keywords: ${classification.matches.join(", ") || "None"}
- Classification confidence: ${classification.confidence}
- Source: Input Document

## Extracted Entities

- Industries: ${entities.industries.join(", ") || "None detected"}
- Policy terms: ${entities.policyTerms.join(", ") || "None detected"}
- Source: Input Document

## Historical Analogues

${analogueLines}

## Current Context

${contextLines}

## Implications

- The issue may resemble selected historical cases while differing in current actors, timing, and implementation details.
- Current context requires monitoring of stakeholders, operational constraints, and source updates.
- Analysts may separate observed facts from interpretation.

## Competing Interpretations

${interpretationLines}

## Mechanisms Detected

${mechanismLines}

## Evidence Assessment

${assessmentLines}

## Historical Response Patterns

- Organizations have historically reviewed counterparties, suppliers, compliance obligations, and implementation details.
- Observed outcomes varied across cases and are not predictive.

## Monitoring Considerations

- Decision-makers may wish to monitor source updates, implementation details, stakeholder responses, and evidence gaps.

## Strategic Questions

- Which stakeholders are most exposed?
- Which evidence should be verified against primary sources?
- Which current-context findings require continued monitoring?

## Evidence Trace

- Source: Input Document
- Source: Historical Database
- Source: Context Knowledge Base
- Source: Agent Router
- Source: Tool Registry
`;
}

function adaptDashboardOutput(markdownText) {
  if (currentMode === "analyst") {
    return markdownText;
  }
  const bulletLines = markdownText
    .split("\n")
    .filter((line) => line.trim().startsWith("- "))
    .slice(0, currentMode === "beginner" ? 8 : 12)
    .join("\n");
  const title = currentMode === "beginner" ? t("documentSummary") : t("executiveBrief");
  return `# ${title}

${t("disclaimer")}

## ${t("questionTypeLabel")}

- ${currentQuestion[currentLanguage]}

## ${t("currentContext")}

${bulletLines}

## ${t("limitations")}

- This localized display is deterministic and template-based.
- Source: Output Adapter
`;
}

function renderFindingList(element, items, renderItem) {
  element.innerHTML = "";
  if (!items.length) {
    element.innerHTML = '<div class="empty">No findings generated.</div>';
    return;
  }
  for (const item of items) {
    const div = document.createElement("div");
    div.className = "finding";
    div.innerHTML = renderItem(item);
    element.appendChild(div);
  }
}

function runAnalysis() {
  const text = document.getElementById("document-input").value.trim();
  currentMode = document.getElementById("mode-select").value;
  if (!text) {
    document.getElementById("summary-section").innerHTML = `<div class="empty">${t("errorEmptyInput")}</div>`;
    return;
  }
  const classification = classifyScenario(text);
  const entities = extractEntities(text);
  const route = routeTools(text, classification, entities);
  const analogues = retrieveAnalogues(classification);
  const contexts = route.selected.includes("ContextRetriever") ? retrieveContext(text) : [];
  const detectedMechanisms = detectMechanisms(text);
  const interpretations = buildInterpretations(classification, detectedMechanisms);
  const assessments = buildEvidenceAssessment(interpretations);
  const fullBrief = buildBrief(text, classification, entities, analogues, contexts, route, detectedMechanisms, interpretations, assessments);
  currentBrief = adaptDashboardOutput(fullBrief);

  document.getElementById("summary-section").innerHTML = `<p>${summarizeDocument(text)}</p><p><strong>${t("questionTypeLabel")}:</strong> ${currentQuestion[currentLanguage]}</p><p><span class="evidence">Source: Input Document</span></p>`;
  document.getElementById("classification-section").innerHTML = `<ul><li>Primary scenario: ${classification.scenario}</li><li>Matched keywords: ${classification.matches.join(", ") || "None"}</li><li>Confidence: ${classification.confidence}</li></ul><p><span class="evidence">Source: Input Document</span></p>`;
  renderFindingList(document.getElementById("analogues-section"), analogues, (item) => `<h3>${item.title}</h3><p>${item.relevance}</p><span class="evidence">Source: ${item.source}</span>`);
  renderFindingList(document.getElementById("context-section"), contexts, (item) => `<h3>${item.industry}</h3><p>${item.text}</p><span class="evidence">Source: ${item.source}</span>`);
  document.getElementById("implications-section").innerHTML = `<ul><li>The issue may resemble selected historical cases, but differences in current actors and timing require monitoring.</li><li>Current context adds stakeholder and operating constraints that historical analogues alone cannot provide.</li></ul><p><span class="evidence">Source: Synthesis from all evidence</span></p>`;
  document.getElementById("tools-section").innerHTML = `<p><strong>Selected:</strong> ${route.selected.join(", ")}</p><p><strong>Skipped:</strong> ${route.skipped.join(", ") || "None"}</p><p><span class="evidence">Source: Agent Router</span></p>`;
  document.getElementById("trace-section").innerHTML = `<ol>${route.trace.map((item) => `<li>${item}</li>`).join("")}</ol><p><span class="evidence">Source: Agent Router</span></p>`;
  document.getElementById("path-section").innerHTML = `<ul><li>Agent Router evaluated the document and selected tools.</li><li>Tool Registry exposed available tools.</li><li>Selected tools produced evidence and synthesis.</li></ul><p><span class="evidence">Source: Tool Registry</span></p>`;
  renderFindingList(document.getElementById("mechanisms-section"), detectedMechanisms, (item) => `<h3>${item.name}</h3><p>${item.observation}</p><span class="evidence">Source: Mechanism Framework</span>`);
  renderFindingList(document.getElementById("interpretations-section"), interpretations, (item) => `<h3>${item.lens}</h3><p>${item.hypothesis}</p><span class="evidence">Source: Multi-Lens Analysis</span>`);
  renderFindingList(document.getElementById("responses-section"), [{ title: "Monitoring and contingency planning", text: "Observed historical choices include reviewing counterparties, suppliers, compliance obligations, and implementation details." }], (item) => `<h3>${item.title}</h3><p>${item.text}</p><span class="evidence">Source: Response Patterns</span>`);
  renderFindingList(document.getElementById("evidence-assessment-section"), assessments, (item) => `<h3>${item.lens}</h3><p>${item.confidence}: ${item.supporting}</p><p>Missing evidence: ${item.missing}</p><span class="evidence">Source: Evidence Assessor</span>`);
  document.getElementById("brief-section").textContent = currentBrief;
}

function exportBrief(format) {
  if (!currentBrief) {
    runAnalysis();
  }
  const content = format === "txt" ? currentBrief.replace(/^#+\s/gm, "") : currentBrief;
  const type = format === "txt" ? "text/plain" : "text/markdown";
  const blob = new Blob([content], { type });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `strategic_intelligence_brief_${currentLanguage}_${currentMode}.${format}`;
  link.click();
  URL.revokeObjectURL(link.href);
}

document.getElementById("language-select").addEventListener("change", (event) => {
  currentLanguage = event.target.value;
  applyLocale();
  runAnalysis();
});

document.getElementById("question-select").addEventListener("change", (event) => {
  currentQuestion = guidedQuestions.find((question) => question.id === event.target.value) || guidedQuestions[0];
  populateGuidedQuestions();
  runAnalysis();
});

document.getElementById("mode-select").addEventListener("change", (event) => {
  currentMode = event.target.value;
  runAnalysis();
});

document.getElementById("file-input").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  document.getElementById("document-input").value = await file.text();
  runAnalysis();
});

document.getElementById("analyze-button").addEventListener("click", runAnalysis);
document.getElementById("export-md").addEventListener("click", () => exportBrief("md"));
document.getElementById("export-txt").addEventListener("click", () => exportBrief("txt"));

applyLocale();
runAnalysis();
