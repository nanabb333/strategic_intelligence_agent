# Next Sprint Plan

## Current Status

Version 4.1 added the Decision Context layer.

The platform now supports project-aware analysis, selected project evidence IDs, evidence bundles, run metadata linked to project and question, workspace state, evidence lifecycle, and durable evidence IDs in decision history.

## Next Sprint: User-Triggered Evidence Retrieval

Live retrieval should only happen when the user explicitly requests it.

## Rules

- No autonomous browsing.
- No background monitoring.
- No autonomous decision-making.
- No agents.
- Retrieved evidence must enter a review queue first.
- Accepted evidence can enter the Evidence Library.
- Selected evidence can enter the Decision Context.
- The deterministic Decision Engine remains unchanged.

## Proposed Flow

User clicks Search Current Evidence

↓

Retrieved Evidence Review Queue

↓

User accepts evidence

↓

Evidence Library

↓

User selects evidence

↓

Analyze

↓

Decision Context

↓

Decision Brief / Timeline / Delta

## UX Cleanup

- Add project delete support with confirmation.
- Add project rename support.
- Add empty-state demo loading separately from user-created projects.
- Keep demo projects out of first-time user workspace by default.