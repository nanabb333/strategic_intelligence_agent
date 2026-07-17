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
Neutral Decision Assessment, Evidence Ledger, Evidence Sufficiency Assessment, and Artifact Completeness Check
  |
  v
English Brief Generation
  |
  v
Artifact Construction
  |
  v
Run Storage
```

The pipeline is deterministic and local. It does not perform live web research, autonomous planning, or probability scoring.

New runs expose `decision_assessment`, `evidence_ledger`, `evidence_sufficiency`, and `artifact_completeness` in `analysis.json`. Legacy `decision_case`, `confidence_assessment`, and `decision_quality_evaluation` fields are read-only compatibility inputs and are not written into new runs.

`decision_assessment.judgment_boundary` records that judgment ownership belongs to the reviewer; it is not a system judgment. Evidence Sufficiency is a structural assessment only, and Artifact Completeness is exported as passed/missing structural checks rather than a quality-like score.

## Outputs Written Per Run

Each run writes these files under `outputs/runs/<run_id>/`:

- `input.txt`
- `analysis.json`
- `brief.md`
- `brief.txt`
- `agent_trace.json`
- `metadata.json`

The pipeline preserves the existing artifact structure used by the dashboard and download endpoints.
