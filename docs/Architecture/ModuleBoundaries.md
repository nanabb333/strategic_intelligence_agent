# Module Boundaries

This document defines ownership for the major Version 5 enterprise modules.

| Module | Responsibility | Inputs | Outputs | Dependencies |
| --- | --- | --- | --- | --- |
| `app.py` | FastAPI route layer and static dashboard mounting. | HTTP requests, project IDs, run IDs. | JSON responses, file downloads. | Service and project modules only. |
| `src/project_workspace.py` | Local JSON project persistence. | Project, question, evidence, review payloads. | Project dictionaries, evidence bundles, timeline, delta. | Standard library and storage helpers. |
| `src/evidence_retrieval.py` | User-triggered retrieval candidate interface. | Query, optional project ID, allowed sources. | Review queue candidates. | Retrieval provider utilities. |
| `src/evidence_provider.py` | Provider-independent retrieval provider contracts. | Provider request parameters. | Raw provider documents or errors. | No decision modules. |
| `src/evidence_retriever.py` | Provider selection and retrieval pipeline. | Search/retrieve request. | Parsed and normalized evidence candidates. | Provider, parser, normalizer. |
| `src/evidence_parser.py` | HTML/text extraction and metadata parsing. | Raw fetched content. | Parsed title, body, metadata, canonical URL. | Standard library. |
| `src/evidence_normalizer.py` | Convert provider documents to EvidenceItem-compatible dictionaries. | Parsed document metadata. | Evidence item dictionaries. | Existing evidence schema conventions. |
| `src/evidence_intelligence.py` | Deterministic evidence-set review support. | Evidence Library items. | Duplicates, conflicts, novelty, coverage, freshness, attention queue. | No readiness/pathway/review dependency. |
| `src/decision_frameworks.py` | Deterministic framework catalog and question classification. | Decision question and context metadata. | Applicable frameworks. | No evidence mutation. |
| `src/domain_evaluation.py` | Domain-specific evidence mapping with advisory boundaries. | Decision question, context, evidence items. | Domain evaluation results, risks, constraints, reviewer questions. | Evidence references and shared utilities. |
| `src/decision_readiness.py` | Map evidence and framework requirements into readiness. | Question, context, evidence, Evidence Intelligence. | Readiness map, gaps, assumptions, unknowns, reviewer questions. | Evidence Intelligence, Decision Framework, Domain Evaluation. |
| `src/decision_pathways.py` | Generate deterministic pathway drafts from readiness. | Decision Readiness Map and evidence refs. | Decision Pathway Draft Set. | Decision Readiness and shared utilities. |
| `src/pathway_comparison.py` | Build categorical comparison matrix. | Pathway drafts, readiness, domain evaluation, evidence intelligence. | Pathway Comparison Matrix. | Downstream of pathways/readiness/domain/evidence intelligence. |
| `src/decision_review.py` | Reviewer-controlled review state and summary. | Reviewer status/note/question updates. | Decision Review State and summary. | Project-scoped data and shared utilities. |
| `src/decision_support_utils.py` | Dependency-free shared helpers. | Evidence refs, strings, project dicts. | De-duplicated refs/strings, selected project question. | None. |

## One-Way Dependency Rule

Evidence modules can support readiness. Readiness can support pathways. Pathways can support comparison. Comparison can support review. Review must not change upstream evidence, readiness, pathway, or comparison outputs.

## Current Refactor Finding

The consolidation extracted duplicated evidence-reference de-duplication and project-question selection into `src/decision_support_utils.py`. No endpoint schema or decision behavior changed.
