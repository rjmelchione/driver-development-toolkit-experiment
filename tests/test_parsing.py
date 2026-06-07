"""Tests for the synthetic session generator and lap segmenter."""

import pytest

from driver_toolkit.parsing.synthetic import generate_synthetic_session, CORNERS
from driver_toolkit.parsing.lap_segmenter import segment_laps
from driver_toolkit.models import TelemetryPoint


class TestSyntheticGenerator:
    def test_returns_session(self, synthetic_session):
        from driver_toolkit.models import Session
        assert isinstance(synthetic_session, Session)

    def test_correct_lap_count(self, synthetic_session):
        assert synthetic_session.lap_count == 10

    def test_all_laps_valid(self, synthetic_session):
        assert synthetic_session.valid_lap_count == 10

    def test_laps_have_points(self, synthetic_session):
        for lap in synthetic_session.valid_laps:
            assert len(lap.points) > 0, f"Lap {lap.lap_number} has no points"

    def test_best_lap_is_first_lap(self, synthetic_session):
        # Lap 1 has no imperfections; it should be the fastest
        best = synthetic_session.best_lap
        assert best.lap_number == 1

    def test_lap_times_are_positive(self, synthetic_session):
        for lap in synthetic_session.laps:
            assert lap.lap_time > 0

    def test_telemetry_channels_in_range(self, synthetic_session):
        for lap in synthetic_session.valid_laps:
            for pt in lap.points:
                assert 0.0 <= pt.throttle <= 1.0, f"Throttle out of range: {pt.throttle}"
                assert 0.0 <= pt.brake <= 1.0, f"Brake out of range: {pt.brake}"
                assert 0.0 <= pt.lap_dist_pct <= 1.0, f"LapDistPct out of range: {pt.lap_dist_pct}"
                assert pt.speed >= 0.0, f"Speed negative: {pt.speed}"
                assert pt.rpm >= 0.0, f"RPM negative: {pt.rpm}"

    def test_deterministic_with_same_seed(self):
        s1 = generate_synthetic_session(seed=99)
        s2 = generate_synthetic_session(seed=99)
        assert s1.best_lap.lap_time == s2.best_lap.lap_time

    def test_different_seeds_produce_different_times(self):
        s1 = generate_synthetic_session(seed=1)
        s2 = generate_synthetic_session(seed=2)
        assert s1.best_lap.lap_time != s2.best_lap.lap_time


class TestLapSegmenter:
    def _make_flat_points(self, num_laps: int = 2) -> list[TelemetryPoint]:
        """Build a flat tick stream simulating multiple laps."""
        points = []
        session_t = 0.0
        lap_duration = 28.0
        ticks_per_lap = int(lap_duration * 60)

        for lap in range(num_laps):
            for tick in range(ticks_per_lap):
                t = tick / 60.0
                points.append(TelemetryPoint(
                    session_time=session_t + t,
                    lap_dist_pct=t / lap_duration,
                    speed=50.0,
                    throttle=1.0,
                    brake=0.0,
                    gear=4,
                    rpm=5000.0,
                    lap_current_lap_time=t,
                ))
            session_t += lap_duration

        return points

    def test_segment_produces_laps(self):
        points = self._make_flat_points(num_laps=3)
        laps = segment_laps(points)
        assert len(laps) >= 2  # first/last may be boundary fragments

    def test_empty_input_returns_empty(self):
        assert segment_laps([]) == []
