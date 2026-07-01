# Enterprise Architecture

Repo 5 is a local-first, deterministic Decision Intelligence product. It uses FastAPI, vanilla dashboard assets, Python modules, local JSON project files, and generated Markdown/TXT/JSON artifacts.

## Product Flow

```mermaid
flowchart TD
  User["Reviewer"]
  Workspace["Decision Workspace"]
  Evidence["Evidence Layer"]
  Intelligence["Evidence Intelligence"]
  Readiness["Decision Readiness"]
  Framework["Decision Framework"]
  Pathways["Decision Pathway Drafts"]
  Comparison["Pathway Comparison Matrix"]
  Review["Decision Review"]
  Record["Decision Record (Future)"]

  User --> Workspace
  Workspace --> Evidence
  Evidence --> Intelligence
  Intelligence --> Readiness
  Readiness --> Framework
  Framework --> Pathways
  Pathways --> Comparison
  Comparison --> Review
  Review --> Record
```

## Module Dependency Direction

```mermaid
flowchart LR
  EI["evidence_intelligence.py"]
  DF["decision_frameworks.py"]
  DR["decision_readiness.py"]
  DP["decision_pathways.py"]
  DE["domain_evaluation.py"]
  PC["pathway_comparison.py"]
  RV["decision_review.py"]
  PW["project_workspace.py"]

  PW --> EI
  EI --> DR
  DF --> DR
  DE --> DR
  DR --> DP
  DP --> PC
  DE --> PC
  PC --> RV
```

The desired direction is evidence to readiness to pathways to comparison to review. Shared utility modules may be imported across layers only when they have no product-layer dependency.

## Runtime Interaction

```mermaid
sequenceDiagram
  participant Browser as Dashboard
  participant API as app.py FastAPI
  participant Workspace as project_workspace.py
  participant Engine as Decision Engine
  participant Artifacts as Local JSON/Markdown/TXT

  Browser->>API: Create/open project
  API->>Workspace: Read/write project JSON
  Browser->>API: Run analysis with project_id, question_id, evidence_ids
  API->>Workspace: Build Evidence Bundle
  API->>Engine: Execute deterministic pipeline
  Engine->>Artifacts: Persist run artifacts
  API->>Workspace: Attach run to project question
  Browser->>API: Read intelligence/readiness/pathways/comparison/review
  API->>Workspace: Read project state
```

## Product Boundaries

- No autonomous background research.
- No scheduled monitoring.
- No LLM orchestration.
- No database or cloud service.
- Retrieval creates reviewable evidence candidates only.
- Decision Review records reviewer interpretation; it does not approve, reject, select, or recommend.
