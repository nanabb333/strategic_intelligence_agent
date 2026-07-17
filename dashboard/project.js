(() => {
  const PROJECT_API_BASE = window.location.origin.startsWith("http")
    ? window.location.origin
    : "http://127.0.0.1:8000";

  let workspaceProject = null;
  let workspaceQuestionId = "";
  let retrievedEvidenceQueue = [];
  let selectedEvidenceIds = new Set();

  function projectEscapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function projectStructuralChecks(passed, total, legacyRate) {
    if (typeof passed === "number" && typeof total === "number") {
      return `${passed} of ${total} structural checks passed`;
    }
    if (typeof legacyRate === "number") {
      return `Legacy completeness rate ${legacyRate.toFixed(3)}; structural counts unavailable`;
    }
    return "Structural checks not available";
  }

  function projectDomId(value) {
    return String(value || "")
      .toLowerCase()
      .replace(/[^a-z0-9_-]+/g, "-")
      .replace(/^-+|-+$/g, "");
  }

  function activeProjectQuestion() {
    if (!workspaceProject || !workspaceQuestionId) return null;
    return (workspaceProject.questions || []).find((item) => item.question_id === workspaceQuestionId) || null;
  }

  function projectRunLink(runId) {
    if (!runId) return "";
    return `<a href="${PROJECT_API_BASE}/run/${projectEscapeHtml(runId)}/download/markdown" target="_blank" rel="noreferrer">Export current assessment for run ${projectEscapeHtml(runId)}</a>`;
  }

  async function loadProjects() {
    const list = document.getElementById("project-list");
    const gettingStarted = document.getElementById("getting-started");
    if (!list) return;
    const isSelect = list.tagName.toLowerCase() === "select";

    try {
      const response = await fetch(`${PROJECT_API_BASE}/projects`);
      if (!response.ok) throw new Error("Projects unavailable.");

      const data = await response.json();
      const projects = data.projects || [];
      if (gettingStarted) {
        gettingStarted.hidden = projects.length > 0;
      }

      if (!projects.length) {
        if (isSelect) {
          list.innerHTML = '<option value="">No project selected</option>';
        } else {
          list.innerHTML = '<div class="empty project-empty-state">No projects yet. Create a project to organize questions, evidence, analyses, and reviewer notes.</div>';
        }
        return;
      }

      list.innerHTML = "";

      if (isSelect) {
        list.innerHTML = [
          '<option value="">Select project</option>',
          ...projects.map((project) => `
            <option value="${projectEscapeHtml(project.project_id)}"${workspaceProject?.project_id === project.project_id ? " selected" : ""}>
              ${projectEscapeHtml(project.name)}
            </option>
          `),
        ].join("");
        list.onchange = () => {
          if (list.value) selectProject(list.value);
        };
        return;
      }

      projects.forEach((project) => {
        const button = document.createElement("button");
        button.type = "button";
        button.className =
          `project-item${workspaceProject?.project_id === project.project_id ? " active" : ""}`;

        button.innerHTML = `
          <span class="project-card-main">
            <strong>${projectEscapeHtml(project.name)}</strong>
            <span>${project.questions?.length || 0} questions - ${project.evidence_library?.length || 0} evidence</span>
          </span>
          <span class="project-card-actions" aria-label="Reserved project actions">
            <span title="Rename action reserved">Rename</span>
            <span title="Archive action reserved">Archive</span>
            <span title="Delete action reserved">Delete</span>
          </span>
        `;

        button.addEventListener("click", () => selectProject(project.project_id));
        list.appendChild(button);
      });
    } catch (error) {
      if (gettingStarted) gettingStarted.hidden = true;
      if (isSelect) {
        list.innerHTML = '<option value="">Projects unavailable</option>';
      } else {
        list.innerHTML = '<div class="empty error-state">Could not load projects. Start the local product and try again.</div>';
      }
    }
  }

  async function createProjectFromInput() {
    const input = document.getElementById("project-name-input");
    if (!input) return;

    const name = input.value.trim();

    if (!name) {
      alert("Enter a project name to create a reviewer-controlled decision project.");
      return;
    }

    const response = await fetch(`${PROJECT_API_BASE}/projects`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        name,
        description: "Decision project",
      }),
    });

    if (!response.ok) {
      alert("Could not create the project. Confirm the local product is running and try again.");
      return;
    }

    input.value = "";
    workspaceProject = await response.json();
    workspaceQuestionId = "";
    selectedEvidenceIds = new Set();
    renderActiveProject(workspaceProject);
    await loadProjects();
  }

  async function selectProject(projectId) {
    const response = await fetch(`${PROJECT_API_BASE}/projects/${projectId}`);

    if (!response.ok) {
      alert("Could not open the project. Refresh the workspace and try again.");
      return;
    }

    workspaceProject = await response.json();
    selectedEvidenceIds = new Set();

    if (!activeProjectQuestion() && (workspaceProject.questions || []).length) {
      workspaceQuestionId = workspaceProject.questions[0].question_id;
    }
    const selectedQuestion = activeProjectQuestion();
    const decisionQuestionInput = document.getElementById("decision-question-input");
    if (decisionQuestionInput && selectedQuestion?.question) {
      decisionQuestionInput.value = selectedQuestion.question;
    }

    renderActiveProject(workspaceProject);
    await loadProjects();
  }

  async function refreshProjectWorkspace() {
    if (!workspaceProject) return;
    await selectProject(workspaceProject.project_id);
  }

  function renderActiveProject(project) {
    const panel = document.getElementById("active-project-panel");
    const name = document.getElementById("active-project-name");

    if (!panel || !name) return;

    panel.hidden = false;
    name.textContent = project.name;
    renderProjectOverview(project);

    renderProjectQuestions(project.questions || []);
    renderProjectEvidence(project.evidence_library || []);
    fetchEvidenceIntelligence(project.project_id);
    fetchDecisionReadiness(project.project_id);
    fetchDecisionPathways(project.project_id);
    fetchPathwayComparison(project.project_id);
    fetchDecisionReview(project.project_id);
    fetchDomainEvaluation(project.project_id);
    renderDecisionTimeline(project);
    renderDecisionDelta(project.project_id);
  }

  function renderProjectOverview(project) {
    const questions = project.questions || [];
    const evidence = project.evidence_library || [];
    const decisions = project.decision_history || [];
    const state = project.workspace_state || {};
    const status = document.getElementById("active-project-status");
    const questionCount = document.getElementById("active-question-count");
    const evidenceCount = document.getElementById("active-evidence-count");
    const decisionCount = document.getElementById("active-decision-count");
    const updatedAt = document.getElementById("active-updated-at");

    if (status) {
      status.textContent = decisions.length ? "Active" : "Ready";
    }
    if (questionCount) questionCount.textContent = String(questions.length);
    if (evidenceCount) evidenceCount.textContent = String(evidence.length);
    if (decisionCount) decisionCount.textContent = String(decisions.length);
    if (updatedAt) {
      updatedAt.textContent = state.last_updated_at || project.updated_at || project.created_at || "Not updated";
    }
  }

  function renderProjectQuestions(questions) {
    const questionList = document.getElementById("project-question-list");
    if (!questionList) return;

    if (!questions.length) {
      questionList.innerHTML = '<div class="empty">No questions saved yet. Add the decision question reviewers need to examine.</div>';
      return;
    }

    questionList.innerHTML = "";

    questions.forEach((item) => {
      const card = document.createElement("button");
      card.type = "button";
      card.className = `project-question-item${workspaceQuestionId === item.question_id ? " active" : ""}`;
      card.innerHTML = `
        <strong>${projectEscapeHtml(item.question)}</strong>
        <span>${projectEscapeHtml(item.created_at || "")}</span>
        ${item.run_id ? `<span>Linked run: ${projectEscapeHtml(item.run_id)}</span>` : "<span>Ready for analysis</span>"}
      `;

      card.addEventListener("click", () => {
        workspaceQuestionId = item.question_id;
        renderProjectQuestions(questions);
        const input = document.getElementById("project-question-input");
        if (input) input.value = item.question || "";
        const decisionQuestionInput = document.getElementById("decision-question-input");
        if (decisionQuestionInput) decisionQuestionInput.value = item.question || "";
      });

      questionList.appendChild(card);
    });
  }

  function renderProjectEvidence(items) {
    const evidenceList = document.getElementById("project-evidence-list");
    if (!evidenceList) return;

    if (!items.length) {
      evidenceList.innerHTML = '<div class="empty">No accepted evidence saved yet. Add a manual note or accept retrieved evidence after human review.</div>';
      return;
    }

    evidenceList.innerHTML = items.map((item) => {
      const evidenceDomId = projectDomId(item.evidence_id || item.id || item.trace_id || item.title);
      return `
      <label class="project-evidence-item"${evidenceDomId ? ` id="evidence-card-${projectEscapeHtml(evidenceDomId)}"` : ""}>
        <input
          type="checkbox"
          data-project-evidence-id="${projectEscapeHtml(item.evidence_id || "")}"
          ${selectedEvidenceIds.has(item.evidence_id) ? "checked" : ""}
        >
        <strong>${projectEscapeHtml(item.title)}</strong>
        <span>Status: ${projectEscapeHtml(item.status || "User Provided")} - Source type: ${projectEscapeHtml(item.source_type || "Manual note")}</span>
        ${(item.source_url || item.uploaded_filename) ? `<span>Source: ${projectEscapeHtml(item.source_url || item.uploaded_filename)}</span>` : ""}
        ${item.freshness_note ? `<span>Freshness: ${projectEscapeHtml(item.freshness_note)}</span>` : ""}
        <p>${projectEscapeHtml(item.summary || item.text_excerpt || "")}</p>
      </label>
    `;
    }).join("");

    evidenceList.querySelectorAll("[data-project-evidence-id]").forEach((input) => {
      input.addEventListener("change", () => {
        const evidenceId = input.getAttribute("data-project-evidence-id");
        if (!evidenceId) return;
        if (input.checked) {
          selectedEvidenceIds.add(evidenceId);
        } else {
          selectedEvidenceIds.delete(evidenceId);
        }
      });
    });
  }

  function renderRetrievedEvidenceQueue(items) {
    const queue = document.getElementById("retrieved-evidence-queue");
    if (!queue) return;

    if (!items.length) {
      queue.innerHTML = '<div class="empty">Retrieved evidence will appear here for review before acceptance.</div>';
      return;
    }

    queue.innerHTML = items.map((item, index) => `
      <label class="retrieved-evidence-item">
        <input type="checkbox" data-retrieved-index="${index}">
        <span class="tier-badge">${projectEscapeHtml(item.credibility_tier || "Tier unknown")}</span>
        <strong>${projectEscapeHtml(item.title)}</strong>
        <span>${projectEscapeHtml(item.source_name || "Unknown source")} - ${projectEscapeHtml(item.source_type || "Retrieved evidence")}</span>
        ${item.source_url ? `<a href="${projectEscapeHtml(item.source_url)}" target="_blank" rel="noreferrer">${projectEscapeHtml(item.source_url)}</a>` : ""}
        <span>Retrieved: ${projectEscapeHtml(item.retrieved_at || "")}${item.published_at ? ` - Published: ${projectEscapeHtml(item.published_at)}` : ""}</span>
        <span>${projectEscapeHtml(item.freshness_note || "")}</span>
        <p>${projectEscapeHtml(item.excerpt || "")}</p>
      </label>
    `).join("");
  }

  async function fetchEvidenceIntelligence(projectId) {
    const panel = document.getElementById("evidence-intelligence-panel");
    if (!panel) return;
    if (!projectId) {
      renderEvidenceIntelligenceEmptyState();
      return;
    }

    panel.innerHTML = '<div class="empty">Preparing evidence intelligence for reviewer triage...</div>';

    try {
      const response = await fetch(`${PROJECT_API_BASE}/projects/${projectId}/evidence/intelligence`);
      if (!response.ok) throw new Error("Evidence intelligence unavailable.");
      const data = await response.json();
      if (workspaceProject?.project_id !== projectId) return;
      renderEvidenceIntelligence(data);
    } catch (error) {
      renderEvidenceIntelligenceError("Could not load evidence intelligence. Existing evidence remains unchanged.");
    }
  }

  function renderEvidenceIntelligence(data) {
    const panel = document.getElementById("evidence-intelligence-panel");
    if (!panel) return;

    const summary = data?.summary || {};
    const total = Number(summary.total_evidence_count || 0);
    if (!total) {
      renderEvidenceIntelligenceEmptyState();
      return;
    }

    const relationships = data.relationships || [];
    const potentialConflicts = relationships.filter((item) => item.relationship === "potential_conflict");
    const possibleSupport = relationships.filter((item) => item.relationship === "supports");
    const novelty = (data.novelty || []).filter((item) => Number(item.novelty_score || 0) > 0);
    const coverage = data.coverage || {};
    const freshness = data.freshness || {};
    const decisionSignalsAvailable = Boolean(
      (data.traceable_signals || []).length ||
      (data.decision_risk_evidence_map || []).length ||
      (data.regulatory_constraint_flags || []).length ||
      (data.historical_pathway_signals || []).length
    );

    panel.innerHTML = `
      <div class="evidence-intelligence-summary">
        <div><strong>${projectEscapeHtml(total)}</strong><span>Evidence items</span></div>
        <div><strong>${projectEscapeHtml((data.attention_items || []).length)}</strong><span>Review recommended</span></div>
        <div><strong>${projectEscapeHtml((data.duplicate_groups || []).length)}</strong><span>Possible duplicate groups</span></div>
        <div><strong>${projectEscapeHtml(coverage.coverage_score ?? "0")}</strong><span>Coverage score</span></div>
      </div>
      ${decisionSignalsAvailable ? "" : '<div class="empty">No decision-grade evidence signals available yet. Add or accept more project evidence for reviewer triage.</div>'}
      ${renderEvidenceIntelligenceSection("Traceable Signals", renderTraceableSignals(data.traceable_signals || []))}
      ${renderEvidenceIntelligenceSection("Decision Risk Evidence Map", renderRiskSignals(data.decision_risk_evidence_map || []))}
      ${renderEvidenceIntelligenceSection("Regulatory / Legal Constraint Flags", renderRegulatoryFlags(data.regulatory_constraint_flags || []))}
      ${renderEvidenceIntelligenceSection("Historical Pathway Signals", renderHistoricalPathwaySignals(data.historical_pathway_signals || []))}
      ${renderEvidenceIntelligenceSection("Reviewer Attention Queue", renderAttentionItems(data.attention_items || []), true)}
      ${renderEvidenceIntelligenceSection("Duplicate / Near-Duplicate Evidence", renderDuplicateGroups(data.duplicate_groups || []))}
      ${renderEvidenceIntelligenceSection("Potential Conflicts", renderRelationships(potentialConflicts, "Potential conflict"))}
      ${renderEvidenceIntelligenceSection("Possible Support Relationships", renderRelationships(possibleSupport, "May support"))}
      ${renderEvidenceIntelligenceSection("Novel Evidence", renderNoveltyItems(novelty))}
      ${renderEvidenceIntelligenceSection("Coverage Summary", renderCoverageSummary(coverage))}
      ${renderEvidenceIntelligenceSection("Freshness / Staleness", renderFreshnessSummary(freshness))}
      ${renderEvidenceIntelligenceSection("Source Diversity", renderSourceDiversity(summary.source_type_counts || {}, total))}
    `;
    bindEvidenceJumpLinks(panel);
  }

  function renderEvidenceIntelligenceEmptyState() {
    const panel = document.getElementById("evidence-intelligence-panel");
    if (!panel) return;
    panel.innerHTML = '<div class="empty">No evidence intelligence available yet. Add or accept project evidence to review duplicates, conflicts, freshness, and coverage.</div>';
  }

  function renderEvidenceIntelligenceError(message) {
    const panel = document.getElementById("evidence-intelligence-panel");
    if (!panel) return;
    panel.innerHTML = `<div class="empty error-state">${projectEscapeHtml(message || "Could not load evidence intelligence.")}</div>`;
  }

  function renderEvidenceIntelligenceSection(title, body, open = false) {
    return `
      <details class="evidence-intelligence-section"${open ? " open" : ""}>
        <summary>${projectEscapeHtml(title)}</summary>
        <div class="evidence-intelligence-body">${body}</div>
      </details>
    `;
  }

  function renderAttentionItems(items) {
    if (!items.length) return '<div class="empty">No review recommendations at this time.</div>';
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>Review recommended: ${projectEscapeHtml(item.evidence_id || "Unknown evidence")}</strong>
        <span>${projectEscapeHtml((item.reasons || []).join(", ") || "Needs reviewer attention")}</span>
        ${renderEvidenceRefs(item.evidence_ref ? [item.evidence_ref] : [], "Triggered by")}
      </div>
    `).join("");
  }

  function renderDuplicateGroups(groups) {
    if (!groups.length) return '<div class="empty">No possible duplicates detected.</div>';
    return groups.map((group) => `
      <div class="intelligence-item">
        <strong>Possible duplicate: ${projectEscapeHtml(group.primary_evidence_id || "Primary evidence")}</strong>
        <span>${projectEscapeHtml(group.duplicate_reason || "Duplicate signal")}</span>
        <span>Also review: ${projectEscapeHtml((group.duplicate_evidence_ids || []).join(", ") || "None")}</span>
        ${renderEvidenceRefs(group.evidence_refs || [], "Related evidence")}
      </div>
    `).join("");
  }

  function renderRelationships(items, label) {
    if (!items.length) return `<div class="empty">No ${projectEscapeHtml(label.toLowerCase())} signals detected.</div>`;
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(label)}: ${projectEscapeHtml((item.evidence_ids || []).join(" / "))}</strong>
        <span>${projectEscapeHtml(item.rationale || "Reviewer should inspect this relationship.")}</span>
        ${renderEvidenceRefs(item.evidence_refs || [], "Related evidence")}
      </div>
    `).join("");
  }

  function renderNoveltyItems(items) {
    if (!items.length) return '<div class="empty">No novelty signals detected.</div>';
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>May introduce new context: ${projectEscapeHtml(item.evidence_id || "Unknown evidence")}</strong>
        <span>Novelty: ${projectEscapeHtml(item.novelty_score ?? "0")}</span>
        <span>${projectEscapeHtml((item.novelty_reasons || []).join(", ") || "No novelty reasons listed")}</span>
        ${renderEvidenceRefs(item.evidence_ref ? [item.evidence_ref] : [], "Triggered by")}
      </div>
    `).join("");
  }

  function renderTraceableSignals(items) {
    if (!items.length) return '<div class="empty">No traceable signals detected.</div>';
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(item.label || "Review recommended")}</strong>
        <span>${projectEscapeHtml(item.reviewer_note || "Reviewer should inspect the related evidence.")}</span>
        ${renderEvidenceRefs(item.evidence_refs || [], "Triggered by")}
      </div>
    `).join("");
  }

  function renderRiskSignals(items) {
    if (!items.length) return '<div class="empty">No decision risk evidence signals detected.</div>';
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>Risk exposure evidence: ${projectEscapeHtml((item.risk_category || "unknown").replaceAll("_", " "))}</strong>
        <span>Confidence: ${projectEscapeHtml(item.confidence_bucket || "low")}</span>
        <span>Matched terms: ${projectEscapeHtml((item.matched_terms || []).join(", ") || "None listed")}</span>
        <p>${projectEscapeHtml(item.reviewer_explanation || "Review recommended.")}</p>
        <p>${projectEscapeHtml(item.limitation_note || "Reviewer should verify context and source quality.")}</p>
        ${renderEvidenceRefs(item.evidence_refs || [], "Triggered by")}
      </div>
    `).join("");
  }

  function renderRegulatoryFlags(items) {
    if (!items.length) return '<div class="empty">No regulatory or legal constraint flags detected.</div>';
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>Potential review flag: ${projectEscapeHtml((item.constraint_category || "unknown").replaceAll("_", " "))}</strong>
        <span>Triggering terms: ${projectEscapeHtml((item.triggering_terms || []).join(", ") || "None listed")}</span>
        <p>${projectEscapeHtml(item.reviewer_note || "May require legal / compliance review. Not legal advice.")}</p>
        <p>${projectEscapeHtml(item.limitation_note || "Reviewer should verify jurisdiction and applicability.")}</p>
        ${renderEvidenceRefs(item.evidence_refs || [], "Triggered by")}
      </div>
    `).join("");
  }

  function renderHistoricalPathwaySignals(items) {
    if (!items.length) return '<div class="empty">No historical pathway signals detected.</div>';
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>Possible pathway: ${projectEscapeHtml((item.pathway_family || "unknown").replaceAll("_", " "))}</strong>
        <span>Triggering terms: ${projectEscapeHtml((item.triggering_terms || []).join(", ") || "None listed")}</span>
        <span>Related risks: ${projectEscapeHtml((item.related_risk_categories || []).join(", ") || "None linked")}</span>
        <p>${projectEscapeHtml(item.reviewer_explanation || "Reviewer should compare similar historical pathways.")}</p>
        <p>${projectEscapeHtml(item.historical_analogue_hint || "")}</p>
        <p>${projectEscapeHtml(item.limitation_note || "No probability is assigned.")}</p>
        ${renderEvidenceRefs(item.evidence_refs || [], "Related evidence")}
      </div>
    `).join("");
  }

  function renderEvidenceRefs(refs, label) {
    if (!refs.length) return "";
    return `
      <div class="evidence-ref-list" aria-label="${projectEscapeHtml(label)}">
        <span class="evidence-ref-heading">${projectEscapeHtml(label)}</span>
        ${refs.map((ref) => {
          const domId = projectDomId(ref.evidence_id);
          return `
            <div class="evidence-ref">
              <span><strong>${projectEscapeHtml(ref.title || "Untitled evidence")}</strong></span>
              <span>${projectEscapeHtml(ref.source || "Unknown source")}${ref.date ? ` - ${projectEscapeHtml(ref.date)}` : ""}</span>
              ${ref.source_url ? `<a href="${projectEscapeHtml(ref.source_url)}" target="_blank" rel="noreferrer">${projectEscapeHtml(ref.source_url)}</a>` : ""}
              ${domId ? `<button type="button" class="evidence-ref-link" data-jump-evidence-id="${projectEscapeHtml(domId)}">Jump to evidence</button>` : ""}
            </div>
          `;
        }).join("")}
      </div>
    `;
  }

  function bindEvidenceJumpLinks(panel) {
    panel.querySelectorAll("[data-jump-evidence-id]").forEach((button) => {
      button.addEventListener("click", () => {
        const domId = button.getAttribute("data-jump-evidence-id");
        const target = document.getElementById(`evidence-card-${domId}`);
        if (!target) return;
        target.scrollIntoView({behavior: "smooth", block: "center"});
        target.classList.add("highlight-evidence-card");
        window.setTimeout(() => target.classList.remove("highlight-evidence-card"), 1600);
      });
    });
  }

  function renderCoverageSummary(coverage) {
    const missing = coverage.missing_categories || [];
    return `
      <div class="intelligence-item">
        <strong>Coverage score: ${projectEscapeHtml(coverage.coverage_score ?? "0")}</strong>
        <span>Covered: ${projectEscapeHtml((coverage.covered_categories || []).join(", ") || "Unknown")}</span>
        <span>Coverage gap: ${projectEscapeHtml(missing.slice(0, 6).join(", ") || "No major category gaps detected")}</span>
        <p>${projectEscapeHtml(coverage.reviewer_recommendation || "Reviewer should inspect source coverage.")}</p>
      </div>
    `;
  }

  function renderFreshnessSummary(freshness) {
    return `
      <div class="intelligence-item">
        <strong>Freshness risk: ${projectEscapeHtml(freshness.freshness_risk || "Unknown")}</strong>
        <span>Current: ${projectEscapeHtml((freshness.current_items || []).join(", ") || "None")}</span>
        <span>Stale evidence: ${projectEscapeHtml((freshness.stale_items || []).join(", ") || "None")}</span>
        <span>Missing dates: ${projectEscapeHtml((freshness.missing_date_items || []).join(", ") || "None")}</span>
      </div>
    `;
  }

  function renderSourceDiversity(sourceTypeCounts, total) {
    const entries = Object.entries(sourceTypeCounts);
    if (!entries.length) return '<div class="empty">Source diversity is unavailable.</div>';
    const sorted = entries.sort((a, b) => Number(b[1]) - Number(a[1]));
    const top = sorted[0];
    const concentration = total ? Number(top[1]) / total : 0;
    const risk = concentration >= 0.6 ? "Source concentration risk" : "Source diversity appears mixed";
    return `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(risk)}</strong>
        <span>Largest category: ${projectEscapeHtml(top[0])} (${projectEscapeHtml(top[1])})</span>
        <span>${projectEscapeHtml(sorted.map(([name, count]) => `${name}: ${count}`).join(" | "))}</span>
      </div>
    `;
  }

  async function fetchDecisionReadiness(projectId) {
    const panel = document.getElementById("decision-readiness-panel");
    if (!panel) return;
    if (!projectId) {
      renderDecisionReadinessEmptyState();
      return;
    }

    panel.innerHTML = '<div class="empty">Preparing decision readiness map for reviewer inspection...</div>';

    try {
      const response = await fetch(`${PROJECT_API_BASE}/projects/${projectId}/decision/readiness`);
      if (!response.ok) throw new Error("Decision readiness unavailable.");
      const data = await response.json();
      if (workspaceProject?.project_id !== projectId) return;
      renderDecisionReadiness(data);
    } catch (error) {
      renderDecisionReadinessError("Could not load decision readiness. Project evidence and review state were not changed.");
    }
  }

  function renderDecisionReadiness(data) {
    const panel = document.getElementById("decision-readiness-panel");
    if (!panel) return;

    const summary = data?.readiness_summary || {};
    if (!data?.decision_question && !Number(summary.evidence_count || 0)) {
      renderDecisionReadinessEmptyState();
      return;
    }

    panel.innerHTML = `
      <div class="evidence-intelligence-summary">
        <div><strong>${projectEscapeHtml(readinessLabel(summary.readiness_state || "unknown"))}</strong><span>Readiness</span></div>
        <div><strong>${projectEscapeHtml(summary.framework_count || 0)}</strong><span>Frameworks</span></div>
        <div><strong>${projectEscapeHtml(summary.evidence_count || 0)}</strong><span>Evidence items</span></div>
        <div><strong>${projectEscapeHtml(summary.issue_count || 0)}</strong><span>Review issues</span></div>
      </div>
      <div class="intelligence-item">
        <strong>Readiness Summary</strong>
        <p>${projectEscapeHtml(summary.reviewer_summary || "Decision readiness is unavailable.")}</p>
        <p>${projectEscapeHtml(summary.limitation || "Readiness is not a recommendation.")}</p>
      </div>
      ${renderEvidenceIntelligenceSection("Applicable Frameworks", renderReadinessFrameworks(data.applicable_frameworks || []), true)}
      ${renderEvidenceIntelligenceSection("Evidence Coverage by Framework", renderFrameworkEvidenceCoverage(data.framework_evidence_maps || []))}
      ${renderEvidenceIntelligenceSection("Key Evidence Gaps", renderReadinessIssues(data.evidence_gaps || [], "No key evidence gaps detected."))}
      ${renderEvidenceIntelligenceSection("Risk / Constraint Coverage", renderRiskConstraintCoverage(data.risk_coverage || [], data.constraint_coverage || []))}
      ${renderEvidenceIntelligenceSection("Historical Support", renderHistoricalSupport(data.historical_support || []))}
      ${renderEvidenceIntelligenceSection("Assumptions & Unknowns", renderAssumptionsAndUnknowns(data.assumption_map || [], data.unknowns_map || []))}
      ${renderEvidenceIntelligenceSection("Reviewer Questions", renderReadinessQuestions(data.reviewer_questions || []))}
      ${renderEvidenceIntelligenceSection("Readiness Issues", renderReadinessIssues(data.readiness_issues || [], "No readiness blockers detected."))}
    `;
    bindEvidenceJumpLinks(panel);
  }

  function renderDecisionReadinessEmptyState() {
    const panel = document.getElementById("decision-readiness-panel");
    if (!panel) return;
    panel.innerHTML = '<div class="empty">No decision readiness available yet. Add a question and accepted evidence to surface assumptions, unknowns, and evidence gaps.</div>';
  }

  function renderDecisionReadinessError(message) {
    const panel = document.getElementById("decision-readiness-panel");
    if (!panel) return;
    panel.innerHTML = `<div class="empty error-state">${projectEscapeHtml(message || "Could not load decision readiness.")}</div>`;
  }

  function readinessLabel(value) {
    return String(value || "unknown").replaceAll("_", " ");
  }

  function renderReadinessFrameworks(items) {
    if (!items.length) return '<div class="empty">No applicable frameworks identified yet. Add evidence that clarifies risks, constraints, or decision criteria.</div>';
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(item.name || item.framework_id || "Framework")}</strong>
        <span>${projectEscapeHtml(item.framework_id || "")}</span>
        <p>${projectEscapeHtml(item.description || "")}</p>
      </div>
    `).join("");
  }

  function renderFrameworkEvidenceCoverage(maps) {
    if (!maps.length) return '<div class="empty">No framework evidence coverage available.</div>';
    return maps.map((item) => {
      const categories = item.evidence_coverage?.required_evidence_categories || [];
      return `
        <div class="intelligence-item">
          <strong>${projectEscapeHtml(item.framework_name || item.framework_id || "Framework")}</strong>
          ${categories.map((category) => `
            <span>${projectEscapeHtml(category.dimension)}: ${projectEscapeHtml(readinessLabel(category.coverage_bucket))}</span>
            ${renderEvidenceRefs(category.evidence_refs || [], "Related evidence")}
          `).join("")}
        </div>
      `;
    }).join("");
  }

  function renderRiskConstraintCoverage(risks, constraints) {
    const riskItems = risks.flatMap((item) => item.risks || []);
    const constraintItems = constraints.flatMap((item) => item.constraints || []);
    if (!riskItems.length && !constraintItems.length) return '<div class="empty">No risk or constraint coverage available.</div>';
    return `
      ${riskItems.map((item) => renderCoverageItem("Risk", item)).join("")}
      ${constraintItems.map((item) => renderCoverageItem("Constraint", item)).join("")}
    `;
  }

  function renderHistoricalSupport(items) {
    const dimensions = items.flatMap((item) => item.historical_dimensions || []);
    if (!dimensions.length) return '<div class="empty">No historical support map available.</div>';
    return dimensions.map((item) => renderCoverageItem("Historical support", item)).join("");
  }

  function renderCoverageItem(label, item) {
    return `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(label)}: ${projectEscapeHtml(item.dimension || "Unknown")}</strong>
        <span>${projectEscapeHtml(readinessLabel(item.coverage_bucket || "unknown"))}</span>
        <p>${projectEscapeHtml(item.reviewer_note || "Reviewer should verify this coverage.")}</p>
        ${renderEvidenceRefs(item.evidence_refs || [], "Related evidence")}
      </div>
    `;
  }

  function renderAssumptionsAndUnknowns(assumptions, unknowns) {
    if (!assumptions.length && !unknowns.length) return '<div class="empty">No assumptions or unknowns mapped yet. Reviewers can add evidence to make unresolved issues visible.</div>';
    return `
      ${assumptions.map((item) => `
        <div class="intelligence-item">
          <strong>Assumption: ${projectEscapeHtml(readinessLabel(item.category))}</strong>
          <p>${projectEscapeHtml(item.explanation || "")}</p>
          <span>${projectEscapeHtml(item.reviewer_question || "")}</span>
          ${renderEvidenceRefs(item.evidence_refs || [], "Related evidence")}
        </div>
      `).join("")}
      ${unknowns.map((item) => `
        <div class="intelligence-item">
          <strong>Unknown: ${projectEscapeHtml(readinessLabel(item.category))}</strong>
          <p>${projectEscapeHtml(item.explanation || "")}</p>
          <span>${projectEscapeHtml(item.reviewer_question || "")}</span>
          ${renderEvidenceRefs(item.evidence_refs || [], "Related evidence")}
        </div>
      `).join("")}
    `;
  }

  function renderReadinessQuestions(items) {
    if (!items.length) return '<div class="empty">No reviewer questions generated yet. Add accepted evidence to expose gaps that need human judgment.</div>';
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(item.question || "Reviewer question")}</strong>
        <span>${projectEscapeHtml(item.source || "readiness")}${item.related_framework_id ? ` - ${projectEscapeHtml(item.related_framework_id)}` : ""}</span>
        ${renderEvidenceRefs(item.evidence_refs || [], "Related evidence")}
      </div>
    `).join("");
  }

  function renderReadinessIssues(items, emptyMessage) {
    if (!items.length) return `<div class="empty">${projectEscapeHtml(emptyMessage)}</div>`;
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(readinessLabel(item.issue_type || "review issue"))}</strong>
        <span>Severity: ${projectEscapeHtml(item.severity || "review")}</span>
        <p>${projectEscapeHtml(item.explanation || "Reviewer should verify this issue.")}</p>
        <span>${projectEscapeHtml(item.reviewer_question || "")}</span>
        ${renderEvidenceRefs(item.evidence_refs || [], "Related evidence")}
      </div>
    `).join("");
  }

  async function fetchDecisionPathways(projectId) {
    const panel = document.getElementById("decision-pathways-panel");
    if (!panel) return;
    if (!projectId) {
      renderDecisionPathwaysEmptyState();
      return;
    }

    panel.innerHTML = '<div class="empty">Preparing pathway drafts for reviewer comparison...</div>';

    try {
      const response = await fetch(`${PROJECT_API_BASE}/projects/${projectId}/decision/pathways`);
      if (!response.ok) throw new Error("Decision pathway drafts unavailable.");
      const data = await response.json();
      if (workspaceProject?.project_id !== projectId) return;
      renderDecisionPathways(data);
    } catch (error) {
      renderDecisionPathwaysError("Could not load decision pathway drafts. No pathway was selected or recommended.");
    }
  }

  function renderDecisionPathways(data) {
    const panel = document.getElementById("decision-pathways-panel");
    if (!panel) return;

    const drafts = data?.pathway_drafts || [];
    if (!drafts.length) {
      renderDecisionPathwaysEmptyState();
      return;
    }

    panel.innerHTML = `
      <div class="evidence-intelligence-summary">
        <div><strong>${projectEscapeHtml(drafts.length)}</strong><span>Drafts</span></div>
        <div><strong>${projectEscapeHtml(readinessLabel(data.readiness_state || "unknown"))}</strong><span>Readiness</span></div>
        <div><strong>${projectEscapeHtml(data.primary_framework?.name || "Framework")}</strong><span>Primary framework</span></div>
        <div><strong>Read-only</strong><span>Reviewer comparison</span></div>
      </div>
      <div class="intelligence-item">
        <strong>Pathway Draft Boundary</strong>
        <p>${projectEscapeHtml(data.generation_note || "Pathway drafts are not recommendations.")}</p>
        ${(data.limitation_notes || []).map((note) => `<span>${projectEscapeHtml(note)}</span>`).join("")}
      </div>
      ${drafts.map((draft, index) => renderPathwayDraft(draft, index === 0)).join("")}
    `;
    bindEvidenceJumpLinks(panel);
  }

  function renderPathwayDraft(draft, open) {
    const title = draft.title || "Possible pathway";
    const body = `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(title)}</strong>
        <span>Family: ${projectEscapeHtml(readinessLabel(draft.pathway_family || "unknown"))}</span>
        <p>${projectEscapeHtml(draft.description || "This pathway would require reviewer validation.")}</p>
        ${renderEvidenceRefs(draft.supporting_evidence_refs || [], "Supporting evidence")}
      </div>
      ${renderEvidenceIntelligenceSection("Risks / Constraints", renderPathwayListBlock([
        ["Risks", draft.related_risk_categories || []],
        ["Constraints", draft.related_constraints || []],
      ]))}
      ${renderEvidenceIntelligenceSection("Assumptions", renderSimpleList(draft.assumptions || [], "No assumptions listed."))}
      ${renderEvidenceIntelligenceSection("Unknowns", renderSimpleList(draft.unknowns || [], "No unknowns listed."))}
      ${renderEvidenceIntelligenceSection("Decision Triggers", renderSimpleList(draft.decision_triggers || [], "No decision triggers listed."))}
      ${renderEvidenceIntelligenceSection("Reviewer Questions", renderSimpleList(draft.reviewer_questions || [], "No reviewer questions listed."))}
      ${renderEvidenceIntelligenceSection("Limitations", renderSimpleList(draft.limitation_notes || [], "No limitation notes listed."))}
      ${renderEvidenceRefs(draft.historical_support_refs || [], "Historical support")}
    `;
    return renderEvidenceIntelligenceSection(title, body, open);
  }

  function renderPathwayListBlock(groups) {
    return groups.map(([label, items]) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(label)}</strong>
        <span>${projectEscapeHtml(items.length ? items.map(readinessLabel).join(", ") : "None mapped")}</span>
      </div>
    `).join("");
  }

  function renderSimpleList(items, emptyMessage) {
    if (!items.length) return `<div class="empty">${projectEscapeHtml(emptyMessage)}</div>`;
    return items.map((item) => `
      <div class="intelligence-item">
        <span>${projectEscapeHtml(item)}</span>
      </div>
    `).join("");
  }

  function renderDecisionPathwaysEmptyState() {
    const panel = document.getElementById("decision-pathways-panel");
    if (!panel) return;
    panel.innerHTML = '<div class="empty">No pathway drafts available yet. Add a question and accepted evidence to compare possible reviewer-validated paths.</div>';
  }

  function renderDecisionPathwaysError(message) {
    const panel = document.getElementById("decision-pathways-panel");
    if (!panel) return;
    panel.innerHTML = `<div class="empty error-state">${projectEscapeHtml(message || "Could not load decision pathway drafts.")}</div>`;
  }

  async function fetchPathwayComparison(projectId) {
    const panel = document.getElementById("pathway-comparison-panel");
    if (!panel) return;
    if (!projectId) {
      renderPathwayComparisonEmptyState();
      return;
    }

    panel.innerHTML = '<div class="empty">Preparing pathway comparison matrix for reviewer inspection...</div>';

    try {
      const response = await fetch(`${PROJECT_API_BASE}/projects/${projectId}/decision/pathway-comparison`);
      if (!response.ok) throw new Error("Pathway comparison unavailable.");
      const data = await response.json();
      if (workspaceProject?.project_id !== projectId) return;
      renderPathwayComparison(data);
    } catch (error) {
      renderPathwayComparisonError("Could not load pathway comparison matrix. No ranking or selection was created.");
    }
  }

  function renderPathwayComparison(data) {
    const panel = document.getElementById("pathway-comparison-panel");
    if (!panel) return;
    const rows = data?.pathway_comparisons || [];
    if (!rows.length) {
      renderPathwayComparisonEmptyState();
      return;
    }

    panel.innerHTML = `
      <div class="evidence-intelligence-summary">
        <div><strong>${projectEscapeHtml(rows.length)}</strong><span>Pathways</span></div>
        <div><strong>${projectEscapeHtml((data.comparison_dimensions || []).length)}</strong><span>Dimensions</span></div>
        <div><strong>Categorical</strong><span>No scores</span></div>
        <div><strong>Read-only</strong><span>No selection</span></div>
      </div>
      <div class="intelligence-item">
        <strong>Comparison Boundary</strong>
        <p>${projectEscapeHtml(data.generation_note || "Comparison matrix is not a recommendation.")}</p>
        ${(data.limitation_notes || []).map((note) => `<span>${projectEscapeHtml(note)}</span>`).join("")}
      </div>
      ${renderEvidenceIntelligenceSection("Side-by-Side Matrix", renderComparisonMatrix(rows), true)}
      ${rows.map((row) => renderComparisonRow(row)).join("")}
    `;
    bindEvidenceJumpLinks(panel);
  }

  function renderComparisonMatrix(rows) {
    const dimensions = [
      ["Evidence support", "evidence_support"],
      ["Key risks", "risk_exposure"],
      ["Regulatory constraints", "regulatory_constraints"],
      ["Domain-specific concerns", "domain_specific_risks"],
      ["Historical support", "historical_support"],
      ["Assumptions", "assumptions_required"],
      ["Unknowns", "unknowns_remaining"],
      ["Execution complexity", "execution_complexity"],
      ["Reversibility", "reversibility"],
      ["Timing sensitivity", "timing_sensitivity"],
      ["Evidence quality concerns", "evidence_quality_concerns"],
    ];
    return `
      <div class="comparison-table" role="table" aria-label="Pathway comparison matrix">
        <div class="comparison-row comparison-row-header" role="row">
          <strong role="columnheader">Dimension</strong>
          ${rows.map((row) => `<strong role="columnheader">${projectEscapeHtml(row.pathway_title || row.pathway_family || "Pathway")}</strong>`).join("")}
        </div>
        ${dimensions.map(([label, key]) => `
          <div class="comparison-row" role="row">
            <span role="cell">${projectEscapeHtml(label)}</span>
            ${rows.map((row) => `<span role="cell">${projectEscapeHtml(readinessLabel(row.dimension_buckets?.[key] || "unknown"))}</span>`).join("")}
          </div>
        `).join("")}
      </div>
    `;
  }

  function renderComparisonRow(row) {
    const body = `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(row.pathway_title || "Possible pathway")}</strong>
        <span>Family: ${projectEscapeHtml(readinessLabel(row.pathway_family || "unknown"))}</span>
        <p>${projectEscapeHtml(row.evidence_support_summary || "")}</p>
        ${renderEvidenceRefs(row.supporting_evidence_refs || [], "Supporting evidence")}
      </div>
      ${renderEvidenceIntelligenceSection("Key Risks", renderComparisonText(row.risk_exposure_summary))}
      ${renderEvidenceIntelligenceSection("Regulatory Constraints", renderComparisonText(row.regulatory_constraint_summary))}
      ${renderEvidenceIntelligenceSection("Domain-Specific Concerns", renderComparisonText(row.domain_evaluation_summary))}
      ${renderEvidenceIntelligenceSection("Historical Support", renderComparisonText(row.historical_support_summary))}
      ${renderEvidenceIntelligenceSection("Assumptions", renderComparisonText(row.assumptions_summary))}
      ${renderEvidenceIntelligenceSection("Unknowns", renderComparisonText(row.unknowns_summary))}
      ${renderEvidenceIntelligenceSection("Decision Triggers", renderSimpleList(row.decision_triggers || [], "No decision triggers listed."))}
      ${renderEvidenceIntelligenceSection("Reviewer Questions", renderSimpleList(row.reviewer_questions || [], "No reviewer questions listed."))}
      ${renderEvidenceIntelligenceSection("Limitations", renderSimpleList(row.limitation_notes || [], "No limitation notes listed."))}
    `;
    return renderEvidenceIntelligenceSection(row.pathway_title || "Pathway comparison", body);
  }

  function renderComparisonText(text) {
    return `
      <div class="intelligence-item">
        <p>${projectEscapeHtml(text || "No comparison detail available.")}</p>
      </div>
    `;
  }

  function renderPathwayComparisonEmptyState() {
    const panel = document.getElementById("pathway-comparison-panel");
    if (!panel) return;
    panel.innerHTML = '<div class="empty">No pathway comparison available yet. Generate pathway drafts before reviewing side-by-side trade-offs.</div>';
  }

  function renderPathwayComparisonError(message) {
    const panel = document.getElementById("pathway-comparison-panel");
    if (!panel) return;
    panel.innerHTML = `<div class="empty error-state">${projectEscapeHtml(message || "Could not load pathway comparison matrix.")}</div>`;
  }

  async function fetchDecisionReview(projectId) {
    const panel = document.getElementById("decision-review-panel");
    if (!panel) return;
    if (!projectId) {
      renderDecisionReviewEmptyState();
      return;
    }

    panel.innerHTML = '<div class="empty">Loading reviewer-controlled decision review state...</div>';

    try {
      const response = await fetch(`${PROJECT_API_BASE}/projects/${projectId}/decision/review`);
      if (!response.ok) throw new Error("Decision review unavailable.");
      const data = await response.json();
      if (workspaceProject?.project_id !== projectId) return;
      renderDecisionReview(data);
    } catch (error) {
      renderDecisionReviewError("Could not load decision review state. Existing notes were not changed.");
    }
  }

  function renderDecisionReview(data) {
    const panel = document.getElementById("decision-review-panel");
    if (!panel) return;
    const summary = data?.review_summary || {};
    panel.innerHTML = `
      <div class="evidence-intelligence-summary">
        <div><strong>${projectEscapeHtml(summary.reviewed_pathways_count || 0)}</strong><span>Reviewed pathways</span></div>
        <div><strong>${projectEscapeHtml(summary.unresolved_issues_count || 0)}</strong><span>Unresolved items</span></div>
        <div><strong>${projectEscapeHtml(summary.needs_more_evidence_count || 0)}</strong><span>Needs evidence</span></div>
        <div><strong>${projectEscapeHtml(summary.needs_legal_or_compliance_review_count || 0)}</strong><span>Compliance review</span></div>
      </div>
      <div class="intelligence-item">
        <strong>Review Boundary</strong>
        <p>Review state records reviewer interpretation only. It does not select a pathway, alter evidence, or change the Decision Brief.</p>
      </div>
      ${renderDecisionReviewForm()}
      ${renderEvidenceIntelligenceSection("Recorded Review Items", renderDecisionReviewItems(data))}
      ${renderEvidenceIntelligenceSection("Reviewer Notes", renderReviewerNotes(data.reviewer_notes || []))}
      ${renderEvidenceIntelligenceSection("Unresolved Questions", renderUnresolvedQuestions(data.unresolved_questions || []))}
    `;
    bindDecisionReviewForm(panel);
  }

  function renderDecisionReviewForm() {
    return `
      <div class="decision-review-form">
        <label for="review-target-type">Review item</label>
        <select id="review-target-type" class="project-input">
          <option value="pathway">Pathway</option>
          <option value="comparison_cell">Comparison cell</option>
          <option value="assumption">Assumption</option>
          <option value="unknown">Unknown</option>
          <option value="decision_trigger">Decision trigger</option>
        </select>
        <label for="review-target-id">Item ID</label>
        <input id="review-target-id" class="project-input" type="text" placeholder="Pathway ID, assumption ID, or item label">
        <label for="review-comparison-dimension">Comparison dimension</label>
        <input id="review-comparison-dimension" class="project-input" type="text" placeholder="Only for comparison cell reviews">
        <label for="review-status-select">Review status</label>
        <select id="review-status-select" class="project-input">
          <option value="reviewed">Mark reviewed</option>
          <option value="accepted_for_consideration">Accepted for consideration</option>
          <option value="questioned">Questioned</option>
          <option value="needs_more_evidence">Needs more evidence</option>
          <option value="needs_legal_or_compliance_review">Needs compliance review</option>
          <option value="unresolved">Unresolved</option>
          <option value="not_reviewed">Not reviewed</option>
        </select>
        <label for="reviewer-note-input">Add reviewer note</label>
        <textarea id="reviewer-note-input" class="question-input" placeholder="Short reviewer note..."></textarea>
        <label for="unresolved-question-input">Unresolved question</label>
        <input id="unresolved-question-input" class="project-input" type="text" placeholder="Optional unresolved decision question">
        <button id="save-decision-review-button" type="button">Save Review State</button>
      </div>
    `;
  }

  function bindDecisionReviewForm(panel) {
    const button = panel.querySelector("#save-decision-review-button");
    if (!button) return;
    button.addEventListener("click", saveDecisionReviewState);
  }

  async function saveDecisionReviewState() {
    if (!workspaceProject) {
      alert("Create or select a project first.");
      return;
    }
    const targetType = document.getElementById("review-target-type")?.value || "pathway";
    const targetId = document.getElementById("review-target-id")?.value.trim() || "";
    const comparisonDimension = document.getElementById("review-comparison-dimension")?.value.trim() || "";
    const reviewStatus = document.getElementById("review-status-select")?.value || "reviewed";
    const reviewerNote = document.getElementById("reviewer-note-input")?.value.trim() || "";
    const unresolvedQuestion = document.getElementById("unresolved-question-input")?.value.trim() || "";

    if (!targetId) {
      alert("Enter an item ID or label to review.");
      return;
    }

    const response = await fetch(`${PROJECT_API_BASE}/projects/${workspaceProject.project_id}/decision/review`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        target_type: targetType,
        target_id: targetId,
        comparison_dimension: comparisonDimension,
        review_status: reviewStatus,
        reviewer_note: reviewerNote,
        unresolved_question: unresolvedQuestion,
      }),
    });

    if (!response.ok) {
      alert("Could not save review state.");
      return;
    }

    const data = await response.json();
    renderDecisionReview(data);
  }

  function renderDecisionReviewItems(data) {
    const items = [
      ...(data.pathway_reviews || []).map((item) => ({...item, label: item.pathway_id, type: "Pathway"})),
      ...(data.comparison_cell_reviews || []).map((item) => ({...item, label: `${item.pathway_id} / ${item.comparison_dimension}`, type: "Comparison cell"})),
      ...(data.assumption_reviews || []).map((item) => ({...item, label: item.assumption_id, type: "Assumption"})),
      ...(data.unknown_reviews || []).map((item) => ({...item, label: item.unknown_id, type: "Unknown"})),
      ...(data.trigger_reviews || []).map((item) => ({...item, label: item.trigger_id, type: "Decision trigger"})),
    ];
    if (!items.length) return '<div class="empty">No review items recorded yet. Mark items only after reviewer inspection.</div>';
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(item.type)}: ${projectEscapeHtml(item.label || "Review item")}</strong>
        <span>Status: ${projectEscapeHtml(readinessLabel(item.review_status || "not_reviewed"))}</span>
        <span>Updated: ${projectEscapeHtml(item.updated_at || item.created_at || "")}</span>
        <p>${projectEscapeHtml(item.reviewer_note || "No reviewer note recorded.")}</p>
        ${renderEvidenceRefs(item.related_evidence_refs || [], "Related evidence")}
      </div>
    `).join("");
  }

  function renderReviewerNotes(items) {
    if (!items.length) return '<div class="empty">No reviewer notes recorded yet. Add notes when human judgment, evidence needs, or compliance review should be preserved.</div>';
    return items.slice(-8).reverse().map((item) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(item.target_type || "Review note")}: ${projectEscapeHtml(item.target_id || "")}</strong>
        <span>${projectEscapeHtml(item.created_at || "")}</span>
        <p>${projectEscapeHtml(item.note || "")}</p>
      </div>
    `).join("");
  }

  function renderUnresolvedQuestions(items) {
    if (!items.length) return '<div class="empty">No unresolved decision questions recorded yet. Add questions when reviewers need more evidence or interpretation.</div>';
    return items.slice(-8).reverse().map((item) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(item.question || "Unresolved question")}</strong>
        <span>${projectEscapeHtml(item.target_type || "")}: ${projectEscapeHtml(item.target_id || "")}</span>
        <span>${projectEscapeHtml(item.created_at || "")}</span>
        ${renderEvidenceRefs(item.related_evidence_refs || [], "Related evidence")}
      </div>
    `).join("");
  }

  function renderDecisionReviewEmptyState() {
    const panel = document.getElementById("decision-review-panel");
    if (!panel) return;
    panel.innerHTML = '<div class="empty">No reviewer notes yet. Record reviewed items, open questions, or evidence needs when ready.</div>';
  }

  function renderDecisionReviewError(message) {
    const panel = document.getElementById("decision-review-panel");
    if (!panel) return;
    panel.innerHTML = `<div class="empty error-state">${projectEscapeHtml(message || "Could not load decision review state.")}</div>`;
  }

  async function fetchDomainEvaluation(projectId) {
    const panel = document.getElementById("domain-evaluation-panel");
    if (!panel) return;
    if (!projectId) {
      renderDomainEvaluationEmptyState();
      return;
    }

    panel.innerHTML = '<div class="empty">Preparing domain evaluation for reviewer inspection...</div>';

    try {
      const response = await fetch(`${PROJECT_API_BASE}/projects/${projectId}/decision/domain-evaluation`);
      if (!response.ok) throw new Error("Domain evaluation unavailable.");
      const data = await response.json();
      if (workspaceProject?.project_id !== projectId) return;
      renderDomainEvaluation(data);
    } catch (error) {
      renderDomainEvaluationError("Could not load domain decision evaluation. Existing evidence and analysis remain unchanged.");
    }
  }

  function renderDomainEvaluation(data) {
    const panel = document.getElementById("domain-evaluation-panel");
    if (!panel) return;
    const results = data?.results || [];
    if (!results.length) {
      renderDomainEvaluationEmptyState();
      return;
    }

    const dimensions = results.flatMap((item) => item.evaluation_dimensions || []);
    const mapped = dimensions.filter((item) => item.status === "mapped").length;
    const issues = results.flatMap((item) => item.issues || []);

    panel.innerHTML = `
      <div class="evidence-intelligence-summary">
        <div><strong>${projectEscapeHtml(results.length)}</strong><span>Domains</span></div>
        <div><strong>${projectEscapeHtml(mapped)}</strong><span>Mapped dimensions</span></div>
        <div><strong>${projectEscapeHtml(issues.length)}</strong><span>Review issues</span></div>
        <div><strong>Read-only</strong><span>No advice</span></div>
      </div>
      <div class="intelligence-item">
        <strong>Domain Evaluation Boundary</strong>
        ${(data.limitation_notes || []).map((note) => `<span>${projectEscapeHtml(note)}</span>`).join("")}
      </div>
      ${results.map((result, index) => renderDomainEvaluationResult(result, index === 0)).join("")}
      ${renderEvidenceIntelligenceSection("Domain Reviewer Questions", renderDomainQuestions(data.reviewer_questions || []))}
    `;
    bindEvidenceJumpLinks(panel);
  }

  function renderDomainEvaluationResult(result, open) {
    const body = `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(readinessLabel(result.domain || "domain"))}</strong>
        <p>${projectEscapeHtml(result.applicable_frameworks?.[0]?.description || "Evidence-backed domain evaluation.")}</p>
        ${renderEvidenceRefs(result.evidence_refs || [], "Related evidence")}
      </div>
      ${renderEvidenceIntelligenceSection("Key Evaluation Dimensions", renderDomainDimensions(result.evaluation_dimensions || []))}
      ${renderEvidenceIntelligenceSection("Risk Exposure Areas", renderSimpleList((result.risk_categories || []).map(readinessLabel), "No risk exposure areas mapped."))}
      ${renderEvidenceIntelligenceSection("Missing Evidence", renderSimpleList(result.unknowns || [], "No missing evidence listed."))}
      ${renderEvidenceIntelligenceSection("Regulatory / Suitability Flags", renderDomainIssues(result.regulatory_suitability_flags || [], "No regulatory or suitability flags detected."))}
      ${renderEvidenceIntelligenceSection("Reviewer Questions", renderDomainQuestions(result.reviewer_questions || []))}
    `;
    return renderEvidenceIntelligenceSection(result.applicable_frameworks?.[0]?.name || readinessLabel(result.domain), body, open);
  }

  function renderDomainDimensions(items) {
    if (!items.length) return '<div class="empty">No domain dimensions available.</div>';
    return items.slice(0, 12).map((item) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(readinessLabel(item.dimension_id || "dimension"))}</strong>
        <span>Status: ${projectEscapeHtml(item.status || "unknown")}</span>
        <p>${projectEscapeHtml(item.reviewer_note || "Reviewer should evaluate this dimension.")}</p>
        ${renderEvidenceRefs(item.evidence_refs || [], "Related evidence")}
      </div>
    `).join("");
  }

  function renderDomainIssues(items, emptyMessage) {
    if (!items.length) return `<div class="empty">${projectEscapeHtml(emptyMessage)}</div>`;
    return items.map((item) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(readinessLabel(item.issue_type || "review issue"))}</strong>
        <p>${projectEscapeHtml(item.explanation || "Reviewer should verify this issue.")}</p>
        <span>${projectEscapeHtml(item.reviewer_question || "")}</span>
        ${renderEvidenceRefs(item.evidence_refs || [], "Related evidence")}
      </div>
    `).join("");
  }

  function renderDomainQuestions(items) {
    if (!items.length) return '<div class="empty">No domain reviewer questions generated.</div>';
    return items.slice(0, 10).map((item) => `
      <div class="intelligence-item">
        <strong>${projectEscapeHtml(item.question || "Reviewer question")}</strong>
        <span>${projectEscapeHtml(readinessLabel(item.domain || "domain"))}${item.related_dimension ? ` - ${projectEscapeHtml(readinessLabel(item.related_dimension))}` : ""}</span>
        ${renderEvidenceRefs(item.evidence_refs || [], "Related evidence")}
      </div>
    `).join("");
  }

  function renderDomainEvaluationEmptyState() {
    const panel = document.getElementById("domain-evaluation-panel");
    if (!panel) return;
    panel.innerHTML = '<div class="empty">No domain evaluation available yet. Add a relevant question and accepted evidence to review domain-specific evidence mapping.</div>';
  }

  function renderDomainEvaluationError(message) {
    const panel = document.getElementById("domain-evaluation-panel");
    if (!panel) return;
    panel.innerHTML = `<div class="empty error-state">${projectEscapeHtml(message || "Could not load domain decision evaluation.")}</div>`;
  }

  function renderDecisionTimeline(project) {
    const timeline = document.getElementById("project-decision-timeline");
    if (!timeline) return;

    const questionsById = new Map((project.questions || []).map((item) => [item.question_id, item.question]));
    const history = project.decision_history || [];

    if (!history.length) {
      timeline.innerHTML = '<div class="empty">Analyze a project question to start the timeline.</div>';
      return;
    }

    timeline.innerHTML = history.map((item) => `
      <div class="timeline-item">
        <span>${projectEscapeHtml(item.created_at || "")}</span>
        <strong>${projectEscapeHtml(questionsById.get(item.question_id) || "Project question")}</strong>
        <p>${projectEscapeHtml(item.assessment_summary || "Legacy assessment; former system recommendation is suppressed.")}</p>
        <span>Evidence Sufficiency: ${projectEscapeHtml(item.evidence_sufficiency_tier || "Not assessed")} — Structural assessment only</span>
        <span>Artifact Completeness: ${projectEscapeHtml(projectStructuralChecks(item.artifact_completeness_passed, item.artifact_completeness_total, item.artifact_completeness_rate))}. Completeness does not establish factual or decision quality.</span>
        ${projectRunLink(item.run_id)}
      </div>
    `).join("");
  }

  async function renderDecisionDelta(projectId) {
    const panel = document.getElementById("project-delta-panel");
    if (!panel) return;

    try {
      const response = await fetch(`${PROJECT_API_BASE}/projects/${projectId}/delta`);
      if (!response.ok) throw new Error("Delta unavailable.");
      const delta = await response.json();

      if (!delta.available) {
        panel.innerHTML = `<div class="empty">${projectEscapeHtml(delta.message || "At least two completed analyses are required.")}</div>`;
        return;
      }

      panel.innerHTML = `
        <div class="delta-grid">
          <div>
            <strong>Previous assessment</strong>
            <p>${projectEscapeHtml(delta.previous_assessment || "Not stated")}</p>
          </div>
          <div>
            <strong>Current assessment</strong>
            <p>${projectEscapeHtml(delta.current_assessment || "Not stated")}</p>
          </div>
        </div>
        <p>${projectEscapeHtml(delta.what_changed || "")}</p>
        <p>Assessment changed: ${delta.assessment_changed ? "Yes" : "No"}</p>
        <p>Evidence Sufficiency: ${projectEscapeHtml(delta.evidence_sufficiency_change?.previous || "Not assessed")} → ${projectEscapeHtml(delta.evidence_sufficiency_change?.current || "Not assessed")} — structural assessment only</p>
        <p>Artifact Completeness: ${projectEscapeHtml(projectStructuralChecks(delta.artifact_completeness_change?.previous_passed, delta.artifact_completeness_change?.previous_total, delta.artifact_completeness_change?.previous))} → ${projectEscapeHtml(projectStructuralChecks(delta.artifact_completeness_change?.current_passed, delta.artifact_completeness_change?.current_total, delta.artifact_completeness_change?.current))}</p>
        <p>Passed structural checks change: ${typeof delta.artifact_completeness_change?.previous_passed === "number" && typeof delta.artifact_completeness_change?.current_passed === "number" ? `${delta.artifact_completeness_change.current_passed - delta.artifact_completeness_change.previous_passed}` : "Counts unavailable"}. This is not a quality score.</p>
        <p>Evidence added: ${projectEscapeHtml((delta.evidence_added || []).join(", ") || "None")}</p>
        <p>Evidence missing or weakened: ${projectEscapeHtml((delta.evidence_missing_or_weakened || []).join(", ") || "None")}</p>
      `;
    } catch (error) {
      panel.innerHTML = '<div class="empty">Could not load decision delta.</div>';
    }
  }

  async function addQuestionToCurrentProject() {
    if (!workspaceProject) {
      alert("Create or select a project first.");
      return;
    }

    const input = document.getElementById("project-question-input");
    if (!input) return;

    const question = input.value.trim();

    if (!question) {
      alert("Please enter a question.");
      return;
    }

    const response = await fetch(`${PROJECT_API_BASE}/projects/${workspaceProject.project_id}/questions`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({question}),
    });

    if (!response.ok) {
      alert("Could not save question.");
      return;
    }

    input.value = "";
    workspaceProject = await response.json();
    const questions = workspaceProject.questions || [];
    workspaceQuestionId = questions.length ? questions[questions.length - 1].question_id : "";
    renderActiveProject(workspaceProject);
    await loadProjects();
  }

  async function addEvidenceToCurrentProject() {
    if (!workspaceProject) {
      alert("Create or select a project first.");
      return;
    }

    const titleInput = document.getElementById("evidence-title-input");
    const noteInput = document.getElementById("evidence-note-input");
    const title = titleInput?.value.trim() || "";
    const note = noteInput?.value.trim() || "";

    if (!title || !note) {
      alert("Please enter an evidence title and note.");
      return;
    }

    const response = await fetch(`${PROJECT_API_BASE}/projects/${workspaceProject.project_id}/evidence`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        title,
        source_type: "Manual note",
        text_excerpt: note,
        summary: note,
        status: "User Provided",
        freshness_note: "Manually added by reviewer.",
      }),
    });

    if (!response.ok) {
      alert("Could not save evidence.");
      return;
    }

    if (titleInput) titleInput.value = "";
    if (noteInput) noteInput.value = "";
    workspaceProject = await response.json();
    renderActiveProject(workspaceProject);
    await loadProjects();
  }

  async function searchCurrentEvidence() {
    if (!workspaceProject) {
      alert("Create or select a project first.");
      return;
    }

    const input = document.getElementById("evidence-search-input");
    const query = input?.value.trim() || "";

    if (!query) {
      alert("Please paste a URL or enter an evidence query.");
      return;
    }

    const response = await fetch(`${PROJECT_API_BASE}/retrieve-evidence`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        query,
        project_id: workspaceProject.project_id,
      }),
    });

    if (!response.ok) {
      alert("Could not retrieve evidence. Review the URL or query and try again.");
      return;
    }

    const data = await response.json();
    retrievedEvidenceQueue = data.items || [];
    renderRetrievedEvidenceQueue(retrievedEvidenceQueue);
  }

  async function acceptSelectedEvidence() {
    if (!workspaceProject) {
      alert("Create or select a project first.");
      return;
    }

    const selected = Array.from(document.querySelectorAll("[data-retrieved-index]:checked"))
      .map((item) => retrievedEvidenceQueue[Number(item.getAttribute("data-retrieved-index"))])
      .filter(Boolean);

    if (!selected.length) {
      alert("Select at least one retrieved evidence item.");
      return;
    }

    const response = await fetch(`${PROJECT_API_BASE}/projects/${workspaceProject.project_id}/evidence/accept`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({items: selected}),
    });

    if (!response.ok) {
      alert("Could not accept selected evidence.");
      return;
    }

    workspaceProject = await response.json();
    retrievedEvidenceQueue = [];
    renderActiveProject(workspaceProject);
    renderRetrievedEvidenceQueue(retrievedEvidenceQueue);
    await loadProjects();
  }

  window.getActiveProjectId = () => workspaceProject?.project_id || "";

  window.getActiveProjectAnalysisContext = () => {
    const question = activeProjectQuestion();
    return {
      project_id: workspaceProject?.project_id || "",
      project_question_id: question?.question_id || "",
      question_text: question?.question || "",
      evidence_ids: [...selectedEvidenceIds],
    };
  };

  window.refreshProjectWorkspace = refreshProjectWorkspace;

  document.addEventListener("DOMContentLoaded", () => {
    document
      .getElementById("create-project-button")
      ?.addEventListener("click", createProjectFromInput);

    document
      .getElementById("add-project-question-button")
      ?.addEventListener("click", addQuestionToCurrentProject);

    document
      .getElementById("add-evidence-button")
      ?.addEventListener("click", addEvidenceToCurrentProject);

    document
      .getElementById("search-evidence-button")
      ?.addEventListener("click", searchCurrentEvidence);

    document
      .getElementById("accept-evidence-button")
      ?.addEventListener("click", acceptSelectedEvidence);

    loadProjects();
  });
})();
