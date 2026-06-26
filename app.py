"""Local FastAPI application for Strategic Intelligence Agent."""

from __future__ import annotations

import json
import base64
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agent_router import route_document  # noqa: E402
from analysis_artifact import build_analysis_artifact  # noqa: E402
from brief_generator import generate_brief  # noqa: E402
from context_retriever import retrieve_current_context  # noqa: E402
from evidence_assessor import assess_evidence  # noqa: E402
from evidence_credibility import assess_evidence_credibility  # noqa: E402
from event_context import extract_event_context  # noqa: E402
from event_understanding import detect_event_understanding  # noqa: E402
from historical_retriever import retrieve_historical_analogues  # noqa: E402
from implication_analyzer import analyze_implications  # noqa: E402
from issue_extractor import extract_issues  # noqa: E402
from knowledge_localization import localize_analysis_payload  # noqa: E402
from mechanism_detector import detect_mechanisms  # noqa: E402
from multi_lens_analyzer import analyze_lenses  # noqa: E402
from localization import localized_question_intent, localized_question_route  # noqa: E402
from output_adapter import adapt_output  # noqa: E402
from markdown_utils import markdown_to_text  # noqa: E402
from outcome_retriever import retrieve_historical_outcomes  # noqa: E402
from question_router import route_question  # noqa: E402
from response_playbook_retriever import retrieve_response_patterns  # noqa: E402
from scenario_classifier import classify_scenarios  # noqa: E402
from strategic_assessment import generate_strategic_assessments  # noqa: E402
from strategic_lessons import generate_strategic_lessons  # noqa: E402
from tool_registry import build_default_registry  # noqa: E402
from pdf_reader import extract_pdf_text  # noqa: E402
from url_reader import fetch_url_text  # noqa: E402
from run_storage import (
    create_run_dir,
    download_links,
    read_json,
    run_dir_or_404,
    write_json,
)  # noqa: E402
from serialization import serializable  # noqa: E402


RUNS_DIR = ROOT / "outputs" / "runs"
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


class ExtractFileRequest(BaseModel):
    """Request payload for local file text extraction."""

    filename: str
    content_base64: str


class AnalyzeResponse(BaseModel):
    """Response payload returned after a run is created."""

    run_id: str
    metadata: dict[str, Any]
    analysis: dict[str, Any]
    brief_markdown: str
    brief_text: str
    downloads: dict[str, str]


