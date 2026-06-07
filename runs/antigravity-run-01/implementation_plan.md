# Implementation Plan - Driver Development Toolkit

This document establishes the architecture, requirements, design decisions, and verification strategy for the Driver Development Toolkit (DDT) MVP.

---

## 1. Product Vision & Requirements

The Driver Development Toolkit helps drivers improve lap times by analyzing offline iRacing `.ibt` telemetry files. The toolkit operates as a **virtual coach**, highlighting the largest areas of time-loss, explaining the root causes (e.g., driver inputs), and recommending practice drills.

### Functional Requirements (FR)
*   **FR-1: Telemetry Parsing:** Parse telemetry samples, headers, and metadata from offline `.ibt` files (or synthetic data fixtures).
*   **FR-2: Lap Extraction:** Automatically identify individual laps and extract their timestamps, lap times, and telemetry arrays.
*   **FR-3: Track Sectoring:** Segment the lap into ovals/sectors (e.g., Turns and Straights).
*   **FR-4: Telemetry Comparison:** Compare a selected lap against the session's fastest lap (or a reference lap) using distance-based interpolation.
*   **FR-5: Delta-T (Time Slip) Calculation:** Calculate the cumulative time delta along the lap.
*   **FR-6: Opportunity Ranking:** Group time-loss by sector and rank them by cumulative time lost.
*   **FR-7: Coaching Heuristics:** Evaluate driver inputs against coaching rules to identify entry, mid-corner, and exit mistakes.
*   **FR-8: Interactive UI:** Display ranked opportunities, coaching tips, and telemetry traces (speed, throttle, brake overlays).

### Non-Functional Requirements (NFR)
*   **NFR-1: Maintainability:** Code must be modular, strongly typed, and structured using clean Python patterns.
*   **NFR-2: Testability:** Core parsing, analysis, and coaching modules must be fully unit-tested with mocked/synthetic data.
*   **NFR-3: Portability:** Run on Windows 11/10 using Python 3.10+ and `uv` package management without requiring an active iRacing game process.

---

## 2. Design Decisions & Tradeoffs

### UI Strategy: Streamlit & Plotly
*   **Selected Option:** Streamlit Web Application + Plotly Charts.
*   **Rationale:** Standard Python GUI frameworks (like Tkinter or PyQt) require substantial boilerplate code to build interactive charts and look outdated. Streamlit provides a premium, responsive web interface natively in Python. Plotly enables high-fidelity, interactive distance-based line overlays (hover, zoom) for throttle/brake traces.
*   **Tradeoff:** Requires the user to run `streamlit run app.py` (which launches a local web server), rather than running a compiled double-clickable `.exe`. For a developer/experienced driver, this is an acceptable tradeoff for a high-quality UI.

### Sectoring Strategy: Curvature-Based Dynamic Turn Detection (Option A)
*   **Selected Option:** Analyze lateral acceleration (`LatAccel`) and steering wheel angle (`SteeringWheelAngle`) over the fastest lap to identify turns.
*   **Assumptions:**
    *   The track is an oval or has clearly defined, repetitive turns.
    *   A continuous region of high lateral acceleration and steering angle indicates a turn.
    *   Straights have low lateral acceleration and near-zero steering.
*   **Risks:** Road courses have complex turns, double apexes, and chicane sections that may confuse a simple threshold-based oval sectoring algorithm.
*   **Mitigation:** The sectoring algorithm will be structured as an abstract interface (`BaseSectorer`). The MVP will implement `OvalSectorer` (threshold-based on smoothed lateral acceleration). A fallback config-based mapping (`ConfigSectorer`) can be added later if needed.

### Data Strategy: Synthetic Telemetry Data
*   **Approach:** Build a telemetry data generator class (`SyntheticTelemetryGenerator`) to produce simulated telemetry arrays for testing.
*   **Rationale:** Allows testing lap parsing, sectoring, delta-T calculation, and coaching heuristics without needing a physical iRacing installation or `.ibt` files during initial development.
*   **Tests Included:**
    *   *Reference Lap:* Smooth lines, optimal corner minimum speed, early throttle.
    *   *Driver Error Lap 1 (Corner Entry):* Late braking, slow brake release, resulting in overshoot and lower corner minimum speed.
    *   *Driver Error Lap 2 (Corner Exit):* Abrupt throttle application causing simulated wheelslip (or delayed throttle application).

---

## 3. Architecture & Module Design

The system follows a clean layered architecture:

