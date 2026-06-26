# Future Engineering Recommendations

This document captures improvements that are worth considering but were intentionally not implemented during the public-readiness pass because they could affect behavior, require product decisions, or deserve their own review.

## Architecture And Packaging

- Decide whether to make `src/` a formal Python package with `__init__.py` files and package-relative imports. This could improve import consistency, but it should be done as a focused migration with tests because current imports rely on the existing path setup.
- Review `live_evidence.py`. It appears to overlap conceptually with URL extraction, but it is tracked at the repository root and should not be removed or moved without confirming whether it is still used as a standalone utility.
- Consider grouping older milestone-specific docs under a version-history or archive folder. This would improve public navigation, but moving many docs can break existing links.

## Testing

- Add tests for file extraction and unsupported file types.
- Add tests for TXT and JSON download content types, not just status codes.
- Add a small regression fixture for one known sample output shape.
- Add a smoke test for localization parity if output structure changes again.
- Add formal golden output fixtures for representative cases, focusing on structure and required sections rather than exact long-form text.

## CI And Quality

- Consider adding a markdown link checker after documentation paths stabilize.
- Consider adding dependency vulnerability scanning after a license and release policy are selected.
- Consider pinning dependency versions for repeatable releases. Current dependencies use broad ranges for local development convenience.

## Product Documentation

- Add a short demo video or verified screenshots from a fresh local run.
- Add a current generated artifact walkthrough showing `analysis.json`, `brief.md`, `agent_trace.json`, and `metadata.json`.
- Add a single "reviewer path" page for recruiters and admissions reviewers if the docs continue to grow.

## Scientific Credibility

- Add human-labeled benchmark documents with reviewer disagreement notes.
- Add source-grounded factual evaluation against primary-source excerpts.
- Separate benchmark consistency metrics from any future human quality judgments.
- Track known failure cases as first-class evaluation artifacts.

## Public Release Decisions

- Select a license before encouraging external reuse.
- Decide whether demo outputs should be treated as stable examples or regenerated for each major portfolio milestone.
- Decide whether the project should remain a local app only or eventually receive a separate production deployment plan.

## Security

- Do not deploy the current app publicly without adding authentication, authorization, input-size limits, production CORS settings, logging policy, and deployment hardening.
- Add a secrets policy before any external API integration is introduced.
