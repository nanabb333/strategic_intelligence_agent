# Changelog

## V4.9 - Enterprise Design Review And Freeze Assessment

### Added

- `docs/EnterpriseDesignReviewFreezeAssessment.md` with product, architecture, cohesion, technical debt, simplification, freeze, and V5-readiness assessments.
- `docs/releases/V4.9.md` release notes.

### Changed

- Documentation Index and release notes index now surface the V4.9 freeze recommendation.

### Recommendation

- Freeze V4 for product behavior, Decision Intelligence logic, evidence workflows, reviewer workflow, dashboard structure, local launch, and CI standards.
- Defer new capabilities to a V5 architecture planning phase.

### Preserved

- No product behavior, API, UI workflow, evidence processing, reasoning logic, evaluation, generated output, or test changes.

## V4.8 - Engineering Excellence Foundation And CI Quality Gates

### Added

- GitHub pull request and issue templates for release-scoped collaboration.
- Contribution standards covering branch strategy, commit conventions, release naming, validation, coding standards, documentation expectations, and privacy.
- GitHub Actions CI quality gates mirroring local validation.
- README CI badge.

### Preserved

- No product behavior, Decision Intelligence, API, UI workflow, evidence processing, generated output, or test changes.

## V4.7 - Enterprise Product Polish Release

### Changed

- Refined public-facing workspace copy, empty states, loading states, error messages, and release footer.
- Replaced stale public-facing agent terminology in the dashboard with product-aligned language.

### Preserved

- No Decision Intelligence, evidence, API, routing, evaluation, reviewer workflow, generated output, or product logic changes.

## V4.6 - Portfolio Demo Package Release

### Added

- `docs/DemoWalkthrough.md` for a three-minute reviewer demo path.
- `docs/PortfolioReviewGuide.md` for product, engineering, Decision Intelligence, and enterprise evaluation.
- Portfolio asset guidance for screenshots, sample inputs, sample outputs, and demo notes.
- Reviewer checklist under `portfolio_assets/demo_notes/`.

### Changed

- README now exposes a Demo in 3 Minutes path.
- Documentation Index now surfaces demo and portfolio review entry points.

### Preserved

- No Decision Intelligence, evidence, API, routing, evaluation, reviewer workflow, or product logic changes.

## V4.5 - Enterprise Product Presentation & Repository Excellence

### Changed

- Refined the repository presentation layer for CTO, technical due diligence, hiring manager, and portfolio review.
- Added product vision, enterprise readiness, and current architecture entry documents.
- Updated documentation navigation around product, architecture, user guides, developer guides, releases, governance, and research.
- Added release notes for V4.3, V4.4, and V4.5.
- Updated GitHub About guidance with non-agent, reviewer-first positioning and recommended topics.
- Updated security guidance for local-first usage and trust boundaries.

### Added

- `docs/ProductVision.md`
- `docs/EnterpriseReadinessChecklist.md`
- `docs/releases/V4.3.md`
- `docs/releases/V4.4.md`
- `docs/releases/V4.5.md`
- `portfolio_assets/` structure for curated screenshots, sample inputs, sample outputs, and future media.

### Preserved

- Existing Decision Intelligence behavior.
- Existing evidence, readiness, pathway, review, retrieval, evaluation, and artifact workflows.
- Existing local-first, deterministic, reviewer-controlled boundaries.

## V4.4 - Product Distribution Release

### Added

- Double-click launchers for macOS and Windows under `launch/`.
- Launcher documentation and local trust note.

### Changed

- Default local launch URL is `http://localhost:8000`.
- `/workspace` and `/dashboard/` both load dashboard assets correctly.

## V4.3 - Launch Experience Release

### Added

- Product landing page at `/`.
- Decision Workspace route at `/workspace`.
- Product-facing launcher flow through `launch.py` and `run_app.sh`.

### Preserved

- Backward-compatible `/dashboard/` route.
- Existing API endpoints and Decision Intelligence behavior.

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
