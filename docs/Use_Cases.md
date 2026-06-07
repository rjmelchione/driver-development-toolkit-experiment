# Use Cases

## UC-001: Generate Coaching Report From One Session

Primary actor: Experienced iRacing driver.

Goal: Understand the most important driving improvements from a local `.ibt` telemetry file.

Main flow:

1. Driver provides the path to an `.ibt` telemetry file.
2. System loads telemetry and identifies completed laps.
3. System selects an internal reference, such as the driver's best valid lap.
4. System compares laps and identifies high-impact differences.
5. System outputs a ranked coaching report.
6. Driver reviews evidence for each recommendation.

Success outcome:

The driver can choose a focused improvement area without manually inspecting raw telemetry graphs.

## UC-002: Review Evidence Behind a Recommendation

Primary actor: Experienced iRacing driver.

Goal: Understand why the system recommended a change.

Main flow:

1. Driver opens a generated recommendation.
2. System shows relevant evidence, such as speed delta, brake/throttle timing, or steering behavior over a segment.
3. Driver can connect the coaching recommendation to telemetry observations.

Success outcome:

The recommendation is understandable and credible.

## UC-003: Identify Consistency Opportunities

Primary actor: Experienced iRacing driver.

Goal: Find areas where inconsistent execution costs lap time.

Main flow:

1. Driver provides a telemetry file with multiple completed laps.
2. System compares lap-to-lap variation by track segment.
3. System identifies segments with high variance or repeated losses.
4. System recommends a practice focus.

Success outcome:

The driver learns where consistency practice is likely to matter most.

## UC-004: Maintain or Extend the System

Primary actor: Future developer.

Goal: Add a new analysis rule, telemetry channel, or report format without reverse engineering the implementation.

Main flow:

1. Developer reads the architecture and requirements docs.
2. Developer locates the relevant module boundary.
3. Developer updates or adds tests.
4. Developer implements the change.
5. Developer updates traceability and decision artifacts if needed.

Success outcome:

The system remains maintainable after the initial run.
