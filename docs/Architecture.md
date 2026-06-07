# Architecture – Driver Development Toolkit

Version: 1.0  
Status: Baseline

---

## Overview

The Driver Development Toolkit is structured as four independent layers. Each layer has a single responsibility. Dependencies flow in one direction only: downward (Presentation → Analysis → Parsing). No lower layer knows about any upper layer.

```
┌─────────────────────────────────────────────┐
│              Presentation Layer              │
│         Streamlit coaching dashboard         │
│   (ui/app.py, ui/components/)               │
└──────────────────┬──────────────────────────┘
                   │ uses
┌──────────────────▼──────────────────────────┐
│               Analysis Layer                 │
│  Opportunity detection, ranking, coaching    │
│  (analysis/, coaching/)                      │
└──────────────────┬──────────────────────────┘
                   │ uses
┌──────────────────▼──────────────────────────┐
│               Data Model Layer               │
│   Session, Lap, TelemetryChannel types       │
│   (models/)                                  │
└──────────────────┬──────────────────────────┘
                   │ uses
┌──────────────────▼──────────────────────────┐
│               Parsing Layer                  │
│   .ibt file reading, lap segmentation        │
│   (parsing/)                                 │
└─────────────────────────────────────────────┘
```

---

## Layer Responsibilities

### Parsing Layer (`src/driver_toolkit/parsing/`)

Responsible for converting raw `.ibt` binary data into structured Python objects.

| Module | Responsibility |
|---|---|
| `ibt_reader.py` | Wraps `pyirsdk` to open an `.ibt` file and iterate over telemetry ticks |
| `lap_segmenter.py` | Converts the flat tick stream into per-lap `Lap` objects |
| `synthetic.py` | Generates realistic synthetic telemetry sessions for testing |

**Key constraint**: This layer is the only layer permitted to reference `pyirsdk`. Upper layers receive only data model types.

### Data Model Layer (`src/driver_toolkit/models/`)

Defines the canonical data structures passed between all layers.

| Type | Description |
|---|---|
| `TelemetryPoint` | A single telemetry tick: time, speed, throttle, brake, gear, RPM, LapDistPct |
| `Lap` | One lap: lap number, lap time, validity flag, list of TelemetryPoints |
| `Session` | A full session: car, track, list of Laps |

**Key constraint**: All model types are plain Python dataclasses with no framework dependencies. They can be serialized, compared, and tested without importing any third-party library.

### Analysis Layer (`src/driver_toolkit/analysis/`, `src/driver_toolkit/coaching/`)

Responsible for deriving coaching insights from structured session data.

| Module | Responsibility |
|---|---|
| `metrics.py` | Computes per-corner metrics (min speed, brake point, throttle point) for a lap |
| `comparator.py` | Compares a lap against the reference lap; computes time delta per corner |
| `opportunity_detector.py` | Identifies, classifies, and quantifies coaching opportunities from lap comparisons |
| `ranker.py` | Sorts opportunities by time impact |
| `coaching/rules.py` | Maps opportunity types to coaching text and practice drill text |

**Key constraint**: This layer is fully deterministic. Given the same session data, it always produces the same opportunities and recommendations. No randomness, no external calls.

### Presentation Layer (`src/driver_toolkit/ui/`)

Responsible for displaying coaching output to the user.

| Module | Responsibility |
|---|---|
| `app.py` | Streamlit application entry point; file upload, page routing |
| `components/summary.py` | Renders the session summary and ranked opportunity list |
| `components/evidence.py` | Renders the telemetry evidence chart for a selected opportunity |

**Key constraint**: The UI contains no analysis logic. It only calls the analysis layer and renders its output.

---

## Data Flow

```
User selects .ibt file
        │
        ▼
ibt_reader.py  ──reads──▶  raw tick stream
        │
        ▼
lap_segmenter.py  ──produces──▶  Session(Lap(TelemetryPoint[]))
        │
        ▼
metrics.py  ──computes──▶  CornerMetrics per lap
        │
        ▼
comparator.py  ──computes──▶  LapComparison (delta per corner)
        │
        ▼
opportunity_detector.py  ──produces──▶  Opportunity[]
        │
        ▼
ranker.py  ──sorts──▶  Opportunity[] (by impact)
        │
        ▼
coaching/rules.py  ──enriches──▶  CoachingResult[]
        │
        ▼
Streamlit UI  ──displays──▶  coaching dashboard
```

