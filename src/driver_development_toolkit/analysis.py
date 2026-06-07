"""Explainable coaching analysis over normalized telemetry."""

from __future__ import annotations

from statistics import mean, pstdev

from driver_development_toolkit.models import (
    Lap,
    Opportunity,
    OpportunityKind,
    TelemetryEvidence,
    TelemetrySample,
    TelemetrySession,
    TrackSegment,
)

DEFAULT_SEGMENTS: tuple[TrackSegment, ...] = (
    TrackSegment("Turn 1 Entry", 0.00, 0.25),
    TrackSegment("Turn 1 Exit", 0.25, 0.50),
    TrackSegment("Turn 2 Entry", 0.50, 0.75),
    TrackSegment("Turn 2 Exit", 0.75, 1.00),
)


def analyze_session(
    session: TelemetrySession,
    segments: tuple[TrackSegment, ...] = DEFAULT_SEGMENTS,
    minimum_impact_s: float = 0.03,
) -> list[Opportunity]:
    """Return ranked coaching opportunities for a session."""

    valid_laps = tuple(lap for lap in session.laps if lap.valid)
    if len(valid_laps) < 2:
        raise ValueError("At least two valid laps are required for self-comparison analysis.")

    reference_lap = min(valid_laps, key=lambda lap: lap.lap_time_s)
    comparison_laps = tuple(lap for lap in valid_laps if lap.number != reference_lap.number)

    opportunities: list[Opportunity] = []
    for lap in comparison_laps:
        for segment in segments:
            impact = _segment_time_delta(lap, reference_lap, segment)
            if impact < minimum_impact_s:
                continue
            opportunities.append(_classify_opportunity(lap, reference_lap, segment, impact))

    opportunities.extend(_consistency_opportunities(valid_laps, segments, minimum_impact_s))
    return sorted(opportunities, key=lambda opportunity: opportunity.impact_s, reverse=True)


def _segment_samples(lap: Lap, segment: TrackSegment) -> tuple[TelemetrySample, ...]:
    return tuple(
        sample for sample in lap.samples if segment.start_pct <= sample.distance_pct < segment.end_pct
    )


def _average_speed(lap: Lap, segment: TrackSegment) -> float:
    samples = _segment_samples(lap, segment)
    if not samples:
        raise ValueError(f"Lap {lap.number} has no samples for segment {segment.name}.")
    return mean(sample.speed_mph for sample in samples)


def _average_throttle(lap: Lap, segment: TrackSegment) -> float:
    samples = _segment_samples(lap, segment)
    return mean(sample.throttle_pct for sample in samples)


def _average_brake(lap: Lap, segment: TrackSegment) -> float:
    samples = _segment_samples(lap, segment)
    return mean(sample.brake_pct for sample in samples)


def _segment_time_delta(lap: Lap, reference_lap: Lap, segment: TrackSegment) -> float:
    speed = _average_speed(lap, segment)
    reference_speed = _average_speed(reference_lap, segment)
    if speed <= 0 or reference_speed <= 0:
        return 0.0

    segment_share = segment.end_pct - segment.start_pct
    lap_segment_time = lap.lap_time_s * segment_share
    speed_loss_ratio = max((reference_speed - speed) / reference_speed, 0.0)
    return round(lap_segment_time * speed_loss_ratio, 3)


