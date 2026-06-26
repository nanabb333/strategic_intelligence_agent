# Contributing

This repository is maintained as a local AI product and portfolio project. Contributions should preserve existing behavior unless a change is explicitly scoped as a feature release.

## Development Principles

- Do not change API routes without a migration plan.
- Do not change request or response schemas casually.
- Do not introduce forecasting, probabilities, trading recommendations, investment advice, or legal advice.
- Keep analysis changes deterministic and reviewable.
- Prefer small pull requests with clear validation results.
- Keep documentation factual and aligned with the current repository.

## Local Setup

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn app:app --reload
```

Open the local dashboard:

```text
http://127.0.0.1:8000/dashboard/
```

## Quality Checks

Run these checks before opening a pull request:

```bash
python3 -m ruff check .
python3 -m compileall app.py src tests
python3 -m pytest
```

## Pull Request Expectations

Every pull request should include:

- A short summary of what changed.
- Confirmation that product behavior is unchanged, or a clear explanation if behavior intentionally changed.
- Validation commands and results.
- Updated docs when user-facing behavior or developer workflow changes.

## Documentation Standards

Documentation should not overclaim. If a capability is not implemented in the repository, describe it as future work or omit it.

Avoid claiming:

- Live monitoring.
- Forecasting.
- Investment, trading, legal, or compliance advice.
- Enterprise deployment.
- Real-world accuracy guarantees.

## Runtime Artifacts

Local run folders under `outputs/runs/` are generated artifacts and should not be committed.
