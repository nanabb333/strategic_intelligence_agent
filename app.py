"""Local FastAPI application for Strategic Intelligence Decision Companion."""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from analysis_service import run_analysis  # noqa: E402
from config import load_config, release_metadata  # noqa: E402
from diagnostics import build_diagnostics  # noqa: E402
from decision_pathways import build_project_decision_pathway_drafts  # noqa: E402
from decision_assessment import (  # noqa: E402
    normalize_stored_decision_assessment,
    render_normalized_stored_assessment,
)
from decision_readiness import build_project_decision_readiness  # noqa: E402
from domain_evaluation import build_project_domain_evaluation  # noqa: E402
from evidence_intelligence import build_evidence_intelligence  # noqa: E402
from evidence_retrieval import retrieve_evidence  # noqa: E402
from evidence_sufficiency import normalize_stored_evidence_sufficiency  # noqa: E402
from markdown_utils import markdown_to_text  # noqa: E402
from pathway_comparison import build_project_pathway_comparison  # noqa: E402
from pdf_reader import extract_pdf_text  # noqa: E402
from project_workspace import (
    add_question_to_project,
    add_evidence_to_project,
    accept_retrieved_evidence,
    attach_run_to_question,
    create_project,
    delete_project,
    decision_delta,
    evidence_bundle_for_project,
    get_decision_review_state,
    get_project,
    list_project_evidence,
    list_projects as list_project_workspaces,
    update_project_decision_review,
)  # noqa: E402
from run_storage import (
    download_links,
    list_run_metadata,
    read_json,
    RUNS_DIR,
    run_dir_or_404,
)  # noqa: E402


APP_CONFIG = load_config()
RUNS_DIR.mkdir(parents=True, exist_ok=True)


class AnalyzeRequest(BaseModel):
    """Request payload for local analysis."""

    text: str = ""
    language: str = "en"
    output_mode: str = "analyst"
    question_id: str = "meaning"
    question_text: str = "What does this issue mean?"
    source_url: str = ""
    input_mode: str = "paste_text"
    uploaded_filename: str = ""
    file_type: str = "text"
    project_id: str = ""
    project_question_id: str = ""
    evidence_ids: list[str] = Field(default_factory=list)


class ExtractFileRequest(BaseModel):
    """Request payload for local file text extraction."""

    filename: str
    content_base64: str


class RetrieveEvidenceRequest(BaseModel):
    """Request payload for user-triggered evidence retrieval."""

    query: str
    project_id: str = ""
    allowed_sources: list[str] = Field(default_factory=list)


class AnalyzeResponse(BaseModel):
    """Response payload returned after a run is created."""

    run_id: str
    metadata: dict[str, Any]
    analysis: dict[str, Any]
    brief_markdown: str
    brief_text: str
    downloads: dict[str, str]


app = FastAPI(
    title=str(APP_CONFIG.get("app", {}).get("api_title") or "Strategic Intelligence Decision Companion Local App"),
    version=str(APP_CONFIG.get("app", {}).get("version") or "5.0.0"),
    description="Local-only API for running the Strategic Intelligence Decision Companion pipeline.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/dashboard", StaticFiles(directory=ROOT / "dashboard", html=True), name="dashboard")
app.mount("/runs", StaticFiles(directory=RUNS_DIR, html=False), name="runs")


