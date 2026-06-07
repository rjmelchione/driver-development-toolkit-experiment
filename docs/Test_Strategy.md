# Test Strategy

## Goals

Testing should prove that the system can ingest telemetry, derive stable analysis outputs, and keep recommendations traceable to evidence.

## Test Levels

| Level | Purpose | Examples |
|---|---|---|
| Unit tests | Validate calculations and rule behavior in isolation. | Segment delta calculation, opportunity ranking, recommendation mapping. |
| Contract tests | Validate assumptions about telemetry parser outputs. | Required channel detection, lap table shape, missing channel handling. |
| Integration tests | Validate end-to-end report generation from fixture telemetry data. | `.ibt` fixture to Markdown report. |
| Documentation checks | Ensure setup and usage instructions remain executable. | `uv sync`, test command, CLI command. |

## Fixture Strategy

Preferred:

- Use one or more representative Late Model `.ibt` files supplied by the human or captured from iRacing.
- Store small fixtures only if license/privacy constraints permit.

Fallback:

- Use synthetic normalized telemetry tables for unit and analysis tests.
- Keep parser integration tests optional until a real `.ibt` fixture is available.

## Minimum MVP Test Coverage

- Loading failure and missing-file behavior.
- Required channel validation.
- Completed lap extraction or graceful failure when lap data is insufficient.
- Best-lap selection.
- Segment delta calculations.
- Opportunity ranking by estimated impact.
- Evidence included for each recommendation.
- Report generation includes all four coaching questions.

## Test Commands

Target commands once the Python project is initialized:

```bash
uv run pytest
uv run ddt analyze path\to\session.ibt
```

Exact commands may change during implementation and should be updated here and in the README.
