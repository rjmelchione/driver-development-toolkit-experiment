"""Per-lap, per-corner performance metrics.

Computes the telemetry characteristics of each corner in a lap.
Corner detection uses local speed minima — see docs/Decision_Log.md DEC-006.
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np

from driver_toolkit.models import Lap, TelemetryPoint

# Tunable corner detection parameters (see DEC-006)
MIN_CORNER_SEPARATION = 0.08   # minimum LapDistPct gap between adjacent corners
MIN_SPEED_DROP = 5.0           # m/s below mean speed to qualify as a corner
SMOOTHING_WINDOW = 5           # ticks for speed smoothing before minima detection


@dataclass
class CornerMetrics:
    """Performance metrics for a single corner in a single lap."""

    corner_id: int              # sequential corner number (1-based)
    apex_dist_pct: float        # LapDistPct at the speed minimum
    min_speed: float            # m/s at the speed minimum
    brake_dist_pct: Optional[float]     # LapDistPct where brake > 0.1 before apex
    throttle_dist_pct: Optional[float]  # LapDistPct where throttle > 0.5 after apex
    zone_entry_dist_pct: float  # LapDistPct start of corner zone (for evidence chart)
    zone_exit_dist_pct: float   # LapDistPct end of corner zone (for evidence chart)
    points: list[TelemetryPoint]  # telemetry points within the zone


def compute_corner_metrics(lap: Lap) -> list[CornerMetrics]:
    """Detect corners and compute per-corner metrics for a lap.

    Args:
        lap: A Lap object with at least SMOOTHING_WINDOW telemetry points.

    Returns:
        List of CornerMetrics, one per detected corner, in track order.
        Returns empty list if fewer than 3 corners are detected.
    """
    if len(lap.points) < SMOOTHING_WINDOW * 2:
        return []

    dist_pcts = np.array([pt.lap_dist_pct for pt in lap.points])
    speeds = np.array([pt.speed for pt in lap.points])
    smoothed = _smooth(speeds, SMOOTHING_WINDOW)

    apex_indices = _find_local_minima(
        dist_pcts=dist_pcts,
        speeds=smoothed,
        min_separation=MIN_CORNER_SEPARATION,
        min_speed_drop=MIN_SPEED_DROP,
        mean_speed=float(np.mean(smoothed)),
    )

    metrics = []
    for corner_id, apex_idx in enumerate(apex_indices, start=1):
        zone_entry, zone_exit = _find_zone_bounds(
            apex_idx=apex_idx,
            dist_pcts=dist_pcts,
            min_sep=MIN_CORNER_SEPARATION / 2,
        )
        zone_points = lap.points[zone_entry:zone_exit + 1]

        brake_pct = _find_brake_point(zone_points, apex_idx - zone_entry)
        throttle_pct = _find_throttle_point(zone_points, apex_idx - zone_entry)

        metrics.append(CornerMetrics(
            corner_id=corner_id,
            apex_dist_pct=round(float(dist_pcts[apex_idx]), 4),
            min_speed=round(float(speeds[apex_idx]), 2),
            brake_dist_pct=brake_pct,
            throttle_dist_pct=throttle_pct,
            zone_entry_dist_pct=round(float(dist_pcts[zone_entry]), 4),
            zone_exit_dist_pct=round(float(dist_pcts[zone_exit]), 4),
            points=zone_points,
        ))

    return metrics


def _smooth(values: np.ndarray, window: int) -> np.ndarray:
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode="same")


def _find_local_minima(
    dist_pcts: np.ndarray,
    speeds: np.ndarray,
    min_separation: float,
    min_speed_drop: float,
    mean_speed: float,
) -> list[int]:
    """Find indices of speed minima that qualify as corners."""
    n = len(speeds)
    candidates = []

    for i in range(1, n - 1):
        if speeds[i] < speeds[i - 1] and speeds[i] < speeds[i + 1]:
            if (mean_speed - speeds[i]) >= min_speed_drop:
                candidates.append(i)

    return _filter_by_separation(candidates, dist_pcts, speeds, min_separation)


def _filter_by_separation(
    candidates: list[int],
    dist_pcts: np.ndarray,
    speeds: np.ndarray,
    min_sep: float,
) -> list[int]:
    """When two candidates are too close, keep the one with the lower speed."""
    if not candidates:
        return []

    filtered = [candidates[0]]
    for idx in candidates[1:]:
        prev = filtered[-1]
        if (dist_pcts[idx] - dist_pcts[prev]) < min_sep:
            if speeds[idx] < speeds[prev]:
                filtered[-1] = idx
        else:
            filtered.append(idx)

    return filtered


def _find_zone_bounds(
    apex_idx: int,
    dist_pcts: np.ndarray,
    min_sep: float,
) -> tuple[int, int]:
    """Return (entry_index, exit_index) for the corner zone around an apex."""
    apex_pct = dist_pcts[apex_idx]
    entry = apex_idx
    while entry > 0 and (apex_pct - dist_pcts[entry]) < min_sep:
        entry -= 1

    exit_ = apex_idx
    while exit_ < len(dist_pcts) - 1 and (dist_pcts[exit_] - apex_pct) < min_sep:
        exit_ += 1

    return entry, exit_


def _find_brake_point(
    points: list[TelemetryPoint],
    apex_local_idx: int,
    brake_threshold: float = 0.1,
) -> Optional[float]:
    """Return LapDistPct where braking begins before the apex."""
    for pt in points[:apex_local_idx]:
        if pt.brake >= brake_threshold:
            return round(pt.lap_dist_pct, 4)
    return None


def _find_throttle_point(
    points: list[TelemetryPoint],
    apex_local_idx: int,
    throttle_threshold: float = 0.5,
) -> Optional[float]:
    """Return LapDistPct where meaningful throttle application begins after the apex."""
    for pt in points[apex_local_idx:]:
        if pt.throttle >= throttle_threshold:
            return round(pt.lap_dist_pct, 4)
    return None