@app.get("/", response_class=HTMLResponse)
def landing_page() -> str:
    """Return the local product landing page."""
    return """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Strategic Intelligence Decision Companion</title>
    <link rel="icon" href="data:,">
    <style>
      :root {
        --primary: #B8A7E8;
        --background: #F7F4FF;
        --highlight: #EFEAFB;
        --ink: #191724;
        --muted: #6E6A7E;
        --line: #DDD6F7;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        min-height: 100vh;
        display: grid;
        place-items: center;
        background: var(--background);
        color: var(--ink);
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      }
      main {
        width: min(760px, calc(100vw - 40px));
        padding: 56px;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: #fff;
        box-shadow: 0 24px 80px rgba(64, 48, 96, 0.12);
      }
      .eyebrow {
        margin: 0 0 16px;
        color: #7563A8;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0;
        text-transform: uppercase;
      }
      h1 {
        margin: 0;
        font-size: clamp(2rem, 5vw, 4rem);
        line-height: 1.02;
        letter-spacing: 0;
      }
      .subtitle {
        margin: 20px 0 0;
        color: var(--muted);
        font-size: 1.24rem;
        line-height: 1.5;
      }
      .principles {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 28px 0 36px;
        padding: 0;
        list-style: none;
      }
      .principles li {
        padding: 9px 12px;
        border: 1px solid var(--line);
        border-radius: 999px;
        background: var(--highlight);
        color: #524579;
        font-size: 0.94rem;
        font-weight: 700;
      }
      .actions {
        display: flex;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
      }
      a.button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 48px;
        padding: 0 20px;
        border-radius: 8px;
        background: var(--primary);
        color: var(--ink);
        text-decoration: none;
        font-weight: 800;
      }
      .version {
        color: var(--muted);
        font-size: 0.95rem;
        font-weight: 700;
      }
      @media (max-width: 640px) {
        main { padding: 32px; }
      }
    </style>
  </head>
  <body>
    <main aria-labelledby="product-title">
      <p class="eyebrow">Reviewer-first Enterprise Decision Intelligence</p>
      <h1 id="product-title">Strategic Intelligence Decision Companion</h1>
      <p class="subtitle">Local, deterministic, evidence-backed, human-in-the-loop decision support.</p>
      <ul class="principles" aria-label="Product principles">
        <li>Local</li>
        <li>Deterministic</li>
        <li>Evidence-backed</li>
        <li>Human-in-the-loop</li>
      </ul>
      <div class="actions">
        <a class="button" href="/workspace">Open Decision Workspace</a>
        <span class="version">V5 Sprint 0 · Build local</span>
      </div>
    </main>
  </body>
</html>
"""


