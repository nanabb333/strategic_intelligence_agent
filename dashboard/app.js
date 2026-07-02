const API_BASE = window.location.origin.startsWith("http") ? window.location.origin : "http://127.0.0.1:8000";

const localeText = {
  en: {
    appTitle: "Strategic Intelligence Decision Companion",
    workbenchLabel: "Enterprise Decision Intelligence",
    helperText: "Frame the decision, provide reviewer context and supporting evidence, then review the assessment before acting.",
    trustNoteTitle: "Trust boundary",
    trustNoteBody: "Local deterministic rules and curated knowledge files support the brief. Treat outputs as decision-support drafts for human review, not forecasts, legal advice, investment advice, or verified research.",
    flowInput: "1. Frame decision",
    flowEvidence: "2. Review evidence",
    flowDecision: "3. Monitor change",
    resultsTitle: "Decision review",
    decisionBriefTitle: "Decision Assessment",
    resultsSubtitle: "Review the decision-support output before acting. Supporting evidence and method details stay available below.",
    decisionGroup: "Decision Assessment",
    supportGroup: "Strategic Considerations",
    analysisGroup: "Evidence Used",
    methodsGroup: "Assumptions and Limitations",
    settingsGroup: "Brief settings",
    artifactsGroup: "Export Assessment",
    downloadsGroup: "Export Assessment",
    runHistory: "Recent Decisions",
    emptyTitle: "Start with a decision question",
    emptyBody: "Start with the decision question, then add decision context and supporting evidence. The product keeps reviewer judgment separate from evidence.",
    emptyDecision: "Decision Assessment appears first for reviewer inspection.",
    emptyEvidence: "Confidence, evidence used, strategic considerations, assumptions, and limitations appear after analysis.",
    emptyDownloads: "Markdown, TXT, and JSON assessment exports become available after analysis.",
    loadingTitle: "Generating decision assessment",
    loadingBody: "Reviewing the question, context, supporting evidence, and local historical cases.",
    decisionQuestionLabel: "Decision Question",
    decisionQuestionPlaceholder: "What decision needs reviewer judgment? What evidence would change the decision?",
    decisionContextLabel: "Decision Context",
    decisionContextPlaceholder: "Optional: background, objectives, constraints, or review criteria. This is reviewer-authored context, not evidence.",
    assistantInputLabel: "Supporting Evidence",
    assistantPlaceholder: "Paste supporting evidence, article text, policy excerpt, earnings note, URL, or operational update here.",
    documentTextLabel: "Paste document or article here",
    questionInputLabel: "Ask a Question",
    questionPlaceholder: "What does this issue mean? What historical events resemble this? How have organizations responded in similar situations? What should I monitor next?",
    documentPlaceholder: "Paste an article, policy excerpt, earnings note, regulatory update, or supply chain memo here. You can also drag and drop a .txt or .md file into this box.",
    outputModeLabel: "Output mode",
    beginnerMode: "Beginner",
    analystMode: "Analyst",
    executiveMode: "Executive",
    inputModeLabel: "Input Mode",
    pasteTextMode: "Paste Text",
    uploadFileMode: "Upload File",
    pasteLinkMode: "Paste URL",
    uploadInstructions: "Upload .txt / .md / .markdown / .pdf",
    noFileSelected: "No file selected",
    pdfLimitNote: "PDF support works for text-based PDFs only. Scanned image PDFs are not supported.",
    sourceUrlLabel: "Paste source link",
    sourceUrlPlaceholder: "https://example.com/source-document",
    linkModeNote: "The app will try to fetch readable webpage text. If it cannot, paste the article text or upload a file.",
    urlModeNote: "Paste a full webpage URL in Supporting Evidence to fetch readable article text. If extraction fails, the app will stop and ask for pasted text or a file.",
    stepOne: "STEP 1",
    stepTwo: "STEP 2",
    stepThree: "STEP 3",
    pasteDocumentStep: "Paste Document",
    chooseInputStep: "Paste Text / Upload File / Paste URL",
    askQuestionStep: "Ask a Question",
    analyzeStep: "Generate Assessment",
    advancedSettings: "Advanced settings and input options",
    advancedNote: "Recent decisions and assessment exports remain available after analysis.",
    pasteModeNote: "Paste mode uses the main document box above.",
    runAnalysis: "Generate Decision Assessment",
    exportMarkdown: "Download Markdown",
    exportTxt: "Download TXT",
    currentEventContext: "Assessment Summary",
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
    evidenceReview: "Evidence Used",
    evidenceCredibility: "Evidence Credibility",
    analysisTransparency: "Analysis Transparency",
    transparencyNote: "This system uses a rules-based workflow to connect the input document with historical cases, common mechanisms, and strategic lessons. A human analyst should review the result.",
    evaluation: "Evaluation",
    executiveBrief: "Assessment Summary",
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
    analyzing: "Generating assessment...",
    pasteFirst: "Add a decision question, decision context, supporting evidence, a URL, or an uploaded file before generating an assessment.",
    downloadFirst: "Generate a decision assessment before exporting.",
  },
};

