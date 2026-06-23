const API_BASE = window.location.origin.startsWith("http") ? window.location.origin : "http://127.0.0.1:8000";
const sourceLabels = ["Historical Database", "Context Knowledge Base", "Input Document"];

const localeText = {
  en: {
    appTitle: "Strategic Intelligence Agent",
    workbenchLabel: "Local Intelligence App",
    helperText: "No prompt writing needed. Step 1 choose a language. Step 2 paste text or upload a file. Step 3 choose a question. Step 4 choose an output mode. Step 5 click Analyze. Step 6 download results.",
    documentTextLabel: "Document text",
    questionTypeLabel: "Question type",
    outputModeLabel: "Output mode",
    languageLabel: "Language",
    beginnerMode: "Beginner",
    analystMode: "Analyst",
    executiveMode: "Executive",
    uploadInstructions: "Upload .md/.txt",
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
    evidenceCredibility: "Evidence Credibility",
    evaluation: "Evaluation",
    executiveBrief: "Executive Brief",
  },
  "zh-CN": {
    appTitle: "战略情报助手",
    workbenchLabel: "本地情报应用",
    helperText: "不用会写提示词。第一步选择语言。第二步粘贴文字或上传文件。第三步选择问题。第四步选择输出模式。第五步点击分析。第六步下载结果。",
    documentTextLabel: "文档文本",
    questionTypeLabel: "问题类型",
    outputModeLabel: "输出模式",
    languageLabel: "语言",
    beginnerMode: "入门",
    analystMode: "分析师",
    executiveMode: "高管",
    uploadInstructions: "上传 .md/.txt",
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
    evidenceCredibility: "证据可信度",
    evaluation: "评估",
    executiveBrief: "高管简报",
  },
  "zh-TW": {
    appTitle: "戰略情報助手",
    workbenchLabel: "本地情報應用",
    helperText: "不用會寫提示詞。第一步選擇語言。第二步貼上文字或上傳檔案。第三步選擇問題。第四步選擇輸出模式。第五步點擊分析。第六步下載結果。",
    documentTextLabel: "文件文字",
    questionTypeLabel: "問題類型",
    outputModeLabel: "輸出模式",
    languageLabel: "語言",
    beginnerMode: "入門",
    analystMode: "分析師",
    executiveMode: "高階主管",
    uploadInstructions: "上傳 .md/.txt",
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
    evidenceCredibility: "證據可信度",
    evaluation: "評估",
    executiveBrief: "高階主管簡報",
  },
};

const guidedQuestions = [
  { id: "meaning", en: "What does this issue mean?", "zh-CN": "这件事是什么意思？", "zh-TW": "這件事是什麼意思？" },
  { id: "analogues", en: "What past events does this resemble?", "zh-CN": "这和过去哪些事件相似？", "zh-TW": "這和過去哪些事件相似？" },
  { id: "mechanisms", en: "What mechanisms may be operating?", "zh-CN": "可能有哪些机制在发挥作用？", "zh-TW": "可能有哪些機制在發揮作用？" },
  { id: "responses", en: "What have actors done in similar situations?", "zh-CN": "历史上相关参与者采取过哪些做法？", "zh-TW": "歷史上相關參與者採取過哪些做法？" },
  { id: "affected", en: "Who may be affected?", "zh-CN": "哪些主体可能受到影响？", "zh-TW": "哪些主體可能受到影響？" },
  { id: "monitor", en: "What should I monitor next?", "zh-CN": "我应该关注哪些后续变化？", "zh-TW": "我應該關注哪些後續變化？" },
  { id: "interpretations", en: "What are competing interpretations?", "zh-CN": "有哪些不同解释？", "zh-TW": "有哪些不同解釋？" },
  { id: "limitations", en: "What is missing from the evidence?", "zh-CN": "证据中还缺少什么？", "zh-TW": "證據中還缺少什麼？" },
];

let currentLanguage = "en";
let currentQuestion = guidedQuestions[0];
let currentRun = null;

function t(key) {
  return localeText[currentLanguage][key] || localeText.en[key] || key;
}

function applyLocale() {
  document.documentElement.lang = currentLanguage;
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  document.getElementById("helper-text").textContent = t("helperText");
  populateQuestions();
}

