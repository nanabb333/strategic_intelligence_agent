---
name: Bug report
about: Report behavior that appears broken, inconsistent, or regressed
title: "[Bug]: "
labels: bug
assignees: ""
---

## Summary

Describe the issue in 2-4 sentences.

## Affected Area

- [ ] Local launch
- [ ] Decision Workspace
- [ ] Project workspace
- [ ] Evidence library or review queue
- [ ] Decision brief or generated artifacts
- [ ] Documentation
- [ ] Tests or developer workflow

## Steps To Reproduce

1. Step one:
2. Step two:
3. Step three:

## Expected Behavior

What should happen?

## Actual Behavior

What happened instead?

## Product Boundary Check

- [ ] This report does not request autonomous research, monitoring, investment advice, legal advice, or unsupported forecasting.
- [ ] This report is about implemented repository behavior, not a future roadmap item.

## Environment

- Operating system:
- Python version:
- Browser, if workspace-related:
- Branch or commit:

## Validation Tried

Paste any commands run and relevant results.

```bash
.venv/bin/ruff check .
python3 -m py_compile app.py src/*.py launch.py
python3 -m pytest
node --check dashboard/app.js
node --check dashboard/project.js
```

## Notes

Do not include private documents, credentials, API keys, tokens, or sensitive source material.
