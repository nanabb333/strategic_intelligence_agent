const API_BASE = window.location.origin.startsWith("http") ? window.location.origin : "http://127.0.0.1:8000";
const sourceLabels = ["Historical Database", "Context Knowledge Base", "Input Document"];

const localeText = {
  en: {
    appTitle: "Analyze a document or current event",
    workbenchLabel: "Local Intelligence App",
    helperText: "Paste a document, ask a plain-language question, and click Analyze. The app shows the executive brief first, with methods and trace details below.",
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
    pasteLinkMode: "Paste Link",
    uploadInstructions: "Upload .txt / .md / .markdown / .pdf",
    noFileSelected: "No file selected",
    pdfLimitNote: "PDF support works for text-based PDFs only. Scanned image PDFs are not supported.",
    sourceUrlLabel: "Paste source link",
    sourceUrlPlaceholder: "https://example.com/source-document",
    linkModeNote: "Live web retrieval is not enabled. Links are stored as source metadata.",
    stepOne: "STEP 1",
    stepTwo: "STEP 2",
    stepThree: "STEP 3",
    pasteDocumentStep: "Paste Document",
    askQuestionStep: "Ask a Question",
    analyzeStep: "Analyze",
    advancedSettings: "Advanced settings and input options",
    pasteModeNote: "Paste mode uses the main document box above.",
    runAnalysis: "Analyze",
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
    evaluation: "Evaluation",
    executiveBrief: "Executive Brief",
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
  },
  "zh-CN": {
    appTitle: "分析文档或当前事件",
    workbenchLabel: "本地情报应用",
    helperText: "粘贴文档，输入一个自然语言问题，然后点击分析。应用会先显示高管简报，方法和执行轨迹放在后面。",
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
    pasteLinkMode: "粘贴链接",
    uploadInstructions: "上传 .txt / .md / .markdown / .pdf",
    noFileSelected: "未选择文件",
    pdfLimitNote: "PDF 支持仅适用于文本型 PDF；暂不支持扫描图片 PDF。",
    sourceUrlLabel: "粘贴来源链接",
    sourceUrlPlaceholder: "https://example.com/source-document",
    linkModeNote: "未启用实时网页检索；链接仅保存为来源元数据。",
    stepOne: "步骤 1",
    stepTwo: "步骤 2",
    stepThree: "步骤 3",
    pasteDocumentStep: "粘贴文档",
    askQuestionStep: "提问",
    analyzeStep: "分析",
    advancedSettings: "高级设置和输入选项",
    pasteModeNote: "粘贴模式使用上方主文档输入框。",
    runAnalysis: "分析",
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
  },
  "zh-TW": {
    appTitle: "分析文件或當前事件",
    workbenchLabel: "本地情報應用",
    helperText: "貼上文件，輸入自然語言問題，然後點擊分析。應用會先顯示高階主管簡報，方法與執行軌跡放在後面。",
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
    pasteLinkMode: "貼上連結",
    uploadInstructions: "上傳 .txt / .md / .markdown / .pdf",
    noFileSelected: "未選擇檔案",
    pdfLimitNote: "PDF 支援僅適用於文字型 PDF；暫不支援掃描圖片 PDF。",
    sourceUrlLabel: "貼上來源連結",
    sourceUrlPlaceholder: "https://example.com/source-document",
    linkModeNote: "未啟用即時網頁檢索；連結僅保存為來源元資料。",
    stepOne: "步驟 1",
    stepTwo: "步驟 2",
    stepThree: "步驟 3",
    pasteDocumentStep: "貼上文件",
    askQuestionStep: "提問",
    analyzeStep: "分析",
    advancedSettings: "進階設定和輸入選項",
    pasteModeNote: "貼上模式使用上方主文件輸入框。",
    runAnalysis: "分析",
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

function applyLocale() {
  document.documentElement.lang = currentLanguage;
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    node.placeholder = t(node.dataset.i18nPlaceholder);
  });
  document.getElementById("helper-text").textContent = t("helperText");
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
  const text = document.getElementById("document-input").value.trim();
  const sourceUrl = document.getElementById("source-url-input").value.trim();
  if (!text && !sourceUrl) {
    setEmpty("summary-section", "Paste text or upload a file first.");
    return;
  }
  const questionText = document.getElementById("question-input").value.trim() || t("questionPlaceholder");
  const button = document.getElementById("analyze-button");
  button.disabled = true;
  button.textContent = "Analyzing...";
  try {
    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        language: currentLanguage,
        output_mode: document.getElementById("mode-select").value,
        question_id: "freeform",
        question_text: questionText,
        source_url: sourceUrl,
        input_mode: currentInputMode,
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

function renderRun(run) {
  const analysis = run.analysis;
  const metadata = run.metadata;
  const issue = analysis.issue || {};
  const scenario = analysis.scenario || {};
  renderEventContext(analysis.event_context || {});
  document.getElementById("run-note").textContent = `Saved run: ${metadata.run_id}. Artifacts are stored under outputs/runs/${metadata.run_id}/.`;
  if (analysis.message && analysis.source_url) {
    document.getElementById("summary-section").innerHTML = `<p>${escapeHtml(analysis.message)}</p><p><span class="evidence">${t("source")}: ${escapeHtml(analysis.source_url)}</span></p>`;
    document.getElementById("brief-section").textContent = run.brief_markdown || "";
    return;
  }
  const sourceLink = analysis.source_url ? `<p><span class="evidence">${t("source")}: ${escapeHtml(analysis.source_url)}</span></p>` : "";
  document.getElementById("summary-section").innerHTML = `<p>${escapeHtml(issue.summary || issue.core_issue || "No summary returned.")}</p><p><span class="evidence">${t("source")}: Input Document</span></p>${sourceLink}`;
  document.getElementById("classification-section").innerHTML = `<ul><li>${t("primaryScenario")}: ${escapeHtml(scenario.primary_scenario || "Other")}</li><li>${t("matchedKeywords")}: ${escapeHtml((scenario.matched_keywords || []).join(", ") || "None")}</li><li>${t("confidenceLabel")}: ${escapeHtml(scenario.confidence_label || "Not available")}</li></ul><p><span class="evidence">${t("source")}: ScenarioClassifier</span></p>`;
  renderCards("analogues-section", analysis.analogues || [], (item) => `<h3>${escapeHtml(item.case_title)}</h3><p>${escapeHtml(item.similarity_reason || "")}</p><p>${sourceMeta(item)}</p>`);
  renderCards("outcomes-section", analysis.historical_outcomes || [], renderOutcomeCard);
  renderCards("lessons-section", analysis.strategic_lessons || [], renderLessonCard);
  renderCards("context-section", analysis.current_context || [], (item) => `<h3>${escapeHtml(item.industry)} - ${escapeHtml(item.scenario_type)}</h3><p>${escapeHtml(item.context_summary || "")}</p><p><span class="evidence">Source: ${escapeHtml(item.evidence_trace || "Context Knowledge Base")}</span></p>`);
  renderCards("mechanisms-section", analysis.mechanisms || [], (item) => `<h3>${escapeHtml(item.mechanism_name)}</h3><p>${escapeHtml(item.description || "")}</p><p>${sourceMeta(item)}</p>`);
  renderCards("interpretations-section", analysis.lenses || [], (item) => `<h3>${escapeHtml(item.lens)}</h3><p>${escapeHtml(item.hypothesis || "")}</p><p><span class="evidence">Source: Multi-Lens Analysis</span></p>`);
  renderCards("responses-section", analysis.response_playbooks || [], (item) => `<h3>${escapeHtml(item.pattern_name)}</h3><p>${escapeHtml((item.observed_historical_choices || []).join(" "))}</p><p>${sourceMeta(item)}</p>`);
  renderCards("evidence-assessment-section", analysis.evidence || [], (item) => `<h3>${escapeHtml(item.lens)} (${escapeHtml(item.confidence_language)})</h3><p>${escapeHtml((item.missing_evidence || []).join(" "))}</p><p><span class="evidence">Source: Evidence Assessor</span></p>`);
  renderEvidenceCredibility(analysis.evidence_credibility || {});
  renderImplications(analysis.implications || []);
  renderTrace(analysis.agent_trace || {});
  document.getElementById("path-section").innerHTML = '<ul><li>Dashboard called FastAPI.</li><li>FastAPI executed the Python pipeline.</li><li>Run artifacts were saved under outputs/runs/.</li></ul><p><span class="evidence">Source: Local App</span></p>';
  document.getElementById("brief-section").textContent = run.brief_markdown || "";
}

function renderEventContext(item) {
  const section = document.getElementById("event-context-section");
  if (!item.event_type) {
    section.innerHTML = '<div class="empty">No current event context returned for this run.</div>';
    return;
  }
  section.innerHTML = `
    <div class="context-grid">
      <div><strong>${t("eventType")}</strong><span>${escapeHtml(item.event_type)}</span></div>
      <div><strong>${t("primaryActor")}</strong><span>${escapeHtml(item.primary_actor)}</span></div>
      <div><strong>${t("secondaryActor")}</strong><span>${escapeHtml(item.secondary_actor)}</span></div>
      <div><strong>${t("affectedSectors")}</strong><span>${escapeHtml((item.affected_sectors || []).join(", ") || "Not specified")}</span></div>
      <div><strong>${t("affectedRegions")}</strong><span>${escapeHtml((item.affected_regions || []).join(", ") || "Not specified")}</span></div>
      <div><strong>${t("policyDomain")}</strong><span>${escapeHtml(item.policy_domain)}</span></div>
      <div><strong>${t("confidence")}</strong><span>${escapeHtml(item.confidence)}</span></div>
    </div>
    <p>${escapeHtml(item.strategic_significance || "")}</p>
    <p><strong>${t("eventSummary")}:</strong> ${escapeHtml(item.event_summary || "")}</p>
    <h3>${t("limitations")}</h3>
    <ul>${(item.context_limitations || []).map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>
    <p><span class="evidence">Source: Input Document + deterministic event-context rules</span></p>
  `;
}

function renderEvidenceCredibility(item) {
  const section = document.getElementById("evidence-credibility-section");
  if (!item.evidence_summary) {
    section.innerHTML = '<div class="empty">No evidence credibility note returned for this run.</div>';
    return;
  }
  section.innerHTML = `
    <p>${escapeHtml(item.evidence_summary)}</p>
    <h3>${t("confidenceDistribution")}</h3>
    ${renderDistribution(item.confidence_distribution || {})}
    <h3>${t("sourceStatusDistribution")}</h3>
    ${renderDistribution(item.source_status_distribution || {})}
    <h3>${t("keyLimitations")}</h3>
    <ul>${(item.key_limitations || []).map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>
    <p><span class="evidence">${t("reviewerNote")}</span></p>
    <p>${escapeHtml(item.reviewer_note || "")}</p>
  `;
}

function renderLessonCard(item) {
  return `
    <div class="card-kicker">${t("lessonLabel")}</div>
    <h3>${escapeHtml(item.lesson)}</h3>
    <p><strong>${t("whyItMatters")}:</strong> ${escapeHtml(item.rationale || "This lesson summarizes recurring patterns across retrieved historical outcomes.")}</p>
    <p><strong>${t("supportingCases")}:</strong> ${escapeHtml((item.supporting_cases || []).join(", ") || "No supporting cases listed")}</p>
    <p><span class="evidence">${t("confidence")}: ${escapeHtml(item.confidence || "Low")}</span></p>
  `;
}

function renderOutcomeCard(item) {
  return `
    <div class="card-kicker">${t("outcomeLabel")}</div>
    <h3>${escapeHtml(item.case_name)} (${escapeHtml(item.year)})</h3>
    <p><strong>${t("observedPattern")}:</strong> ${escapeHtml(item.observed_outcome || "")}</p>
    <p><strong>${t("relevantCases")}:</strong> ${escapeHtml(item.event_family || "")} / ${escapeHtml(item.sector || "")}</p>
    <p><strong>${t("strategicResponse")}:</strong> ${escapeHtml(item.strategic_response || "")}</p>
    <p><span class="evidence">${t("confidence")}: ${escapeHtml(item.confidence || "Not stated")}</span></p>
  `;
}

function renderDistribution(distribution) {
  const entries = Object.entries(distribution);
  if (!entries.length) {
    return '<p>None reported.</p>';
  }
  return `<ul>${entries.map(([key, value]) => `<li>${escapeHtml(key)}: ${escapeHtml(value)}</li>`).join("")}</ul>`;
}

function renderImplications(items) {
  const section = document.getElementById("implications-section");
  if (!items.length) {
    setEmpty("implications-section", "No implications returned.");
    return;
  }
  const item = items[0];
  section.innerHTML = `<ul>${[
    ...(item.business_considerations || []),
    ...(item.operational_considerations || []),
    ...(item.geopolitical_considerations || []),
  ].map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul><p><span class="evidence">Source: ImplicationAnalyzer</span></p>`;
}

function renderTrace(trace) {
  document.getElementById("tools-section").innerHTML = `<p><strong>Selected:</strong> ${escapeHtml((trace.selected_tools || []).join(", ") || "None")}</p><p><strong>Skipped:</strong> ${escapeHtml((trace.skipped_tools || []).join(", ") || "None")}</p><p><span class="evidence">Source: Agent Router</span></p>`;
  document.getElementById("trace-section").innerHTML = `<ol>${(trace.trace || []).map((step) => `<li>${escapeHtml(step.event)}: ${escapeHtml(step.detail)}</li>`).join("")}</ol><p><span class="evidence">Source: agent_trace.json</span></p>`;
}

function renderCards(elementId, items, renderItem) {
  const element = document.getElementById(elementId);
  element.innerHTML = "";
  if (!items.length) {
    element.innerHTML = '<div class="empty">No findings returned for this run.</div>';
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
  return `<span class="evidence">Source: ${escapeHtml(item.source_title || item.evidence_trace || "source pending")}</span>
    <span class="evidence">Type: ${escapeHtml(item.source_type || "source pending")}</span>
    <span class="evidence">URL: ${escapeHtml(item.source_url || "source pending")}</span>
    <span class="evidence">Confidence: ${escapeHtml(item.confidence_note || "source pending")}</span>`;
}

function setEmpty(elementId, message) {
  document.getElementById(elementId).innerHTML = `<div class="empty">${escapeHtml(message)}</div>`;
}

function downloadArtifact(kind) {
  if (!currentRun) {
    setEmpty("summary-section", "Run an analysis before downloading.");
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
document.getElementById("file-input").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  await extractUploadedFile(file);
});
const documentInput = document.getElementById("document-input");
documentInput.addEventListener("dragover", (event) => {
  event.preventDefault();
  documentInput.classList.add("drag-active");
});
documentInput.addEventListener("dragleave", () => {
  documentInput.classList.remove("drag-active");
});
documentInput.addEventListener("drop", async (event) => {
  event.preventDefault();
  documentInput.classList.remove("drag-active");
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
  documentInput.value = payload.text || "";
  setInputMode("paste");
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
