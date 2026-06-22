# Repository Audit

## Current Repository State

This checkout currently contains Git metadata but no tracked application files.
`git status --short` is clean, `git branch --all --verbose` returns no branches,
and `git ls-tree -r --name-only HEAD` fails because there is no valid `HEAD`.

The prior project name was `financial_rubric_agent`, but no source files from
that version are present in this working tree. Because of that, this audit
cannot identify concrete reusable modules from the previous implementation.

## Existing Files

| File | Purpose | Keep | Refactor | Remove | Notes |
| --- | --- | --- | --- | --- | --- |
| `.git/` | Local Git repository metadata | Yes | No | No | Required for version control. Not part of application architecture. |

## Reuse Assessment

No application files are available in the current checkout, so reuse is limited
to the conceptual lineage of the old project:

- Document input can become `src/document_loader.py`.
- Rubric scoring can evolve into scenario classification and structured issue
  assessment.
- AI writing can evolve into executive brief generation.

If the previous `financial_rubric_agent` code exists in another branch, remote,
archive, or local folder, the most likely reusable components are:

- Document parsing and text extraction utilities.
- Prompt templates for structured analysis.
- LLM client wrappers.
- Output formatting logic.
- Any CLI or workflow orchestration code.

## Migration Principle

Do not delete or overwrite prior work when it becomes available. Instead,
wrap reusable functionality behind the new Strategic Intelligence Agent module
interfaces and migrate behavior incrementally.

