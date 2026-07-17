# Product Overview

Strategic Intelligence Decision Companion is a deterministic, auditable, reviewer-first strategic decision-support system. The local FastAPI application turns a defined decision, reviewer context, and supporting evidence into inspectable decision-support artifacts.

## Product Purpose

```text
Decision Question
  -> Decision Context
  -> Supporting Evidence
  -> Decision Assessment
  -> Human Review
  -> Export
```

The decision is the primary product object. A Project may persist related questions, evidence, assessments, timeline, delta, and review state, but project management is secondary to the decision-first workflow.

## Reviewer Control

The reviewer defines the question and context, chooses the supporting evidence, inspects assumptions and limitations, records review state, and makes any final decision. Pathway drafts support comparison without ranking, preferred-option selection, or autonomous recommendation.

## Inputs

The current local app supports:

- a plain-language Decision Question
- optional reviewer-authored Decision Context
- pasted supporting evidence
- uploaded `.txt`, `.md`, `.markdown`, and text-based `.pdf` files
- user-provided readable URLs when extraction succeeds
- accepted evidence stored in the current Project

PDF extraction is text-based only; scanned image PDFs are not supported.

## Outputs

The dashboard and pipeline provide:

- beginner, analyst, and executive output modes
- a Neutral Decision Assessment with no automatic pathway selection
- evidence sufficiency, strategic considerations, assumptions, uncertainties, and limitations
- an Artifact Completeness Check that validates structure rather than decision quality
- evidence-intelligence and readiness views
- non-ranked pathway drafts and categorical comparison
- reviewer-controlled notes, statuses, and unresolved questions
- Markdown, TXT, JSON, tool-routing compatibility trace, and metadata artifacts under `outputs/runs/`

## Product Value

The product helps a reviewer ask:

- What decision requires judgment?
- What context and constraints shape it?
- Which evidence supports or weakens the assessment?
- What assumptions, unknowns, and gaps remain?
- Which possible pathways deserve comparison?
- What requires human review or later reassessment?

## Boundaries

The product is local-first and single-user. It does not provide autonomous research, background monitoring, forecasts or probabilities, preferred-option selection, investment or legal advice, compliance automation, authentication, cloud deployment, OCR, or real-world accuracy guarantees. All outputs require human review.

## Related Documentation

- [README](../README.md)
- [Documentation Index](DocumentationIndex.md)
- [Product Vision](ProductVision.md)
- [Product Terminology](ProductTerminology.md)
- [Canonical Architecture](architecture.md)
- [Engineering Architecture](EngineeringArchitecture.md)
- [Testing](Testing.md)