@app.get("/workspace", response_class=FileResponse)
def decision_workspace() -> FileResponse:
    """Return the Decision Workspace interface."""
    return FileResponse(ROOT / "dashboard" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    """Return local app health."""
    return {
        "status": "ok",
        "app": str(APP_CONFIG.get("app", {}).get("name") or "Strategic Intelligence Decision Companion"),
        "version": str(APP_CONFIG.get("app", {}).get("version") or "5.0.0"),
    }


@app.get("/version")
def version() -> dict[str, Any]:
    """Return product release metadata."""
    return release_metadata()


@app.get("/diagnostics")
def diagnostics() -> dict[str, Any]:
    """Return a local diagnostic snapshot without changing workspace state."""
    return build_diagnostics()


@app.post("/extract-file")
def extract_file(request: ExtractFileRequest) -> dict[str, str]:
    """Extract text from a local uploaded text, Markdown, or text-based PDF file."""
    filename = request.filename.strip()
    suffix = Path(filename).suffix.lower()
    try:
        raw = base64.b64decode(request.content_base64)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not decode uploaded file.") from exc

    if suffix in {".txt", ".md", ".markdown"}:
        return {
            "filename": filename,
            "file_type": suffix.lstrip("."),
            "text": raw.decode("utf-8", errors="replace"),
            "limitation": "",
        }
    if suffix == ".pdf":
        return {
            "filename": filename,
            "file_type": "pdf",
            "text": extract_pdf_text(raw),
            "limitation": "PDF support works for text-based PDFs only. Scanned image PDFs are not supported.",
        }
    raise HTTPException(status_code=400, detail="Unsupported file type. Use .txt, .md, .markdown, or .pdf.")


@app.post("/retrieve-evidence")
def post_retrieve_evidence(request: RetrieveEvidenceRequest) -> dict[str, Any]:
    """Retrieve user-triggered evidence candidates for review before acceptance."""
    try:
        return retrieve_evidence(
            query=request.query,
            project_id=request.project_id,
            allowed_sources=request.allowed_sources,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Run the real Python pipeline and persist run artifacts."""
    if request.language != "en":
        raise HTTPException(status_code=400, detail="English is the official product language for this release.")

    project = None
    project_question_id = request.project_question_id
    evidence_bundle: list[dict[str, Any]] = []
    if request.project_id:
        try:
            project = get_project(request.project_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Project not found.") from exc
        if project_question_id and not any(
            item.get("question_id") == project_question_id
            for item in project.get("questions", [])
        ):
            raise HTTPException(status_code=404, detail="Project question not found.")
        if not project_question_id:
            project = add_question_to_project(
                project_id=request.project_id,
                question=request.question_text,
            )
            project_question_id = project["questions"][-1]["question_id"]
        evidence_bundle = evidence_bundle_for_project(project, [str(item) for item in request.evidence_ids])

    result = run_analysis(
        text=request.text,
        language=request.language,
        output_mode=request.output_mode,
        question_id=request.question_id,
        question_text=request.question_text,
        source_url=request.source_url,
        input_mode=request.input_mode,
        uploaded_filename=request.uploaded_filename,
        file_type=request.file_type,
        project_id=request.project_id,
        project_question_id=project_question_id,
        evidence_bundle=evidence_bundle,
    )
    if request.project_id:
        try:
            attach_run_to_question(
                request.project_id,
                question_id=project_question_id,
                run_id=result["run_id"],
                analysis=result["analysis"],
                brief_path=result["downloads"]["markdown"],
                evidence_ids=[item["evidence_id"] for item in evidence_bundle],
            )
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Project or question not found.") from exc
    return AnalyzeResponse(**result)


@app.get("/projects")
def get_projects() -> dict[str, list[dict[str, Any]]]:
    """List project workspaces."""
    return {"projects": list_project_workspaces()}


@app.post("/projects")
def post_project(payload: dict[str, Any]) -> dict[str, Any]:
    """Create a new project workspace."""
    name = str(payload.get("name", "")).strip()
    description = str(payload.get("description", "")).strip()

    if not name:
        raise HTTPException(status_code=400, detail="Project name is required.")

    return create_project(name=name, description=description)


@app.delete("/projects/{project_id}")
def delete_project_endpoint(project_id: str) -> dict[str, Any]:
    try:
        delete_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="Project not found."
        ) from exc

    return {"status": "deleted", "project_id": project_id}


@app.get("/projects/{project_id}")
def get_project_workspace(project_id: str) -> dict[str, Any]:
    """Return one project workspace."""
    try:
        return get_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc


@app.post("/projects/{project_id}/questions")
def post_project_question(project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Add a question record to a project workspace."""
    question = str(payload.get("question", "")).strip()
    run_id = payload.get("run_id")
    brief_path = payload.get("brief_path")
    analysis = payload.get("analysis")

    if not question:
        raise HTTPException(status_code=400, detail="Question is required.")

    if run_id and analysis is None:
        try:
            analysis = read_json(run_dir_or_404(str(run_id)) / "analysis.json")
        except HTTPException:
            analysis = None

    try:
        return add_question_to_project(
            project_id=project_id,
            question=question,
            run_id=run_id,
            brief_path=brief_path,
            analysis=analysis,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc


@app.post("/projects/{project_id}/evidence")
def post_project_evidence(project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Add a manual evidence item to a project workspace."""
    try:
        return add_evidence_to_project(project_id, payload)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc


@app.get("/projects/{project_id}/evidence")
def get_project_evidence(project_id: str) -> dict[str, list[dict[str, Any]]]:
    """List evidence items stored under one project workspace."""
    try:
        return {"evidence": list_project_evidence(project_id)}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc


@app.get("/projects/{project_id}/evidence/intelligence")
def get_project_evidence_intelligence(project_id: str) -> dict[str, Any]:
    """Return deterministic read-only evidence intelligence for one project."""
    try:
        project = get_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc
    return build_evidence_intelligence(project.get("evidence_library", []))


@app.get("/projects/{project_id}/decision/readiness")
def get_project_decision_readiness(project_id: str) -> dict[str, Any]:
    """Return deterministic read-only decision readiness for one project."""
    try:
        project = get_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc
    return build_project_decision_readiness(project)


@app.get("/projects/{project_id}/decision/pathways")
def get_project_decision_pathways(project_id: str) -> dict[str, Any]:
    """Return deterministic read-only decision pathway drafts for one project."""
    try:
        project = get_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc
    return build_project_decision_pathway_drafts(project)


@app.get("/projects/{project_id}/decision/domain-evaluation")
def get_project_domain_evaluation(project_id: str) -> dict[str, Any]:
    """Return deterministic read-only domain decision evaluation for one project."""
    try:
        project = get_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc
    return build_project_domain_evaluation(project)


@app.get("/projects/{project_id}/decision/pathway-comparison")
def get_project_pathway_comparison(project_id: str) -> dict[str, Any]:
    """Return deterministic read-only pathway comparison matrix for one project."""
    try:
        project = get_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc
    return build_project_pathway_comparison(project)


@app.get("/projects/{project_id}/decision/review")
def get_project_decision_review(project_id: str) -> dict[str, Any]:
    """Return reviewer-controlled decision review state for one project."""
    try:
        return get_decision_review_state(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc


@app.put("/projects/{project_id}/decision/review")
def put_project_decision_review(project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Persist reviewer-controlled decision review state for one project."""
    try:
        return update_project_decision_review(project_id, payload)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/projects/{project_id}/evidence/accept")
def post_accept_project_evidence(project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Accept reviewed retrieved evidence candidates into a project."""
    items = payload.get("items") or []
    if not isinstance(items, list):
        raise HTTPException(status_code=400, detail="Items must be a list.")
    try:
        return accept_retrieved_evidence(project_id, items)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc


@app.get("/projects/{project_id}/delta")
def get_project_delta(project_id: str) -> dict[str, Any]:
    """Compare the two latest completed project decisions."""
    try:
        return decision_delta(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Project not found.") from exc


@app.get("/runs")
def list_runs() -> list[dict[str, Any]]:
    """List previous local analysis runs."""
    return list_run_metadata()


@app.get("/run/{run_id}")
def get_run(run_id: str) -> dict[str, Any]:
    """Return stored artifacts for one run."""
    run_dir = run_dir_or_404(run_id)
    stored_analysis = read_json(run_dir / "analysis.json")
    stored_brief = (run_dir / "brief.md").read_text(encoding="utf-8")
    is_legacy = not bool(stored_analysis.get("decision_assessment"))
    analysis = _current_analysis_view(stored_analysis)
    if is_legacy:
        stored_brief = render_normalized_stored_assessment(analysis["decision_assessment"])
    payload = {
        "metadata": read_json(run_dir / "metadata.json"),
        "analysis": analysis,
        "tool_routing_trace": read_json(run_dir / "agent_trace.json"),
        "brief_markdown": stored_brief,
        "brief_text": markdown_to_text(stored_brief),
        "downloads": download_links(run_id),
    }
    if is_legacy:
        payload["legacy_contract"] = _legacy_contract_marker(run_id)
        payload["historical_raw_downloads"] = _historical_raw_download_links(run_id)
    return payload


@app.get("/run/{run_id}/download/{artifact}")
def download_run_artifact(run_id: str, artifact: str) -> Response:
    """Export the current assessment contract, neutralizing legacy runs."""
    filename_by_artifact = {
        "markdown": "brief.md",
        "txt": "brief.txt",
        "json": "analysis.json",
    }
    filename = filename_by_artifact.get(artifact)
    if not filename:
        raise HTTPException(status_code=404, detail="Unknown artifact.")
    run_dir = run_dir_or_404(run_id)
    path = run_dir / filename
    stored_analysis = read_json(run_dir / "analysis.json")
    if not stored_analysis.get("decision_assessment"):
        analysis = _current_analysis_view(stored_analysis)
        markdown = render_normalized_stored_assessment(analysis["decision_assessment"])
        if artifact == "markdown":
            return _download_response(markdown, "current-neutral-assessment.md", "text/markdown")
        if artifact == "txt":
            return _download_response(markdown_to_text(markdown), "current-neutral-assessment.txt", "text/plain")
        return _download_response(
            json.dumps(analysis, indent=2, ensure_ascii=False),
            "current-neutral-assessment.json",
            "application/json",
        )
    media_type = "application/json" if artifact == "json" else "text/plain"
    return FileResponse(path, media_type=media_type, filename=filename)


@app.get("/run/{run_id}/download/historical-raw/{artifact}")
def download_historical_raw_artifact(run_id: str, artifact: str) -> FileResponse:
    """Download an unchanged artifact generated under a superseded contract."""
    filename_by_artifact = {"markdown": "brief.md", "txt": "brief.txt", "json": "analysis.json"}
    filename = filename_by_artifact.get(artifact)
    if not filename:
        raise HTTPException(status_code=404, detail="Unknown historical raw artifact.")
    run_dir = run_dir_or_404(run_id)
    if read_json(run_dir / "analysis.json").get("decision_assessment"):
        raise HTTPException(status_code=404, detail="This run does not use a superseded historical contract.")
    path = run_dir / filename
    media_type = "application/json" if artifact == "json" else "text/plain"
    return FileResponse(
        path,
        media_type=media_type,
        filename=f"historical-raw-read-only-{filename}",
        headers={
            "X-Artifact-Mode": "historical-raw-read-only",
            "X-Artifact-Contract": "superseded",
        },
    )


def _current_analysis_view(stored_analysis: dict[str, Any]) -> dict[str, Any]:
    """Return current-contract fields without exposing superseded evaluative keys."""
    is_legacy = not bool(stored_analysis.get("decision_assessment"))
    analysis = _strip_legacy_evaluative_fields(stored_analysis) if is_legacy else dict(stored_analysis)
    analysis["decision_assessment"] = normalize_stored_decision_assessment(stored_analysis)
    sufficiency = normalize_stored_evidence_sufficiency(stored_analysis)
    if sufficiency:
        analysis["evidence_sufficiency"] = sufficiency
    for key in ("decision_case", "confidence_assessment", "decision_quality_evaluation"):
        analysis.pop(key, None)
    if is_legacy:
        analysis["legacy_contract"] = _legacy_contract_marker("")
    return analysis


def _strip_legacy_evaluative_fields(value: Any) -> Any:
    """Remove superseded recommendation, confidence, and quality keys from a current view."""
    prohibited = {
        "recommended_path",
        "recommendation",
        "preferred_path",
        "confidence",
        "confidence_level",
        "confidence_assessment",
        "decision_quality_evaluation",
        "overall_score",
        "overall_label",
        "recommendation_score",
    }
    if isinstance(value, dict):
        return {
            key: _strip_legacy_evaluative_fields(item)
            for key, item in value.items()
            if key not in prohibited
        }
    if isinstance(value, list):
        return [_strip_legacy_evaluative_fields(item) for item in value]
    return value


def _legacy_contract_marker(run_id: str) -> dict[str, Any]:
    return {
        "is_legacy": True,
        "read_only": True,
        "contract_status": "superseded",
        "display_mode": "neutralized-current-assessment",
        "statement": (
            "The original run was generated under a superseded recommendation-oriented contract. "
            "Historical raw artifacts remain available separately for audit only."
        ),
        "run_id": run_id,
    }


def _historical_raw_download_links(run_id: str) -> dict[str, str]:
    base = f"/run/{run_id}/download/historical-raw"
    return {"markdown": f"{base}/markdown", "txt": f"{base}/txt", "json": f"{base}/json"}


def _download_response(content: str, filename: str, media_type: str) -> Response:
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
