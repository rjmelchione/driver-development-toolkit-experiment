# Implementation Plan

## Proposed Development Approach

Use an incremental, artifact-backed development process:

1. Establish a Python/uv project skeleton with tests and lint-friendly structure.
2. Validate the selected `.ibt` parser on Windows.
3. Build a small domain model around sessions, laps, telemetry evidence, opportunities, and recommendations.
4. Implement analysis rules with synthetic data tests first.
5. Add parser integration behind a stable ingestion boundary, with real `.ibt` validation deferred until a representative file is available.
6. Keep documentation and traceability updated at each meaningful milestone.

## First Implementation Milestone

Milestone 1: Coaching report foundation.

Target outcome:

- A local Python package managed by uv.
- A CLI entry point that accepts a telemetry path.
- Telemetry ingestion abstraction with `libibt` as the first implementation candidate.
- Analysis pipeline that can produce a ranked Markdown/text coaching report from synthetic fixtures now and real telemetry later.
- Unit tests for analysis rules using synthetic telemetry fixtures.
- Documented parser validation status.

## Initial Task Sequence

| Step | Task | Exit Criteria |
|---|---|---|
| 1 | Initialize Python/uv project structure. | Done: `pyproject.toml`, package directory, test directory, and basic README instructions exist. |
| 2 | Add dependencies after validation. | Parser and analysis dependencies are justified and recorded. |
| 3 | Implement domain model. | Done: core data classes exist. |
| 4 | Implement synthetic analysis pipeline. | Done: tests show ranked opportunities and evidence output. |
| 5 | Implement report rendering. | Done: sample report can be generated from synthetic data. |
| 6 | Preserve real `.ibt` validation path. | Done: parser interface and documented limitation exist; real-file test can be added when data is available. |

## Current Gate Before Code

Implementation code may begin. The human confirmed that synthetic telemetry fixtures are acceptable until a representative Late Model `.ibt` file is available, and that a CLI-generated Markdown/text coaching report is acceptable for the first milestone.
