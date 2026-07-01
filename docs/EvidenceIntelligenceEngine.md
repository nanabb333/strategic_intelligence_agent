# Evidence Intelligence Engine

Version 6.0 Phase 4 added a deterministic Evidence Intelligence Engine for reviewer workflows.
Version 6.0 Phase 6 extends it with decision-grade traceability, risk evidence mapping, regulatory / legal constraint awareness, and historical pathway signals.

The engine does not retrieve evidence, accept evidence, reject evidence, search the web, monitor sources, call an LLM, make investment recommendations, provide legal advice, or generate a Decision Brief. It reads an evidence set and returns reviewer-facing signals about evidence quality, overlap, coverage, freshness, attention needs, and decision-relevant evidence patterns.

## What It Produces

Given EvidenceItem-like records, the engine returns:

- evidence set summary
- duplicate and near-duplicate groups
- support / potential conflict / insufficient information relationships
- novelty signals
- source coverage analysis
- freshness and staleness analysis
- reviewer attention queue
- traceable signal records with evidence references
- decision risk evidence map
- regulatory / legal constraint flags
- historical pathway signals

## Deterministic Heuristics

Duplicate detection uses:

- same source URL
- same canonical URL when present
- same normalized title
- high token overlap in excerpt or summary

Relationship detection uses conservative labels:

- `supports`: overlapping topic terms plus compatible source category or close published dates
- `potential_conflict`: explicit contradiction markers or opposing claim phrases
- `insufficient_information`: not enough deterministic evidence to infer support or conflict

Novelty detection checks whether an item adds:

- new source
- new date
- new source type
- new claim keywords
- new geography
- new company, regulator, or actor mention

Coverage analysis maps evidence into deterministic categories such as official government, regulator, company IR, SEC filing, major news, academic, legal/regulatory, financial market, and unknown.

Freshness analysis uses `published_at` and `retrieved_at` only. Missing dates are surfaced as reviewer risks.

## Signal Traceability

Every new decision-grade signal includes evidence references. References use existing stable evidence identifiers when available:

- `id`
- `evidence_id`
- `trace_id`
- source URL
- title
- source name
- published / retrieved / created date

If an older evidence record has no stable ID, the engine creates a deterministic fallback reference from normalized title, normalized URL, normalized source, and created or retrieved timestamp. The fallback is stable for the same record and does not use random IDs.

Dashboard sections show the evidence title, source, date, source URL when available, and a “Jump to evidence” control when a matching evidence card can be found in the current project view.

## Decision Risk Evidence Map

The risk map classifies evidence text into deterministic categories such as:

- market risk
- financial risk
- policy risk
- regulatory risk
- legal / compliance risk
- sanctions / export control risk
- antitrust / competition risk
- disclosure / reporting risk
- supply chain risk
- operational execution risk
- geopolitical risk
- reputational risk
- data privacy / security risk
- counterparty risk
- uncertainty / unknowns

Each signal includes:

- risk category
- evidence references
- matched terms
- reviewer explanation
- confidence bucket: `high`, `medium`, or `low`
- limitation note, especially when the evidence is sparse

The map is a reviewer triage aid. It does not determine whether a risk is material or decide how to act.

## Regulatory / Legal Constraint Awareness

Constraint flags identify evidence that may require legal or compliance review. Categories include securities disclosure, sanctions / export controls, antitrust / competition, data privacy, licensing / approval, litigation / enforcement, fiduciary / governance, labor / employment, environmental regulation, consumer protection, and unknown regulatory exposure.

Every flag uses cautious language:

- “May require legal / compliance review.”
- “Reviewer should verify jurisdiction and applicability.”
- “Not legal advice.”

The engine does not conclude that conduct is allowed, prohibited, valid, invalid, or legally sufficient. It only flags terms and evidence references for human review.

## Historical Pathway Foundation

Historical pathway signals identify possible scenario families without probabilities:

- base case continuity
- market repricing
- regulatory escalation
- policy relief
- supply chain reconfiguration
- corporate strategy shift
- litigation or enforcement path
- geopolitical escalation
- demand shock
- earnings revision
- delayed resolution

Each pathway signal includes evidence references, triggering terms, related risk categories, a reviewer explanation, an analogue hint, and a limitation note. These are not forecasts. Reviewers should compare facts, timing, actors, source quality, and evidence sequence before using a pathway in analysis.

## API

The optional read-only API is:

```text
GET /projects/{project_id}/evidence/intelligence
```

It reads the project evidence library and returns evidence intelligence. It does not mutate project state, retrieve new evidence, run analysis, or generate a Decision Brief.

## Dashboard Panel

The dashboard exposes Evidence Intelligence inside the active Project Workspace, directly below the Evidence Library retrieval and review queue.

The panel is read-only. It calls:

```text
GET /projects/{project_id}/evidence/intelligence
```

It helps reviewers inspect:

- review recommendations
- possible duplicate evidence
- potential conflicts
- possible support relationships
- evidence that may introduce new context
- source coverage gaps
- stale or undated evidence
- source concentration risk
- traceable decision-grade signals
- risk evidence categories
- regulatory / legal review flags
- possible historical pathway families

The panel does not accept evidence, reject evidence, retrieve URLs, search, monitor sources, or change the Decision Brief. Reviewers still decide which evidence to accept and which accepted evidence to select for an analysis run.

## Reviewer Use

Reviewers should treat these outputs as triage signals:

- duplicate groups reduce repeated review effort
- support relationships show corroborating items
- potential conflicts identify pairs requiring manual review
- novelty helps prioritize genuinely new evidence
- coverage gaps show what source categories are absent
- freshness risk highlights stale or undated evidence

These signals are deterministic aids, not automated judgments. The reviewer remains responsible for accepting evidence and deciding whether it should be used in an analysis run.

The workflow remains reviewer-controlled:

1. A reviewer adds or accepts evidence into the project evidence library.
2. The read-only Evidence Intelligence panel summarizes deterministic signals.
3. The reviewer selects which accepted evidence should be used in an analysis run.
4. The existing deterministic Decision Intelligence pipeline generates the Decision Brief.

## Limitations

The engine uses simple token, metadata, and phrase heuristics. It cannot verify factual truth, infer complex legal meaning, resolve contradictions, forecast outcomes, estimate probabilities, or provide investment or legal advice. It intentionally avoids LLM interpretation so the output remains predictable, inspectable, and testable.
