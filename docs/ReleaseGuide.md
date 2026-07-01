# Release Guide

This repository does not currently use packaged semantic releases. This guide describes a lightweight release process suitable for a local portfolio product.

## Release Criteria

A release should be considered only when:

- Product behavior is stable.
- README and product docs match the current implementation.
- Tests pass locally.
- CI passes on GitHub.
- Limitations are clearly stated.
- Demo scenarios and sample outputs are reviewable.

## Suggested Versioning

Use simple tags for portfolio milestones:

```text
v1.0
v2.0
v3.0-rc
v3.0
```

Avoid tagging experimental work as a release unless the repository is in a clean, validated state.

## Release Checklist

1. Run local quality checks:

   ```bash
   python3 -m ruff check .
   python3 -m compileall app.py src tests
   python3 -m pytest
   ```

2. Run a local smoke test:

   ```bash
   python3 -m uvicorn app:app --reload --port 8001
   ```

3. Verify:

   - `GET /health`
   - `POST /analyze`
   - download routes for Markdown, TXT, and JSON

4. Review documentation:

   - README
   - Product Overview
   - Decision Intelligence Framework
   - Evidence Architecture
   - Demo Scenarios
   - Engineering Architecture
   - Research Agenda
   - Testing
   - Future Engineering Recommendations

5. Confirm generated runtime artifacts under `outputs/runs/` are not staged.

## Release Notes Format

Use this structure:

```text
## Summary

## Product Scope

## Engineering Changes

## Documentation Changes

## Validation

## Known Limitations
```
