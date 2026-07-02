## Release Theme

Name the release, sprint, issue, or maintenance theme this pull request supports.

## Objectives

- Objective 1:
- Objective 2:
- Objective 3:

## Scope

Describe the files, modules, docs, or product surfaces intentionally changed.

## Explicit Non-goals

Confirm what this pull request does not change.

- [ ] No Decision Intelligence logic changes
- [ ] No evidence processing changes
- [ ] No API route or schema changes
- [ ] No reviewer workflow changes
- [ ] No autonomous behavior added
- [ ] No unsupported product claims added

If any item is unchecked, explain why the change is explicitly in scope.

## Product Behavior Impact

- [ ] No product behavior changed
- [ ] Behavior changed intentionally and is described below

Notes:

## Validation

Paste commands run and results.

```bash
.venv/bin/ruff check .
python3 -m py_compile app.py src/*.py launch.py
python3 -m pytest
node --check dashboard/app.js
node --check dashboard/project.js
```

## Documentation

- [ ] README updated if needed
- [ ] Documentation index updated if needed
- [ ] Architecture or user docs updated if needed
- [ ] Release notes or changelog updated if needed
- [ ] Documentation accurately describes implemented behavior

## Risks

List known risks, limitations, review concerns, or follow-up work.

## Reviewer Checklist

- [ ] Scope matches the stated release theme
- [ ] No unrelated files changed
- [ ] Product boundaries remain clear
- [ ] Reviewer control and traceability are preserved
- [ ] Validation results are credible
- [ ] Documentation is consistent with implementation
