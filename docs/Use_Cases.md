# Use Cases – Driver Development Toolkit

Version: 1.0  
Status: Baseline

---

## UC-001 – Analyze a Session for Coaching

**Actor**: Driver  
**Goal**: Understand where lap time is being lost and receive prioritized coaching recommendations  
**Requirements**: FR-001, FR-002, FR-003, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-011, FR-012, FR-013, FR-015

**Preconditions**:
- Driver has completed an iRacing session that produced an `.ibt` file
- At least two valid laps exist in the file

**Main Flow**:
1. Driver opens the application in a browser (Streamlit)
2. Driver uploads or specifies the path to their `.ibt` file
3. System parses the file and identifies all valid laps
4. System selects the fastest valid lap as the reference lap
5. System compares remaining laps to the reference and identifies performance opportunities
6. System ranks opportunities by estimated lap time impact
7. System displays:
   - Session summary (car, track, lap count, best lap time, consistency score)
   - Ranked list of coaching opportunities, each showing:
     - Location (corner identifier)
     - Estimated time impact
     - Opportunity type and brief description
     - Coaching recommendation
     - Practice drill
8. Driver reviews the opportunities in priority order

**Postconditions**:
- Driver can see their largest time loss opportunities
- Each opportunity has a coaching recommendation and practice drill
- Telemetry evidence is accessible via drill-down

**Exceptions**:
- File contains no valid laps: System displays an error explaining the issue
- File cannot be parsed: System displays a clear error message

---

## UC-002 – Review Telemetry Evidence for an Opportunity

**Actor**: Driver  
**Goal**: Understand the telemetry data that supports a coaching recommendation  
**Requirements**: FR-014, FR-016

**Preconditions**:
- UC-001 has been completed and coaching opportunities are displayed

**Main Flow**:
1. Driver selects a coaching opportunity from the ranked list
2. System displays the telemetry evidence view for that opportunity:
   - Track segment identifier (corner number, estimated location)
   - Overlay chart showing speed, throttle, and brake vs. LapDistPct for:
     - The reference lap (best lap)
     - The driver's average across other laps
   - Annotations highlighting the specific divergence causing the time loss
3. Driver interprets the telemetry overlay
4. Driver may return to the opportunity list and select another opportunity

**Postconditions**:
- Driver understands the specific telemetry behavior behind the recommendation

---

## UC-003 – Review Session Consistency

**Actor**: Driver  
**Goal**: Understand how consistent their lap times were across the session  
**Requirements**: FR-017

**Preconditions**:
- UC-001 has been completed and the session summary is visible

**Main Flow**:
1. Driver views the session summary panel
2. System displays:
   - Lap time for each valid lap
   - Best lap time
   - Average lap time
   - Standard deviation of lap times
   - Consistency score (derived from standard deviation relative to best lap)
3. Driver assesses whether consistency or raw pace is their primary focus

**Postconditions**:
- Driver understands how consistent their session was and can decide whether to focus on pace or repeatability

---

## UC-004 – Load a Session with No Real .ibt File (Development/Demo)

**Actor**: Developer or evaluator  
**Goal**: Run the application without a real iRacing telemetry file to validate coaching output  
**Requirements**: NFR-005

**Preconditions**:
- Application is installed and running
- No real `.ibt` file is available

**Main Flow**:
1. Developer selects "Use Demo Session" in the application
2. System generates a synthetic session using the built-in telemetry generator
3. System processes the synthetic session through the full analysis pipeline
4. System displays coaching output as in UC-001

**Postconditions**:
- Developer can evaluate coaching output and UI without real telemetry data
- Synthetic session behavior is documented and reproducible

---

## Traceability

| Use Case | Requirements Covered |
|---|---|
| UC-001 | FR-001 through FR-015 |
| UC-002 | FR-014, FR-016 |
| UC-003 | FR-017 |
| UC-004 | NFR-005 |
