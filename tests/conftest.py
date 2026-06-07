"""Shared pytest fixtures."""

import pytest

from driver_toolkit.models import Session, Lap, TelemetryPoint
from driver_toolkit.parsing.synthetic import generate_synthetic_session


@pytest.fixture(scope="session")
def synthetic_session() -> Session:
    """A full 10-lap synthetic session with planted coaching opportunities."""
    return generate_synthetic_session(num_laps=10, seed=42)


@pytest.fixture
def minimal_lap() -> Lap:
    """A minimal valid lap with a simple sinusoidal speed profile."""
    points = [
        TelemetryPoint(
            session_time=float(i) / 60,
            lap_dist_pct=i / 100,
            speed=50.0 - 20.0 * abs(0.5 - (i / 100)) * 2,  # simple V-shape
            throttle=1.0 if i > 60 else 0.0,
            brake=1.0 if i < 40 else 0.0,
            gear=4,
            rpm=5000.0,
            lap_current_lap_time=float(i) / 60,
        )
        for i in range(100)
    ]
    return Lap(lap_number=1, lap_time=1.667, is_valid=True, points=points)
