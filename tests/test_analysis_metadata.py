from types import SimpleNamespace

from analysis_metadata import build_analysis_metadata


def test_build_analysis_metadata_preserves_keys_and_paths() -> None:
    question_route = SimpleNamespace(question_text="What matters?", intent="Decision Support")

    metadata = build_analysis_metadata(
        run_id="run_20260626_001",
        language="en",
        output_mode="analyst",
        question_id="meaning",
        question_route=question_route,
        source_url="",
        input_mode="paste_text",
        uploaded_filename="",
        file_type="text",
    )

    assert metadata["run_id"] == "run_20260626_001"
    assert metadata["question_text"] == "What matters?"
    assert metadata["question_intent"] == "Decision Support"
    assert metadata["question_intent_label"] == "Decision Support"
    assert metadata["status"] == "complete"
    assert metadata["artifact_paths"] == {
        "input": "outputs/runs/run_20260626_001/input.txt",
        "analysis": "outputs/runs/run_20260626_001/analysis.json",
        "brief_markdown": "outputs/runs/run_20260626_001/brief.md",
        "brief_text": "outputs/runs/run_20260626_001/brief.txt",
        "agent_trace": "outputs/runs/run_20260626_001/agent_trace.json",
        "metadata": "outputs/runs/run_20260626_001/metadata.json",
    }
    assert "created_at" in metadata
