# Architecture

## Context

Driver Development Toolkit is a local Python application that ingests iRacing `.ibt` telemetry files and produces coaching-first reports. The first milestone focuses on the analysis engine and report output, not a full graphical interface.

## Architectural Goals

- Keep telemetry ingestion separate from coaching logic.
- Make recommendations traceable to structured evidence.
- Allow future support for additional cars, tracks, report formats, and reference laps.
- Keep the MVP simple enough to understand and test.

## Proposed Components

```text
Local .ibt file
  -> Telemetry ingestion
  -> Session/lap model
  -> Segment comparison
  -> Opportunity detection
  -> Coaching recommendation generation
  -> Report rendering
```

## Module Responsibilities

| Area | Responsibility |
|---|---|
| Ingestion | Load `.ibt` files using a proven parser and normalize telemetry into internal tables/models. |
| Domain model | Represent sessions, laps, segments, telemetry channels, opportunities, recommendations, and evidence. |
| Lap processing | Identify completed laps, best lap, segment boundaries, and comparable telemetry samples. |
| Opportunity detection | Find time-loss areas and classify likely causes using explainable rules. |
| Coaching | Convert detected opportunities into actionable recommendations and practice activities. |
| Reporting | Render coaching-first output with supporting evidence. |
| CLI | Provide a documented local entry point for generating reports. |

## Data Model Sketch

| Concept | Purpose |
|---|---|
| `TelemetrySession` | Metadata, laps, and available telemetry channels from one file. |
| `Lap` | Lap number, time, validity if available, and sampled channel data. |
| `TrackSegment` | Comparable range of lap distance or normalized distance. |
| `TelemetryEvidence` | Structured observations supporting a recommendation. |
| `Opportunity` | Ranked time-loss opportunity with location, impact, cause, and evidence. |
| `CoachingRecommendation` | Human-facing guidance and practice drill derived from an opportunity. |

## Initial Analysis Strategy

The MVP should compare the driver's laps against the best valid lap from the same file. If valid lap metadata is unavailable, the system should use documented fallback logic and flag the confidence level.

Initial opportunity categories:

- Corner entry speed or braking timing loss.
- Brake release/coast phase loss.
- Throttle application delay.
- Inconsistent segment execution.

These categories are intentionally conservative and explainable.

## Interfaces

Initial interface:

- CLI command that accepts an `.ibt` path and writes a Markdown or text coaching report.

Future interfaces:

- Desktop GUI or local web UI.
- Rich telemetry evidence charts.
- Reference lap comparison workflow.

## Dependency Direction

Presentation depends on coaching outputs. Coaching depends on opportunities and evidence. Opportunity detection depends on normalized lap/session models. Domain models do not depend on CLI or report rendering.

## Risks

- Real `.ibt` channel availability may vary by file or iRacing version.
- Lap validity and segment boundaries may require domain-specific fallback logic.
- Without representative sample files, parser and analysis validation will be limited.
