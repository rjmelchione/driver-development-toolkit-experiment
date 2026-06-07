# Test Strategy – Driver Development Toolkit

Version: 1.0  
Status: Baseline

---

## Objectives

Tests exist to:
1. Verify that the analysis layer produces correct results given known inputs
2. Verify that the coaching layer maps opportunity types to correct recommendations
3. Verify that data models behave as expected
4. Provide a regression safety net for future changes
5. Demonstrate that the system works end-to-end without real `.ibt` files

Tests do **not** exist to:
- Prove the Streamlit UI renders correctly (manual verification required)
- Validate analysis against real iRacing driving scenarios (deferred; requires real files)

---

## Test Framework

- **Framework**: pytest
- **Coverage tool**: pytest-cov
- **Location**: `tests/`
- **Execution**: `uv run pytest` from project root

---

## Test Scope

### Unit Tests

| File | Tests |
|---|---|
| `test_models.py` | TelemetryPoint, Lap, Session construction; validity flags; edge cases |
| `test_parsing.py` | Synthetic generator produces valid Session; lap count; channel presence |
| `test_metrics.py` | Corner detection finds expected corners; metrics computed correctly |
| `test_comparator.py` | Time delta computed correctly; reference lap selection |
| `test_opportunity_detector.py` | Opportunities identified for known lap differences; classification correct |
| `test_coaching.py` | Each opportunity type maps to non-empty coaching text and practice drill |

### Integration Tests

| File | Tests |
|---|---|
| `test_integration.py` | Full pipeline: synthetic session → Session object → analysis → CoachingResult list; validates end-to-end output structure and content |

### Manual Verification

| Area | Verification Method |
|---|---|
| Streamlit UI layout | Run `uv run streamlit run src/driver_toolkit/ui/app.py` and verify coaching display |
| Chart rendering | Visually inspect telemetry overlay charts in the demo session |
| Ranking order | Verify opportunities appear in descending impact order |
| Real .ibt file | Deferred until files available |

---

## Coverage Target

- Analysis layer (`analysis/`, `coaching/`): **≥ 80%** line coverage
- Models: **≥ 90%** line coverage
- Parsing (excluding pyirsdk wrapper): **≥ 70%** line coverage
- UI: **Not measured** (Streamlit UI testing deferred)

---

## Synthetic Data Strategy

The `synthetic.py` module generates sessions with the following properties:
- Configurable number of laps (default: 10)
- One "reference quality" lap with optimal corner performance
- Remaining laps with deliberate imperfections:
  - Over-slowing at specific corners (minimum speed 5–15% below reference)
  - Late throttle application at specific corners
  - Inconsistent brake points (varied by ±2% LapDistPct across laps)
- Known lap times that differ by known amounts
- All standard telemetry channels populated with realistic values

This allows tests to assert:
- Specific opportunities are detected at the expected corners
- Time delta estimates are within tolerance of the known lap time differences
- Coaching recommendations are generated for the planted imperfections

---

## Test Data Assumptions

See A-002 in Requirements.md. Tests against synthetic data validate analysis logic, not parsing of real files. A separate integration test (run manually when files are available) will validate the parsing layer against real data.

---

## Regression Policy

- All tests must pass before any commit is accepted
- Tests are run via `uv run pytest` — no manual test execution
- A failing test blocks completion of the affected requirement
