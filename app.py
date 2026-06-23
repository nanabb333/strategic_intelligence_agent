"""Local FastAPI application for Strategic Intelligence Agent."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from datetime import datetime
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

from agent_router import route_document  # noqa: E402
from brief_generator import generate_brief  # noqa: E402
from context_retriever import retrieve_current_context  # noqa: E402
from evidence_assessor import assess_evidence  # noqa: E402
from historical_retriever import retrieve_historical_analogues  # noqa: E402
from implication_analyzer import analyze_implications  # noqa: E402
from issue_extractor import extract_issues  # noqa: E402
from mechanism_detector import detect_mechanisms  # noqa: E402
from multi_lens_analyzer import analyze_lenses  # noqa: E402
from output_adapter import adapt_output  # noqa: E402
from outcome_retriever import retrieve_historical_outcomes  # noqa: E402
from response_playbook_retriever import retrieve_response_patterns  # noqa: E402
from scenario_classifier import classify_scenarios  # noqa: E402
from strategic_lessons import generate_strategic_lessons  # noqa: E402
from tool_registry import build_default_registry  # noqa: E402


RUNS_DIR = ROOT / "outputs" / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)


class AnalyzeRequest(BaseModel):
    """Request payload for local analysis."""

    text: str = Field(..., min_length=1)
    language: str = "en"
    output_mode: str = "analyst"
    question_id: str = "meaning"
    question_text: str = "What does this issue mean?"


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
    version="7.0",
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
    return {"status": "ok", "app": "Strategic Intelligence Agent", "version": "7.0"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Run the real Python pipeline and persist run artifacts."""
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")

    run_id = _next_run_id()
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    registry = build_default_registry()
    route = route_document(text, registry)
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
        response_patterns=response_patterns,
    )
    brief_markdown = adapt_output(base_brief, mode=request.output_mode, language=request.language)
    brief_text = _markdown_to_text(brief_markdown)

    metadata = {
        "run_id": run_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "language": request.language,
        "output_mode": request.output_mode,
        "question_id": request.question_id,
        "question_text": request.question_text,
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
        response_patterns=response_patterns,
        route=route,
        metadata=metadata,
    )
    agent_trace = {
        "selected_tools": route.selected_tools,
        "skipped_tools": route.skipped_tools,
        "trace": _serializable(route.trace),
        "reasoning_record": _serializable(route.reasoning_record),
        "reasoning_stages": [
            "Historical analogue retrieval",
            "Historical outcome retrieval",
            "Strategic lesson generation",
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
    existing = sorted(RUNS_DIR.glob(f"run_{date_part}_*"))
    next_index = len(existing) + 1
    return f"run_{date_part}_{next_index:03d}"


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
        "scenario": _serializable(classifications[0]) if classifications else {},
        "mechanisms": _serializable(items["mechanisms"].get(issue_title, [])),
        "analogues": _serializable(items["analogues"].get(issue_title, [])),
        "historical_outcomes": _serializable(items["historical_outcomes"].get(issue_title, [])),
        "strategic_lessons": _serializable(items["strategic_lessons"].get(issue_title, [])),
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
                "Historical analogue retrieval",
                "Historical outcome retrieval",
                "Strategic lesson generation",
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
