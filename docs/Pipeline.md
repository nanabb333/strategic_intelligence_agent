# Analysis Pipeline

The analysis pipeline lives in `src/analysis_pipeline.py`.

## Related Docs

- [Documentation Index](DocumentationIndex.md)
- [Product Overview](ProductOverview.md)
- [Engineering Architecture](EngineeringArchitecture.md)
- [Folder Structure](FolderStructure.md)
- [Testing](Testing.md)

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
Document Routing and Question Routing
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
Decision Case, Evidence Ledger, Confidence Assessment, and Decision Quality Evaluation
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

The pipeline is deterministic and local. It does not perform live web research, autonomous planning, or probability scoring.

The V2 decision-quality layer is additive. It exposes `decision_case`, `evidence_ledger`, `confidence_assessment`, and `decision_quality_evaluation` in `analysis.json` without removing earlier fields or changing download behavior.

## Outputs Written Per Run

Each run writes these files under `outputs/runs/<run_id>/`:

- `input.txt`
- `analysis.json`
- `brief.md`
- `brief.txt`
- `agent_trace.json`
- `metadata.json`

The pipeline preserves the existing artifact structure used by the dashboard and download endpoints.