const sourceLocale = {
  en: {},
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
  return false;
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
    status.textContent = "Local product connected";
    status.classList.remove("offline");
  } catch (error) {
    status.textContent = "Start local product";
    status.classList.add("offline");
  }
}

async function analyzeDocument() {
  const decisionQuestionValue = document.getElementById("decision-question-input")?.value.trim() || "";
  const decisionContextValue = document.getElementById("decision-context-input")?.value.trim() || "";
  const assistantValue = document.getElementById("assistant-input").value.trim();
  const combinedInput = buildDecisionInput(decisionQuestionValue, decisionContextValue, assistantValue);
  const parsedInput = parseAssistantInput(combinedInput);
  if (!parsedInput.text && !parsedInput.sourceUrl) {
    setEmpty("summary-section", t("pasteFirst"));
    return;
  }
  const projectContext = window.getActiveProjectAnalysisContext
    ? window.getActiveProjectAnalysisContext()
    : { project_id: "", project_question_id: "", question_text: "" };
  const questionText = projectContext.question_text || decisionQuestionValue || parsedInput.questionText || t("decisionQuestionPlaceholder");
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
        project_id: projectContext.project_id || "",
        project_question_id: projectContext.project_question_id || "",
        evidence_ids: projectContext.evidence_ids || [],
      }),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || "Analysis failed.");
    }
    currentRun = await response.json();
    renderRun(currentRun);
    if (window.refreshProjectWorkspace) {
      await window.refreshProjectWorkspace();
    }
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

function buildDecisionInput(question, context, evidence) {
  const parts = [];
  if (question) {
    parts.push(`Decision Question:\n${question}`);
  }
  if (context) {
    parts.push(`Decision Context (reviewer-authored, not evidence):\n${context}`);
  }
  if (evidence) {
    parts.push(`Supporting Evidence:\n${evidence}`);
  }
  return parts.join("\n\n");
}