function populateQuestions() {
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
      populateQuestions();
    });
    buttons.appendChild(button);
  });
  select.value = currentQuestion.id;
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
  if (!text) {
    setEmpty("summary-section", "Paste text or upload a file first.");
    return;
  }
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
        question_id: currentQuestion.id,
        question_text: currentQuestion[currentLanguage],
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
  document.getElementById("summary-section").innerHTML = `<p>${escapeHtml(issue.summary || issue.core_issue || "No summary returned.")}</p><p><span class="evidence">Source: Input Document</span></p>`;
  document.getElementById("classification-section").innerHTML = `<ul><li>Primary scenario: ${escapeHtml(scenario.primary_scenario || "Other")}</li><li>Matched keywords: ${escapeHtml((scenario.matched_keywords || []).join(", ") || "None")}</li><li>Confidence label: ${escapeHtml(scenario.confidence_label || "Not available")}</li></ul><p><span class="evidence">Source: ScenarioClassifier</span></p>`;
  renderCards("analogues-section", analysis.analogues || [], (item) => `<h3>${escapeHtml(item.case_title)}</h3><p>${escapeHtml(item.similarity_reason || "")}</p><p>${sourceMeta(item)}</p>`);
  renderCards("outcomes-section", analysis.historical_outcomes || [], (item) => `<h3>${escapeHtml(item.case_name)} (${escapeHtml(item.year)})</h3><p>${escapeHtml(item.observed_outcome || "")}</p><p><strong>Strategic response:</strong> ${escapeHtml(item.strategic_response || "")}</p><p><span class="evidence">Confidence: ${escapeHtml(item.confidence || "Not stated")}</span> <span class="evidence">Source: ${escapeHtml(item.source_status || "source pending")}</span></p>`);
  renderCards("lessons-section", analysis.strategic_lessons || [], (item) => `<h3>${escapeHtml(item.lesson)}</h3><p><strong>Supporting cases:</strong> ${escapeHtml((item.supporting_cases || []).join(", "))}</p><p>${escapeHtml(item.rationale || "")}</p><p><span class="evidence">Confidence: ${escapeHtml(item.confidence || "Low")}</span></p>`);
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
      <div><strong>Event type</strong><span>${escapeHtml(item.event_type)}</span></div>
      <div><strong>Primary actor</strong><span>${escapeHtml(item.primary_actor)}</span></div>
      <div><strong>Secondary actor</strong><span>${escapeHtml(item.secondary_actor)}</span></div>
      <div><strong>Affected sectors</strong><span>${escapeHtml((item.affected_sectors || []).join(", ") || "Not specified")}</span></div>
      <div><strong>Affected regions</strong><span>${escapeHtml((item.affected_regions || []).join(", ") || "Not specified")}</span></div>
      <div><strong>Policy domain</strong><span>${escapeHtml(item.policy_domain)}</span></div>
      <div><strong>Confidence</strong><span>${escapeHtml(item.confidence)}</span></div>
    </div>
    <p>${escapeHtml(item.strategic_significance || "")}</p>
    <p><strong>Event summary:</strong> ${escapeHtml(item.event_summary || "")}</p>
    <h3>Limitations</h3>
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
    <h3>Confidence distribution</h3>
    ${renderDistribution(item.confidence_distribution || {})}
    <h3>Source status distribution</h3>
    ${renderDistribution(item.source_status_distribution || {})}
    <h3>Key limitations</h3>
    <ul>${(item.key_limitations || []).map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul>
    <p><span class="evidence">Reviewer note</span></p>
    <p>${escapeHtml(item.reviewer_note || "")}</p>
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
document.getElementById("question-select").addEventListener("change", (event) => {
  currentQuestion = guidedQuestions.find((question) => question.id === event.target.value) || guidedQuestions[0];
  populateQuestions();
});
document.getElementById("file-input").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  document.getElementById("document-input").value = await file.text();
});
document.getElementById("analyze-button").addEventListener("click", analyzeDocument);
document.getElementById("export-md").addEventListener("click", () => downloadArtifact("markdown"));
document.getElementById("export-txt").addEventListener("click", () => downloadArtifact("txt"));
document.getElementById("export-json").addEventListener("click", () => downloadArtifact("json"));

applyLocale();
checkHealth();
loadHistory();
