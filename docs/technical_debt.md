# Technical Debt

## High Priority

### 1. output_adapter.py has too many responsibilities

Current responsibilities:
- output mode adaptation
- Beginner / Analyst / Executive formatting
- Chinese localization
- heading parity
- decision section rendering

Risk:
Future changes may break English / Chinese parity or output modes.

Suggested future fix:
After product flow stabilizes, split localization and mode adaptation into separate helper modules.

Status:
Do not refactor yet. Revisit after V14 or product freeze.

---

### 2. brief_generator.py is large

Current role:
Builds most decision-first report sections.

Risk:
Adding more reasoning layers may make the file harder to maintain.

Suggested future fix:
Eventually split decision sections, scenario profiles, and historical evidence formatting.

Status:
Do not refactor yet. Current product is still evolving.

---

## Medium Priority

### 3. Validation scripts are versioned

Current:
validate_v120.py through validate_v133.py

Risk:
Validation may become harder to manage as versions increase.

Suggested future fix:
Create validate_current.py wrapper that runs all current validation scripts.

---

### 4. README may become too version-heavy

Risk:
README should explain the current product, not become a long changelog.

Suggested future fix:
Move version history to docs/changelog.md.
