"""Lap comparison — computes per-corner time deltas vs. a reference lap.

The reference lap is the driver's best valid lap (see docs/Decision_Log.md DEC-004).
A future enhancement can accept an external reference lap without changing this interface.
"""

from dataclasses import dataclass
from typing import Optional
import statistics

from driver_toolkit.models import Lap, Session
from driver_toolkit.analysis.metrics import CornerMetrics, compute_corner_metrics


@dataclass
class CornerDelta:
    """Performance difference at a single corner between a lap and the reference."""

    corner_id: int
    apex_dist_pct: float

    # Reference (best lap) metrics
    ref_min_speed: float
    ref_brake_dist_pct: Optional[float]
    ref_throttle_dist_pct: Optional[float]

    # This lap's metrics
    lap_min_speed: float
    lap_brake_dist_pct: Optional[float]
    lap_throttle_dist_pct: Optional[float]

    # Derived differences
    speed_delta: float            # lap_min_speed - ref_min_speed (negative = slower)
    brake_dist_delta: Optional[float]   # positive = braking earlier than reference
    throttle_dist_delta: Optional[float]  # positive = throttle later than reference

    @property
    def is_slower_corner(self) -> bool:
        return self.speed_delta < 0


@dataclass
class LapComparison:
    """Comparison of a single lap against the reference lap, per corner."""

    lap: Lap
    reference_lap: Lap
    corner_deltas: list[CornerDelta]

    @property
    def total_speed_loss(self) -> float:
        return sum(min(0.0, d.speed_delta) for d in self.corner_deltas)


@dataclass
class SessionConsistency:
    """Lap-time consistency metrics for a session."""

    best_lap_time: float
    average_lap_time: float
    std_dev: float
    consistency_score: float   # 0–100; higher = more consistent
    lap_times: list[float]


def compare_to_reference(session: Session) -> tuple[Lap, list[LapComparison]]:
    """Compare all valid laps in a session against the best lap.

    Args:
        session: A Session with at least 2 valid laps.

    Returns:
        Tuple of (reference_lap, list_of_LapComparison).

    Raises:
        ValueError: If the session has fewer than 2 valid laps.
    """
    valid = session.valid_laps
    if len(valid) < 2:
        raise ValueError(
            f"Session needs at least 2 valid laps for comparison; got {len(valid)}"
        )

    reference = session.best_lap  # guaranteed non-None given len(valid) >= 2
    ref_metrics = compute_corner_metrics(reference)

    if not ref_metrics:
        raise ValueError("Could not detect any corners in the reference lap.")

    comparisons = []
    for lap in valid:
        if lap is reference:
            continue
        lap_metrics = compute_corner_metrics(lap)
        deltas = _compute_deltas(ref_metrics, lap_metrics)
        comparisons.append(LapComparison(
            lap=lap,
            reference_lap=reference,
            corner_deltas=deltas,
        ))

    return reference, comparisons


def compute_session_consistency(session: Session) -> SessionConsistency:
    """Compute lap-time consistency metrics for the session."""
    valid = session.valid_laps
    if not valid:
        return SessionConsistency(
            best_lap_time=0.0,
            average_lap_time=0.0,
            std_dev=0.0,
            consistency_score=0.0,
            lap_times=[],
        )

    times = [lap.lap_time for lap in valid]
    best = min(times)
    avg = statistics.mean(times)
    std = statistics.stdev(times) if len(times) > 1 else 0.0

    # Consistency score: 100 = perfect (0 std dev), drops as variation increases
    # A std dev of 1.0s on a 28s lap (3.6%) gives ~64/100
    pct_variation = (std / best) * 100 if best > 0 else 0.0
    score = max(0.0, 100.0 - pct_variation * 10)

    return SessionConsistency(
        best_lap_time=round(best, 3),
        average_lap_time=round(avg, 3),
        std_dev=round(std, 3),
        consistency_score=round(score, 1),
        lap_times=[round(t, 3) for t in times],
    )


def _compute_deltas(
    ref_metrics: list[CornerMetrics],
    lap_metrics: list[CornerMetrics],
) -> list[CornerDelta]:
    """Match corners between two laps by proximity and compute deltas."""
    deltas = []
    for ref_corner in ref_metrics:
        lap_corner = _find_matching_corner(ref_corner.apex_dist_pct, lap_metrics)
        if lap_corner is None:
            continue

        brake_delta = None
        if ref_corner.brake_dist_pct is not None and lap_corner.brake_dist_pct is not None:
            brake_delta = round(ref_corner.brake_dist_pct - lap_corner.brake_dist_pct, 4)

        throttle_delta = None
        if ref_corner.throttle_dist_pct is not None and lap_corner.throttle_dist_pct is not None:
            throttle_delta = round(lap_corner.throttle_dist_pct - ref_corner.throttle_dist_pct, 4)

        deltas.append(CornerDelta(
            corner_id=ref_corner.corner_id,
            apex_dist_pct=ref_corner.apex_dist_pct,
            ref_min_speed=ref_corner.min_speed,
            ref_brake_dist_pct=ref_corner.brake_dist_pct,
            ref_throttle_dist_pct=ref_corner.throttle_dist_pct,
            lap_min_speed=lap_corner.min_speed,
            lap_brake_dist_pct=lap_corner.brake_dist_pct,
            lap_throttle_dist_pct=lap_corner.throttle_dist_pct,
            speed_delta=round(lap_corner.min_speed - ref_corner.min_speed, 2),
            brake_dist_delta=brake_delta,
            throttle_dist_delta=throttle_delta,
        ))

    return deltas


def _find_matching_corner(
    target_pct: float,
    candidates: list[CornerMetrics],
    max_distance: float = 0.05,
) -> Optional[CornerMetrics]:
    """Find the corner in candidates closest to target_pct."""
    best = None
    best_dist = float("inf")
    for corner in candidates:
        dist = abs(corner.apex_dist_pct - target_pct)
        if dist < best_dist and dist <= max_distance:
            best_dist = dist
            best = corner
    return best
