# Sprint 2 Evidence-Aware Decision Intelligence Architecture

Sprint 2 adds deterministic evidence foundations without changing the Decision Brief, reasoning engine, dashboard workflow, or backend architecture.

## Product Boundary

Evidence retrieval remains user-triggered. Providers produce normalized `EvidenceItem` records only. Reviewers decide which evidence is accepted into a project, and project-aware analysis consumes accepted evidence through the existing Evidence Ledger boundary.

The system does not add autonomous browsing, scheduled monitoring, autonomous conclusions, chatbot behavior, multi-agent orchestration, databases, or cloud services.

## Normalized EvidenceItem

`src/evidence_retrieval.py` defines a normalized evidence record with:

- stable `evidence_id`
- stable `trace_id`
- source metadata
- published and retrieved dates
- excerpt and summary
- credibility tier and internal credibility score
- freshness note
- relevance score
- validation status and validation notes
- conflict status
- reviewer lifecycle status

This schema is additive. Existing project evidence remains compatible.

## Provider Boundary

Providers are small adapters that return raw evidence-like records for normalization:

- `ExistingRetrievedEvidenceProvider`
- `ManualEvidenceProvider`
- `LocalDocumentEvidenceProvider`

Providers do not make decisions and do not run automatically.

## Validation And Ranking

Validation flags missing title, source, date, excerpt, weak metadata, duplicate title or URL, stale evidence, and unsupported source type.

Ranking is deterministic. It combines credibility, freshness, relevance, completeness, validation status, and reviewer acceptance status. It does not use LLM judgment.

## Traceability

Each normalized item carries a stable `trace_id`. Accepted evidence preserves evidence metadata in project storage so reviewers can trace:

```text
EvidenceItem -> Project Evidence -> Accepted Evidence -> Analysis Input -> Decision Run
```

## Missing And Conflicting Evidence

Sprint 2 prepares deterministic flags for:

- no official evidence
- no reviewer-accepted evidence
- evidence requiring metadata review
- explicit or potential conflicts
- stale evidence

Conflicts are surfaced only when available metadata or explicit labels indicate them.

## Confidence Impact Preparation

The module prepares additive confidence-impact metadata:

- evidence that may improve confidence
- evidence that may reduce confidence
- missing-evidence notes

Final confidence behavior is unchanged.

## Historical Analogue Interaction

Historical analogues remain structural context. Live or current evidence provides factual grounding only after reviewer acceptance. Conflicts between current evidence and historical patterns should be surfaced, not hidden, and current evidence should not automatically override historical analogy.
