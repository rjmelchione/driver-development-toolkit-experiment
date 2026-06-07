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
