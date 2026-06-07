"""Converts a flat telemetry tick stream into structured Lap objects.

This module exists to provide a reusable segmentation function for both
the .ibt file reader and the synthetic generator. Real .ibt files emit
telemetry as a continuous stream; lap boundaries are identified by
watching LapCurrentLapTime reset near zero.
"""

from driver_toolkit.models import Lap, TelemetryPoint

LAP_TIME_RESET_THRESHOLD = 0.5  # seconds; LapCurrentLapTime below this = new lap


def segment_laps(
    points: list[TelemetryPoint],
    min_lap_time: float = 10.0,
    min_points_per_lap: int = 100,
) -> list[Lap]:
    """Split a flat list of TelemetryPoints into per-lap Lap objects.

    A new lap starts when LapCurrentLapTime resets to near zero after having
    been above LAP_TIME_RESET_THRESHOLD.

    Args:
        points: Chronologically ordered telemetry ticks from a session.
        min_lap_time: Laps shorter than this (seconds) are marked invalid.
            Catches partial laps at session start/end and pit entry/exit.
        min_points_per_lap: Laps with fewer points are marked invalid.

    Returns:
        List of Lap objects. First and last laps may be invalid (out-lap,
        in-lap). All laps are included; filtering is the caller's responsibility.
    """
    if not points:
        return []

    lap_boundaries = _find_lap_boundaries(points)

    laps = []
    for lap_idx, (start, end) in enumerate(lap_boundaries):
        lap_points = points[start:end]
        if not lap_points:
            continue

        lap_time = lap_points[-1].lap_current_lap_time
        is_valid = (
            lap_time >= min_lap_time
            and len(lap_points) >= min_points_per_lap
        )

        laps.append(Lap(
            lap_number=lap_idx + 1,
            lap_time=round(lap_time, 3),
            is_valid=is_valid,
            points=lap_points,
        ))

    return laps


def _find_lap_boundaries(points: list[TelemetryPoint]) -> list[tuple[int, int]]:
    """Return (start_index, end_index) pairs for each lap in the point stream."""
    boundaries = []
    lap_start = 0
    in_lap = False

    for i, pt in enumerate(points):
        if pt.lap_current_lap_time > LAP_TIME_RESET_THRESHOLD:
            in_lap = True
        elif in_lap and pt.lap_current_lap_time < LAP_TIME_RESET_THRESHOLD:
            boundaries.append((lap_start, i))
            lap_start = i
            in_lap = False

    if lap_start < len(points):
        boundaries.append((lap_start, len(points)))

    return boundaries
