# Assumptions

## Active Assumptions

| ID | Assumption | Impact | Review Needed? |
|---|---|---|---|
| A-001 | The first MVP may use a CLI/report workflow before a richer UI. | Keeps first milestone focused on analysis and coaching logic. | Confirmed 2026-06-06 |
| A-002 | No representative Late Model `.ibt` file is currently available. Proceed with synthetic telemetry fixtures and keep ingestion ready for later real-file validation. | Parser integration cannot be fully validated yet; analysis behavior can still be tested. | Confirmed 2026-06-06 |
| A-003 | Self-comparison against the driver's best valid lap is acceptable for the first MVP when no external reference lap is provided. | Enables useful analysis from a single telemetry file. | Yes |
| A-004 | Rule-based coaching heuristics are acceptable for the MVP if evidence and limitations are documented. | Supports explainability and testability. | Yes |
| A-005 | The initial report can be text or Markdown as long as it is coaching-first and evidence-backed. | Avoids premature UI complexity. | Confirmed 2026-06-06 |

## Material Clarification Questions

No material clarification questions are currently blocking Milestone 1.
