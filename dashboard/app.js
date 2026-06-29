const API_BASE = window.location.origin.startsWith("http") ? window.location.origin : "http://127.0.0.1:8000";

const localeText = {
  en: {
    appTitle: "Decide what to do next",
    workbenchLabel: "Decision Companion",
    helperText: "Turn source material into a recommendation, confidence view, evidence summary, and monitoring plan before reviewing method details.",
    trustNoteTitle: "Trust boundary",
    trustNoteBody: "Local deterministic rules and curated knowledge files support the brief. Treat outputs as decision-support drafts for human review, not forecasts, legal advice, investment advice, or verified research.",
    flowInput: "1. Frame decision",
    flowEvidence: "2. Review evidence",
    flowDecision: "3. Monitor change",
    resultsTitle: "Decision review",
    decisionBriefTitle: "Recommended Action",
    resultsSubtitle: "Start with what to do, why, confidence, and what to monitor. Supporting evidence and method details stay available below.",
    decisionGroup: "Decision",
    supportGroup: "Supporting material",
    analysisGroup: "Analysis",
    methodsGroup: "Method details",
    settingsGroup: "Brief settings",
    artifactsGroup: "Artifacts",
    downloadsGroup: "Downloads",
    runHistory: "Run History",
    emptyTitle: "Start with a situation",
    emptyBody: "Paste a policy excerpt, earnings note, supply chain update, URL, or internal memo. Ask the decision question you want the brief to address.",
    emptyDecision: "Recommendation, confidence, rationale, risks, and next monitoring window appear first.",
    emptyEvidence: "Evidence summary, historical cases, and decision quality checks appear after the first run.",
    emptyDownloads: "Markdown, TXT, and JSON downloads become available after analysis.",
    loadingTitle: "Building decision brief",
    loadingBody: "Reviewing the input, matching local historical cases, and preparing downloadable artifacts.",
    assistantInputLabel: "Decision question and source material",
    assistantPlaceholder: "What decision does this situation raise?\nWhich historical cases are most similar?\nWhat trade-offs should be considered?\nWhat evidence would change today's recommendation?\n\nPaste an article, policy excerpt, earnings note, URL, or operational update here.",
    documentTextLabel: "Paste document or article here",
    questionInputLabel: "Ask a Question",
    questionPlaceholder: "What does this issue mean? What historical events resemble this? How have organizations responded in similar situations? What should I monitor next?",
    documentPlaceholder: "Paste an article, policy excerpt, earnings note, regulatory update, or supply chain memo here. You can also drag and drop a .txt or .md file into this box.",
    outputModeLabel: "Output mode",
    languageLabel: "Language",
    beginnerMode: "Beginner",
    analystMode: "Analyst",
    executiveMode: "Executive",
    inputModeLabel: "Input Mode",
    pasteTextMode: "Paste Text",
    uploadFileMode: "Upload File",
    pasteLinkMode: "Analyze Link",
    uploadInstructions: "Upload .txt / .md / .markdown / .pdf",
    noFileSelected: "No file selected",
    pdfLimitNote: "PDF support works for text-based PDFs only. Scanned image PDFs are not supported.",
    sourceUrlLabel: "Paste source link",
    sourceUrlPlaceholder: "https://example.com/source-document",
    linkModeNote: "The app will try to fetch readable webpage text. If it cannot, paste the article text or upload a file.",
    urlModeNote: "Paste a full webpage URL in the box to fetch readable article text. If extraction fails, the app will stop and ask for pasted text or a file.",
    stepOne: "STEP 1",
    stepTwo: "STEP 2",
    stepThree: "STEP 3",
    pasteDocumentStep: "Paste Document",
    chooseInputStep: "Upload File / Paste Article / Analyze Link",
    askQuestionStep: "Ask a Question",
    analyzeStep: "Analyze",
    advancedSettings: "Advanced settings and input options",
    advancedNote: "Downloads, run history, and stored artifacts remain available after analysis.",
    pasteModeNote: "Paste mode uses the main document box above.",
    runAnalysis: "Build decision brief",
    exportMarkdown: "Download Markdown",
    exportTxt: "Download TXT",
    currentEventContext: "Current Event Context",
    documentSummary: "Document Summary",
    scenarioClassification: "Scenario Classification",
    historicalAnalogues: "Historical Analogues",
    historicalOutcomes: "Historical Outcomes",
    strategicLessons: "Strategic Lessons",
    currentContext: "Current Context",
    implications: "Implications",
    selectedTools: "Selected Tools",
    executionTrace: "Execution Trace",
    analysisPath: "Analysis Path",
    mechanisms: "Mechanisms",
    interpretations: "Interpretations",
    historicalResponses: "Historical Responses",
    evidenceAssessment: "Evidence Assessment",
    evidenceReview: "Evidence Review",
    evidenceCredibility: "Evidence Credibility",
    analysisTransparency: "Analysis Transparency",
    transparencyNote: "This system uses a rules-based workflow to connect the input document with historical cases, common mechanisms, and strategic lessons. A human analyst should review the result.",
    evaluation: "Evaluation",
    executiveBrief: "Decision Snapshot",
    detailedAnalysis: "Detailed Analysis",
    methodDetails: "Method Details",
    primaryScenario: "Primary scenario",
    matchedKeywords: "Matched keywords",
    confidenceLabel: "Confidence label",
    source: "Source",
    eventType: "Event type",
    primaryActor: "Primary actor",
    secondaryActor: "Secondary actor",
    affectedSectors: "Affected sectors",
    affectedRegions: "Affected regions",
    policyDomain: "Policy domain",
    confidence: "Confidence",
    eventSummary: "Event summary",
    limitations: "Limitations",
    strategicResponse: "Strategic response",
    supportingCases: "Supporting historical cases",
    confidenceDistribution: "Confidence distribution",
    sourceStatusDistribution: "Source status distribution",
    keyLimitations: "Key limitations",
    reviewerNote: "Reviewer note",
    lessonLabel: "Lesson",
    whyItMatters: "Why it matters",
    outcomeLabel: "Outcome",
    observedPattern: "Observed pattern",
    relevantCases: "Relevant cases",
    selected: "Selected",
    skipped: "Skipped",
    none: "None",
    noSummary: "No summary returned.",
    noFindings: "No findings returned for this run.",
    noContext: "No article content was detected. Please paste article text, upload a file, or use a working webpage link.",
    noImplications: "No implications returned.",
    analyzing: "Analyzing...",
    pasteFirst: "Paste text or upload a file first.",
    downloadFirst: "Run an analysis before downloading.",
  },
  "zh-CN": {
    appTitle: "理解战略情境，辅助判断",
    workbenchLabel: "决策辅助工作台",
    helperText: "输入决策问题并添加来源材料。应用会先返回决策简报，再提供支持证据、分析细节和可下载产物。",
    trustNoteTitle: "可信边界",
    trustNoteBody: "本地规则和人工整理的知识文件用于支持简报。输出应作为人工复核的决策辅助草稿，不是预测、法律建议、投资建议或已验证研究。",
    flowInput: "1. 添加情境",
    flowEvidence: "2. 查看证据",
    flowDecision: "3. 判断观察重点",
    resultsTitle: "决策工作区",
    decisionBriefTitle: "决策简报",
    resultsSubtitle: "先看当前建议，再按需要查看支持材料和方法细节。",
    decisionGroup: "决策",
    supportGroup: "支持材料",
    analysisGroup: "分析",
    methodsGroup: "方法细节",
    settingsGroup: "简报设置",
    artifactsGroup: "产物",
    downloadsGroup: "下载",
    runHistory: "运行历史",
    emptyTitle: "先添加一个情境",
    emptyBody: "粘贴政策摘录、财报说明、供应链更新、网址或内部备忘录，并说明你希望简报回答的决策问题。",
    emptyDecision: "决策简报会优先显示在这里。",
    emptyEvidence: "首次运行后会显示支持证据、历史案例和局限性。",
    emptyDownloads: "分析完成后可下载 Markdown、TXT 和 JSON。",
    loadingTitle: "正在生成决策简报",
    loadingBody: "正在读取输入、匹配本地历史案例，并准备可下载产物。",
    assistantInputLabel: "决策问题和来源材料",
    assistantPlaceholder: "这个情境提出了什么决策问题？\n哪些历史案例最相似？\n应考虑哪些取舍？\n哪些证据会改变今天的判断？\n\n在这里粘贴文章、政策摘录、财报说明、网址或运营更新。",
    documentTextLabel: "在这里粘贴文档或文章",
    questionInputLabel: "提问",
    questionPlaceholder: "这件事是什么意思？这和哪些历史事件相似？类似情况下组织如何应对？接下来应关注什么？",
    documentPlaceholder: "在这里粘贴文章、政策摘录、财报说明、监管更新或供应链备忘录。也可以把 .txt 或 .md 文件拖放到此框。",
    outputModeLabel: "输出模式",
    languageLabel: "语言",
    beginnerMode: "入门",
    analystMode: "分析师",
    executiveMode: "高管",
    inputModeLabel: "输入模式",
    pasteTextMode: "粘贴文本",
    uploadFileMode: "上传文件",
    pasteLinkMode: "分析链接",
    uploadInstructions: "上传 .txt / .md / .markdown / .pdf",
    noFileSelected: "未选择文件",
    pdfLimitNote: "PDF 支持仅适用于文本型 PDF；暂不支持扫描图片 PDF。",
    sourceUrlLabel: "粘贴来源链接",
    sourceUrlPlaceholder: "https://example.com/source-document",
    linkModeNote: "应用会尝试读取网页正文；如果无法读取，请粘贴文章文本或上传文件。",
    urlModeNote: "在输入框中粘贴完整网页链接即可尝试读取正文。如果读取失败，应用会停止并要求粘贴文本或上传文件。",
    stepOne: "步骤 1",
    stepTwo: "步骤 2",
    stepThree: "步骤 3",
    pasteDocumentStep: "粘贴文档",
    chooseInputStep: "上传文件 / 粘贴文章 / 分析链接",
    askQuestionStep: "提问",
    analyzeStep: "分析",
    advancedSettings: "高级设置和输入选项",
    advancedNote: "分析完成后仍可使用下载、运行历史和本地保存的产物。",
    pasteModeNote: "粘贴模式使用上方主文档输入框。",
    runAnalysis: "生成决策简报",
    exportMarkdown: "下载 Markdown",
    exportTxt: "下载 TXT",
    currentEventContext: "当前事件背景",
    documentSummary: "文档摘要",
    scenarioClassification: "情境分类",
    historicalAnalogues: "历史相似案例",
    historicalOutcomes: "历史结果",
    strategicLessons: "战略经验",
    currentContext: "当前背景",
    implications: "影响分析",
    selectedTools: "已选择工具",
    executionTrace: "执行轨迹",
    analysisPath: "分析路径",
    mechanisms: "机制",
    interpretations: "多种解释",
    historicalResponses: "历史应对模式",
    evidenceAssessment: "证据评估",
    evidenceReview: "证据审查",
    evidenceCredibility: "证据可信度",
    analysisTransparency: "分析透明度",
    transparencyNote: "本系统使用规则式分析流程，将输入文件连接到历史案例、常见机制与战略经验。结果应由人工分析者复核。",
    evaluation: "评估",
    executiveBrief: "高管简报",
    detailedAnalysis: "详细分析",
    methodDetails: "方法细节",
    primaryScenario: "主要情境",
    matchedKeywords: "匹配关键词",
    confidenceLabel: "置信标签",
    source: "来源",
    eventType: "事件类型",
    primaryActor: "主要参与者",
    secondaryActor: "次要参与者",
    affectedSectors: "受影响行业",
    affectedRegions: "受影响地区",
    policyDomain: "政策领域",
    confidence: "置信标签",
    eventSummary: "事件摘要",
    limitations: "局限性",
    strategicResponse: "战略应对",
    supportingCases: "支持历史案例",
    confidenceDistribution: "置信分布",
    sourceStatusDistribution: "来源状态分布",
    keyLimitations: "主要局限性",
    reviewerNote: "审阅说明",
    lessonLabel: "经验",
    whyItMatters: "为什么重要",
    outcomeLabel: "结果",
    observedPattern: "观察到的模式",
    relevantCases: "相关案例",
    selected: "已选择",
    skipped: "已跳过",
    none: "无",
    noSummary: "未返回摘要。",
    noFindings: "本次运行未返回发现。",
    noContext: "未检测到文章内容。请粘贴文章文本、上传文件，或使用可读取的网页链接。",
    noImplications: "未返回影响分析。",
    analyzing: "分析中...",
    pasteFirst: "请先粘贴文本或上传文件。",
    downloadFirst: "请先运行一次分析再下载。",
  },
  "zh-TW": {
    appTitle: "理解策略情境，輔助判斷",
    workbenchLabel: "決策輔助工作台",
    helperText: "輸入決策問題並加入來源材料。應用會先返回決策簡報，再提供支持證據、分析細節和可下載產物。",
    trustNoteTitle: "可信邊界",
    trustNoteBody: "本地規則和人工整理的知識文件用於支持簡報。輸出應作為人工複核的決策輔助草稿，不是預測、法律建議、投資建議或已驗證研究。",
    flowInput: "1. 加入情境",
    flowEvidence: "2. 查看證據",
    flowDecision: "3. 判斷觀察重點",
    resultsTitle: "決策工作區",
    decisionBriefTitle: "決策簡報",
    resultsSubtitle: "先看目前建議，再按需要查看支持材料和方法細節。",
    decisionGroup: "決策",
    supportGroup: "支持材料",
    analysisGroup: "分析",
    methodsGroup: "方法細節",
    settingsGroup: "簡報設定",
    artifactsGroup: "產物",
    downloadsGroup: "下載",
    runHistory: "執行歷史",
    emptyTitle: "先加入一個情境",
    emptyBody: "貼上政策摘錄、財報說明、供應鏈更新、網址或內部備忘錄，並說明你希望簡報回答的決策問題。",
    emptyDecision: "決策簡報會優先顯示在這裡。",
    emptyEvidence: "首次執行後會顯示支持證據、歷史案例和限制。",
    emptyDownloads: "分析完成後可下載 Markdown、TXT 和 JSON。",
    loadingTitle: "正在產生決策簡報",
    loadingBody: "正在讀取輸入、匹配本地歷史案例，並準備可下載產物。",
    assistantInputLabel: "決策問題和來源材料",
    assistantPlaceholder: "這個情境提出了什麼決策問題？\n哪些歷史案例最相似？\n應考慮哪些取捨？\n哪些證據會改變今天的判斷？\n\n在這裡貼上文章、政策摘錄、財報說明、網址或營運更新。",
    documentTextLabel: "在這裡貼上文件或文章",
    questionInputLabel: "提問",
    questionPlaceholder: "這件事是什麼意思？這和哪些歷史事件相似？類似情況下組織如何應對？接下來應關注什麼？",
    documentPlaceholder: "在這裡貼上文章、政策摘錄、財報說明、監管更新或供應鏈備忘錄。也可以把 .txt 或 .md 檔案拖放到此框。",
    outputModeLabel: "輸出模式",
    languageLabel: "語言",
    beginnerMode: "入門",
    analystMode: "分析師",
    executiveMode: "高階主管",
    inputModeLabel: "輸入模式",
    pasteTextMode: "貼上文字",
    uploadFileMode: "上傳檔案",
    pasteLinkMode: "分析連結",
    uploadInstructions: "上傳 .txt / .md / .markdown / .pdf",
    noFileSelected: "未選擇檔案",
    pdfLimitNote: "PDF 支援僅適用於文字型 PDF；暫不支援掃描圖片 PDF。",
    sourceUrlLabel: "貼上來源連結",
    sourceUrlPlaceholder: "https://example.com/source-document",
    linkModeNote: "應用會嘗試讀取網頁正文；如果無法讀取，請貼上文章文字或上傳檔案。",
    urlModeNote: "在輸入框中貼上完整網頁連結即可嘗試讀取正文。如果讀取失敗，應用會停止並要求貼上文字或上傳檔案。",
    stepOne: "步驟 1",
    stepTwo: "步驟 2",
    stepThree: "步驟 3",
    pasteDocumentStep: "貼上文件",
    chooseInputStep: "上傳檔案 / 貼上文章 / 分析連結",
    askQuestionStep: "提問",
    analyzeStep: "分析",
    advancedSettings: "進階設定和輸入選項",
    advancedNote: "分析完成後仍可使用下載、執行歷史和本地保存的產物。",
    pasteModeNote: "貼上模式使用上方主文件輸入框。",
    runAnalysis: "產生決策簡報",
    exportMarkdown: "下載 Markdown",
    exportTxt: "下載 TXT",
    currentEventContext: "當前事件背景",
    documentSummary: "文件摘要",
    scenarioClassification: "情境分類",
    historicalAnalogues: "歷史相似案例",
    historicalOutcomes: "歷史結果",
    strategicLessons: "策略經驗",
    currentContext: "當前背景",
    implications: "影響分析",
    selectedTools: "已選工具",
    executionTrace: "執行軌跡",
    analysisPath: "分析路徑",
    mechanisms: "機制",
    interpretations: "多種解釋",
    historicalResponses: "歷史應對模式",
    evidenceAssessment: "證據評估",
    evidenceReview: "證據審查",
    evidenceCredibility: "證據可信度",
    analysisTransparency: "分析透明度",
    transparencyNote: "本系統使用規則式分析流程，將輸入文件連結到歷史案例、常見機制與策略經驗。結果應由人工分析者複核。",
    evaluation: "評估",
    executiveBrief: "高階主管簡報",
    detailedAnalysis: "詳細分析",
    methodDetails: "方法細節",
    primaryScenario: "主要情境",
    matchedKeywords: "匹配關鍵字",
    confidenceLabel: "信心標籤",
    source: "來源",
    eventType: "事件類型",
    primaryActor: "主要參與者",
    secondaryActor: "次要參與者",
    affectedSectors: "受影響產業",
    affectedRegions: "受影響地區",
    policyDomain: "政策領域",
    confidence: "信心標籤",
    eventSummary: "事件摘要",
    limitations: "限制",
    strategicResponse: "策略應對",
    supportingCases: "支持歷史案例",
    confidenceDistribution: "信心分布",
    sourceStatusDistribution: "來源狀態分布",
    keyLimitations: "主要限制",
    reviewerNote: "審閱說明",
    lessonLabel: "經驗",
    whyItMatters: "為什麼重要",
    outcomeLabel: "結果",
    observedPattern: "觀察到的模式",
    relevantCases: "相關案例",
    selected: "已選擇",
    skipped: "已跳過",
    none: "無",
    noSummary: "未返回摘要。",
    noFindings: "本次執行未返回發現。",
    noContext: "未偵測到文章內容。請貼上文章文字、上傳檔案，或使用可讀取的網頁連結。",
    noImplications: "未返回影響分析。",
    analyzing: "分析中...",
    pasteFirst: "請先貼上文字或上傳檔案。",
    downloadFirst: "請先執行一次分析再下載。",
  },
};

