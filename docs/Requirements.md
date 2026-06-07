# Requirements

## Functional Requirements

| ID | Requirement | Source | Priority | Notes |
|---|---|---|---|---|
| FR-001 | The system shall load iRacing `.ibt` telemetry files from the local filesystem. | Product Vision | Must | Initial source format. |
| FR-002 | The system shall identify completed laps available in a loaded telemetry file. | Product Vision | Must | Required for lap and session analysis. |
| FR-003 | The system shall extract key driving telemetry channels needed for Late Model coaching analysis. | Product Vision | Must | Expected channels include speed, throttle, brake, steering, lap distance/time, and lap identifiers when available. |
| FR-004 | The system shall compare laps within a session to identify where time is lost. | Product Vision | Must | Self-comparison should work without reference driver data. |
| FR-005 | The system shall rank improvement opportunities by estimated lap-time impact. | Product Vision | Must | Supports coaching-first prioritization. |
| FR-006 | For each significant opportunity, the system shall explain the likely cause using telemetry observations. | Product Vision | Must | Explanations must be evidence-backed. |
| FR-007 | For each significant opportunity, the system shall recommend a driving adjustment. | Product Vision | Must | Coaching action, not only diagnosis. |
| FR-008 | For each significant opportunity, the system shall recommend a focused practice activity. | Product Vision | Should | Central to driver development value. |
| FR-009 | The system shall expose supporting telemetry evidence for each recommendation. | Product Vision | Must | Traceability requirement. |
| FR-010 | The system shall produce a readable coaching report for a loaded telemetry file. | Agent-derived from UX goals | Must | First MVP interface; may be CLI/text/Markdown initially. |
| FR-011 | The system should support future reference lap comparison without requiring it for MVP operation. | Product Vision | Should | Design should not block future expansion. |
| FR-012 | The system shall allow users to limit report length from the CLI. | Agent-derived from coaching-first usability | Should | Supports focused review of highest-impact opportunities. |
| FR-013 | The system shall allow users to exclude consistency findings from the CLI report. | Agent-derived from coaching-first usability | Should | Separates direct lap-comparison coaching from repeatability coaching when desired. |
| FR-014 | The system shall include analysis provenance in generated reports. | Agent-derived from explainability and traceability goals | Must | Includes reference lap, thresholds, report limits, and validation notes. |
| FR-015 | The system shall support an on-disk synthetic telemetry fixture format for repeatable tests and demos. | Human clarification / testability need | Must | Used until representative `.ibt` data is available. |

## Non-Functional Requirements

| ID | Requirement | Source | Priority | Notes |
|---|---|---|---|---|
| NFR-001 | The system shall be understandable and maintainable by a future developer. | Product Vision | Must | Documentation and clear module boundaries required. |
| NFR-002 | Major assumptions, decisions, and tradeoffs shall be documented. | Product Vision / Experiment Plan | Must | Maintained in run and docs artifacts. |
| NFR-003 | Recommendations shall be explainable rather than opaque whenever practical. | Product Vision | Must | Drives rule-based MVP choice. |
| NFR-004 | The implementation shall use Python and uv unless a deviation is justified before adoption. | Execution Guide | Must | No deviation currently planned. |
| NFR-005 | Existing open-source solutions shall be researched before custom telemetry parsing. | Execution Guide | Must | Captured in Research Log. |
| NFR-006 | Core analysis behavior shall be covered by automated tests. | Experiment Plan | Must | Test strategy defines levels. |
| NFR-007 | The MVP shall run locally on Windows. | Execution Guide | Must | Avoid cloud or service dependencies. |

## Initial Acceptance Criteria

For a representative `.ibt` file with completed laps:

- The user can run one documented command to generate a coaching report.
- The report lists ranked opportunities with estimated time impact.
- Repeated lap findings for the same segment are consolidated into a readable coaching opportunity.
- Each opportunity includes where, why, what to change, how to practice, and supporting evidence.
- The report states the analysis assumptions and validation boundary used to produce it.
- Tests can be run with one documented command.
