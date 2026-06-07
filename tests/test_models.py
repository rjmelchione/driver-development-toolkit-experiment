"""Tests for core data model types."""

import pytest

from driver_toolkit.models import TelemetryPoint, Lap, Session


class TestTelemetryPoint:
    def test_construction(self):
        pt = TelemetryPoint(
            session_time=1.0,
            lap_dist_pct=0.5,
            speed=50.0,
            throttle=0.8,
            brake=0.0,
            gear=4,
            rpm=5500.0,
            lap_current_lap_time=10.0,
        )
        assert pt.speed == 50.0
        assert pt.throttle == 0.8
        assert pt.gear == 4


class TestLap:
    def test_valid_complete_lap(self):
        points = [
            TelemetryPoint(0.0, 0.0, 50.0, 1.0, 0.0, 4, 5000.0, 0.0),
            TelemetryPoint(1.0, 0.5, 40.0, 0.0, 0.8, 3, 4000.0, 1.0),
        ]
        lap = Lap(lap_number=1, lap_time=28.0, is_valid=True, points=points)
        assert lap.is_complete
        assert lap.is_valid

    def test_incomplete_lap_no_points(self):
        lap = Lap(lap_number=1, lap_time=28.0, is_valid=True, points=[])
        assert not lap.is_complete

    def test_zero_lap_time_not_complete(self):
        lap = Lap(lap_number=1, lap_time=0.0, is_valid=True, points=[
            TelemetryPoint(0.0, 0.0, 50.0, 1.0, 0.0, 4, 5000.0, 0.0)
        ])
        assert not lap.is_complete

    def test_negative_lap_time_raises(self):
        with pytest.raises(ValueError):
            Lap(lap_number=1, lap_time=-1.0, is_valid=True, points=[])


class TestSession:
    def _make_session_with_laps(self) -> Session:
        points = [TelemetryPoint(0.0, float(i) / 10, 50.0, 1.0, 0.0, 4, 5000.0, float(i))
                  for i in range(10)]
        return Session(
            car="Late Model",
            track="Test Track",
            laps=[
                Lap(1, 28.5, True, points),
                Lap(2, 27.8, True, points),
                Lap(3, 29.1, True, points),
                Lap(4, 0.0, False, []),     # invalid
            ],
        )

    def test_valid_laps_excludes_invalid(self):
        session = self._make_session_with_laps()
        assert session.valid_lap_count == 3

    def test_best_lap_is_fastest(self):
        session = self._make_session_with_laps()
        assert session.best_lap.lap_time == 27.8

    def test_best_lap_none_when_no_valid_laps(self):
        session = Session(car="", track="", laps=[Lap(1, 0.0, False, [])])
        assert session.best_lap is None

    def test_lap_count_includes_all(self):
        session = self._make_session_with_laps()
        assert session.lap_count == 4
