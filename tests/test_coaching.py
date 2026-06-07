"""Tests for the coaching rules layer."""

import pytest

from driver_toolkit.analysis.comparator import compare_to_reference
from driver_toolkit.analysis.opportunity_detector import detect_opportunities, OpportunityType
from driver_toolkit.coaching.rules import get_coaching, CoachingResult


class TestGetCoaching:
    def _get_results(self, synthetic_session):
        _, comparisons = compare_to_reference(synthetic_session)
        opps = detect_opportunities(comparisons)
        return [get_coaching(opp) for opp in opps]

    def test_returns_coaching_result(self, synthetic_session):
        results = self._get_results(synthetic_session)
        assert len(results) > 0
        for r in results:
            assert isinstance(r, CoachingResult)

    def test_cause_is_non_empty(self, synthetic_session):
        results = self._get_results(synthetic_session)
        for r in results:
            assert len(r.cause) > 10, f"Cause too short for {r.corner_label}"

    def test_recommendation_is_non_empty(self, synthetic_session):
        results = self._get_results(synthetic_session)
        for r in results:
            assert len(r.recommendation) > 10

    def test_drill_is_non_empty(self, synthetic_session):
        results = self._get_results(synthetic_session)
        for r in results:
            assert len(r.drill) > 10

    def test_all_opportunity_types_have_rules(self, synthetic_session):
        """Every OpportunityType must produce a non-empty coaching result."""
        from driver_toolkit.analysis.opportunity_detector import Opportunity

        for opp_type in OpportunityType:
            dummy = Opportunity(
                corner_id=1,
                apex_dist_pct=0.25,
                opportunity_type=opp_type,
                time_impact=0.15,
                speed_delta=-3.0,
            )
            result = get_coaching(dummy)
            assert result.cause, f"No cause for {opp_type}"
            assert result.recommendation, f"No recommendation for {opp_type}"
            assert result.drill, f"No drill for {opp_type}"

    def test_corner_label_in_coaching_text(self, synthetic_session):
        results = self._get_results(synthetic_session)
        for r in results:
            # At least one of the coaching texts should reference the corner
            texts = r.cause + r.recommendation + r.drill
            assert r.corner_label in texts, (
                f"Corner label '{r.corner_label}' not found in coaching text"
            )
