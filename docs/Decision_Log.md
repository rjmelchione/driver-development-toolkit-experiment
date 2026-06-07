# Decision Log – Driver Development Toolkit

Version: 1.0  
Status: Active

---

## DEC-001 – UI Framework: Streamlit

**Date**: 2026-06-06  
**Context**: The product vision requires a coaching-first interface with telemetry evidence drill-down. No specific UI type was prescribed.

**Options Considered**:
- Streamlit (web app, local browser)
- CLI with Rich formatted output
- PyQt6 desktop GUI
- Plotly Dash

**Decision**: Streamlit

**Rationale**:
The product vision specifically calls for ranked coaching lists with telemetry overlay charts (speed, throttle, brake traces). Streamlit provides this capability in pure Python without requiring a separate frontend stack. The coaching-first layout (ranked list → drill-down evidence) maps naturally to Streamlit's column and expander widgets. Plotly integration is first-class in Streamlit. The tool runs locally via `streamlit run` and opens in the user's browser.

**Tradeoffs**:
- Requires a browser to view the application. Acceptable for a data analysis tool.
- Streamlit's layout model has some constraints compared to a custom frontend. Sufficient for the MVP coaching dashboard.
- Not a native desktop application. Future enhancement if needed.

**Impact**: All UI code lives in `src/driver_toolkit/ui/`. The analysis layer has no Streamlit dependency.

---

## DEC-002 – .ibt Parsing Library: pyirsdk

**Date**: 2026-06-06  
**Context**: iRacing `.ibt` is a proprietary binary format. A Python library is needed to read it without custom binary parsing.

**Options Considered**:
- pyirsdk (Python, live SDK + .ibt file support)
- Custom binary parser (Python)
- ibt-telemetry (JavaScript — wrong language)
- teamjorge/ibt (Go — wrong language)

**Decision**: pyirsdk

**Rationale**:
pyirsdk is the established Python library for iRacing telemetry, actively maintained (v1.3.5, March 2024). It confirms offline `.ibt` file reading support. Implementing a custom binary parser for an undocumented proprietary format introduces risk without benefit.

**Tradeoffs**:
- pyirsdk was primarily designed for live SDK use; lap segmentation from `.ibt` ticks requires additional logic
- Library relies on reverse-engineered format knowledge; iRacing format changes could break compatibility
- Not yet validated against a real `.ibt` file

**Mitigation**: pyirsdk is isolated to the Parsing layer (`ibt_reader.py`). Replacement requires changes only to that module.

**Validation**: See A-001 in Requirements.md.

---

## DEC-003 – Coaching Approach: Rules-Based

**Date**: 2026-06-06  
**Context**: The system needs to generate coaching recommendations from telemetry observations.

**Options Considered**:
- Rules-based (deterministic, coded rules per opportunity type)
- LLM-powered (API call to language model for coaching text)
- Hybrid (rules for detection, LLM for text generation)

**Decision**: Rules-based

**Rationale**:
Rules-based coaching keeps the system fully offline, deterministic, and auditable. Each coaching recommendation is directly traceable to a specific telemetry observation (e.g., "minimum corner speed 8% below reference → over-slowing recommendation"). No API key is required. The product vision emphasizes explainable recommendations traceable to telemetry evidence — rules-based coaching naturally satisfies this.

**Tradeoffs**:
- Coaching text is limited to what was explicitly programmed. Novel driving issues without a matching rule produce no recommendation.
- Rules require domain expertise to encode correctly. Errors in rules produce incorrect coaching.
- LLM coaching would generalize better and produce more natural language. Deferred to future enhancement.

**Extension point**: `coaching/rules.py` implements a well-defined interface (`get_coaching(opportunity: Opportunity) → CoachingResult`). An LLM-based implementation can replace the rules module without changing any other layer.

---

## DEC-004 – Reference Lap: Driver's Best Lap (Self-Comparison)

**Date**: 2026-06-06  
**Context**: The product vision supports both self-comparison and reference lap comparison from other drivers. The vision states reference laps from other drivers "may enhance analysis but should not be required."

**Decision**: Self-comparison by default (driver's fastest valid lap); external reference lap supported but not provided

**Rationale**:
The MVP must function without any external data. The driver's fastest valid lap provides a meaningful benchmark — it represents what the driver is capable of and focuses coaching on closing the gap to their own best.

**Tradeoffs**:
- Analysis is relative to the driver's own performance, not an absolute benchmark. A driver may be fast but still have poor technique. Future: reference lap from a coach or faster driver.
- Track evolution (rubber laid down) means the fastest lap may not represent "clean conditions." Noted as A-004 in Requirements.md.

**Extension point**: `comparator.py` accepts any `Lap` object as the reference. No architectural change is needed to support an external reference lap.

---

## DEC-005 – Test Data: Synthetic Generator

**Date**: 2026-06-06  
**Context**: No real `.ibt` files are available for development. Tests are required.

**Decision**: Implement a synthetic session generator that produces realistic telemetry data

**Rationale**:
Synthetic data allows full development and testing of the analysis and coaching layers without real files. The generator creates sessions with known properties (lap times, corner locations, deliberate inconsistencies) that allow precise assertions in tests.

**Tradeoffs**:
- Synthetic data may not capture edge cases present in real `.ibt` files (corrupt laps, channel dropouts, pit stops, etc.)
- Analysis validation against real-world coaching recommendations is not possible until real files are available
- Human confirmation that coaching output is correct is deferred

**Mitigation**:
- Document all synthetic data assumptions (A-002 in Requirements.md)
- Integration with real `.ibt` files must be validated when files become available
- Synthetic generator uses the same channel names and value ranges as documented for pyirsdk

---

## DEC-006 – Corner Detection: Speed Minima Algorithm

**Date**: 2026-06-06  
**Context**: Analysis requires identifying corners in a lap without a track-specific database.

**Decision**: Detect corners as local speed minima in the speed trace

**Rationale**:
In any road course or oval, the driver slows most at the corner apex. Local minima in the speed trace correspond to corner apices. This approach requires no external track data and generalizes across track types. `scipy.signal.argrelmin` or a numpy-based implementation can identify these reliably.

**Tradeoffs**:
- On ovals, "corners" may be long arcs rather than tight minima; the algorithm may detect fewer corners than expected
- Noise in the speed signal may produce false minima. A minimum prominence threshold filters most noise.
- Chicanes (two quick direction changes) may produce multiple closely-spaced minima that logically represent one corner. Minimum spacing between detected corners filters this.

**Configuration**: Minimum corner separation (in LapDistPct) and minimum speed drop (to qualify as a corner) are tunable parameters, defaulting to values appropriate for typical iRacing tracks.

---

## DEC-007 – Code Layout: src Layout

**Date**: 2026-06-06  
**Context**: Python project layout choice.

**Decision**: `src/` layout (`src/driver_toolkit/`)

**Rationale**:
The `src/` layout prevents accidental imports of the package from the project root during development. This is the modern Python packaging standard and avoids subtle import resolution bugs. `pyproject.toml` is configured with `tool.hatch.build.targets.wheel.packages = ["src/driver_toolkit"]`.

**Tradeoffs**: Requires `uv sync` and `PYTHONPATH` configuration or editable install (`uv pip install -e .`) for test discovery. Handled via `pyproject.toml` configuration.