const sourceLocale = {
  en: {},
  "zh-CN": {
    "Source": "来源",
    "Type": "类型",
    "URL": "链接",
    "Confidence": "置信标签",
    "All Evidence": "全部证据",
    "Tool Registry": "工具注册表",
    "Agent Router": "智能路由",
    "Multi-Lens Analysis": "多维分析",
    "Synthesis": "综合分析",
    "Mechanism Framework": "机制框架",
    "Historical Database": "历史数据库",
    "Historical Outcomes Database": "历史结果数据库",
    "Strategic Lessons Engine": "战略经验引擎",
    "Input Document": "输入文件",
    "Context Knowledge Base": "背景知识库",
    "Evidence Review": "证据审查",
    "Evidence Assessor": "证据评估器",
    "Evidence Credibility Layer": "证据可信度层",
    "Benchmark Framework": "评估框架",
    "Response Patterns": "应对模式",
    "Local App": "本地应用",
    "agent_trace.json": "执行轨迹文件",
    "source pending": "来源待补充",
  },
  "zh-TW": {
    "Source": "來源",
    "Type": "類型",
    "URL": "連結",
    "Confidence": "信心標籤",
    "All Evidence": "全部證據",
    "Tool Registry": "工具註冊表",
    "Agent Router": "智能路由",
    "Multi-Lens Analysis": "多維分析",
    "Synthesis": "綜合分析",
    "Mechanism Framework": "機制框架",
    "Historical Database": "歷史資料庫",
    "Historical Outcomes Database": "歷史結果資料庫",
    "Strategic Lessons Engine": "策略經驗引擎",
    "Input Document": "輸入文件",
    "Context Knowledge Base": "背景知識庫",
    "Evidence Review": "證據審查",
    "Evidence Assessor": "證據評估器",
    "Evidence Credibility Layer": "證據可信度層",
    "Benchmark Framework": "評估框架",
    "Response Patterns": "應對模式",
    "Local App": "本地應用",
    "agent_trace.json": "執行軌跡檔案",
    "source pending": "來源待補充",
  },
};

