# Public Release Checklist

Use this checklist before presenting the repository as a public flagship portfolio project.

## Repository Presentation

- [x] README explains what the project is.
- [x] README states that the app is local.
- [x] README avoids forecasting, investment advice, legal advice, and trading claims.
- [x] Product overview exists.
- [x] Demo scenarios exist.
- [x] Portfolio narrative exists.
- [x] Architecture and pipeline docs describe the real implementation.
- [x] CI is configured for compile, Ruff, and pytest.

## Developer Workflow

- [x] Dependency installation command is documented.
- [x] Local server command is documented.
- [x] Test commands are documented.
- [x] Contribution guidance exists.
- [x] Generated run folders are ignored.

## Before A Formal Public Release

- [ ] Select and add a license.
- [ ] Decide whether older milestone docs should remain in the main `docs/` folder or move under an archive index.
- [ ] Decide whether `live_evidence.py` should remain as a root utility, move under `src/`, or be retired.
- [ ] Add a short demo video or verified screenshots if public presentation needs stronger visual proof.
- [ ] Review all demo outputs for tone, disclaimers, and source-status clarity.
- [ ] Perform a security review before any internet-facing deployment.

## Release Validation

Run:

```bash
python3 -m ruff check .
python3 -m compileall app.py src tests
python3 -m pytest
```

Optional local runtime smoke test:

```bash
python3 -m uvicorn app:app --reload --port 8001
```

Verify:

- `GET /health`
- `POST /analyze`
- `/run/{run_id}/download/markdown`
- `/run/{run_id}/download/txt`
- `/run/{run_id}/download/json`