---

## Key Design Decisions

**Coaching over telemetry**: The UI is structured to show coaching conclusions first and raw telemetry as supporting evidence. This matches the product vision's "coaching-first" requirement.

**Rules-based coaching**: Coaching recommendations are encoded as deterministic rules mapped to opportunity types. This produces auditable, traceable recommendations without LLM dependencies.

**Synthetic data for testing**: Because no real `.ibt` files are available, a synthetic generator produces realistic sessions with known lap time variations. This allows full test coverage of the analysis layer.

**Corner detection by speed minima**: Corners are identified algorithmically as local speed minima in the lap trace. This requires no track-specific database and generalizes across track types.

**pyirsdk isolation**: The `pyirsdk` dependency is isolated entirely within the Parsing layer. If the library is replaced or the `.ibt` format changes, only `ibt_reader.py` needs to change.

---

## Extension Points

The following design decisions intentionally enable future expansion:

- **Additional vehicle classes**: Vehicle class is stored in `Session.car` but analysis rules are not car-specific in the MVP. Car-specific thresholds can be added to a configuration file.
- **Reference lap from another driver**: `comparator.py` accepts any `Lap` as the reference. Providing a lap from a different source requires only a different `Lap` object.
- **LLM coaching**: `coaching/rules.py` can be replaced with an LLM-based module that takes the same `Opportunity` input and returns the same `CoachingResult` output.
- **Additional telemetry channels**: `TelemetryPoint` is extensible; new channels from `.ibt` files are passed through without breaking existing analysis.

---

## Technology Choices

| Technology | Role | Rationale |
|---|---|---|
| Python 3.11+ | Implementation language | Experiment specification; strong data science ecosystem |
| uv | Package manager | Experiment specification; fast, modern |
| pyirsdk | .ibt file parsing | Established Python library for iRacing telemetry |
| Streamlit | UI framework | Coaching-first dashboards with charts; pure Python; local execution |
| pandas | Data manipulation | Standard tabular data handling for telemetry series |
| numpy | Numerical computation | Signal processing for corner detection (local minima) |
| plotly | Charting | Interactive telemetry overlays in Streamlit |
| pytest | Testing | Standard Python test framework |

---

## Repository Structure

```
driver-development-toolkit-experiment/
├── docs/                      ← engineering artifacts
│   ├── Requirements.md
│   ├── Architecture.md
│   ├── Use_Cases.md
│   ├── Research_Log.md
│   ├── Decision_Log.md
│   ├── Test_Strategy.md
│   └── Maintainer_Handoff.md
├── src/
│   └── driver_toolkit/
│       ├── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── session.py
│       ├── parsing/
│       │   ├── __init__.py
│       │   ├── ibt_reader.py
│       │   ├── lap_segmenter.py
│       │   └── synthetic.py
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── metrics.py
│       │   ├── comparator.py
│       │   ├── opportunity_detector.py
│       │   └── ranker.py
│       ├── coaching/
│       │   ├── __init__.py
│       │   └── rules.py
│       └── ui/
│           ├── __init__.py
│           ├── app.py
│           └── components/
│               ├── __init__.py
│               ├── summary.py
│               └── evidence.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_parsing.py
│   ├── test_metrics.py
│   ├── test_comparator.py
│   ├── test_opportunity_detector.py
│   ├── test_coaching.py
│   └── test_integration.py
├── runs/
│   └── claude-run-03/
│       ├── Run_Log.md
│       ├── Artifact_Inventory.md
│       ├── Decision_Log.md
│       ├── Human_Observation_Log.md
│       └── Escalation_Log.md
├── experiment/                ← read-only experiment inputs
├── evaluation/                ← evaluation templates
├── pyproject.toml
├── README.md
└── .gitignore
```