async function loadHistory() {
  const list = document.getElementById("history-list");
  try {
    const response = await fetch(`${API_BASE}/runs`);
    if (!response.ok) throw new Error("History unavailable");
    const runs = await response.json();
    if (!runs.length) {
      list.innerHTML = '<div class="empty">No recent decisions yet. Generate a Decision Assessment to create a local review artifact.</div>';
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
    list.innerHTML = '<div class="empty">Start the local product to view recent decisions.</div>';
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
  document.getElementById("run-note").textContent = `Saved assessment: ${metadata.run_id}. Exports are stored under outputs/runs/${metadata.run_id}/.`;
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
  if (title === "Evidence and Confidence") {
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
  const snapshot = briefSection(sections, ["Decision Snapshot"]);
  if (!snapshot) return "";

  const recommendation = sectionField(snapshot, ["Current Position"]) || firstMeaningfulLine(snapshot);
  const confidence = sectionField(snapshot, ["Confidence"]) || analysis.confidence_assessment?.confidence_level || "Not stated";
  const why = sectionField(snapshot, ["Why"]) || "Review the full brief for rationale.";
  const nextWindow = sectionField(snapshot, ["Next 30-90 Days", "未来 30-90 天", "未來 30-90 天"]) || firstBullet(briefSection(sections, ["What to Monitor"]));
  const topRisks = topRiskLines(sections);
  const trustSignals = trustSignalItems(analysis);

  return `
    <article class="decision-overview">
      <div class="overview-main">
        <div class="overview-kicker">Review before acting</div>
        <h3>${formatInline(recommendation)}</h3>
        <div class="overview-grid">
          <div>
            <strong>Confidence</strong>
            <p>${formatInline(confidence)}</p>
          </div>
          <div>
            <strong>Why this position</strong>
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
  const tradeoffs = briefSection(sections, ["Trade-offs"]);
  const change = briefSection(sections, ["What Could Change This Recommendation"]);
  const risks = [];
  if (tradeoffs) {
    tradeoffs.lines.slice(1).forEach((line) => {
      if (/risk|wrong|change/i.test(line)) {
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
  const decisionTitles = ["Decision Snapshot"];
  const criteriaTitles = ["Decision Criteria"];
  const choiceTitles = ["Decision Paths"];
  const rankingTitles = ["Option Ranking"];
  const preferredTitles = ["Preferred Path"];
  const assumptionTitles = ["Assumptions"];
  const roleTitles = ["Role-Based Implications"];
  const tradeoffTitles = ["Trade-offs"];
  const changeTitles = ["What Could Change This Recommendation"];
  const blindSpotTitles = ["Decision Blind Spots"];
  const actionTitles = ["Action Timeline"];
  const monitorTitles = ["What to Monitor"];
  const qualityTitles = ["Decision Quality Review"];
  const supportingTitles = [
    "Historical Evidence",
    "Market Expectations vs Actual Outcomes",
    "Evidence Used",
    "Limitations",
  ];
  if (decisionTitles.includes(title)) classes.push("decision-card");
  if (criteriaTitles.includes(title)) classes.push("criteria-card");
  if (choiceTitles.includes(title)) classes.push("choices-card");
  if (rankingTitles.includes(title)) classes.push("ranking-card");
  if (preferredTitles.includes(title)) classes.push("recommended-card");
  if (assumptionTitles.includes(title)) classes.push("assumption-card");
  if (roleTitles.includes(title)) classes.push("role-card");
  if (tradeoffTitles.includes(title)) classes.push("tradeoff-card");
  if (changeTitles.includes(title)) classes.push("change-card");
  if (blindSpotTitles.includes(title)) classes.push("blindspot-card");
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
    .replace(/Criteria Fit/g, '<span class="criteria-fit-label">Criteria Fit</span>');
}

function renderEventContext(item) {
  const section = document.getElementById("event-context-section");
  if (!item.event_type) {
    section.innerHTML = `<div class="empty">${t("noContext")}</div>`;
    return;
  }
  const sectors = (item.affected_sectors || []).join(", ") || t("none");
  const regions = (item.affected_regions || []).join(", ") || t("none");
  const significance = item.strategic_significance || "";
  const summary = item.event_summary || "";
  const limitations = item.context_limitations || [];
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
  const summary = item.evidence_summary;
  const limitations = item.key_limitations || [];
  const reviewer = item.reviewer_note || "";
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

function renderContextCard(item) {
  return `<h3>${escapeHtml(item.industry)} - ${escapeHtml(item.scenario_type)}</h3><p>${escapeHtml(item.context_summary || "")}</p><p>${sourceBadge(item.evidence_trace || "Context Knowledge Base")}</p>`;
}

function renderMechanismCard(item) {
  return `<h3>${escapeHtml(item.mechanism_name)}</h3><p>${escapeHtml(item.description || "")}</p><p>${sourceMeta(item)}</p>`;
}

function renderInterpretationCard(item) {
  return `<h3>${escapeHtml(item.lens)}</h3><p>${escapeHtml(item.hypothesis || "")}</p><p>${sourceBadge("Multi-Lens Analysis")}</p>`;
}

function renderEvidenceAssessmentCard(item) {
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
  const item = items[0];
  section.innerHTML = `<ul>${[
    ...(item.business_considerations || []),
    ...(item.operational_considerations || []),
    ...(item.geopolitical_considerations || []),
  ].map((line) => `<li>${escapeHtml(line)}</li>`).join("")}</ul><p>${sourceBadge("Synthesis")}</p>`;
}

function renderTrace(trace) {
  document.getElementById("tools-section").innerHTML = `<p><strong>${t("selected")}:</strong> ${escapeHtml((trace.selected_tools || []).join(", ") || t("none"))}</p><p><strong>${t("skipped")}:</strong> ${escapeHtml((trace.skipped_tools || []).join(", ") || t("none"))}</p><p>${sourceBadge("Tool Router")}</p>`;
  document.getElementById("trace-section").innerHTML = `<ol>${(trace.trace || []).map((step) => `<li>${escapeHtml(step.event)}: ${escapeHtml(step.detail)}</li>`).join("")}</ol><p>${sourceBadge("agent_trace.json")}</p>`;
}

function renderPath() {
  return `<ul><li>The Decision Assessment interface called the local API.</li><li>The local API executed the Python pipeline.</li><li>Assessment exports were saved under outputs/runs/.</li></ul><p>${sourceBadge("Local App")}</p>`;
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
document.getElementById("export-md")?.addEventListener("click", () => downloadArtifact("markdown"));
document.getElementById("export-txt")?.addEventListener("click", () => downloadArtifact("txt"));
document.getElementById("export-json")?.addEventListener("click", () => downloadArtifact("json"));
document.getElementById("download-shelf-md")?.addEventListener("click", () => downloadArtifact("markdown"));
document.getElementById("download-shelf-txt")?.addEventListener("click", () => downloadArtifact("txt"));
document.getElementById("download-shelf-json")?.addEventListener("click", () => downloadArtifact("json"));

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
