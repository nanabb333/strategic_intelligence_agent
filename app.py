"""Local FastAPI application for Strategic Intelligence Agent."""

from __future__ import annotations

import json
import base64
import sys
from dataclasses import asdict, is_dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from agent_router import route_document  # noqa: E402
from brief_generator import generate_brief  # noqa: E402
from context_retriever import retrieve_current_context  # noqa: E402
from evidence_assessor import assess_evidence  # noqa: E402
from evidence_credibility import assess_evidence_credibility  # noqa: E402
from event_context import extract_event_context  # noqa: E402
from historical_retriever import retrieve_historical_analogues  # noqa: E402
from implication_analyzer import analyze_implications  # noqa: E402
from issue_extractor import extract_issues  # noqa: E402
from knowledge_localization import localize_analysis_payload  # noqa: E402
from mechanism_detector import detect_mechanisms  # noqa: E402
from multi_lens_analyzer import analyze_lenses  # noqa: E402
from localization import localized_question_intent, localized_question_route  # noqa: E402
from output_adapter import adapt_output  # noqa: E402
from outcome_retriever import retrieve_historical_outcomes  # noqa: E402
from question_router import route_question  # noqa: E402
from response_playbook_retriever import retrieve_response_patterns  # noqa: E402
from scenario_classifier import classify_scenarios  # noqa: E402
from strategic_assessment import generate_strategic_assessments  # noqa: E402
from strategic_lessons import generate_strategic_lessons  # noqa: E402
from tool_registry import build_default_registry  # noqa: E402


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
    version="9.5",
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
    return {"status": "ok", "app": "Strategic Intelligence Agent", "version": "9.5"}


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
            "text": _extract_pdf_text(raw),
            "limitation": "PDF support works for text-based PDFs only. Scanned image PDFs are not supported.",
        }
    raise HTTPException(status_code=400, detail="Unsupported file type. Use .txt, .md, .markdown, or .pdf.")


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Run the real Python pipeline and persist run artifacts."""
    text = request.text.strip()
    source_url = request.source_url.strip()
    if not text:
        if source_url:
            text = _fetch_url_text(source_url)
        raise HTTPException(status_code=400, detail="Text is required.")

    run_id, run_dir = _create_run_dir()

    registry = build_default_registry()
    route = route_document(text, registry)
    question_route = route_question(request.question_text)
    event_context = extract_event_context(text)
    issues = extract_issues(text)
    classifications = classify_scenarios(issues)
    analogues = retrieve_historical_analogues(issues, classifications)
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
    strategic_assessments = generate_strategic_assessments(issues, classifications, historical_outcomes)
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
        source_url=source_url,
    )
    brief_markdown = adapt_output(base_brief, mode=request.output_mode, language=request.language)
    brief_text = _markdown_to_text(brief_markdown)

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
    analysis = _build_analysis_artifact(
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
        "trace": _serializable(route.trace),
        "reasoning_record": _serializable(route.reasoning_record),
        "reasoning_stages": [
            "Current event context extraction",
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
    _write_json(run_dir / "analysis.json", analysis)
    (run_dir / "brief.md").write_text(brief_markdown, encoding="utf-8")
    (run_dir / "brief.txt").write_text(brief_text, encoding="utf-8")
    _write_json(run_dir / "agent_trace.json", agent_trace)
    _write_json(run_dir / "metadata.json", metadata)

    return AnalyzeResponse(
        run_id=run_id,
        metadata=metadata,
        analysis=analysis,
        brief_markdown=brief_markdown,
        brief_text=brief_text,
        downloads=_download_links(run_id),
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
    run_dir = _run_dir_or_404(run_id)
    return {
        "metadata": _read_json(run_dir / "metadata.json"),
        "analysis": _read_json(run_dir / "analysis.json"),
        "agent_trace": _read_json(run_dir / "agent_trace.json"),
        "brief_markdown": (run_dir / "brief.md").read_text(encoding="utf-8"),
        "brief_text": (run_dir / "brief.txt").read_text(encoding="utf-8"),
        "downloads": _download_links(run_id),
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
    path = _run_dir_or_404(run_id) / filename
    media_type = "application/json" if artifact == "json" else "text/plain"
    return FileResponse(path, media_type=media_type, filename=filename)


def _next_run_id() -> str:
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    date_part = datetime.now().strftime("%Y%m%d")
    existing = {path.name for path in RUNS_DIR.glob(f"run_{date_part}_*")}
    next_index = 1
    while True:
        candidate = f"run_{date_part}_{next_index:03d}"
        if candidate not in existing and not (RUNS_DIR / candidate).exists():
            return candidate
        next_index += 1


def _create_run_dir() -> tuple[str, Path]:
    """Create a unique run directory, retrying if concurrent requests collide."""
    for _ in range(100):
        run_id = _next_run_id()
        run_dir = RUNS_DIR / run_id
        try:
            run_dir.mkdir(parents=True, exist_ok=False)
            return run_id, run_dir
        except FileExistsError:
            continue
    raise HTTPException(status_code=500, detail="Could not allocate a run folder.")


class _ReadableHTMLParser(HTMLParser):
    """Extract readable text from simple article pages."""

    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        cleaned = " ".join(data.split())
        if len(cleaned) >= 40:
            self._parts.append(cleaned)

    def text(self) -> str:
        return "\n\n".join(self._parts)


def _fetch_url_text(source_url: str) -> str:
    """Fetch readable webpage text for Paste Link mode."""
    if not source_url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=400,
            detail="Please paste a full http:// or https:// URL, or paste the article text directly.",
        )
    request = Request(source_url, headers={"User-Agent": "StrategicIntelligenceAgent/LocalDemo"})
    try:
        with urlopen(request, timeout=12) as response:
            content_type = response.headers.get("content-type", "")
            raw = response.read(1_000_000)
    except (URLError, TimeoutError, OSError) as exc:
        raise HTTPException(
            status_code=400,
            detail=(
                "Could not read webpage content from this link. Please paste the article text or upload a file. "
                "This local app only analyzes a link when readable page text can be fetched."
            ),
        ) from exc
    if "html" not in content_type and "text" not in content_type:
        raise HTTPException(
            status_code=400,
            detail="This link does not look like a readable text page. Please paste article text or upload a file.",
        )
    html = raw.decode("utf-8", errors="replace")
    parser = _ReadableHTMLParser()
    parser.feed(html)
    text = parser.text().strip()
    if len(text) < 300:
        raise HTTPException(
            status_code=400,
            detail="No readable article content was detected. Please paste article text or upload a file.",
        )
    return text


def _run_dir_or_404(run_id: str) -> Path:
    run_dir = RUNS_DIR / run_id
    if not run_dir.exists() or not run_dir.is_dir():
        raise HTTPException(status_code=404, detail="Run not found.")
    return run_dir


def _build_analysis_artifact(**items: Any) -> dict[str, Any]:
    issues = items["issues"]
    classifications = items["classifications"]
    route = items["route"]
    issue_title = issues[0].title if issues else "Untitled issue"
    return {
        "issue": _serializable(issues[0]) if issues else {},
        "source_url": items["source_url"],
        "input_mode": items["input_mode"],
        "uploaded_filename": items["uploaded_filename"],
        "file_type": items["file_type"],
        "event_context": _serializable(items["event_context"]),
        "question_route": _serializable(items["localized_question_route"]),
        "scenario": _serializable(classifications[0]) if classifications else {},
        "mechanisms": _serializable(items["mechanisms"].get(issue_title, [])),
        "analogues": _serializable(items["analogues"].get(issue_title, [])),
        "historical_outcomes": _serializable(items["historical_outcomes"].get(issue_title, [])),
        "strategic_lessons": _serializable(items["strategic_lessons"].get(issue_title, [])),
        "strategic_assessment": _serializable(items["strategic_assessments"].get(issue_title, {})),
        "evidence_credibility": _serializable(items["evidence_credibility"].get(issue_title, {})),
        "current_context": _serializable(items["contexts"].get(issue_title, [])),
        "implications": _serializable(items["analyses"]),
        "response_playbooks": _serializable(items["response_patterns"].get(issue_title, [])),
        "lenses": _serializable(items["interpretations"].get(issue_title, [])),
        "evidence": _serializable(items["evidence_assessments"].get(issue_title, [])),
        "agent_trace": {
            "document_type": route.document_type,
            "scenario_type": route.scenario_type,
            "selected_tools": route.selected_tools,
            "skipped_tools": route.skipped_tools,
            "trace": _serializable(route.trace),
            "reasoning_record": _serializable(route.reasoning_record),
            "reasoning_stages": [
                "Current event context extraction",
                "Historical analogue retrieval",
                "Historical outcome retrieval",
                "Strategic assessment generation",
                "Strategic lesson generation",
                "Evidence credibility assessment",
                "Response playbook retrieval",
                "Executive brief generation",
            ],
        },
        "evaluation_metadata": {
            "framework": "V5 deterministic benchmark framework",
            "note": "Run artifacts are generated by the local deterministic pipeline; they are not real-world accuracy claims.",
        },
        "metadata": items["metadata"],
    }


def _serializable(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if isinstance(value, list):
        return [_serializable(item) for item in value]
    if isinstance(value, dict):
        return {key: _serializable(item) for key, item in value.items()}
    return value


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _markdown_to_text(markdown: str) -> str:
    lines = []
    for line in markdown.splitlines():
        cleaned = line.replace("#", "").replace("**", "").replace("`", "").strip()
        if cleaned:
            lines.append(cleaned)
    return "\n".join(lines) + "\n"


def _download_links(run_id: str) -> dict[str, str]:
    return {
        "markdown": f"/run/{run_id}/download/markdown",
        "txt": f"/run/{run_id}/download/txt",
        "json": f"/run/{run_id}/download/json",
    }


def _extract_pdf_text(raw: bytes) -> str:
    """Extract text from a text-based PDF. OCR is intentionally unsupported."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise HTTPException(
            status_code=500,
            detail="PDF extraction requires pypdf. Install dependencies with python3 -m pip install -r requirements.txt.",
        ) from exc

    temp_path = ROOT / "outputs" / "_uploaded_temp.pdf"
    try:
        temp_path.write_bytes(raw)
        reader = PdfReader(str(temp_path))
        text_parts = [(page.extract_text() or "") for page in reader.pages]
    finally:
        if temp_path.exists():
            temp_path.unlink()
    extracted = "\n\n".join(part.strip() for part in text_parts if part.strip()).strip()
    if not extracted:
        raise HTTPException(
            status_code=400,
            detail="No extractable text found. PDF support works for text-based PDFs only; scanned image PDFs are not supported.",
        )
    return extracted
