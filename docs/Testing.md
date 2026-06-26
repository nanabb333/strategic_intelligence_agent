# Testing

The repository uses `pytest` for lightweight behavior-preserving tests.

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

The tests avoid:

- external network calls
- uvicorn server startup
- real PDF files
- exact long-form analysis text assertions

This keeps tests stable while still protecting the public API shape and core artifact helpers.

## CI

GitHub Actions runs the same basic checks on push and pull request:

```text
install dependencies -> compile project -> run ruff -> run pytest
```
