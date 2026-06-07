# Maintainer Handoff - Driver Development Toolkit

This document provides a guide for developers inheriting or maintaining the Driver Development Toolkit.

---

## 1. System Overview

The Driver Development Toolkit (DDT) is a data-driven coaching application for sim racers. It extracts driving telemetry from offline iRacing `.ibt` logs, segments the laps into turn and straight sectors, compares laps on a distance-aligned grid, and runs coaching heuristics to diagnose driver input mistakes. Findings and interactive charts are presented in a Streamlit local dashboard.

---

## 2. Architectural Structure

The codebase is written in Python and is divided into modular, decoupled layers:

1.  **Data Layer (`parser.py`)**:
    *   `Lap` and `TelemetrySession` classes hold session-level metadata and time-series DataFrames.
    *   `parse_ibt_file()` reads binary `.ibt` logs via `pyirsdk` structures.
    *   `SyntheticTelemetryGenerator` simulates realistic, physically consistent lap data (Reference, Corner Entry Error, and Corner Exit Error) for offline validation and test suite execution.
2.  **Analysis Layer (`analyzer.py`)**:
    *   `OvalSectorer` dynamically detects turn zones (Turn 1-2, Turn 3-4) and straights from smoothed lateral Gs.
    *   `TelemetryComparer` uses linear interpolation to map different time-series datasets to a shared distance-based grid (e.g. 1-meter intervals) and computes the cumulative delta-T (time slip).
3.  **Coaching Layer (`coaching.py`)**:
    *   `CoachingEngine` executes rule-based driving heuristics on the entry, apex, and exit zones of detected turns to diagnose time-loss causes (Late braking, slow brake release, coasting, sawing the wheel, exit throttle lifts, delayed power).
    *   Rank and formats advices and focused practice drills.
4.  **UI Layer (`app.py`)**:
    *   Streamlit-based dashboard representing key lap indicators, ranked coaching recommendations, interactive multi-panel Plotly charts (aligned on a shared distance X-axis), and sector table sheets.

---

## 3. Repository Directory Layout

```text
d:\Dev\driver-development-toolkit-experiment\
├── pyproject.toml                  # Python package and dependency configuration
├── uv.lock                         # Locked dependency graph
├── driver_development_toolkit/     # Core library source code
│   ├── __init__.py
│   ├── parser.py                   # Parsing and synthetic generation logic
│   ├── analyzer.py                 # Turn detection and distance alignment
│   ├── coaching.py                 # Coaching rules engine
│   └── app.py                      # Interactive Streamlit UI dashboard
├── tests/                          # Automated test suite
│   ├── test_parser.py              # Telemetry loading unit tests
│   ├── test_analyzer.py            # Sectoring and comparison unit tests
│   └── test_coaching.py            # Heuristics rules unit tests
├── runs/
│   └── antigravity-run-01/         # Run logs and engineering artifacts
│       ├── images/                 # Screenshot assets
│       ├── implementation_plan.md  # Core design artifact
│       ├── task.md                 # Checked task logs
│       ├── Maintainer_Handoff.md   # This onboarding guide
│       └── walkthrough.md          # Implementation review
└── evaluation/                     # Empty experiment template forms
```

---

## 4. Setup & Running Locally

The project uses the `uv` tool for fast virtual environment and dependency management.

### Prerequisites
*   Windows 10/11
*   Python 3.11+
*   `uv` (Python packaging tool)

### Installation
From the project workspace root, initialize the virtual environment and install all dependencies:
```bash
uv sync
```

### Starting the Dashboard
To start the Streamlit local web application dashboard:
```bash
$env:PYTHONPATH="."
uv run streamlit run driver_development_toolkit/app.py --server.headless true
```
Open a browser and navigate to `http://localhost:8501`.

---

## 5. Test Suite Execution

To execute the unit tests and verify the code against all physics and edge cases:
```bash
uv run python -m pytest
```

---

## 6. Key Design Decisions & Rationale

*   **Distance-Based Comparison**: Telemetry comparisons must always align by distance (`LapDist`), never by time (`SessionTime`), because the speed difference shifts the locations of speed traces in time. Alignment via `numpy.interp` provides correct delta-T analysis.
*   **Dynamic Curve Turn Detection**: The dynamic sectorer avoids track-specific configurations. By finding where smoothed lateral acceleration exceeds $1.5\text{ m/s}^2$ (G-forces), it finds turn boundaries natively.
*   **Physics Sim for Tests**: Synthetic generation solves the problem of not having a physical simulator on test machines, producing consistent traces with realistic G-forces, speed curves, and input behaviors.
*   **Isolated Sector Sim**: Speed resetting (resetting to 40m/s at 500m) stops mistakes in Turn 1-2 from compounding into Turn 3-4, ensuring unit tests can isolate and target individual sector recommendations.

---

## 7. Known Limitations & Future Improvements

1.  **Oval Optimization**: The `OvalSectorer` is tuned for tracks with exactly 2 main turning zones (short ovals). On road courses, the thresholding method may need to be replaced with a path-curvature algorithm or track metadata map configs.
2.  **Telemetry Format**: The physical parser wraps `pyirsdk.IBT` which operates via memory mapping and standard C-types. If `pyirsdk` suffers breaking updates, parsing could fail. A fallback pure-python native `.ibt` binary parser can be implemented.
3.  **Advanced Metrics**: Adding tire heat overlays, suspension travel graphs, and steering trace overlays would further enhance coaching quality for setup tuning.
