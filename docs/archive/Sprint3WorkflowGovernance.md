# Sprint 3 Evidence-Aware Workflow Governance

Sprint 3 connects project evidence to reviewer workflow, decision lifecycle metadata, evidence audit records, timeline readiness, and confidence metadata. It remains deterministic and local-first.

## Product Boundary

Repo 5 is still not an autonomous agent, chatbot, autonomous browsing system, monitoring service, workflow engine, approval system, or multi-agent orchestration system.

Evidence retrieval remains user-triggered. Reviewer actions control acceptance, rejection, review status, and archival.

## Evidence Lifecycle

Evidence lifecycle states are deterministic metadata:

- `retrieved`
- `validated`
- `ranked`
- `needs_review`
- `accepted`
- `rejected`
- `referenced`
- `archived`

Retrieval, validation, and ranking do not imply acceptance. Acceptance remains reviewer-controlled.

## Decision Lifecycle

Decision lifecycle states are lightweight governance metadata:

- `draft`
- `evidence_review`
- `reviewed`
- `finalized`
- `superseded`
- `archived`

The default state is `draft`. A completed analysis run can be marked `reviewed` as decision metadata, but this does not imply legal, business, or executive approval.

## Reviewer Workflow Metadata

Project evidence can carry:

- `reviewer_status`
- `reviewer_note`
- `reviewed_at`
- `review_reason`
- `evidence_action`

Supported reviewer actions:

- `accept`
- `reject`
- `mark_needs_review`
- `archive`
- `reference_in_decision`

There is no authentication or approval workflow in Sprint 3.

## Evidence Workflow Ledger

The project can store append-only evidence audit entries under `evidence_audit_log`. Each entry records:

- project and question context
- decision run ID when relevant
- evidence ID and trace ID
- lifecycle state
- reviewer action and rationale
- validation status
- ranking score when available
- confidence-effect metadata
- timestamp

The ledger is an audit layer, not another narrative report.

## Confidence Metadata

Sprint 3 records additive confidence-effect metadata such as:

- `strengthens_confidence_metadata`
- `weakens_confidence_metadata`
- `requires_reviewer_attention`
- `neutral_confidence_metadata`

This does not change final confidence behavior or Decision Brief generation.

## Timeline Readiness

Decision Timeline and future Evidence Timeline views can derive records from:

- `decision_history`
- `evidence_audit_log`
- selected evidence IDs
- run metadata

No dashboard redesign is required for the metadata to remain useful.

## Rollback Safety

All Sprint 3 fields are additive. If lifecycle and ledger metadata are ignored:

- Decision Brief still works.
- Project Workspace still works.
- existing evidence acceptance still works.
- analysis still works.
- older project evidence remains readable.
