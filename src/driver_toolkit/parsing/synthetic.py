"""Synthetic telemetry session generator for testing and demonstration.

Generates a realistic iRacing-style session without requiring a real .ibt file.

Assumptions documented in docs/Requirements.md (A-002):
- Synthetic data uses the same channel names and value ranges as real .ibt files
- Corner positions and telemetry profiles are modeled on a generic 4-corner oval
- The generator produces known imperfections at specified corners to enable
  precise assertions in tests

Track model: simplified 4-corner oval
  Corner 1: LapDistPct 0.10–0.20 (turn 1-2)
  Corner 2: LapDistPct 0.35–0.45 (turn 3-4)
  Corner 3: LapDistPct 0.60–0.70 (turn 5-6, back stretch)
  Corner 4: LapDistPct 0.80–0.90 (turn 7-8)
"""

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np

from driver_toolkit.models import Session, Lap, TelemetryPoint

TICKS_PER_SECOND = 60
BASE_LAP_TIME = 28.0  # seconds — representative of a short oval lap

# Corner definitions: (center_dist_pct, entry_dist_pct, exit_dist_pct)
CORNERS = [
    {"id": 1, "center": 0.15, "entry": 0.10, "exit": 0.20},
    {"id": 2, "center": 0.40, "entry": 0.35, "exit": 0.45},
    {"id": 3, "center": 0.65, "entry": 0.60, "exit": 0.70},
    {"id": 4, "center": 0.85, "entry": 0.80, "exit": 0.90},
]

# Speed profile parameters (m/s)
STRAIGHT_SPEED = 55.0   # ~198 km/h, typical for a late model on a short oval
CORNER_SPEED = 38.0     # base min speed through corners (~136 km/h)


@dataclass
class LapImperfection:
    """Describes a deliberate performance deficit planted in a lap at a specific corner."""

    corner_id: int
    type: str           # "over_slowing" | "late_throttle" | "early_brake"
    magnitude: float    # fractional deficit; 0.1 = 10% worse than reference


def generate_synthetic_session(
    num_laps: int = 10,
    car: str = "Late Model Stock",
    track: str = "Bristol Motor Speedway [Synthetic]",
    seed: int = 42,
) -> Session:
    """Generate a synthetic session with realistic coaching opportunities.

    The first valid lap is the reference (best) lap. Subsequent laps contain
    deliberate imperfections at specific corners so that the analysis layer can
    detect and rank them correctly.

    Returns a Session that passes through the full analysis pipeline identically
    to a session loaded from a real .ibt file.
    """
    rng = np.random.default_rng(seed)

    imperfections_by_lap: dict[int, list[LapImperfection]] = {
        2: [LapImperfection(corner_id=1, type="over_slowing", magnitude=0.12)],
        3: [
            LapImperfection(corner_id=1, type="over_slowing", magnitude=0.08),
            LapImperfection(corner_id=3, type="late_throttle", magnitude=0.10),
        ],
        4: [LapImperfection(corner_id=2, type="early_brake", magnitude=0.09)],
        5: [
            LapImperfection(corner_id=1, type="over_slowing", magnitude=0.15),
            LapImperfection(corner_id=3, type="late_throttle", magnitude=0.12),
        ],
        6: [LapImperfection(corner_id=4, type="over_slowing", magnitude=0.07)],
        7: [LapImperfection(corner_id=2, type="early_brake", magnitude=0.11)],
        8: [
            LapImperfection(corner_id=1, type="over_slowing", magnitude=0.10),
            LapImperfection(corner_id=2, type="early_brake", magnitude=0.08),
        ],
        9: [LapImperfection(corner_id=3, type="late_throttle", magnitude=0.14)],
        10: [LapImperfection(corner_id=4, type="over_slowing", magnitude=0.06)],
    }

    session = Session(car=car, track=track, source_file=None)
    session_time = 0.0

    for lap_num in range(1, num_laps + 1):
        imperfections = imperfections_by_lap.get(lap_num, [])
        lap_time_offset = _estimate_lap_time_offset(imperfections)
        lap_time = BASE_LAP_TIME + lap_time_offset + rng.uniform(-0.05, 0.05)

        points = _generate_lap_points(
            lap_number=lap_num,
            lap_time=lap_time,
            imperfections=imperfections,
            session_time_offset=session_time,
            rng=rng,
        )

        lap = Lap(
            lap_number=lap_num,
            lap_time=round(lap_time, 3),
            is_valid=True,
            points=points,
        )
        session.laps.append(lap)
        session_time += lap_time

    return session


