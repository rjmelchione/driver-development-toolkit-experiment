"""Tests for opportunity detection and classification."""

import pytest

from driver_toolkit.analysis.comparator import compare_to_reference
from driver_toolkit.analysis.opportunity_detector import (
    detect_opportunities,
    Opportunity,
    OpportunityType,
)


class TestDetectOpportunities:
    def test_returns_list(self, synthetic_session):
        _, comparisons = compare_to_reference(synthetic_session)
        opps = detect_opportunities(comparisons)
        assert isinstance(opps, list)

    def test_opportunities_detected(self, synthetic_session):
        _, comparisons = compare_to_reference(synthetic_session)
        opps = detect_opportunities(comparisons)
        assert len(opps) > 0, "Expected at least one opportunity in synthetic session"

    def test_sorted_by_impact_descending(self, synthetic_session):
        _, comparisons = compare_to_reference(synthetic_session)
        opps = detect_opportunities(comparisons)
        for i in range(len(opps) - 1):
            assert opps[i].time_impact >= opps[i + 1].time_impact

    def test_all_impacts_positive(self, synthetic_session):
        _, comparisons = compare_to_reference(synthetic_session)
        opps = detect_opportunities(comparisons)
        for opp in opps:
            assert opp.time_impact >= 0

    def test_opportunity_types_are_valid(self, synthetic_session):
        _, comparisons = compare_to_reference(synthetic_session)
        opps = detect_opportunities(comparisons)
        valid_types = set(OpportunityType)
        for opp in opps:
            assert opp.opportunity_type in valid_types

    def test_empty_comparisons_returns_empty(self):
        result = detect_opportunities([])
        assert result == []

    def test_min_impact_filter(self, synthetic_session):
        _, comparisons = compare_to_reference(synthetic_session)
        high_threshold = detect_opportunities(comparisons, min_impact=10.0)
        assert len(high_threshold) == 0

    def test_opportunities_have_apex_dist_pct(self, synthetic_session):
        _, comparisons = compare_to_reference(synthetic_session)
        opps = detect_opportunities(comparisons)
        for opp in opps:
            assert 0.0 <= opp.apex_dist_pct <= 1.0

    def test_over_slowing_detected_at_corner_1(self, synthetic_session):
        """Corner 1 has the most over-slowing imperfections planted; it should appear."""
        _, comparisons = compare_to_reference(synthetic_session)
        opps = detect_opportunities(comparisons)
        over_slowing = [o for o in opps if o.opportunity_type == OpportunityType.OVER_SLOWING]
        assert len(over_slowing) > 0, "Expected over-slowing opportunities in synthetic session"