let currentLanguage = "en";
let currentRun = null;
let currentInputMode = "paste";
let uploadedFilename = "";
let uploadedFileType = "text";

function t(key) {
  return localeText[currentLanguage][key] || localeText.en[key] || key;
}

function isChinese() {
  return currentLanguage === "zh-CN" || currentLanguage === "zh-TW";
}

function sourceLabel(value) {
  return sourceLocale[currentLanguage]?.[value] || value;
}

function sourceBadge(value) {
  return `<span class="evidence">${sourceLabel("Source")}: ${escapeHtml(sourceLabel(value))}</span>`;
}

function applyLocale() {
  document.documentElement.lang = currentLanguage;
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    node.placeholder = t(node.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("[data-source]").forEach((node) => {
    node.textContent = sourceLabel(node.dataset.source);
  });
  document.getElementById("helper-text").textContent = t("helperText");
  applyOutputModeVisibility();
  if (!currentRun) {
    renderEmptyWorkspace();
  }
}

function currentOutputMode() {
  return document.getElementById("mode-select").value;
}

function applyOutputModeVisibility() {
  const beginner = currentOutputMode() === "beginner";
  document.body.classList.toggle("beginner-mode", beginner);
  document.body.classList.toggle("analyst-mode", !beginner);
  document.querySelectorAll(".internal-detail").forEach((node) => {
    node.hidden = beginner;
    if (beginner && node.tagName.toLowerCase() === "details") {
      node.open = false;
    }
  });
  document.querySelectorAll(".beginner-only").forEach((node) => {
    node.hidden = !beginner;
  });
}

async function checkHealth() {
  const status = document.getElementById("api-status");
  try {
    const response = await fetch(`${API_BASE}/health`);
    if (!response.ok) throw new Error("Health check failed");
    status.textContent = "Server connected";
    status.classList.remove("offline");
  } catch (error) {
    status.textContent = "Start FastAPI server";
    status.classList.add("offline");
  }
}

async function analyzeDocument() {
  const assistantValue = document.getElementById("assistant-input").value.trim();
  const parsedInput = parseAssistantInput(assistantValue);
  if (!parsedInput.text && !parsedInput.sourceUrl) {
    setEmpty("summary-section", t("pasteFirst"));
    return;
  }
  const questionText = parsedInput.questionText || t("assistantPlaceholder").split("\n")[0];
  const button = document.getElementById("analyze-button");
  button.disabled = true;
  button.textContent = t("analyzing");
  renderLoadingWorkspace();
  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: parsedInput.text,
        language: currentLanguage,
        output_mode: currentOutputMode(),
        question_id: "freeform",
        question_text: questionText,
        source_url: parsedInput.sourceUrl,
        input_mode: parsedInput.inputMode,
        uploaded_filename: uploadedFilename,
        file_type: uploadedFileType,
      }),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "Analysis failed.");
    }
    currentRun = await response.json();
    renderRun(currentRun);
    await loadHistory();
  } catch (error) {
    setEmpty("summary-section", `Could not run analysis. ${error.message}`);
  } finally {
    button.disabled = false;
    button.textContent = t("runAnalysis");
  }
}

