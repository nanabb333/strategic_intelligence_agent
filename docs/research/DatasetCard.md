# Research Dataset Card

## Status and Intended Scope

The final research dataset has not been assembled. This card defines its intended contract. The existing `evaluation/benchmark_cases.csv` contains synthetic regression cases and is not the final research dataset, an independent held-out test set, or evidence of external validity.

The planned dataset will contain strategic decision-review cases drawn from traceable public materials across a deliberately bounded set of domains. Scope and domain balance must be frozen before final evaluation.

## Required Source Metadata

Each source record must include a stable identifier, title, publisher, publication date, retrieval date, URL or archival locator, primary/secondary source type, language, jurisdiction where relevant, and license or permitted-use note.

Each annotated claim must include the exact claim, a claim-level supporting passage, source identifier, support relationship, annotator identifier, annotation timestamp, and adjudication status.

## Temporal Cutoff and Hindsight Leakage

Each case must define a decision-time cutoff. Only material available on or before that cutoff may be included in the input condition. Later outcomes may be stored separately for retrospective analysis but must not enter retrieval, labels, prompts, pathway construction, or reviewer materials. Dataset build scripts should enforce the cutoff and log exclusions.

## Inclusion Criteria

- Traceable public source with sufficient context for review.
- Clear decision question or a documented procedure for framing it.
- At least one independently identifiable supporting or weakening claim.
- Source date and retrieval provenance available.
- Use is compatible with copyright, privacy, and research-governance requirements.

## Exclusion Criteria

- Unverifiable summaries with no source locator.
- Material requiring confidential or personal data without approval.
- Cases written solely to reproduce current keyword rules.
- Cases whose gold labels were used to tune the evaluated rule set.
- Sources published after the case's decision-time cutoff.

## Provenance and Versioning

Raw-source manifests, normalized records, annotations, exclusions, and transformations must be versioned separately. Releases should use immutable dataset versions and checksums. Corrections require a changelog and must not silently alter previously reported results.

## Annotation Procedure

An annotation guide will define unsupported claims, attribution correctness, critical limitations, rationale completeness, analogue relevance, and ambiguous cases. At least two independent annotators are planned for research outcomes, followed by documented adjudication. Annotators should not see system condition labels when feasible.

## Data Splits

Development, pilot, and final evaluation cases must be separated before main analysis. The final evaluation set must not be used to author keyword rules, pathway templates, expected labels, or thresholds.

## Current Limitations

The repository knowledge base still contains educational summaries with incomplete primary-source provenance. Those records may support software demonstrations but are not automatically eligible for the research dataset. No final dataset size, domain distribution, annotation agreement, or performance result is currently claimed.
