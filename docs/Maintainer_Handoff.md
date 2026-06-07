# Maintainer Handoff – Driver Development Toolkit

Version: 1.0  
Run: Claude Code Run 03 (branch: runs/claude-run-03)  
Date: 2026-06-06

This document allows a developer with Python experience to understand, set up, and extend the Driver Development Toolkit without requiring knowledge of the experiment that produced it.

---

## What This System Does

The Driver Development Toolkit reads an iRacing `.ibt` telemetry file and produces ranked coaching recommendations. For each session it identifies the corners where the driver is losing the most time, classifies the likely cause (over-slowing, late throttle, early brake, inconsistent braking), and generates a specific driving recommendation and a focused practice drill.

The system is coaching-first: the user sees recommendations immediately, with telemetry evidence available on demand via interactive charts.

---

## Quick Setup

```bash
# 1. Clone the repository and checkout this branch
git checkout runs/claude-run-03

# 2. Install dependencies (requires uv)
uv sync

# 3. Run the application
uv run streamlit run src/driver_toolkit/ui/app.py

# 4. Run tests
uv run pytest
uv run pytest --cov --cov-report=term-missing  # with coverage
```

The application opens in your browser at http://localhost:8501.
Select **Demo Session** in the sidebar to see a coached session without a real `.ibt` file.

---

## Repository Map

```
src/driver_toolkit/
  models/session.py          ← TelemetryPoint, Lap, Session (the shared data contract)
  parsing/ibt_reader.py      ← loads real .ibt files via pyirsdk
  parsing/lap_segmenter.py   ← splits tick stream into Lap objects
  parsing/synthetic.py       ← generates fake sessions for testing and demo
  analysis/metrics.py        ← detects corners, computes min speed / brake / throttle points
  analysis/comparator.py     ← compares laps to the reference, computes per-corner deltas
  analysis/opportunity_detector.py  ← identifies and classifies coaching opportunities
  analysis/ranker.py         ← sorts opportunities by time impact
  coaching/rules.py          ← maps opportunity types to coaching text and practice drills
  ui/app.py                  ← Streamlit application entry point
  ui/components/summary.py   ← session summary and ranked coaching list
  ui/components/evidence.py  ← telemetry overlay chart for drill-down

tests/                       ← pytest unit and integration tests
docs/                        ← engineering artifacts (requirements, architecture, etc.)
runs/claude-run-03/          ← experiment evidence (run log, decision log, etc.)
```

---

## Architecture in One Diagram

```
.ibt file → ibt_reader.py → Session(Lap(TelemetryPoint[]))
                                      │
                              metrics.py (corner detection)
                                      │
                             comparator.py (lap delta)
                                      │
                        opportunity_detector.py (classify)
                                      │
                            coaching/rules.py (text)
                                      │
                           Streamlit UI (display)
```

Dependencies only flow downward. The UI calls the analysis layer; the analysis layer calls the models layer; only the parsing layer knows about pyirsdk. This means you can change the coaching rules without touching the analysis engine, and change the UI without touching anything below it.

---

## Key Design Decisions

Full rationale is in [docs/Decision_Log.md](Decision_Log.md). Brief summary:

| Decision | What and Why |
|---|---|
| Streamlit UI | Coaching dashboards with telemetry charts, pure Python, local browser |
| pyirsdk | Established Python library for .ibt parsing; isolated to one module |
| Rules-based coaching | Fully offline, deterministic, auditable; LLM coaching is a drop-in extension |
| Self-comparison | Analysis works from one driver's own laps; external reference lap optional |
| Synthetic test data | No real .ibt files during development; generator produces known sessions |
| Speed minima for corners | No track database needed; generalizes across track types |

---

## How Coaching Works

1. **Corner detection**: Speed minima in the lap trace identify corner apices. Local minima below a threshold qualify as corners.

2. **Per-corner metrics**: For each corner, the system records minimum speed, brake application point, and throttle application point.

3. **Comparison**: Each lap is compared to the reference (fastest) lap corner by corner. Deltas are computed.

4. **Opportunity detection**: Corners where the average speed delta exceeds a threshold become coaching opportunities. The opportunity is classified:
   - `OVER_SLOWING`: avg speed delta ≤ -1.5 m/s
   - `EARLY_BRAKE`: avg brake point earlier than reference by ≥ 0.015 LapDistPct
   - `LATE_THROTTLE`: avg throttle point later than reference by ≥ 0.015 LapDistPct
   - `GENERAL_CORNER`: time loss without a dominant single cause

5. **Coaching**: `coaching/rules.py` maps each type to a (cause, recommendation, drill) tuple.

---

## Known Limitations

- **Not tested against real .ibt files.** The parsing layer (pyirsdk) has not been validated with a real iRacing session. Integration testing is required when files are available. See Requirements A-001.
- **Coaching rules are not validated by a real driving coach.** The rules encode reasonable general motorsport principles but have not been reviewed by an expert.
- **Speed minima detection has limitations on ovals.** Long sweeping bends may not produce a clean minimum. Tunable parameters: `MIN_CORNER_SEPARATION` and `MIN_SPEED_DROP` in `analysis/metrics.py`.
- **Time impact estimation is approximate.** The model `time_impact = abs(speed_delta) * 0.13` is a linear approximation. A physics-based model would be more accurate but requires track geometry.
- **Only one imperfection type per corner is classified.** If a driver is both over-slowing and late on throttle, only the dominant pattern is reported.

---

## How to Extend

### Add a new coaching rule

1. Add a value to `OpportunityType` in `opportunity_detector.py`
2. Add a detection condition in `_classify()` in `opportunity_detector.py`
3. Add a rule function in `coaching/rules.py`
4. Register it in the `_RULES` dict at the bottom of `rules.py`
5. Add a test in `tests/test_coaching.py`

### Replace coaching rules with an LLM

`coaching/rules.py` implements `get_coaching(opportunity: Opportunity) → CoachingResult`. You can replace the implementation with an API call while keeping the same function signature. No other module changes.

### Support real .ibt files

When real files are available:
1. Test `load_ibt(path)` from `parsing/ibt_reader.py` against a real file
2. Verify channel names match what pyirsdk returns (Speed, Throttle, Brake, etc.)
3. If pyirsdk's `freeze_var_buffer_latest()` iteration needs adjustment, only `_read_all_ticks()` in `ibt_reader.py` changes

### Add a new telemetry channel

1. Add the field to `TelemetryPoint` in `models/session.py`
2. Populate it in `parsing/synthetic.py` (for tests) and `parsing/ibt_reader.py` (for real files)
3. Use it in the analysis layer

### Support additional vehicle classes

The analysis is not car-specific. To add car-specific thresholds (e.g. different corner speed expectations), add a configuration lookup keyed by `Session.car` in `analysis/opportunity_detector.py`.

---

## Running Tests

```bash
uv run pytest                                    # all tests
uv run pytest tests/test_integration.py -v      # integration test with verbose output
uv run pytest --cov --cov-report=term-missing   # coverage report
```

All 58 tests should pass. Tests cover all modules except the Streamlit UI (manual verification).

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| pyirsdk | ≥1.3.5 | .ibt file reading |
| streamlit | ≥1.30.0 | UI framework |
| pandas | ≥2.0.0 | Tabular data in UI |
| numpy | ≥1.24.0 | Corner detection (local minima) |
| plotly | ≥5.18.0 | Telemetry overlay charts |
| scipy | ≥1.11.0 | Signal processing (available for future use) |
| pytest | dev | Test framework |
| pytest-cov | dev | Coverage reporting |
