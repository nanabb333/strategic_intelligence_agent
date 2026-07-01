# Changelog

## Enterprise Product Consolidation

### Changed

- Reframed the README as an enterprise software product README.
- Standardized official product terminology in `docs/ProductTerminology.md`.
- Reorganized documentation navigation around product, architecture, evidence, decision, governance, and developer review paths.
- Clarified English as the official product language for the consolidated release.
- Grouped dashboard workspace panels into Evidence, Decision, and Review.
- Added architecture, module-boundary, API convention, demo-scenario, naming-review, and repository-maturity documentation.
- Consolidated duplicated decision-support helper logic into `src/decision_support_utils.py`.

### Removed

- Removed active Chinese language-selection UI and Chinese output paths.
- Removed Chinese-specific locale files, docs, and demo output artifacts from the current product surface.

### Preserved

- Existing Decision Brief generation behavior.
- Existing project workspace, evidence library, evidence retrieval, Evidence Intelligence, Decision Readiness, Domain Decision Evaluation, Decision Pathway Drafts, Pathway Comparison Matrix, and Decision Review workflows.
- Existing local JSON storage model.
- Existing deterministic, reviewer-first, non-autonomous product boundaries.
