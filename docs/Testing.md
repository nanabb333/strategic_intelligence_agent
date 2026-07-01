# Testing

The repository uses `pytest` for lightweight behavior-preserving tests.

## Related Docs

- [Documentation Index](DocumentationIndex.md)
- [Product Overview](ProductOverview.md)
- [Engineering Architecture](EngineeringArchitecture.md)
- [Analysis Pipeline](Pipeline.md)
- [Folder Structure](FolderStructure.md)

## Run Tests

```bash
python3 -m pytest
```

## Lint Check

```bash
python3 -m ruff check .
```

## Compile Check

```bash
python3 -m compileall app.py src tests
```

## Test Scope

Current tests cover:

- pure serialization behavior
- markdown-to-text conversion
- metadata artifact construction
- agent trace construction
- analysis artifact shape
- FastAPI `/health`
- FastAPI `/analyze`
- FastAPI `/run/{run_id}`
- markdown artifact download route
- markdown, TXT, and JSON download routes
- project workspace creation, questions, evidence, timeline, and delta
- user-triggered evidence retrieval interfaces and URL provider behavior
- Evidence Intelligence
- Decision Framework classification
- Decision Readiness
- Domain Decision Evaluation
- Decision Pathway Drafts
- Pathway Comparison Matrix
- Decision Review state and API behavior
- enterprise diagnostics and release metadata

The tests avoid:

- external network calls
- uvicorn server startup
- external provider credentials
- exact long-form analysis text assertions

This keeps tests stable while still protecting the public API shape and core artifact helpers.

## CI

GitHub Actions runs the same basic checks on push and pull request:

```text
install dependencies -> compile project -> run ruff -> run pytest
```
