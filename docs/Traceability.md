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
| Keep coaching output focused. | FR-012, FR-013 | Analysis config, CLI controls, reporting | CLI tests |
| Preserve analysis provenance. | FR-014, FR-015 | Analysis summary, synthetic fixture reader, reporting | Analysis, ingestion, CLI, and reporting tests |
| Maintainable future extension. | NFR-001, NFR-002, NFR-006 | Layered architecture, docs, tests | Unit/integration tests and docs review |

## Requirement-to-Implementation Traceability

| Requirement IDs | Implementation Area | Tests |
|---|---|---|
| FR-001, FR-002, FR-003 | `driver_development_toolkit.ingestion`, `driver_development_toolkit.models` | `tests/test_ingestion.py` |
| FR-004, FR-005, FR-006, FR-007, FR-008, FR-009 | `driver_development_toolkit.analysis`, `docs/Analysis_Rules.md` | `tests/test_analysis.py` |
| FR-010, FR-012, FR-013, FR-014 | `driver_development_toolkit.cli`, `driver_development_toolkit.reporting` | `tests/test_cli.py`, `tests/test_reporting.py` |
| FR-015 | `driver_development_toolkit.ingestion`, `tests/fixtures/synthetic_late_model_session.json` | `tests/test_ingestion.py`, `tests/test_cli.py` |
| NFR-001, NFR-002, NFR-006 | `docs/`, `runs/codex-run-02/`, `tests/` | Documentation review and `uv run pytest` |

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