def _classify_opportunity(
    lap: Lap,
    reference_lap: Lap,
    segment: TrackSegment,
    impact_s: float,
) -> Opportunity:
    throttle_delta = _average_throttle(reference_lap, segment) - _average_throttle(lap, segment)
    brake_delta = _average_brake(lap, segment) - _average_brake(reference_lap, segment)
    speed_delta = _average_speed(reference_lap, segment) - _average_speed(lap, segment)

    if throttle_delta >= 8:
        return _build_opportunity(
            segment,
            OpportunityKind.THROTTLE_APPLICATION,
            impact_s,
            "Throttle application is later or weaker than the reference lap.",
            "Begin unwinding steering and committing to throttle earlier once the car is stable.",
            "Run five-lap sets focused only on matching the reference throttle pickup point.",
            (
                TelemetryEvidence(
                    "Average throttle",
                    f"{throttle_delta:.1f} percentage points lower than reference",
                    "Delayed throttle is a likely contributor to exit speed loss.",
                ),
                TelemetryEvidence(
                    "Average speed",
                    f"{speed_delta:.1f} mph slower than reference",
                    "Lower speed in this segment creates measurable lap-time loss.",
                ),
            ),
            lap.number,
            reference_lap.number,
        )

    if brake_delta >= 8:
        return _build_opportunity(
            segment,
            OpportunityKind.BRAKE_RELEASE,
            impact_s,
            "Brake pressure remains higher than the reference lap through the segment.",
            "Release brake pressure more progressively and avoid carrying unnecessary brake after turn-in.",
            "Practice a brake-release drill: same brake point, smoother release, compare minimum speed.",
            (
                TelemetryEvidence(
                    "Average brake",
                    f"{brake_delta:.1f} percentage points higher than reference",
                    "Excess brake pressure can bind the car and reduce rolling speed.",
                ),
                TelemetryEvidence(
                    "Average speed",
                    f"{speed_delta:.1f} mph slower than reference",
                    "The braking difference aligns with lower segment speed.",
                ),
            ),
            lap.number,
            reference_lap.number,
        )

    return _build_opportunity(
        segment,
        OpportunityKind.CORNER_ENTRY,
        impact_s,
        "Entry or mid-corner speed is lower than the best lap without a dominant input difference.",
        "Review entry placement and minimum-speed confidence before adding more throttle.",
        "Run comparison laps focused on carrying one mph more minimum speed while holding line discipline.",
        (
            TelemetryEvidence(
                "Average speed",
                f"{speed_delta:.1f} mph slower than reference",
                "Speed loss is visible even though no single input dominates the diagnosis.",
            ),
        ),
        lap.number,
        reference_lap.number,
    )


def _build_opportunity(
    segment: TrackSegment,
    kind: OpportunityKind,
    impact_s: float,
    cause: str,
    recommendation: str,
    practice: str,
    evidence: tuple[TelemetryEvidence, ...],
    comparison_lap: int | None = None,
    reference_lap: int | None = None,
) -> Opportunity:
    return Opportunity(
        segment=segment,
        kind=kind,
        impact_s=impact_s,
        cause=cause,
        recommendation=recommendation,
        practice=practice,
        evidence=evidence,
        comparison_lap=comparison_lap,
        reference_lap=reference_lap,
    )


def _consistency_opportunities(
    laps: tuple[Lap, ...],
    segments: tuple[TrackSegment, ...],
    minimum_impact_s: float,
) -> list[Opportunity]:
    opportunities: list[Opportunity] = []
    reference_lap = min(laps, key=lambda item: item.lap_time_s)
    for segment in segments:
        segment_impacts = [_segment_time_delta(lap, reference_lap, segment) for lap in laps]
        variability = pstdev(segment_impacts) if len(segment_impacts) > 1 else 0.0
        if variability < minimum_impact_s:
            continue
        opportunities.append(
            _build_opportunity(
                segment,
                OpportunityKind.CONSISTENCY,
                round(variability, 3),
                "Lap-to-lap execution varies enough to create repeatable time loss risk.",
                "Prioritize repeatable marks and input timing before searching for more peak pace.",
                "Run a ten-lap consistency set and score only this segment against the target feel.",
                (
                    TelemetryEvidence(
                        "Segment variability",
                        f"{variability:.3f}s standard deviation versus best-lap segment estimate",
                        "Higher variation indicates the segment is not yet repeatable.",
                    ),
                ),
            )
        )
    return opportunities