```
┌────────────────────────────────────────────────────────┐
│                   UI Layer (app.py)                    │
│      (Renders Streamlit layout, Plotly charts)         │
└───────────────────────────┬────────────────────────────┘
                            │ Uses
┌───────────────────────────▼────────────────────────────┐
│              Coaching Layer (coaching.py)              │
│       (Evaluates heuristics, generates advice)         │
└───────────────────────────┬────────────────────────────┘
                            │ Uses
┌───────────────────────────▼────────────────────────────┐
│              Analysis Layer (analyzer.py)              │
│  (Sectoring, interpolation, lap splitting, delta-T)    │
└───────────────────────────┬────────────────────────────┘
                            │ Uses
┌───────────────────────────▼────────────────────────────┐
│               Data Layer (parser.py)                   │
│         (Loads .ibt via pyirsdk or Synthetic)          │
└────────────────────────────────────────────────────────┘
```

### Core Classes & Interfaces
1.  **`TelemetrySession`**: Represents a parsed telemetry log containing metadata (track name, car type) and a list of `Lap` objects.
2.  **`Lap`**: Contains the raw time series DataFrame for a single lap (channels: `Speed`, `Throttle`, `Brake`, `Steering`, `LapDist`, `LatAccel`, etc.) along with summary statistics (lap time, max speed).
3.  **`BaseSectorer`**: Interface for partitioning a lap into sectors.
    *   `OvalSectorer`: Detects Turn 1-2, Backstretch, Turn 3-4, Frontstretch using lateral acceleration.
4.  **`TelemetryComparer`**: Compares a target `Lap` with a reference `Lap` by interpolating all channels onto a common distance grid (e.g., 1-meter intervals). Computes `delta_t` at each point.
5.  **`CoachingEngine`**: Evaluates the telemetry arrays for each corner and straight using heuristics to flag performance opportunities.

---

## 4. MVP Coaching Heuristics

We implement three primary heuristics targeting Late Models on short ovals:

### 1. Corner Entry Braking (Turn entry)
*   **Opportunity:** Turn entry speed loss.
*   **Rule:** Compare target lap braking point and brake release profile to the reference lap.
    *   *Late Braking/Over-driving:* If target braking point is $> 5$ meters deeper and minimum speed is lower, flag "Braking too late".
    *   *Slow Release:* If brake pressure stays high too long in the turn-in phase (compared to reference), flag "Braking too hard/abrupt release, causing front understeer".
*   **Drill Recommendation:** "Brake Release Drill - Focus on rolling speed into the turn by gradually releasing the brake as you turn the wheel."

### 2. Mid-Corner Stability (Apex)
*   **Opportunity:** Unstable mid-corner steering/speed.
*   **Rule:**
    *   *Coasting:* If driver is at 0% throttle and 0% brake for $> 1.5$ seconds, flag "Excessive coasting".
    *   *Over-steering/Sawtooth inputs:* If steering angle variance is high ($> \text{threshold}$), flag "Unstable steering inputs mid-corner".
*   **Drill Recommendation:** "Steering Smoothness Drill - Try to hold a single steering angle through the center of the corner rather than sawing at the wheel."

### 3. Corner Exit Traction (Turn exit)
*   **Opportunity:** Delayed/inefficient exit power.
*   **Rule:**
    *   *Delayed Throttle:* Target throttle reaches 100% significantly later in distance ($> 8$ meters) than reference.
    *   *Unstable Throttle:* Throttle trace fluctuates (sawtooth) during exit, indicating wheelspin or correction.
*   **Drill Recommendation:** "Throttle Progression Drill - Wait until the car is rotated, then apply throttle in one smooth, continuous motion."

---

## 5. Implementation Milestones

### Milestone 1: Environment & Telemetry Foundations (Current)
*   Create `pyproject.toml` with `uv` configurations.
*   Implement `parser.py` (offline `.ibt` reading using `pyirsdk` structures, plus a fallback `SyntheticTelemetryGenerator`).
*   Implement lap detection logic.
*   *Verification:* Unit tests checking that laps are parsed and segmented correctly.

### Milestone 2: Sectoring & Comparison Engine
*   Implement `OvalSectorer` to partition laps into sectors.
*   Implement `TelemetryComparer` for distance-based alignment and delta-T computation.
*   *Verification:* Test alignment algorithms and sector boundary consistency.

### Milestone 3: Coaching Engine & Rules
*   Implement `coaching.py` with entry, mid, and exit heuristics.
*   Map outcomes to ranked opportunities and structured practice drills.
*   *Verification:* Assert coaching engine outputs correct warnings for synthetic error laps.

### Milestone 4: Streamlit UI Development
*   Implement interactive dashboard with session summary, lap selectors, ranked coaching cards, and Plotly overlays.
*   *Verification:* Launch local app, upload/load files, verify chart interactions and visual responsiveness.

### Milestone 5: Retrospective & Documentation
*   Write maintainer handoff guide and final test walkthrough.
*   Refine code comments and documentation.