def _estimate_lap_time_offset(imperfections: list[LapImperfection]) -> float:
    """Approximate additional lap time caused by the given imperfections."""
    total = 0.0
    for imp in imperfections:
        if imp.type == "over_slowing":
            total += imp.magnitude * 1.5
        elif imp.type == "late_throttle":
            total += imp.magnitude * 1.2
        elif imp.type == "early_brake":
            total += imp.magnitude * 0.9
    return total


def _generate_lap_points(
    lap_number: int,
    lap_time: float,
    imperfections: list[LapImperfection],
    session_time_offset: float,
    rng: np.random.Generator,
) -> list[TelemetryPoint]:
    """Generate the tick-by-tick telemetry for one lap."""
    imperfection_map = {imp.corner_id: imp for imp in imperfections}
    total_ticks = max(1, int(lap_time * TICKS_PER_SECOND))
    points = []

    for tick in range(total_ticks):
        dist_pct = tick / total_ticks
        elapsed = tick / TICKS_PER_SECOND
        session_time = session_time_offset + elapsed

        speed, throttle, brake, gear, rpm = _compute_controls(
            dist_pct=dist_pct,
            imperfection_map=imperfection_map,
            rng=rng,
        )

        points.append(TelemetryPoint(
            session_time=round(session_time, 4),
            lap_dist_pct=round(dist_pct, 4),
            speed=round(speed, 2),
            throttle=round(max(0.0, min(1.0, throttle)), 3),
            brake=round(max(0.0, min(1.0, brake)), 3),
            gear=gear,
            rpm=round(rpm, 0),
            lap_current_lap_time=round(elapsed, 4),
        ))

    return points


def _compute_controls(
    dist_pct: float,
    imperfection_map: dict[int, LapImperfection],
    rng: np.random.Generator,
) -> tuple[float, float, float, int, float]:
    """Compute speed, throttle, brake, gear, rpm for a given track position."""
    corner_factor, corner_id = _corner_influence(dist_pct)
    imperfection = imperfection_map.get(corner_id) if corner_id else None

    base_min_speed = CORNER_SPEED
    if imperfection and imperfection.type == "over_slowing":
        base_min_speed *= (1.0 - imperfection.magnitude)

    speed = STRAIGHT_SPEED - (STRAIGHT_SPEED - base_min_speed) * corner_factor
    speed += rng.normal(0, 0.3)

    in_braking_zone = _in_braking_zone(dist_pct, corner_id, imperfection)
    in_throttle_zone = _in_throttle_zone(dist_pct, corner_id, imperfection)
    at_apex = corner_factor > 0.85 and corner_id is not None

    if in_braking_zone:
        throttle = 0.0
        brake = min(1.0, corner_factor * 0.8 + rng.uniform(0, 0.1))
        gear = 3
    elif at_apex:
        throttle = 0.0
        brake = 0.0
        gear = 3
    elif in_throttle_zone:
        throttle = min(1.0, (1.0 - corner_factor) * 1.2 + rng.uniform(0, 0.05))
        brake = 0.0
        gear = 4
    else:
        throttle = min(1.0, 0.95 + rng.uniform(-0.03, 0.03))
        brake = 0.0
        gear = 5

    rpm = 3000 + speed * 70 + rng.normal(0, 50)

    return speed, throttle, brake, gear, max(500.0, rpm)


def _corner_influence(dist_pct: float) -> tuple[float, Optional[int]]:
    """Return (influence 0-1, corner_id) for the given track position.

    Influence is 1.0 at the apex and 0.0 on the straights.
    """
    best_influence = 0.0
    best_corner_id = None

    for corner in CORNERS:
        half_width = (corner["exit"] - corner["entry"]) / 2
        center = corner["center"]
        dist = abs(dist_pct - center)
        if dist <= half_width:
            influence = math.cos(math.pi * dist / half_width) * 0.5 + 0.5
            if influence > best_influence:
                best_influence = influence
                best_corner_id = corner["id"]

    return best_influence, best_corner_id


def _in_braking_zone(
    dist_pct: float,
    corner_id: Optional[int],
    imperfection: Optional[LapImperfection],
) -> bool:
    if corner_id is None:
        return False
    corner = next(c for c in CORNERS if c["id"] == corner_id)
    brake_start = corner["entry"] - 0.04
    brake_end = corner["center"] - 0.01

    if imperfection and imperfection.type == "early_brake":
        brake_start -= 0.015

    return brake_start <= dist_pct < brake_end


def _in_throttle_zone(
    dist_pct: float,
    corner_id: Optional[int],
    imperfection: Optional[LapImperfection],
) -> bool:
    if corner_id is None:
        return False
    corner = next(c for c in CORNERS if c["id"] == corner_id)
    throttle_start = corner["center"] + 0.01

    if imperfection and imperfection.type == "late_throttle":
        throttle_start += 0.02

    throttle_end = corner["exit"] + 0.01
    return throttle_start <= dist_pct < throttle_end
