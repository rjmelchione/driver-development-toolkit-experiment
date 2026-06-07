# Requirements – Driver Development Toolkit

Version: 1.0  
Status: Baseline  
Derived from: Product Vision (experiment/Product_Vision.md)

---

## Functional Requirements

### FR-001 – Load Telemetry File
The system shall accept an iRacing `.ibt` telemetry file as its primary data input.

### FR-002 – Parse Session Laps
The system shall extract all laps recorded in a session from the telemetry file, including lap number, lap time, and per-tick telemetry data.

### FR-003 – Extract Telemetry Channels
The system shall extract the following channels per telemetry tick:
- `Speed` (m/s)
- `Throttle` (0.0–1.0)
- `Brake` (0.0–1.0)
- `Gear` (integer)
- `RPM`
- `LapDistPct` (0.0–1.0, distance through lap as a percentage)
- `SessionTime` (seconds since session start)
- `LapCurrentLapTime` (elapsed time in current lap)

Additional channels shall be extracted if present in the file without breaking existing behavior.

### FR-004 – Identify Valid Laps
The system shall distinguish valid complete laps from out-laps, in-laps, and incomplete laps. Invalid laps shall be excluded from comparative analysis.

### FR-005 – Select Reference Lap
The system shall automatically select the driver's fastest valid lap as the reference lap for comparison. A user-provided reference lap is supported but not required.

### FR-006 – Segment Lap into Corners
The system shall segment each lap into corners (performance zones) by identifying local speed minima. Each identified minimum represents the apex of a corner.

### FR-007 – Compute Per-Corner Metrics
For each corner in each lap, the system shall compute:
- Minimum corner speed
- Brake application point (as LapDistPct)
- Throttle application point (as LapDistPct)
- Time delta vs. reference lap for that corner zone

### FR-008 – Identify Performance Opportunities
The system shall identify corners where the driver is losing measurable lap time relative to their reference lap. An opportunity exists when the time delta for a corner exceeds a configurable minimum threshold (default: 0.05 seconds).

### FR-009 – Determine Opportunity Type
For each identified opportunity, the system shall classify the likely cause using telemetry evidence:
- **Over-slowing**: Minimum corner speed significantly lower than reference
- **Late throttle**: Throttle application point later than reference
- **Early brake**: Brake applied earlier than reference
- **Inconsistent braking**: High variance in brake point across laps

### FR-010 – Quantify Time Impact
Each opportunity shall be associated with an estimated lap time impact in seconds.

### FR-011 – Rank Opportunities
Opportunities shall be ranked by estimated time impact in descending order.

### FR-012 – Generate Coaching Recommendation
For each opportunity, the system shall generate a specific driving adjustment recommendation addressing the identified cause.

### FR-013 – Generate Practice Drill
For each opportunity, the system shall recommend a focused practice activity targeting the identified weakness.

### FR-014 – Present Telemetry Evidence
For each opportunity, the system shall present the supporting telemetry traces (speed, throttle, brake) showing the difference between the reference lap and the driver's typical laps at that corner.

### FR-015 – Coaching-First Display
The primary application view shall display:
- Session summary (car, track, lap count, best lap time)
- Ranked list of coaching opportunities with time impact estimates
- Coaching recommendation for each opportunity
- Practice drill for each opportunity

### FR-016 – Drill-Down Evidence View
The user shall be able to select any opportunity and view the supporting telemetry overlay for that corner zone.

### FR-017 – Session Consistency Analysis
The system shall report lap-to-lap consistency metrics (standard deviation of lap time, consistency score) as part of the session summary.

---

## Non-Functional Requirements

### NFR-001 – Local Execution
The system shall run entirely on the user's local machine without internet access, external API calls, or cloud dependencies.

### NFR-002 – Performance
The system shall process a 30-lap session and produce coaching output in under 30 seconds on a modern consumer PC.

### NFR-003 – Technology Stack
The system shall be implemented in Python 3.11 or later and use `uv` as the package manager.

### NFR-004 – Maintainability
The system shall be structured such that a developer with Python experience can understand, modify, and extend it without reverse engineering the implementation. Engineering artifacts shall support this without requiring source-level analysis.

### NFR-005 – Testability
The analysis and coaching layers shall be testable using automated unit tests without requiring a real `.ibt` file.

### NFR-006 – Windows Compatibility
The system shall run on Windows 10/11 as the primary target platform.

### NFR-007 – Installability
The system shall be installable using `uv sync` from the project root. Setup shall be documented in a single README.

---

## Out of Scope (MVP)

The following are explicitly excluded from this version:

- Real-time telemetry (live iRacing SDK connection)
- Vehicle setup analysis or recommendations
- Race strategy analysis
- Crew chief or spotter functionality
- Reference laps from other drivers (supported by design but not provided)
- Cloud storage, accounts, or networking
- Multi-user or team features
- Support for vehicle classes other than Late Model (supported by design but not validated)
- AI/LLM-powered coaching (deferred to future enhancement)

---

## Assumptions

**A-001**: The `.ibt` file format can be read using `pyirsdk`. This assumption must be validated against a real file when one becomes available.

**A-002**: Synthetic test data modeled on known iRacing telemetry channel names and value ranges is sufficient to validate analysis logic. Integration with real files requires separate validation.

**A-003**: Lap segmentation by speed minima is a valid approach for identifying corners on the track types used in iRacing Late Model sessions (primarily ovals and short tracks).

**A-004**: A driver's fastest valid lap is a meaningful reference lap for self-comparison coaching. This may not hold for sessions with significant track evolution (rubber laid down over time).

**A-005**: The minimum time delta threshold of 0.05 seconds per corner is sufficient to filter noise while surfacing meaningful opportunities. This value should be tunable.
