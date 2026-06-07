# Assumptions

## Active Assumptions

| ID | Assumption | Impact | Review Needed? |
|---|---|---|---|
| A-001 | The first MVP may use a CLI/report workflow before a richer UI. | Keeps first milestone focused on analysis and coaching logic. | Yes |
| A-002 | A representative Late Model `.ibt` file will be available for validation before the MVP is considered complete. | Required for confidence in parser integration and coaching output. | Yes |
| A-003 | Self-comparison against the driver's best valid lap is acceptable for the first MVP when no external reference lap is provided. | Enables useful analysis from a single telemetry file. | Yes |
| A-004 | Rule-based coaching heuristics are acceptable for the MVP if evidence and limitations are documented. | Supports explainability and testability. | Yes |
| A-005 | The initial report can be text or Markdown as long as it is coaching-first and evidence-backed. | Avoids premature UI complexity. | Yes |

## Material Clarification Questions

1. Can you provide at least one representative iRacing Late Model `.ibt` file for validation, or should the first milestone proceed with synthetic telemetry fixtures until one is available?
2. Is a local CLI-generated Markdown report acceptable for the first implementation milestone, with a richer UI deferred until the analysis engine is credible?
