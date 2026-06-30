(() => {
const PROJECT_API_BASE = window.location.origin.startsWith("http")
  ? window.location.origin
  : "http://127.0.0.1:8000";

let workspaceProject = null;
let workspaceQuestionId = "";

function projectEscapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function projectScore(value) {
  if (typeof value !== "number") return "Not scored";
  return `${(value * 10).toFixed(1)} / 10`;
}

function activeProjectQuestion() {
  if (!workspaceProject || !workspaceQuestionId) return null;
  return (workspaceProject.questions || []).find((item) => item.question_id === workspaceQuestionId) || null;
}

function projectRunLink(runId) {
  if (!runId) return "";
  return `<a href="${PROJECT_API_BASE}/run/${projectEscapeHtml(runId)}/download/markdown" target="_blank" rel="noreferrer">Run ${projectEscapeHtml(runId)}</a>`;
}

async function loadProjects() {
  const list = document.getElementById("project-list");
  if (!list) return;

  try {
    const response = await fetch(`${PROJECT_API_BASE}/projects`);
    if (!response.ok) throw new Error("Projects unavailable.");

    const data = await response.json();
    const projects = data.projects || [];

    if (!projects.length) {
      list.innerHTML = '<div class="empty">No projects yet.</div>';
      return;
    }

    list.innerHTML = "";

    projects.forEach((project) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `project-item${workspaceProject?.project_id === project.project_id ? " active" : ""}`;
      button.innerHTML = `
        <strong>${projectEscapeHtml(project.name)}</strong>
        <span>${projectEscapeHtml(project.description || "Decision workspace")}</span>
        <span>${project.questions?.length || 0} questions - ${project.evidence_library?.length || 0} evidence items</span>
      `;
      button.addEventListener("click", () => selectProject(project.project_id));
      list.appendChild(button);
    });
  } catch (error) {
    list.innerHTML = '<div class="empty">Could not load projects.</div>';
  }
}

async function createProjectFromInput() {
  const input = document.getElementById("project-name-input");
  if (!input) return;

  const name = input.value.trim();

  if (!name) {
    alert("Please enter a project name.");
    return;
  }

  const response = await fetch(`${PROJECT_API_BASE}/projects`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      name,
      description: "Decision workspace",
    }),
  });

  if (!response.ok) {
    alert("Could not create project.");
    return;
  }

  input.value = "";
  workspaceProject = await response.json();
  workspaceQuestionId = "";
  renderActiveProject(workspaceProject);
  await loadProjects();
}

async function selectProject(projectId) {
  const response = await fetch(`${PROJECT_API_BASE}/projects/${projectId}`);

  if (!response.ok) {
    alert("Could not open project.");
    return;
  }

  workspaceProject = await response.json();
  if (!activeProjectQuestion() && (workspaceProject.questions || []).length) {
    workspaceQuestionId = workspaceProject.questions[0].question_id;
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

  renderProjectQuestions(project.questions || []);
  renderProjectEvidence(project.evidence_library || []);
  renderDecisionTimeline(project);
  renderDecisionDelta(project.project_id);
}

function renderProjectQuestions(questions) {
  const questionList = document.getElementById("project-question-list");
  if (!questionList) return;

  if (!questions.length) {
    questionList.innerHTML = '<div class="empty">No questions saved in this project yet.</div>';
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
    });
    questionList.appendChild(card);
  });
}

function renderProjectEvidence(items) {
  const evidenceList = document.getElementById("project-evidence-list");
  if (!evidenceList) return;

  if (!items.length) {
    evidenceList.innerHTML = '<div class="empty">No reusable evidence saved yet.</div>';
    return;
  }

  evidenceList.innerHTML = items.map((item) => `
    <div class="project-evidence-item">
      <strong>${projectEscapeHtml(item.title)}</strong>
      <span>Status: ${projectEscapeHtml(item.status || "User Provided")} - Source type: ${projectEscapeHtml(item.source_type || "Manual note")}</span>
      ${(item.source_url || item.uploaded_filename) ? `<span>Source: ${projectEscapeHtml(item.source_url || item.uploaded_filename)}</span>` : ""}
      ${item.freshness_note ? `<span>Freshness: ${projectEscapeHtml(item.freshness_note)}</span>` : ""}
      <p>${projectEscapeHtml(item.summary || item.text_excerpt || "")}</p>
    </div>
  `).join("");
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
      <p>${projectEscapeHtml(item.recommendation_summary || "Review stored decision brief.")}</p>
      <span>Confidence: ${projectEscapeHtml(item.confidence_label || "Not stated")} - Decision Quality: ${projectScore(item.decision_quality_score)}</span>
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
          <strong>Previous recommendation</strong>
          <p>${projectEscapeHtml(delta.previous_recommendation || "Not stated")}</p>
        </div>
        <div>
          <strong>Current recommendation</strong>
          <p>${projectEscapeHtml(delta.current_recommendation || "Not stated")}</p>
        </div>
      </div>
      <p>${projectEscapeHtml(delta.what_changed || "")}</p>
      <p>Recommendation changed: ${delta.recommendation_changed ? "Yes" : "No"}</p>
      <p>Confidence: ${projectEscapeHtml(delta.confidence_change?.previous || "Not stated")} -> ${projectEscapeHtml(delta.confidence_change?.current || "Not stated")}</p>
      <p>Decision Quality: ${projectScore(delta.decision_quality_change?.previous)} -> ${projectScore(delta.decision_quality_change?.current)}</p>
      <p>Decision Quality Change: ${typeof delta.decision_quality_change?.delta === "number" ? `${(delta.decision_quality_change.delta * 10).toFixed(1)} / 10` : "Not scored"}</p>
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

window.getActiveProjectId = () => workspaceProject?.project_id || "";
window.getActiveProjectAnalysisContext = () => {
  const question = activeProjectQuestion();
  return {
    project_id: workspaceProject?.project_id || "",
    project_question_id: question?.question_id || "",
    question_text: question?.question || "",
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

  loadProjects();
});
})();
