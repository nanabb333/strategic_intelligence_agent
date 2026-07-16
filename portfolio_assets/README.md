# Portfolio Assets

This folder contains the curated product presentation assets that are not generated runtime outputs.

Use it for materials that help reviewers understand the product quickly:

- screenshots
- historical screenshot references

Generated run artifacts should remain under `outputs/` or `demo_case_outputs/`. This folder is for curated portfolio-facing assets only.

## Structure

```text
portfolio_assets/
  screenshots/
    historical/
```

## Current Status

The README uses the archived placeholder at `screenshots/historical/dashboard-overview.png`. It predates V5 Sprint 0 and does not represent the current interface. No verified current screenshot is available.

## Recommended Review Path

1. [Demo Walkthrough](../docs/DemoWalkthrough.md)
2. [Portfolio Review Guide](../docs/PortfolioReviewGuide.md)
3. [V4 Project Demo](../demo_case_outputs/v4_workspace/README.md)
4. [Current demo scenarios](../docs/GettingStarted/DemoScenarios.md)

Demo inputs remain under `demo_cases/` and `examples/demo_inputs/`. Generated and curated outputs remain under `demo_case_outputs/`, `demo_outputs/`, and `outputs/` because historical validation scripts depend on those paths.
