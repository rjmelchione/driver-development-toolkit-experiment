# Artifact Inventory – Claude Code Run 03

| Artifact | Type | Created By | Stage | Purpose | Quality Notes | Agent Generated? |
|---|---|---|---|---|---|---|
| docs/Requirements.md | Requirements | Agent | Stage 1 | Functional and non-functional requirements derived from product vision | Covers FR and NFR; includes explicit out-of-scope | Yes |
| docs/Architecture.md | Architecture | Agent | Stage 1 | System layer design, component responsibilities, data flow | 4-layer separation with dependency rules | Yes |
| docs/Use_Cases.md | Use Cases | Agent | Stage 1 | Concrete user scenarios scoping implementation | 4 use cases covering primary workflows | Yes |
| docs/Research_Log.md | Research | Agent | Stage 1 | Library evaluation and adoption rationale | pyirsdk selected; alternatives documented | Yes |
| docs/Decision_Log.md | Decision | Agent | Stage 1 | Major architecture, technology, and design decisions | 5 decisions documented with rationale and tradeoffs | Yes |
| docs/Test_Strategy.md | Test Plan | Agent | Stage 1 | Test approach, scope, coverage targets | pytest, analysis-layer focus, synthetic data | Yes |
| runs/claude-run-03/Run_Log.md | Evidence | Agent | Stage 1 | Records milestones, decisions, human interactions | Maintained throughout run | Yes |
| runs/claude-run-03/Artifact_Inventory.md | Evidence | Agent | Stage 1 | Tracks all artifacts created or introduced | This file | Yes |
| runs/claude-run-03/Decision_Log.md | Evidence | Agent | Stage 1 | Cross-reference to significant decisions for evaluation | Links to docs/Decision_Log.md | Yes |
| pyproject.toml | Project Config | Agent | Stage 1 | uv/Python project definition, dependencies | Standard Python packaging with optional dev deps | Yes |
| src/driver_toolkit/models/ | Implementation | Agent | Stage 1 | Core data types: Session, Lap, TelemetryChannel | Typed dataclasses; no framework coupling | Yes |
| src/driver_toolkit/parsing/ | Implementation | Agent | Stage 1 | .ibt file reader and lap segmentation | pyirsdk wrapper; synthetic data fallback | Yes |
| src/driver_toolkit/analysis/ | Implementation | Agent | Stage 1 | Opportunity detection, quantification, ranking | Rules-based; fully deterministic | Yes |
| src/driver_toolkit/coaching/ | Implementation | Agent | Stage 1 | Coaching recommendations and practice drills | Rules mapped to opportunity types | Yes |
| src/driver_toolkit/ui/ | Implementation | Agent | Stage 1 | Streamlit coaching dashboard with drill-down | Coaching-first layout per vision | Yes |
| tests/ | Tests | Agent | Stage 1 | Unit and integration tests for analysis layer | pytest; synthetic data; 80%+ analysis layer coverage | Yes |
| docs/Maintainer_Handoff.md | Handoff | Agent | Stage 1 | System overview, setup, known limits for future developers | Written at run completion | Yes |
