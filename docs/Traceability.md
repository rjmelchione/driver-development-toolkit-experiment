# Traceability

## Vision-to-Requirement Traceability

| Vision Goal | Requirement IDs | Planned Design Area | Test Coverage |
|---|---|---|---|
| Analyze real iRacing telemetry data. | FR-001, FR-002, FR-003 | Ingestion, lap processing | Parser contract tests, integration tests |
| Identify where lap time is being lost. | FR-004, FR-005 | Segment comparison, opportunity detection | Segment delta and ranking tests |
| Determine likely causes. | FR-006 | Opportunity detection, evidence model | Rule classification tests |
| Recommend driving adjustments. | FR-007 | Coaching | Recommendation mapping tests |
| Suggest focused practice activities. | FR-008 | Coaching | Practice mapping tests |
| Present telemetry evidence. | FR-009, FR-010 | Evidence model, reporting | Report content tests |
| Maintainable future extension. | NFR-001, NFR-002, NFR-006 | Layered architecture, docs, tests | Unit/integration tests and docs review |

## Artifact Traceability

| Artifact | Supports |
|---|---|
| `docs/Product_Understanding.md` | Shared interpretation of vision and scope. |
| `docs/Requirements.md` | Functional and non-functional implementation targets. |
| `docs/Use_Cases.md` | User workflows and acceptance intent. |
| `docs/Architecture.md` | Maintainable structure and dependency boundaries. |
| `docs/Test_Strategy.md` | Quality and reproducibility expectations. |
| `runs/codex-run-02/Decision_Log.md` | Major technology and tradeoff decisions. |
| `runs/codex-run-02/Research_Log.md` | Evidence for reuse-before-build expectation. |
