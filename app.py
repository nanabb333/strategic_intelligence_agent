"""Local FastAPI application for Strategic Intelligence Agent."""

from __future__ import annotations

import base64
import sys
from pathlib import Path
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
from decision_readiness import build_project_decision_readiness  # noqa: E402
from domain_evaluation import build_project_domain_evaluation  # noqa: E402
from evidence_intelligence import build_evidence_intelligence  # noqa: E402
from evidence_retrieval import retrieve_evidence  # noqa: E402
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
    title=str(APP_CONFIG.get("app", {}).get("api_title") or "Strategic Intelligence Agent Local App"),
    version=str(APP_CONFIG.get("app", {}).get("version") or "5.0.0"),
    description="Local-only API for running the Strategic Intelligence Agent pipeline.",
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


@app.get("/health")
def health() -> dict[str, str]:
    """Return local app health."""
    return {
        "status": "ok",
        "app": str(APP_CONFIG.get("app", {}).get("name") or "Strategic Intelligence Agent"),
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
    return {
        "metadata": read_json(run_dir / "metadata.json"),
        "analysis": read_json(run_dir / "analysis.json"),
        "agent_trace": read_json(run_dir / "agent_trace.json"),
        "brief_markdown": (run_dir / "brief.md").read_text(encoding="utf-8"),
        "brief_text": (run_dir / "brief.txt").read_text(encoding="utf-8"),
        "downloads": download_links(run_id),
    }


@app.get("/run/{run_id}/download/{artifact}")
def download_run_artifact(run_id: str, artifact: str) -> FileResponse:
    """Download a stored run artifact."""
    filename_by_artifact = {
        "markdown": "brief.md",
        "txt": "brief.txt",
        "json": "analysis.json",
    }
    filename = filename_by_artifact.get(artifact)
    if not filename:
        raise HTTPException(status_code=404, detail="Unknown artifact.")
    path = run_dir_or_404(run_id) / filename
    media_type = "application/json" if artifact == "json" else "text/plain"
    return FileResponse(path, media_type=media_type, filename=filename)
