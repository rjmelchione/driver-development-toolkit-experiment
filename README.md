# Driver Development Toolkit Experiment

This repository supports an agentic software development experiment.

The objective is to evaluate whether AI development agents can transform a product vision into a maintainable software engineering effort with minimal human-generated engineering artifacts.

See:

- experiment/Experiment_Plan_v3.md
- experiment/Product_Vision.md
- experiment/Execution_Guide_v1.md

## Current Codex Run

The active run is `runs/codex-run-02`.

Milestone 1 is a Python/uv CLI foundation that generates a coaching-first Markdown report from synthetic telemetry fixtures while preserving an ingestion boundary for future real iRacing `.ibt` validation.

## Development

Install dependencies:

```bash
uv sync
```

Run tests:

```bash
uv run pytest
```

Generate a demo coaching report:

```bash
uv run ddt --demo
```

Limit report length:

```bash
uv run ddt --demo --max-opportunities 3
```

Generate only direct lap comparison opportunities:

```bash
uv run ddt --demo --no-consistency
```

Analyze the checked-in synthetic JSON fixture:

```bash
uv run ddt tests\fixtures\synthetic_late_model_session.json --max-opportunities 2
```

The current `.ibt` reader is intentionally blocked until a representative iRacing Late Model `.ibt` file is available for validation.