app = FastAPI(
    title="Strategic Intelligence Agent Local App",
    version="12.0",
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
    return {"status": "ok", "app": "Strategic Intelligence Agent", "version": "12.0"}


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


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Run the real Python pipeline and persist run artifacts."""
    text = request.text.strip()
    source_url = request.source_url.strip()

    # If the user pasted a URL into the main text box,
    # treat it as a URL automatically.
    if text.startswith(("http://", "https://")) and not source_url:
        source_url = text
        text = fetch_url_text(source_url)

    elif not text:
        if source_url:
            text = fetch_url_text(source_url)
        else:
            raise HTTPException(
                status_code=400,
                detail="Text is required.",
            )

    question_text = request.question_text.strip()
    analysis_text = f"{question_text}\n\n{text}".strip() if question_text else text

    run_id, run_dir = create_run_dir()

    registry = build_default_registry()
    route = route_document(analysis_text, registry)
    question_route = route_question(request.question_text)
    event_context = extract_event_context(analysis_text)
    event_understanding = detect_event_understanding(analysis_text, request.question_text)
    issues = extract_issues(analysis_text)
    classifications = classify_scenarios(issues)
    analogues = retrieve_historical_analogues(
        issues,
        classifications,
        event_understanding=event_understanding,
    )
    contexts = (
        retrieve_current_context(issues, classifications)
        if "ContextRetriever" in route.selected_tools
        else {issue.title: [] for issue in issues}
    )
    analyses = analyze_implications(issues, classifications, analogues, contexts)
    mechanisms = detect_mechanisms(issues, classifications)
    interpretations = analyze_lenses(issues, classifications, mechanisms, analogues, contexts)
    evidence_assessments = assess_evidence(interpretations)
    historical_outcomes = retrieve_historical_outcomes(analogues)
    strategic_lessons = generate_strategic_lessons(historical_outcomes)
    strategic_assessments = generate_strategic_assessments(
        issues,
        classifications,
        historical_outcomes,
        event_understanding=event_understanding,
    )
    evidence_credibility = assess_evidence_credibility(historical_outcomes, strategic_lessons)
    response_patterns = retrieve_response_patterns(analogues, mechanisms)
    base_brief = generate_brief(
        issues,
        classifications,
        analogues,
        contexts,
        analyses,
        agent_route=route,
        mechanisms=mechanisms,
        interpretations=interpretations,
        evidence_assessments=evidence_assessments,
        historical_outcomes=historical_outcomes,
        strategic_lessons=strategic_lessons,
        strategic_assessments=strategic_assessments,
        evidence_credibility=evidence_credibility,
        response_patterns=response_patterns,
        event_context=event_context,
        event_understanding=event_understanding,
        source_url=source_url,
    )
    brief_markdown = adapt_output(base_brief, mode=request.output_mode, language=request.language)
    brief_text = markdown_to_text(brief_markdown)

    metadata = {
        "run_id": run_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "language": request.language,
        "output_mode": request.output_mode,
        "question_id": request.question_id,
        "question_text": question_route.question_text,
        "question_intent": question_route.intent,
        "question_intent_label": localized_question_intent(question_route.intent, request.language),
        "source_url": source_url,
        "input_mode": request.input_mode,
        "uploaded_filename": request.uploaded_filename,
        "file_type": request.file_type,
        "status": "complete",
        "artifact_paths": {
            "input": f"outputs/runs/{run_id}/input.txt",
            "analysis": f"outputs/runs/{run_id}/analysis.json",
            "brief_markdown": f"outputs/runs/{run_id}/brief.md",
            "brief_text": f"outputs/runs/{run_id}/brief.txt",
            "agent_trace": f"outputs/runs/{run_id}/agent_trace.json",
            "metadata": f"outputs/runs/{run_id}/metadata.json",
        },
    }
    analysis = build_analysis_artifact(
        issues=issues,
        classifications=classifications,
        analogues=analogues,
        contexts=contexts,
        analyses=analyses,
        mechanisms=mechanisms,
        interpretations=interpretations,
        evidence_assessments=evidence_assessments,
        historical_outcomes=historical_outcomes,
        strategic_lessons=strategic_lessons,
        strategic_assessments=strategic_assessments,
        evidence_credibility=evidence_credibility,
        response_patterns=response_patterns,
        event_context=event_context,
        event_understanding=event_understanding,
        question_route=question_route,
        localized_question_route=localized_question_route(question_route, request.language),
        source_url=source_url,
        input_mode=request.input_mode,
        uploaded_filename=request.uploaded_filename,
        file_type=request.file_type,
        route=route,
        metadata=metadata,
    )
    analysis = localize_analysis_payload(analysis, request.language)
    agent_trace = {
        "selected_tools": route.selected_tools,
        "skipped_tools": route.skipped_tools,
        "trace": serializable(route.trace),
        "reasoning_record": serializable(route.reasoning_record),
        "reasoning_stages": [
            "Current event context extraction",
            "Event-family understanding",
            "Historical analogue retrieval",
            "Historical outcome retrieval",
            "Strategic assessment generation",
            "Strategic lesson generation",
            "Evidence credibility assessment",
            "Response playbook retrieval",
            "Executive brief generation",
        ],
    }

    (run_dir / "input.txt").write_text(text, encoding="utf-8")
    write_json(run_dir / "analysis.json", analysis)
    (run_dir / "brief.md").write_text(brief_markdown, encoding="utf-8")
    (run_dir / "brief.txt").write_text(brief_text, encoding="utf-8")
    write_json(run_dir / "agent_trace.json", agent_trace)
    write_json(run_dir / "metadata.json", metadata)

    return AnalyzeResponse(
        run_id=run_id,
        metadata=metadata,
        analysis=analysis,
        brief_markdown=brief_markdown,
        brief_text=brief_text,
        downloads=download_links(run_id),
    )


@app.get("/runs")
def list_runs() -> list[dict[str, Any]]:
    """List previous local analysis runs."""
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    runs = []
    for metadata_path in sorted(RUNS_DIR.glob("*/metadata.json"), reverse=True):
        runs.append(json.loads(metadata_path.read_text(encoding="utf-8")))
    return runs


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
