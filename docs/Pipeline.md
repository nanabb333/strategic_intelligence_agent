# Analysis Pipeline

The analysis pipeline lives in `src/analysis_pipeline.py`.

## Main Function

```python
execute_analysis_pipeline(
    *,
    text: str,
    language: str,
    output_mode: str,
    question_id: str,
    question_text: str,
    source_url: str,
    input_mode: str,
    uploaded_filename: str,
    file_type: str,
) -> dict[str, Any]
```

## Current Workflow

```text
Input Preparation
  |
  v
Run Folder Creation
  |
  v
Agent Routing and Question Routing
  |
  v
Event Context and Event Understanding
  |
  v
Issue Extraction and Scenario Classification
  |
  v
Historical Analogue and Context Retrieval
  |
  v
Implication, Mechanism, Lens, and Evidence Analysis
  |
  v
Historical Outcome and Strategic Lesson Retrieval
  |
  v
Strategic Assessment and Response Pattern Retrieval
  |
  v
Executive Brief Generation and Localization
  |
  v
Artifact Construction
  |
  v
Run Storage
```

## Outputs Written Per Run

Each run writes these files under `outputs/runs/<run_id>/`:

- `input.txt`
- `analysis.json`
- `brief.md`
- `brief.txt`
- `agent_trace.json`
- `metadata.json`

The pipeline preserves the existing artifact structure used by the dashboard and download endpoints.
