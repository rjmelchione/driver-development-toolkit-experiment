"""Tests for lap comparison and session consistency."""

import pytest

from driver_toolkit.analysis.comparator import compare_to_reference, compute_session_consistency
from driver_toolkit.models import Session, Lap, TelemetryPoint


class TestCompareToReference:
    def test_raises_with_fewer_than_two_valid_laps(self, synthetic_session):
        one_lap_session = Session(
            car="Test",
            track="Test",
            laps=[synthetic_session.valid_laps[0]],
        )
        with pytest.raises(ValueError, match="2 valid laps"):
            compare_to_reference(one_lap_session)

    def test_returns_reference_and_comparisons(self, synthetic_session):
        ref, comparisons = compare_to_reference(synthetic_session)
        assert ref is not None
        assert len(comparisons) > 0

    def test_reference_is_best_lap(self, synthetic_session):
        ref, _ = compare_to_reference(synthetic_session)
        assert ref.lap_time == synthetic_session.best_lap.lap_time

    def test_comparisons_exclude_reference_lap(self, synthetic_session):
        ref, comparisons = compare_to_reference(synthetic_session)
        for comp in comparisons:
            assert comp.lap is not ref

    def test_corner_deltas_populated(self, synthetic_session):
        _, comparisons = compare_to_reference(synthetic_session)
        for comp in comparisons:
            assert len(comp.corner_deltas) > 0


class TestSessionConsistency:
    def test_returns_consistency_for_valid_session(self, synthetic_session):
        consistency = compute_session_consistency(synthetic_session)
        assert consistency.best_lap_time > 0
        assert 0.0 <= consistency.consistency_score <= 100.0

    def test_empty_session_returns_zeros(self):
        empty = Session(car="", track="", laps=[])
        consistency = compute_session_consistency(empty)
        assert consistency.best_lap_time == 0.0
        assert consistency.consistency_score == 0.0

    def test_single_valid_lap_has_zero_std(self):
        points = [TelemetryPoint(float(i), float(i) / 100, 50.0, 1.0, 0.0, 4, 5000.0, float(i))
                  for i in range(100)]
        session = Session(
            car="", track="",
            laps=[Lap(1, 28.0, True, points)]
        )
        consistency = compute_session_consistency(session)
        assert consistency.std_dev == 0.0
