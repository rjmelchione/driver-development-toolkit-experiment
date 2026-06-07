# Decision Log – Claude Code Run 03

This file records significant decisions made during the run for evaluation purposes.
Full decision rationale is in [docs/Decision_Log.md](../../docs/Decision_Log.md).

| Decision | Context | Options Considered | Selected Option | Rationale | Risk / Tradeoff |
|---|---|---|---|---|---|
| UI framework | Vision requires coaching dashboard with charts and drill-down | Streamlit, CLI, PyQt desktop | Streamlit | Coaching-first layout with charts is natural in Streamlit; pure Python; runs locally | Requires browser; not a native app |
| .ibt parsing library | Need to read iRacing telemetry files in Python | pyirsdk, custom binary parser, ibt-telemetry (JS) | pyirsdk | Established library, active maintenance, offline .ibt support confirmed | Primarily designed for live SDK; lap iteration requires custom logic on top |
| Coaching approach | Need to generate coaching from telemetry | Rules-based, LLM-powered, hybrid | Rules-based | Fully offline, deterministic, auditable, no API key required | Must encode coaching rules explicitly; won't generalize to novel edge cases |
| Reference lap requirement | Vision states reference laps should not be required | Require reference lap, optional reference lap, self-comparison only | Self-comparison (optional reference) | Vision explicitly states reference not required; self-comparison provides coaching from any session | Analysis relative to driver's own performance, not absolute benchmark |
| Test data strategy | No real .ibt files available | Wait for files, use synthetic data, use recorded community data | Synthetic data generator | Allows full development without external dependency; deterministic test data | Synthetic data may not match real .ibt edge cases; validation needed when real files become available |
| Code layout | Python project structure | Flat layout, src layout | src layout | Prevents accidental imports from project root; standard for installable packages | Slightly more path configuration |
| Package manager | Dependency management | pip, poetry, uv | uv (per experiment spec) | Specified in experiment constraints; fast and modern | Requires uv installed on developer machine |