function parseAssistantInput(value) {
  const urlMatch = value.match(/https?:\/\/[^\s)]+/i);
  const sourceUrl = urlMatch ? urlMatch[0].replace(/[.,;]+$/, "") : "";
  const withoutUrl = sourceUrl ? value.replace(sourceUrl, "").trim() : value;
  const isQuestionOnly = withoutUrl.length < 260 && /(\?|what|which|how|why|monitor|compare|meaning|mean)/i.test(withoutUrl);
  if (sourceUrl && withoutUrl.length < 80) {
    return {
      text: "",
      sourceUrl,
      questionText: withoutUrl || "What does this event mean?",
      inputMode: "assistant_url",
    };
  }
  return {
    text: withoutUrl || value,
    sourceUrl,
    questionText: isQuestionOnly ? withoutUrl : "What does this event mean? Which historical cases are most similar? What should I monitor next?",
    inputMode: uploadedFilename ? "assistant_upload" : sourceUrl ? "assistant_text_with_url" : isQuestionOnly ? "assistant_question" : "assistant_text",
  };
}

async function loadHistory() {
  const list = document.getElementById("history-list");
  try {
    const response = await fetch(`${API_BASE}/runs`);
    if (!response.ok) throw new Error("History unavailable");
    const runs = await response.json();
    if (!runs.length) {
      list.innerHTML = '<div class="empty">No saved runs yet.</div>';
      return;
    }
    list.innerHTML = "";
    runs.slice(0, 10).forEach((run) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "history-item";
      button.innerHTML = `<strong>${run.run_id}</strong><span>${run.created_at || ""}</span><span>${run.language} / ${run.output_mode}</span>`;
      button.addEventListener("click", () => openRun(run.run_id));
      list.appendChild(button);
    });
  } catch (error) {
    list.innerHTML = '<div class="empty">Start the local server to view history.</div>';
  }
}

async function openRun(runId) {
  const response = await fetch(`${API_BASE}/run/${runId}`);
  if (!response.ok) {
    setEmpty("summary-section", "Could not open saved run.");
    return;
  }
  currentRun = await response.json();
  renderRun(currentRun);
}

function renderEmptyWorkspace() {
  document.getElementById("brief-section").innerHTML = `
    <article class="empty-workspace">
      <div class="empty-kicker">${escapeHtml(t("decisionGroup"))}</div>
      <h3>${escapeHtml(t("emptyTitle"))}</h3>
      <p>${escapeHtml(t("emptyBody"))}</p>
      <div class="empty-grid">
        <div><strong>${escapeHtml(t("emptyDecision"))}</strong></div>
        <div><strong>${escapeHtml(t("emptyEvidence"))}</strong></div>
        <div><strong>${escapeHtml(t("emptyDownloads"))}</strong></div>
      </div>
    </article>
  `;
}

function renderLoadingWorkspace() {
  document.getElementById("brief-section").innerHTML = `
    <article class="loading-workspace" aria-live="polite">
      <div class="loading-mark" aria-hidden="true"></div>
      <div>
        <h3>${escapeHtml(t("loadingTitle"))}</h3>
        <p>${escapeHtml(t("loadingBody"))}</p>
      </div>
    </article>
  `;
}

function renderRun(run) {
  applyOutputModeVisibility();
  const analysis = run.analysis;
  const metadata = run.metadata;
  const issue = analysis.issue || {};
  const scenario = analysis.scenario || {};
  renderEventContext(analysis.event_context || {});
  document.getElementById("run-note").textContent = `Saved run: ${metadata.run_id}. Artifacts are stored under outputs/runs/${metadata.run_id}/.`;
  if (analysis.message && analysis.source_url) {
    document.getElementById("summary-section").innerHTML = `<p>${escapeHtml(analysis.message)}</p><p><span class="evidence">${t("source")}: ${escapeHtml(analysis.source_url)}</span></p>`;
    document.getElementById("brief-section").innerHTML = renderBriefCards(run.brief_markdown || "");
    return;
  }
  const sourceLink = analysis.source_url ? `<p><span class="evidence">${t("source")}: ${escapeHtml(analysis.source_url)}</span></p>` : "";
  document.getElementById("summary-section").innerHTML = `<p>${escapeHtml(issue.summary || issue.core_issue || t("noSummary"))}</p><p>${sourceBadge("Input Document")}</p>${sourceLink}`;
  document.getElementById("classification-section").innerHTML = `<ul><li>${t("primaryScenario")}: ${escapeHtml(scenario.primary_scenario || "Other")}</li><li>${t("matchedKeywords")}: ${escapeHtml((scenario.matched_keywords || []).join(", ") || t("none"))}</li><li>${t("confidenceLabel")}: ${escapeHtml(scenario.confidence_label || t("none"))}</li></ul><p>${sourceBadge("Input Document")}</p>`;
  renderCards("analogues-section", analysis.analogues || [], (item) => `<h3>${escapeHtml(item.case_title)}</h3><p>${escapeHtml(item.similarity_reason || "")}</p><p>${sourceMeta(item)}</p>`);
  renderCards("outcomes-section", analysis.historical_outcomes || [], renderOutcomeCard);
  renderCards("lessons-section", analysis.strategic_lessons || [], renderLessonCard);
  renderCards("context-section", analysis.current_context || [], renderContextCard);
  renderCards("mechanisms-section", analysis.mechanisms || [], renderMechanismCard);
  renderCards("interpretations-section", analysis.lenses || [], renderInterpretationCard);
  renderCards("responses-section", analysis.response_playbooks || [], (item) => `<h3>${escapeHtml(item.pattern_name)}</h3><p>${escapeHtml((item.observed_historical_choices || []).join(" "))}</p><p>${sourceMeta(item)}</p>`);
  renderCards("evidence-assessment-section", analysis.evidence || [], renderEvidenceAssessmentCard);
  renderEvidenceCredibility(analysis.evidence_credibility || {});
  renderImplications(analysis.implications || []);
  renderTrace(analysis.agent_trace || {});
  document.getElementById("path-section").innerHTML = renderPath();
  document.getElementById("brief-section").innerHTML = renderBriefCards(run.brief_markdown || "", analysis);
}

