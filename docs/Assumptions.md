# Assumptions

## Active Assumptions

| ID | Assumption | Impact | Review Needed? |
|---|---|---|---|
| A-001 | The first MVP may use a CLI/report workflow before a richer UI. | Keeps first milestone focused on analysis and coaching logic. | Confirmed 2026-06-06 |
| A-002 | No representative Late Model `.ibt` file is currently available. Proceed with synthetic telemetry fixtures and keep ingestion ready for later real-file validation. | Parser integration cannot be fully validated yet; analysis behavior can still be tested. | Confirmed 2026-06-06 |
| A-003 | Self-comparison against the driver's best valid lap is acceptable for the first MVP when no external reference lap is provided. | Enables useful analysis from a single telemetry file. | Yes |
| A-004 | Rule-based coaching heuristics are acceptable for the MVP if evidence and limitations are documented. | Supports explainability and testability. | Yes |
| A-005 | The initial report can be text or Markdown as long as it is coaching-first and evidence-backed. | Avoids premature UI complexity. | Confirmed 2026-06-06 |
| A-006 | The fastest valid lap can serve as the internal reference lap for self-comparison. | Enables single-session analysis without external reference data. | Needs validation with real telemetry |
| A-007 | Fixed normalized-distance segments are acceptable for synthetic fixture development. | Keeps analysis testable until real track/corner metadata is available. | Needs replacement or refinement with real telemetry |
| A-008 | Repeated lower-impact findings for the same segment should be evidence for the primary segment opportunity rather than separate ranked rows. | Produces a more coaching-first report. | Needs user review |
| A-009 | Reports should state validation notes directly in user-visible output while synthetic fixtures are the only validation source. | Prevents synthetic-demo output from being mistaken for real driver evidence. | Confirmed by project priorities |

## Material Clarification Questions

No material clarification questions are currently blocking Milestone 1.
