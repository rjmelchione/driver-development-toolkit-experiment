"""Core data model for a telemetry session.

These types are the contract between all layers of the system. No layer
imports from another layer's internals — they exchange only these types.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TelemetryPoint:
    """A single telemetry sample (tick) recorded during a lap.

    All fields use the same units as iRacing's .ibt format.
    LapDistPct is 0.0 at the start/finish line and 1.0 at lap completion.
    """

    session_time: float       # seconds since session start
    lap_dist_pct: float       # 0.0–1.0 position through lap
    speed: float              # m/s
    throttle: float           # 0.0–1.0
    brake: float              # 0.0–1.0
    gear: int                 # 0=reverse, 1–6=forward gears
    rpm: float
    lap_current_lap_time: float  # elapsed seconds in current lap


@dataclass
class Lap:
    """One complete lap recorded during a session.

    A lap is considered valid if it was completed normally (no safety car,
    no pit stop, no off-track incident that reset LapDistPct abnormally).
    Invalid laps are retained in the session but excluded from analysis.
    """

    lap_number: int
    lap_time: float                          # seconds; 0.0 if lap not completed
    is_valid: bool                           # True if usable for analysis
    points: list[TelemetryPoint] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.lap_time < 0:
            raise ValueError(f"lap_time cannot be negative: {self.lap_time}")

    @property
    def is_complete(self) -> bool:
        return self.lap_time > 0 and len(self.points) > 0


@dataclass
class Session:
    """A full iRacing telemetry session, containing one or more laps.

    car and track are strings as reported by iRacing (e.g. "Late Model Stock",
    "Bristol Motor Speedway"). They may be empty for synthetic sessions.
    """

    car: str
    track: str
    laps: list[Lap] = field(default_factory=list)
    source_file: Optional[str] = None  # path to the .ibt file, if loaded from one

    @property
    def valid_laps(self) -> list[Lap]:
        return [lap for lap in self.laps if lap.is_valid and lap.is_complete]

    @property
    def best_lap(self) -> Optional[Lap]:
        valid = self.valid_laps
        if not valid:
            return None
        return min(valid, key=lambda lap: lap.lap_time)

    @property
    def lap_count(self) -> int:
        return len(self.laps)

    @property
    def valid_lap_count(self) -> int:
        return len(self.valid_laps)
