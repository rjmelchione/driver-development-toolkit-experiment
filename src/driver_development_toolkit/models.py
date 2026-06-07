"""Core domain models for telemetry-backed coaching."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class OpportunityKind(str, Enum):
    """Supported MVP opportunity categories."""

    CORNER_ENTRY = "corner_entry"
    BRAKE_RELEASE = "brake_release"
    THROTTLE_APPLICATION = "throttle_application"
    CONSISTENCY = "consistency"


@dataclass(frozen=True)
class TelemetrySample:
    """One normalized telemetry point within a lap."""

    distance_pct: float
    speed_mph: float
    throttle_pct: float
    brake_pct: float
    steering_deg: float = 0.0


@dataclass(frozen=True)
class Lap:
    """A completed lap with normalized telemetry samples."""

    number: int
    lap_time_s: float
    samples: tuple[TelemetrySample, ...]
    valid: bool = True


@dataclass(frozen=True)
class TelemetrySession:
    """Telemetry session prepared for analysis."""

    source: str
    car: str
    track: str
    laps: tuple[Lap, ...]


@dataclass(frozen=True)
class TrackSegment:
    """Comparable portion of a lap."""

    name: str
    start_pct: float
    end_pct: float


@dataclass(frozen=True)
class TelemetryEvidence:
    """A supporting observation for a coaching recommendation."""

    metric: str
    observed: str
    interpretation: str


@dataclass(frozen=True)
class Opportunity:
    """A ranked coaching opportunity derived from telemetry."""

    segment: TrackSegment
    kind: OpportunityKind
    impact_s: float
    cause: str
    recommendation: str
    practice: str
    evidence: tuple[TelemetryEvidence, ...]
    comparison_lap: Optional[int] = None
    reference_lap: Optional[int] = None
