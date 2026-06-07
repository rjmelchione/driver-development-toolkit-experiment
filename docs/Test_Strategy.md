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
- Consolidation of repeated segment findings.
- Evidence included for each recommendation.
- Report generation includes all four coaching questions.
- CLI report-shaping options.

## Test Commands

Target commands once the Python project is initialized:

```bash
uv run pytest
uv run ddt --demo
uv run ddt --demo --max-opportunities 3
uv run ddt --demo --no-consistency
```

Real `.ibt` validation is deferred until a representative Late Model telemetry file is available. Until then, parser contract coverage verifies that the ingestion boundary reports the limitation clearly.

Current automated coverage: 10 tests covering analysis, CLI behavior, ingestion boundaries, and report rendering.