function parseBriefSections(markdownText) {
  return markdownText
    .replace(/^# .*\n+/, "")
    .split(/\n(?=## )/g)
    .map((section) => section.trim())
    .filter(Boolean)
    .map((section) => {
      const lines = section.split("\n").map((line) => line.trim()).filter(Boolean);
      return {
        title: lines[0].replace(/^#+\s*/, ""),
        lines,
      };
    });
}

function renderBriefCards(markdownText, analysis = {}) {
  const sections = parseBriefSections(markdownText);
  const overview = renderDecisionOverview(sections, analysis);

  const cards = sections.filter(({ title }) => !["Decision Snapshot", "决策快照", "決策快照"].includes(title)).map(({ title, lines }) => {
    const body = renderSectionBody(title, lines.slice(1));
    const sectionClass = briefSectionClass(title);

    return `
      <article class="${sectionClass}">
        <h3>${escapeHtml(title)}</h3>
        ${body}
      </article>
    `;
  }).join("");

  return `${overview}${cards}`;
}

function renderSectionBody(title, lines) {
  if (["Evidence and Confidence", "证据与信心", "證據與信心"].includes(title)) {
    return renderEvidenceConfidenceSection(lines);
  }
  return renderMarkdownLines(lines);
}

function renderEvidenceConfidenceSection(lines) {
  const overviewLines = [];
  const evidenceItems = [];
  const subsections = [];
  let currentItem = null;
  let currentSubsection = null;

  lines.forEach((line) => {
    if (line === "### Evidence Ledger") {
      currentSubsection = null;
      return;
    }
    if (line.startsWith("### ")) {
      if (currentItem) {
        evidenceItems.push(currentItem);
        currentItem = null;
      }
      currentSubsection = { title: line.replace(/^### /, ""), lines: [] };
      subsections.push(currentSubsection);
      return;
    }
    const itemMatch = line.match(/^- \*\*(E\d+)\s+\((.*?)\)\*\*/);
    if (itemMatch) {
      if (currentItem) evidenceItems.push(currentItem);
      currentItem = {
        id: itemMatch[1],
        type: itemMatch[2],
        attributes: [],
      };
      currentSubsection = null;
      return;
    }
    if (currentItem) {
      const attribute = line.match(/^- ([^:]+):\s*(.*)$/);
      if (attribute) {
        currentItem.attributes.push({ label: attribute[1], value: attribute[2] });
      } else if (currentItem.attributes.length) {
        const last = currentItem.attributes[currentItem.attributes.length - 1];
        last.value = `${last.value}\n${line}`.trim();
      }
      return;
    }
    if (currentSubsection) {
      currentSubsection.lines.push(line);
      return;
    }
    overviewLines.push(line);
  });
  if (currentItem) evidenceItems.push(currentItem);

  const overview = renderEvidenceOverview(overviewLines);
  const ledger = evidenceItems.length ? `
    <div class="evidence-ledger-grid">
      ${evidenceItems.map(renderEvidenceLedgerItem).join("")}
    </div>
  ` : "";
  const supporting = subsections.map((section) => `
    <section class="evidence-subsection">
      <h4>${escapeHtml(section.title)}</h4>
      ${renderMarkdownLines(section.lines)}
    </section>
  `).join("");

  return `
    ${overview}
    ${ledger}
    ${supporting ? `<div class="evidence-subsection-grid">${supporting}</div>` : ""}
  `;
}

function renderEvidenceOverview(lines) {
  const values = lines
    .map((line) => line.match(/^\*\*(.*?):\*\*\s*(.*)$/))
    .filter(Boolean)
    .map((match) => ({ label: match[1], value: match[2] }));
  if (!values.length) return "";
  return `
    <div class="evidence-confidence-summary">
      ${values.map((item) => `
        <div>
          <strong>${escapeHtml(item.label)}</strong>
          <p>${formatInline(item.value)}</p>
        </div>
      `).join("")}
    </div>
  `;
}

function renderEvidenceLedgerItem(item) {
  const relevance = item.attributes.find((attribute) => attribute.label === "Relevance");
  const attributes = item.attributes.filter((attribute) => attribute.label !== "Relevance");
  const relevanceText = relevance?.value || "";
  return `
    <article class="evidence-ledger-card">
      <div class="evidence-ledger-header">
        <span>${escapeHtml(item.id)}</span>
        <strong>${escapeHtml(item.type)}</strong>
      </div>
      <div class="evidence-attribute-grid">
        ${attributes.map((attribute) => `
          <div class="evidence-attribute ${attribute.label.toLowerCase().replaceAll(" ", "-")}">
            <strong>${escapeHtml(attribute.label)}</strong>
            <p>${formatInline(attribute.value)}</p>
          </div>
        `).join("")}
      </div>
      ${relevanceText ? `<div class="evidence-meta-row">${renderEvidenceMeta(relevanceText)}</div>` : ""}
    </article>
  `;
}

function renderEvidenceMeta(value) {
  return value.split(";").map((part) => {
    const [label, ...rest] = part.split(":");
    if (!rest.length) return `<span>${escapeHtml(part.trim())}</span>`;
    return `<span><strong>${escapeHtml(label.trim())}</strong> ${escapeHtml(rest.join(":").trim())}</span>`;
  }).join("");
}

function renderDecisionOverview(sections, analysis) {
  const snapshot = briefSection(sections, ["Decision Snapshot", "决策快照", "決策快照"]);
  if (!snapshot) return "";

  const recommendation = sectionField(snapshot, ["Current Position", "当前判断", "目前判斷"]) || firstMeaningfulLine(snapshot);
  const confidence = sectionField(snapshot, ["Confidence", "置信", "信心"]) || analysis.confidence_assessment?.confidence_level || "Not stated";
  const why = sectionField(snapshot, ["Why", "原因"]) || "Review the full brief for rationale.";
  const nextWindow = sectionField(snapshot, ["Next 30-90 Days", "未来 30-90 天", "未來 30-90 天"]) || firstBullet(briefSection(sections, ["What to Monitor", "后续观察重点", "後續觀察重點"]));
  const topRisks = topRiskLines(sections);
  const trustSignals = trustSignalItems(analysis);

  return `
    <article class="decision-overview">
      <div class="overview-main">
        <div class="overview-kicker">Recommended Action</div>
        <h3>${formatInline(recommendation)}</h3>
        <div class="overview-grid">
          <div>
            <strong>Confidence</strong>
            <p>${formatInline(confidence)}</p>
          </div>
          <div>
            <strong>Why this recommendation</strong>
            <p>${formatInline(why)}</p>
          </div>
          <div>
            <strong>Top Risks</strong>
            ${renderCompactList(topRisks)}
          </div>
          <div>
            <strong>Next 30-90 Days</strong>
            <p>${formatInline(nextWindow || "Monitor new evidence that could change the recommendation.")}</p>
          </div>
        </div>
      </div>
      <div class="trust-strip" aria-label="Trust signals">
        ${trustSignals.map((item) => `
          <div>
            <strong>${escapeHtml(item.label)}</strong>
            <span>${escapeHtml(item.value)}</span>
          </div>
        `).join("")}
      </div>
    </article>
  `;
}

function briefSection(sections, titles) {
  return sections.find((section) => titles.includes(section.title));
}

function sectionField(section, labels) {
  if (!section) return "";
  for (const line of section.lines.slice(1)) {
    const match = line.match(/^\*\*(.*?):\*\*\s*(.*)$/);
    if (match && labels.includes(match[1].trim())) {
      return match[2].trim();
    }
  }
  return "";
}

function firstMeaningfulLine(section) {
  if (!section) return "";
  return section.lines.slice(1).find((line) => !line.startsWith("**")) || "";
}

function firstBullet(section) {
  if (!section) return "";
  const line = section.lines.slice(1).find((item) => item.startsWith("- "));
  return line ? line.replace(/^- /, "") : "";
}

function topRiskLines(sections) {
  const tradeoffs = briefSection(sections, ["Trade-offs", "取舍：得到什么、放弃什么、风险还在哪里", "取捨：得到什麼、放棄什麼、風險還在哪裡"]);
  const change = briefSection(sections, ["What Could Change This Recommendation", "哪些新证据会改变今天的判断", "哪些新證據會改變今天的判斷"]);
  const risks = [];
  if (tradeoffs) {
    tradeoffs.lines.slice(1).forEach((line) => {
      if (/risk|风险|風險|wrong|改变|改變/i.test(line)) {
        risks.push(line.replace(/^- /, "").replace(/^\*\*Risks still unresolved:\*\*\s*/, ""));
      }
    });
  }
  if (change && risks.length < 2) {
    change.lines.slice(1).filter((line) => line.startsWith("- ")).slice(0, 2 - risks.length).forEach((line) => {
      risks.push(line.replace(/^- /, ""));
    });
  }
  return risks.slice(0, 2);
}

function renderCompactList(items) {
  if (!items.length) {
    return "<p>Review change triggers and evidence gaps below.</p>";
  }
  return `<ul>${items.map((item) => `<li>${formatInline(item)}</li>`).join("")}</ul>`;
}

function trustSignalItems(analysis) {
  const evidenceCount = analysis.evidence_ledger?.items?.length || 0;
  const analogueCount = analysis.analogues?.length || 0;
  const qualityItems = analysis.decision_quality_evaluation?.dimensions || {};
  const qualityCount = Object.keys(qualityItems).length || 8;
  const confidenceLevel = analysis.confidence_assessment?.confidence_level || "Qualitative";
  return [
    { label: "Evidence Summary", value: evidenceCount ? `${evidenceCount} ledger items` : "Reviewable evidence ledger" },
    { label: "Historical Analogues", value: analogueCount ? `${analogueCount} retrieved cases` : "Local analogue comparison" },
    { label: "Confidence Assessment", value: confidenceLevel },
    { label: "Decision Quality Check", value: `${qualityCount} deterministic checks` },
  ];
}

function briefSectionClass(title) {
  const classes = ["brief-card"];
  const decisionTitles = ["Decision Snapshot", "决策快照", "決策快照"];
  const criteriaTitles = ["Decision Criteria", "最重要的判断因素", "最重要的判斷因素"];
  const choiceTitles = ["Decision Paths", "可行方案"];
  const rankingTitles = ["Option Ranking", "方案排序"];
  const preferredTitles = ["Preferred Path", "目前最佳方案"];
  const assumptionTitles = ["Assumptions", "当前假设", "目前假設"];
  const tradeoffTitles = ["Trade-offs", "取舍：得到什么、放弃什么、风险还在哪里", "取捨：得到什麼、放棄什麼、風險還在哪裡"];
  const changeTitles = ["What Could Change This Recommendation", "哪些新证据会改变今天的判断", "哪些新證據會改變今天的判斷"];
  const actionTitles = ["Action Timeline", "行动时间表", "行動時間表"];
  const monitorTitles = ["What to Monitor", "后续观察重点", "後續觀察重點"];
  const qualityTitles = ["Decision Quality Review"];
  const supportingTitles = [
    "Historical Evidence",
    "Market Expectations vs Actual Outcomes",
    "Evidence Used",
    "Limitations",
    "历史证据",
    "歷史證據",
    "市场预期与实际结果",
    "市場預期與實際結果",
    "使用的证据",
    "使用的證據",
    "限制说明",
    "限制說明",
  ];
  if (decisionTitles.includes(title)) classes.push("decision-card");
  if (criteriaTitles.includes(title)) classes.push("criteria-card");
  if (choiceTitles.includes(title)) classes.push("choices-card");
  if (rankingTitles.includes(title)) classes.push("ranking-card");
  if (preferredTitles.includes(title)) classes.push("recommended-card");
  if (assumptionTitles.includes(title)) classes.push("assumption-card");
  if (tradeoffTitles.includes(title)) classes.push("tradeoff-card");
  if (changeTitles.includes(title)) classes.push("change-card");
  if (actionTitles.includes(title)) classes.push("action-card");
  if (monitorTitles.includes(title)) classes.push("monitor-card");
  if (qualityTitles.includes(title)) classes.push("quality-card");
  if (supportingTitles.includes(title)) {
    classes.push("supporting-card");
  }
  return classes.join(" ");
}

function renderMarkdownLines(lines) {
  let html = "";
  let inList = false;
  let inTable = false;
  lines.forEach((line) => {
    if (!line || /^---+$/.test(line)) return;
    if (line.startsWith("|")) {
      if (!inTable) {
        html += "<table>";
        inTable = true;
      }
      if (/^\|\s*-/.test(line)) return;
      const cells = line.split("|").slice(1, -1).map((cell) => `<td>${formatInline(cell.trim())}</td>`).join("");
      html += `<tr>${cells}</tr>`;
      return;
    }
    if (inTable) {
      html += "</table>";
      inTable = false;
    }
    if (line.startsWith("- ")) {
      if (!inList) {
        html += "<ul>";
        inList = true;
      }
      html += `<li>${formatInline(line.replace(/^- /, ""))}</li>`;
      return;
    }
    if (inList) {
      html += "</ul>";
      inList = false;
    }
    if (line.startsWith("### ")) {
      const heading = line.replace(/^### /, "");
      const className = heading.includes("Recommended") ? ' class="recommended-option"' : "";
      html += `<h4${className}>${formatInline(heading)}</h4>`;
    } else {
      html += `<p>${formatInline(line.replace(/^#+\s*/, ""))}</p>`;
    }
  });
  if (inList) html += "</ul>";
  if (inTable) html += "</table>";
  return html;
}

function formatInline(value) {
  return escapeHtml(value)
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/Importance: High/g, '<span class="importance high">Importance: High</span>')
    .replace(/Importance: Medium/g, '<span class="importance medium">Importance: Medium</span>')
    .replace(/Importance: Low/g, '<span class="importance low">Importance: Low</span>')
    .replace(/重要性：高/g, '<span class="importance high">重要性：高</span>')
    .replace(/重要性：中/g, '<span class="importance medium">重要性：中</span>')
    .replace(/重要性：低/g, '<span class="importance low">重要性：低</span>')
    .replace(/Criteria Fit/g, '<span class="criteria-fit-label">Criteria Fit</span>')
    .replace(/与判断因素的符合程度/g, '<span class="criteria-fit-label">与判断因素的符合程度</span>')
    .replace(/與判斷因素的符合程度/g, '<span class="criteria-fit-label">與判斷因素的符合程度</span>');
}

function renderEventContext(item) {
  const section = document.getElementById("event-context-section");
  if (!item.event_type) {
    section.innerHTML = `<div class="empty">${t("noContext")}</div>`;
    return;
  }
  const sectors = (item.affected_sectors || []).join(", ") || t("none");
  const regions = (item.affected_regions || []).join(", ") || t("none");
  const significance = isChinese()
    ? (currentLanguage === "zh-CN"
      ? "该部分根据输入文档识别事件类型、参与者、行业和政策领域，用于支持后续比较分析。"
      : "該部分根據輸入文件識別事件類型、參與者、產業和政策領域，用於支持後續比較分析。")
    : item.strategic_significance || "";
  const summary = isChinese()
    ? (currentLanguage === "zh-CN"
      ? "事件摘要来自用户提交的文本和本地确定性规则；未执行实时网页检索。"
      : "事件摘要來自使用者提交的文字和本地確定性規則；未執行即時網頁檢索。")
    : item.event_summary || "";
  const limitations = isChinese()
    ? (currentLanguage === "zh-CN"
      ? ["结果依赖输入文本中的明确信号。", "行业、地区和参与者标签可能遗漏细微差别。"]
      : ["結果依賴輸入文字中的明確訊號。", "產業、地區和參與者標籤可能遺漏細微差別。"])
    : item.context_limitations || [];
  section.innerHTML = `
    <div class="context-grid">
      <div><strong>${t("eventType")}</strong><span>${escapeHtml(item.event_type)}</span></div>
      <div><strong>${t("primaryActor")}</strong><span>${escapeHtml(item.primary_actor)}</span></div>
      <div><strong>${t("secondaryActor")}</strong><span>${escapeHtml(item.secondary_actor)}</span></div>
      <div><strong>${t("affectedSectors")}</strong><span>${escapeHtml(sectors)}</span></div>
      <div><strong>${t("affectedRegions")}</strong><span>${escapeHtml(regions)}</span></div>
      <div><strong>${t("policyDomain")}</strong><span>${escapeHtml(item.policy_domain)}</span></div>
      <div><strong>${t("confidence")}</strong><span>${escapeHtml(item.confidence)}</span></div>
    </div>
    <p>${escapeHtml(significance)}</p>
    <p><strong>${t("eventSummary")}:</strong> ${escapeHtml(summary)}</p>
    <h3>${t("limitations")}</h3>
    <ul>${limitations.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>
    <p>${sourceBadge("Input Document")}</p>
  `;
}

function renderEvidenceCredibility(item) {
  const section = document.getElementById("evidence-credibility-section");
  if (!item.evidence_summary) {
    section.innerHTML = '<div class="empty">No evidence credibility note returned for this run.</div>';
    return;
  }
  const summary = isChinese()
    ? (currentLanguage === "zh-CN"
      ? "证据可信度说明用于区分输入文件、本地知识库、历史结果和待补充来源。该说明不代表外部事实核验。"
      : "證據可信度說明用於區分輸入文件、本地知識庫、歷史結果和待補充來源。該說明不代表外部事實核驗。")
    : item.evidence_summary;
  const limitations = isChinese()
    ? (currentLanguage === "zh-CN"
      ? ["部分教育性数据仍标记为来源待补充。", "分数和置信标签仅反映内部规则，不代表现实世界准确率。"]
      : ["部分教育性資料仍標記為來源待補充。", "分數和信心標籤僅反映內部規則，不代表現實世界準確率。"])
    : item.key_limitations || [];
  const reviewer = isChinese()
    ? (currentLanguage === "zh-CN"
      ? "建议由人工分析师复核关键事实、来源和适用性。"
      : "建議由人工分析師複核關鍵事實、來源和適用性。")
    : item.reviewer_note || "";
  section.innerHTML = `
    <p>${escapeHtml(summary)}</p>
    <h3>${t("confidenceDistribution")}</h3>
    ${renderDistribution(item.confidence_distribution || {})}
    <h3>${t("sourceStatusDistribution")}</h3>
    ${renderDistribution(item.source_status_distribution || {})}
    <h3>${t("keyLimitations")}</h3>
    <ul>${limitations.map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>
    <p><span class="evidence">${t("reviewerNote")}</span></p>
    <p>${escapeHtml(reviewer)}</p>
  `;
}

function renderLessonCard(item) {
  if (isChinese()) {
    const rationale = currentLanguage === "zh-CN"
      ? "该经验整理了检索到的历史结果中反复出现的模式，供决策讨论使用。"
      : "該經驗整理了檢索到的歷史結果中反覆出現的模式，供決策討論使用。";
    return `
      <div class="card-kicker">${t("lessonLabel")}</div>
      <h3>${t("strategicLessons")}</h3>
      <p><strong>${t("whyItMatters")}:</strong> ${rationale}</p>
      <p><strong>${t("supportingCases")}:</strong> ${escapeHtml((item.supporting_cases || []).join(", ") || t("none"))}</p>
      <p><span class="evidence">${t("confidence")}: ${escapeHtml(item.confidence || t("none"))}</span></p>
    `;
  }
  return `
    <div class="card-kicker">${t("lessonLabel")}</div>
    <h3>${escapeHtml(item.lesson)}</h3>
    <p><strong>${t("whyItMatters")}:</strong> ${escapeHtml(item.rationale || "This lesson summarizes recurring patterns across retrieved historical outcomes.")}</p>
    <p><strong>${t("supportingCases")}:</strong> ${escapeHtml((item.supporting_cases || []).join(", ") || "No supporting cases listed")}</p>
    <p><span class="evidence">${t("confidence")}: ${escapeHtml(item.confidence || "Low")}</span></p>
  `;
}

function renderOutcomeCard(item) {
  if (isChinese()) {
    const observed = currentLanguage === "zh-CN"
      ? "该案例显示，类似事件可能伴随运营调整、合规审查、供应链重新评估或管理层沟通。"
      : "該案例顯示，類似事件可能伴隨營運調整、合規審查、供應鏈重新評估或管理層溝通。";
    const response = currentLanguage === "zh-CN"
      ? "历史应对被保留为教育性模式，用于比较而不是预测。"
      : "歷史應對被保留為教育性模式，用於比較而不是預測。";
    return `
      <div class="card-kicker">${t("outcomeLabel")}</div>
      <h3>${escapeHtml(item.case_name)} (${escapeHtml(item.year)})</h3>
      <p><strong>${t("observedPattern")}:</strong> ${observed}</p>
      <p><strong>${t("relevantCases")}:</strong> ${escapeHtml(item.event_family || t("none"))} / ${escapeHtml(item.sector || t("none"))}</p>
      <p><strong>${t("strategicResponse")}:</strong> ${response}</p>
      <p><span class="evidence">${t("confidence")}: ${escapeHtml(item.confidence || t("none"))}</span></p>
    `;
  }
  return `
    <div class="card-kicker">${t("outcomeLabel")}</div>
    <h3>${escapeHtml(item.case_name)} (${escapeHtml(item.year)})</h3>
    <p><strong>${t("observedPattern")}:</strong> ${escapeHtml(item.observed_outcome || "")}</p>
    <p><strong>${t("relevantCases")}:</strong> ${escapeHtml(item.event_family || "")} / ${escapeHtml(item.sector || "")}</p>
    <p><strong>${t("strategicResponse")}:</strong> ${escapeHtml(item.strategic_response || "")}</p>
    <p><span class="evidence">${t("confidence")}: ${escapeHtml(item.confidence || "Not stated")}</span></p>
  `;
}

function renderContextCard(item) {
  if (isChinese()) {
    const summary = currentLanguage === "zh-CN"
      ? "该背景条目提供本地知识库中的行业和情境上下文，用于支持结构化判断。"
      : "該背景條目提供本地知識庫中的產業和情境上下文，用於支持結構化判斷。";
    return `<h3>${escapeHtml(item.industry)} - ${escapeHtml(item.scenario_type)}</h3><p>${summary}</p><p>${sourceBadge("Context Knowledge Base")}</p>`;
  }
  return `<h3>${escapeHtml(item.industry)} - ${escapeHtml(item.scenario_type)}</h3><p>${escapeHtml(item.context_summary || "")}</p><p>${sourceBadge(item.evidence_trace || "Context Knowledge Base")}</p>`;
}

function renderMechanismCard(item) {
  if (isChinese()) {
    const description = currentLanguage === "zh-CN"
      ? "此机制用于说明事件背后的作用路径，供分析师比较和讨论。"
      : "此機制用於說明事件背後的作用路徑，供分析師比較和討論。";
    return `<h3>${escapeHtml(item.mechanism_name)}</h3><p>${description}</p><p>${sourceMeta(item)}</p>`;
  }
  return `<h3>${escapeHtml(item.mechanism_name)}</h3><p>${escapeHtml(item.description || "")}</p><p>${sourceMeta(item)}</p>`;
}

function renderInterpretationCard(item) {
  if (isChinese()) {
    const hypothesis = currentLanguage === "zh-CN"
      ? "一种可能解释是，该事件可从该分析视角观察其参与者、约束条件和组织反应。"
      : "一種可能解釋是，該事件可從該分析視角觀察其參與者、約束條件和組織反應。";
    return `<h3>${escapeHtml(item.lens)}</h3><p>${hypothesis}</p><p>${sourceBadge("Multi-Lens Analysis")}</p>`;
  }
  return `<h3>${escapeHtml(item.lens)}</h3><p>${escapeHtml(item.hypothesis || "")}</p><p>${sourceBadge("Multi-Lens Analysis")}</p>`;
}

function renderEvidenceAssessmentCard(item) {
  if (isChinese()) {
    const missing = currentLanguage === "zh-CN"
      ? "仍需补充来源、事实核验和专家判断，才能提高解释的可信度。"
      : "仍需補充來源、事實核驗和專家判斷，才能提高解釋的可信度。";
    return `<h3>${escapeHtml(item.lens)} (${escapeHtml(item.confidence_language || t("none"))})</h3><p>${missing}</p><p>${sourceBadge("Evidence Assessor")}</p>`;
  }
  return `<h3>${escapeHtml(item.lens)} (${escapeHtml(item.confidence_language)})</h3><p>${escapeHtml((item.missing_evidence || []).join(" "))}</p><p>${sourceBadge("Evidence Assessor")}</p>`;
}

function renderDistribution(distribution) {
  const entries = Object.entries(distribution);
  if (!entries.length) {
    return `<p>${t("none")}</p>`;
  }
  return `<ul>${entries.map(([key, value]) => `<li>${escapeHtml(sourceLabel(key))}: ${escapeHtml(value)}</li>`).join("")}</ul>`;
}

function renderImplications(items) {
  const section = document.getElementById("implications-section");
  if (!items.length) {
    setEmpty("implications-section", t("noImplications"));
    return;
  }
  if (isChinese()) {
    const lines = currentLanguage === "zh-CN"
      ? [
        "商业层面可关注客户、供应商、市场准入和合规成本的变化。",
        "运营层面可关注库存、替代供应、交付周期和流程治理。",
        "地缘政治层面可关注政策信号、跨境限制和利益相关者反应。",
      ]
      : [
        "商業層面可關注客戶、供應商、市場准入和合規成本的變化。",
        "營運層面可關注庫存、替代供應、交付週期和流程治理。",
        "地緣政治層面可關注政策訊號、跨境限制和利害關係人反應。",
      ];
    section.innerHTML = `<ul>${lines.map((line) => `<li>${line}</li>`).join("")}</ul><p>${sourceBadge("Synthesis")}</p>`;
    return;
  }
  const item = items[0];
  section.innerHTML = `<ul>${[
    ...(item.business_considerations || []),
    ...(item.operational_considerations || []),
    ...(item.geopolitical_considerations || []),
  ].map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul><p>${sourceBadge("Synthesis")}</p>`;
}

function renderTrace(trace) {
  if (isChinese()) {
    const selected = currentLanguage === "zh-CN"
      ? "系统已根据问题类型和输入内容选择本地确定性分析模块。"
      : "系統已根據問題類型和輸入內容選擇本地確定性分析模組。";
    const traceLines = currentLanguage === "zh-CN"
      ? ["接收输入文本。", "执行情境分类和机制检测。", "检索历史案例、历史结果和战略经验。", "生成本地简报和可下载产物。"]
      : ["接收輸入文字。", "執行情境分類和機制偵測。", "檢索歷史案例、歷史結果和策略經驗。", "生成本地簡報和可下載產物。"];
    document.getElementById("tools-section").innerHTML = `<p><strong>${t("selected")}:</strong> ${selected}</p><p>${sourceBadge("Agent Router")}</p>`;
    document.getElementById("trace-section").innerHTML = `<ol>${traceLines.map((line) => `<li>${line}</li>`).join("")}</ol><p>${sourceBadge("agent_trace.json")}</p>`;
    return;
  }
  document.getElementById("tools-section").innerHTML = `<p><strong>${t("selected")}:</strong> ${escapeHtml((trace.selected_tools || []).join(", ") || t("none"))}</p><p><strong>${t("skipped")}:</strong> ${escapeHtml((trace.skipped_tools || []).join(", ") || t("none"))}</p><p>${sourceBadge("Agent Router")}</p>`;
  document.getElementById("trace-section").innerHTML = `<ol>${(trace.trace || []).map((step) => `<li>${escapeHtml(step.event)}: ${escapeHtml(step.detail)}</li>`).join("")}</ol><p>${sourceBadge("agent_trace.json")}</p>`;
}

function renderPath() {
  if (isChinese()) {
    const lines = currentLanguage === "zh-CN"
      ? ["仪表盘调用本地 FastAPI。", "FastAPI 执行 Python 分析流水线。", "运行产物保存在 outputs/runs/。"]
      : ["儀表板呼叫本地 FastAPI。", "FastAPI 執行 Python 分析流水線。", "執行產物保存在 outputs/runs/。"];
    return `<ul>${lines.map((line) => `<li>${line}</li>`).join("")}</ul><p>${sourceBadge("Local App")}</p>`;
  }
  return `<ul><li>Dashboard called FastAPI.</li><li>FastAPI executed the Python pipeline.</li><li>Run artifacts were saved under outputs/runs/.</li></ul><p>${sourceBadge("Local App")}</p>`;
}

function renderCards(elementId, items, renderItem) {
  const element = document.getElementById(elementId);
  element.innerHTML = "";
  if (!items.length) {
    element.innerHTML = `<div class="empty">${t("noFindings")}</div>`;
    return;
  }
  items.forEach((item) => {
    const div = document.createElement("div");
    div.className = "finding";
    div.innerHTML = renderItem(item);
    element.appendChild(div);
  });
}

function sourceMeta(item) {
  const pending = sourceLabel("source pending");
  const sourceTitle = item.source_title || item.evidence_trace || "source pending";
  return `<span class="evidence">${sourceLabel("Source")}: ${escapeHtml(sourceLabel(sourceTitle))}</span>
    <span class="evidence">${sourceLabel("Type")}: ${escapeHtml(sourceLabel(item.source_type || "source pending"))}</span>
    <span class="evidence">${sourceLabel("URL")}: ${escapeHtml(item.source_url || pending)}</span>
    <span class="evidence">${sourceLabel("Confidence")}: ${escapeHtml(sourceLabel(item.confidence_note || "source pending"))}</span>`;
}

function setEmpty(elementId, message) {
  document.getElementById(elementId).innerHTML = `<div class="empty">${escapeHtml(message)}</div>`;
}

function downloadArtifact(kind) {
  if (!currentRun) {
    setEmpty("summary-section", t("downloadFirst"));
    return;
  }
  const url = currentRun.downloads?.[kind];
  if (!url) return;
  window.location.href = `${API_BASE}${url}`;
}

function exportBrief(format) {
  downloadArtifact(format === "md" ? "markdown" : "txt");
}

function adaptDashboardOutput(markdownText) {
  return markdownText;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

document.getElementById("language-select").addEventListener("change", (event) => {
  currentLanguage = event.target.value;
  applyLocale();
});
document.getElementById("mode-select").addEventListener("change", applyOutputModeVisibility);
document.getElementById("file-input").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  await extractUploadedFile(file);
});
const assistantInput = document.getElementById("assistant-input");
assistantInput.addEventListener("dragover", (event) => {
  event.preventDefault();
  assistantInput.classList.add("drag-active");
});
assistantInput.addEventListener("dragleave", () => {
  assistantInput.classList.remove("drag-active");
});
assistantInput.addEventListener("drop", async (event) => {
  event.preventDefault();
  assistantInput.classList.remove("drag-active");
  const file = event.dataTransfer.files[0];
  if (file && supportedFile(file.name)) {
    await extractUploadedFile(file);
  }
});
document.querySelectorAll(".input-mode").forEach((button) => {
  button.addEventListener("click", () => setInputMode(button.dataset.mode));
});
document.getElementById("analyze-button").addEventListener("click", analyzeDocument);
document.getElementById("export-md").addEventListener("click", () => downloadArtifact("markdown"));
document.getElementById("export-txt").addEventListener("click", () => downloadArtifact("txt"));
document.getElementById("export-json").addEventListener("click", () => downloadArtifact("json"));
document.getElementById("download-shelf-md").addEventListener("click", () => downloadArtifact("markdown"));
document.getElementById("download-shelf-txt").addEventListener("click", () => downloadArtifact("txt"));
document.getElementById("download-shelf-json").addEventListener("click", () => downloadArtifact("json"));

applyLocale();
checkHealth();
loadHistory();

function setInputMode(mode) {
  currentInputMode = mode;
  document.querySelectorAll(".input-mode").forEach((button) => {
    button.classList.toggle("active", button.dataset.mode === mode);
  });
  document.querySelectorAll(".input-mode-panel").forEach((panel) => {
    panel.classList.remove("active");
  });
  document.getElementById(`${mode}-panel`).classList.add("active");
}

function supportedFile(filename) {
  return [".txt", ".md", ".markdown", ".pdf"].some((suffix) => filename.toLowerCase().endsWith(suffix));
}

async function extractUploadedFile(file) {
  if (!supportedFile(file.name)) {
    setEmpty("summary-section", "Unsupported file type. Use .txt, .md, .markdown, or .pdf.");
    return;
  }
  uploadedFilename = file.name;
  uploadedFileType = file.name.split(".").pop().toLowerCase();
  document.getElementById("uploaded-file-name").textContent = file.name;
  const contentBase64 = await fileToBase64(file);
  const response = await fetch(`${API_BASE}/extract-file`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ filename: file.name, content_base64: contentBase64 }),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    setEmpty("summary-section", error.detail || "Could not extract uploaded file.");
    return;
  }
  const payload = await response.json();
  assistantInput.value = payload.text || "";
  currentInputMode = "assistant_upload";
}

function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = String(reader.result || "");
      resolve(result.includes(",") ? result.split(",")[1] : result);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
