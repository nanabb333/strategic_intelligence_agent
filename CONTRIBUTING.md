# Contributing

Strategic Intelligence Decision Companion is maintained as a local-first, reviewer-first Enterprise Decision Intelligence product. Contributions should improve product quality, engineering maturity, documentation accuracy, or explicitly scoped functionality without weakening determinism, traceability, or reviewer control.

This repository is not a chatbot project, autonomous agent, forecasting system, legal advisor, investment advisor, or live monitoring service.

## Branch Strategy

- Use short-lived branches for focused work.
- Prefer descriptive branch names such as `docs/v4-8-engineering-foundation`, `fix/evidence-review-copy`, or `product/v4-7-polish`.
- Keep `main` releasable.
- Rebase or merge from `main` before review when a branch has drifted.
- Do not force-push shared branches unless maintainers explicitly agree.

## Commit Message Convention

Use a short conventional prefix followed by the release or change intent:

```text
docs: clarify decision readiness workflow
fix: load workspace assets from product routes
product: V4.7 enterprise product polish release
engineering: V4.8 sprint 1 engineering foundation
```

Recommended prefixes:

- `product:` for product presentation, release packaging, or portfolio polish.
- `engineering:` for repository standards, maintainability, or developer workflow.
- `docs:` for documentation-only changes.
- `fix:` for bug fixes.
- `test:` for test-only changes.
- `chore:` for small maintenance changes with no product behavior impact.

## Release Naming Convention

Release work should include:

- Release version, for example `V4.8 Sprint 1`.
- Release theme, for example `Engineering Excellence Foundation`.
- Clear objectives.
- Explicit non-goals.
- Validation results.
- Known risks or follow-up work.

Avoid mixing unrelated release themes in one pull request.

## Coding Standards

- Preserve deterministic behavior unless a feature release explicitly changes it.
- Keep module responsibilities narrow and aligned with existing architecture.
- Do not change API routes, request schemas, response schemas, or storage formats casually.
- Do not introduce autonomous research, autonomous monitoring, hidden LLM orchestration, external RAG frameworks, databases, cloud services, or background workers without an approved architecture decision.
- Keep user-facing scores explicit, for example `7.5 / 10` or `82%`.
- Prefer clear, small changes over broad rewrites.
- Do not commit local credentials, private source material, generated scratch artifacts, or environment-specific files.

## Documentation Standards

Documentation must describe implemented behavior accurately.

Update documentation when a change affects:

- Product workflow.
- API usage.
- Local setup.
- Architecture or module responsibilities.
- Release notes or repository navigation.
- User-facing limitations.

Do not claim unsupported capabilities such as real-world accuracy guarantees, legal conclusions, investment recommendations, live monitoring, autonomous browsing, or enterprise cloud deployment.

## Validation Checklist Before Merge

Run the relevant checks before opening or merging a pull request. For release-level changes, run the full suite:

```bash
.venv/bin/ruff check .
python3 -m py_compile app.py src/*.py launch.py
python3 -m pytest
node --check dashboard/app.js
node --check dashboard/project.js
```

GitHub Actions runs the same core quality gates on push and pull request through `.github/workflows/ci.yml`. Local validation is still expected before review so failures can be corrected before CI runs.

For documentation-only changes, also verify repository-local Markdown links when practical.

Document commands run and results in the pull request.

## Pull Request Expectations

Every pull request should include:

- Summary of what changed.
- Release theme or issue context.
- Scope and explicit non-goals.
- Product behavior impact.
- Validation commands and results.
- Documentation updates, if applicable.
- Risks, limitations, or follow-up work.

If product behavior changes, explain why the change is in scope and how reviewer control, traceability, and deterministic execution are preserved.

## Runtime Artifacts

Local run folders under `outputs/runs/` are generated artifacts and should not be committed unless a release explicitly includes curated demo outputs.

## Security And Privacy

- Do not include credentials, tokens, API keys, private documents, or sensitive source material in issues, pull requests, commits, screenshots, or demo artifacts.
- Keep local-first operation clear in documentation.
- Treat reviewer notes, evidence samples, and project files as potentially sensitive unless they are clearly synthetic demo assets.
