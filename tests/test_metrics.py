"""Tests for corner detection and per-corner metrics computation."""

import math
import pytest
import numpy as np

from driver_toolkit.analysis.metrics import compute_corner_metrics
from driver_toolkit.models import Lap, TelemetryPoint


def _make_lap_with_corners(num_corners: int = 4, ticks: int = 600) -> Lap:
    """Build a lap with evenly spaced speed minima representing corners."""
    points = []
    for i in range(ticks):
        pct = i / ticks
        # Create sinusoidal speed minima at evenly-spaced positions
        speed = 55.0
        for c in range(num_corners):
            corner_center = (c + 0.5) / num_corners
            dist = abs(pct - corner_center)
            if dist < 0.1:
                speed -= 20.0 * math.cos(math.pi * dist / 0.1) * 0.5 + 10.0

        speed = max(25.0, speed)
        in_brake = any(
            abs(pct - (c + 0.5) / num_corners) < 0.08
            and pct < (c + 0.5) / num_corners
            for c in range(num_corners)
        )
        in_throttle = any(
            abs(pct - (c + 0.5) / num_corners) < 0.08
            and pct > (c + 0.5) / num_corners
            for c in range(num_corners)
        )

        points.append(TelemetryPoint(
            session_time=i / 60.0,
            lap_dist_pct=round(pct, 4),
            speed=round(speed, 2),
            throttle=0.9 if in_throttle else 0.0,
            brake=0.8 if in_brake else 0.0,
            gear=4,
            rpm=5000.0,
            lap_current_lap_time=i / 60.0,
        ))

    return Lap(lap_number=1, lap_time=10.0, is_valid=True, points=points)


class TestComputeCornerMetrics:
    def test_detects_corners(self):
        lap = _make_lap_with_corners(num_corners=4, ticks=600)
        metrics = compute_corner_metrics(lap)
        # Should detect at least 2 corners (noise tolerance)
        assert len(metrics) >= 2

    def test_corner_ids_are_sequential(self):
        lap = _make_lap_with_corners(num_corners=4, ticks=600)
        metrics = compute_corner_metrics(lap)
        for i, m in enumerate(metrics, start=1):
            assert m.corner_id == i

    def test_apex_dist_pct_in_range(self):
        lap = _make_lap_with_corners(ticks=600)
        metrics = compute_corner_metrics(lap)
        for m in metrics:
            assert 0.0 <= m.apex_dist_pct <= 1.0

    def test_min_speed_is_positive(self):
        lap = _make_lap_with_corners(ticks=600)
        metrics = compute_corner_metrics(lap)
        for m in metrics:
            assert m.min_speed > 0

    def test_zone_bounds_bracket_apex(self):
        lap = _make_lap_with_corners(ticks=600)
        metrics = compute_corner_metrics(lap)
        for m in metrics:
            assert m.zone_entry_dist_pct <= m.apex_dist_pct
            assert m.apex_dist_pct <= m.zone_exit_dist_pct

    def test_too_few_points_returns_empty(self):
        tiny_lap = Lap(
            lap_number=1, lap_time=1.0, is_valid=True,
            points=[TelemetryPoint(0.0, float(i) / 20, 50.0, 1.0, 0.0, 4, 5000.0, 0.0)
                    for i in range(8)]
        )
        assert compute_corner_metrics(tiny_lap) == []

    def test_synthetic_session_corners(self, synthetic_session):
        """Corner detection works on the actual synthetic session data."""
        best = synthetic_session.best_lap
        metrics = compute_corner_metrics(best)
        assert len(metrics) >= 2, "Expected at least 2 corners in synthetic session"
