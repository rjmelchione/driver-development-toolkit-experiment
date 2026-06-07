# Analysis Rules

## Purpose

This document describes the current explainable MVP coaching logic. These rules are intentionally conservative and synthetic-fixture validated. They should be revisited after real Late Model `.ibt` telemetry is available.

## Reference Lap Selection

The analyzer uses the fastest valid lap in the session as the self-comparison reference lap.

Current assumption:

- The fastest valid lap is the best available internal reference when no external reference lap is supplied.

## Segmentation

The MVP divides a lap into four fixed normalized-distance segments:

| Segment | Distance Range |
|---|---|
| Turn 1 Entry | 0%-25% |
| Turn 1 Exit | 25%-50% |
| Turn 2 Entry | 50%-75% |
| Turn 2 Exit | 75%-100% |

Current assumption:

- Fixed synthetic segments are acceptable until real track/corner metadata is available.

## Impact Estimate

For each comparison lap and segment:

1. Calculate average speed for the comparison lap segment.
2. Calculate average speed for the reference lap segment.
3. Estimate loss as the segment's share of lap time multiplied by the relative speed deficit.
4. Ignore opportunities below `0.03s`.

This estimate is intended for ranking, not final race-engineering-grade timing.

## Classification Rules

Rules are evaluated in order:

| Rule | Threshold | Classification |
|---|---:|---|
| Average throttle is lower than reference | `>= 8.0` percentage points | Throttle application |
| Average brake is higher than reference | `>= 8.0` percentage points | Brake release |
| Speed loss remains without a dominant input difference | Any remaining significant speed loss | Corner entry / mid-corner speed |

## Consolidation

Multiple pace findings for the same segment are consolidated into the highest-impact opportunity for that segment. Repeated lower-impact findings are retained as supporting evidence.

Rationale:

- The product vision asks for ranked coaching opportunities, not one row per lap comparison.
- Repeated findings should increase confidence without overwhelming the report.

## Consistency Opportunities

The analyzer calculates segment loss variability across valid laps using population standard deviation. If variability exceeds the minimum impact threshold, a consistency opportunity is added for that segment.

## CLI Controls

The current CLI exposes:

- `--max-opportunities N` to limit report length.
- `--no-consistency` to exclude consistency opportunities.

## Analysis Provenance

Generated CLI reports include:

- Source type.
- Reference lap and reference lap time.
- Valid lap count.
- Segment count.
- Minimum impact threshold.
- Throttle and brake classification thresholds.
- Consistency inclusion setting.
- Report opportunity limit.
- Validation notes.

## Validation Boundary

Real `.ibt` ingestion remains intentionally blocked until representative Late Model telemetry is available for validation. The current rules are tested against synthetic telemetry fixtures only.

Synthetic fixture sources are labeled in reports and should not be treated as real driver evidence.
