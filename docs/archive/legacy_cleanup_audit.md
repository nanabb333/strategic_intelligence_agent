# Legacy Cleanup Audit

## Purpose

This audit documents how the preserved `financial_rubric_agent` files were
handled during the Strategic Intelligence Agent V0.1 portfolio cleanup.

## Decisions

| File or Folder | Decision | Reason |
| --- | --- | --- |
| `README.md` | Replaced at root; old version moved to `legacy/financial_rubric_agent/README.md` | The root README now needs to present Strategic Intelligence Agent. The old README still documents project evolution. |
| `ai_writer.py` | Moved to `legacy/financial_rubric_agent/ai_writer.py` | Useful prior OpenAI prompt and narrative-generation logic, but finance-specific and not part of the active V0.1 workflow. |
| `main.py` | Moved to `legacy/financial_rubric_agent/main.py` | Preserves the old CLI, report generation, CSV export, and orchestration logic for reference. |
| `rubric.py` | Moved to `legacy/financial_rubric_agent/rubric.py` | Preserves prior rule-based scoring logic, but it should not drive the new strategic intelligence workflow. |
| `requirements.txt` | Replaced at root; old version copied to `legacy/financial_rubric_agent/requirements.txt` | Active V0.1 uses only the Python standard library. Legacy dependencies remain documented separately. |
| `outputs/*_report_*.txt` | Moved to `legacy/financial_rubric_agent/outputs/` | Historical generated financial reports are not active Strategic Intelligence Agent outputs. |
| `outputs/comparison_results_*.csv` | Moved to `legacy/financial_rubric_agent/outputs/` | Historical generated comparison data is preserved as legacy output. |
| `__pycache__/` and `*.pyc` | Removed from tracking | Compiled bytecode should not be versioned. `.gitignore` now excludes Python cache files. |
| `outputs/sample_brief.md` | Kept | Active V0.1 sample output for the Strategic Intelligence Agent workflow. |

## Reuse Opportunities

The legacy project should not be reused as an investment or trading system.
However, it contains patterns that may be useful later:

- CLI orchestration from `main.py`.
- Report formatting helpers from `main.py`.
- Prompt construction discipline from `ai_writer.py`.
- Rule-based scoring structure from `rubric.py`, adapted only for
  non-investment strategic scenario assessment.

