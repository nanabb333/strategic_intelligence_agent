# Validation Scripts

Current validation entry points are `validate_v50.py`, the full pytest suite,
Ruff, JavaScript syntax checks, and `validate_markdown_links.py`.

`validate_v120.py` through `validate_v133.py` preserve historical V12/V13
contracts that required Option B rankings and Preferred Path output. They are
retired, are not used by current CI, and exit immediately when invoked. Their
source remains in place only for historical traceability; it must not be used
to evaluate the current neutral-assessment contract.
