"""Identifies and classifies coaching opportunities from lap comparisons.

An opportunity is a corner where the driver is losing measurable time due to
a specific, addressable technique issue. Each opportunity is classified into
one of four types (see OpportunityType) based on the telemetry evidence.

Thresholds and classification logic are documented in docs/Requirements.md
FR-008 and FR-009.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from driver_toolkit.analysis.comparator import CornerDelta, LapComparison
from driver_toolkit.models import TelemetryPoint

MIN_TIME_IMPACT = 0.05       # seconds; minimum impact to report as an opportunity
OVER_SLOWING_THRESHOLD = -1.5  # m/s; average speed delta below this = over-slowing
EARLY_BRAKE_DIST_THRESHOLD = 0.015  # LapDistPct; braking this much earlier = early brake
LATE_THROTTLE_DIST_THRESHOLD = 0.015  # LapDistPct; throttle this much later = late throttle
INCONSISTENCY_STD_THRESHOLD = 0.01    # LapDistPct std dev for brake points = inconsistent


class OpportunityType(str, Enum):
    OVER_SLOWING = "over_slowing"
    LATE_THROTTLE = "late_throttle"
    EARLY_BRAKE = "early_brake"
    INCONSISTENT_BRAKING = "inconsistent_braking"
    GENERAL_CORNER = "general_corner"  # time loss without clear single cause


@dataclass
class Opportunity:
    """A specific, ranked coaching opportunity identified in the driver's telemetry.

    Addresses FR-008 through FR-011. Contains all information needed for the
    coaching layer to generate a recommendation and for the UI to display evidence.
    """

    corner_id: int
    apex_dist_pct: float              # position on track for UI display
    opportunity_type: OpportunityType
    time_impact: float                # estimated seconds lost per lap
    speed_delta: float                # m/s; negative = driver is slower than reference

    # Supporting telemetry (for the evidence view)
    ref_telemetry: list[TelemetryPoint] = field(default_factory=list)
    lap_telemetry: list[TelemetryPoint] = field(default_factory=list)

    # Human-readable context
    zone_entry_dist_pct: float = 0.0
    zone_exit_dist_pct: float = 0.0

    @property
    def corner_label(self) -> str:
        return f"Corner {self.corner_id}"

    @property
    def impact_label(self) -> str:
        return f"+{self.time_impact:.2f}s"


def detect_opportunities(
    comparisons: list[LapComparison],
    min_impact: float = MIN_TIME_IMPACT,
) -> list[Opportunity]:
    """Aggregate lap comparisons into a set of unique coaching opportunities.

    Per-corner performance across all comparison laps is averaged, then
    evaluated against thresholds to identify and classify opportunities.

    Args:
        comparisons: List of LapComparison from comparator.compare_to_reference.
        min_impact: Minimum estimated impact (seconds) to surface as opportunity.

    Returns:
        List of Opportunity sorted by time_impact descending (highest impact first).
    """
    if not comparisons:
        return []

    corner_ids = {delta.corner_id for comp in comparisons for delta in comp.corner_deltas}
    opportunities = []

    for corner_id in sorted(corner_ids):
        deltas_for_corner = [
            delta
            for comp in comparisons
            for delta in comp.corner_deltas
            if delta.corner_id == corner_id
        ]
        if not deltas_for_corner:
            continue

        opp = _evaluate_corner(corner_id, deltas_for_corner, comparisons)
        if opp and opp.time_impact >= min_impact:
            opportunities.append(opp)

    return sorted(opportunities, key=lambda o: o.time_impact, reverse=True)


def _evaluate_corner(
    corner_id: int,
    deltas: list[CornerDelta],
    comparisons: list[LapComparison],
) -> Optional[Opportunity]:
    """Analyze one corner across all laps and produce an Opportunity if warranted."""
    avg_speed_delta = sum(d.speed_delta for d in deltas) / len(deltas)
    time_impact = _speed_delta_to_time_impact(avg_speed_delta)

    if time_impact <= 0:
        return None

    opp_type = _classify(deltas, avg_speed_delta)
    apex_pct = deltas[0].apex_dist_pct

    # Gather telemetry evidence: reference vs. representative lap
    ref_telem, lap_telem = _gather_evidence(corner_id, comparisons)

    return Opportunity(
        corner_id=corner_id,
        apex_dist_pct=apex_pct,
        opportunity_type=opp_type,
        time_impact=round(time_impact, 3),
        speed_delta=round(avg_speed_delta, 2),
        ref_telemetry=ref_telem,
        lap_telemetry=lap_telem,
    )


def _classify(deltas: list[CornerDelta], avg_speed_delta: float) -> OpportunityType:
    """Classify the primary cause of the time loss at this corner."""
    avg_brake_delta = _mean_optional([d.brake_dist_delta for d in deltas])
    avg_throttle_delta = _mean_optional([d.throttle_dist_delta for d in deltas])

    if avg_speed_delta <= OVER_SLOWING_THRESHOLD:
        return OpportunityType.OVER_SLOWING

    if avg_brake_delta is not None and avg_brake_delta >= EARLY_BRAKE_DIST_THRESHOLD:
        return OpportunityType.EARLY_BRAKE

    if avg_throttle_delta is not None and avg_throttle_delta >= LATE_THROTTLE_DIST_THRESHOLD:
        return OpportunityType.LATE_THROTTLE

    return OpportunityType.GENERAL_CORNER


def _speed_delta_to_time_impact(speed_delta: float) -> float:
    """Convert an average corner speed deficit into an estimated lap time impact.

    Approximation: each 1 m/s of corner speed loss costs ~0.13 seconds per lap.
    This is a simplified model; a physics-based model would be more accurate but
    requires track geometry data not available in the MVP.
    """
    if speed_delta >= 0:
        return 0.0
    return abs(speed_delta) * 0.13


def _mean_optional(values: list[Optional[float]]) -> Optional[float]:
    valid = [v for v in values if v is not None]
    if not valid:
        return None
    return sum(valid) / len(valid)


def _gather_evidence(
    corner_id: int,
    comparisons: list[LapComparison],
) -> tuple[list[TelemetryPoint], list[TelemetryPoint]]:
    """Return reference and representative lap telemetry for a corner zone."""
    from driver_toolkit.analysis.metrics import compute_corner_metrics

    if not comparisons:
        return [], []

    ref_lap = comparisons[0].reference_lap
    ref_metrics = compute_corner_metrics(ref_lap)
    ref_corner = next((m for m in ref_metrics if m.corner_id == corner_id), None)
    ref_telem = ref_corner.points if ref_corner else []

    # Use the slowest comparison lap at this corner for the clearest evidence
    worst_comp = max(
        comparisons,
        key=lambda c: abs(
            next((d.speed_delta for d in c.corner_deltas if d.corner_id == corner_id), 0)
        ),
    )
    worst_lap_metrics = compute_corner_metrics(worst_comp.lap)
    worst_corner = next((m for m in worst_lap_metrics if m.corner_id == corner_id), None)
    lap_telem = worst_corner.points if worst_corner else []

    return ref_telem, lap_telem
