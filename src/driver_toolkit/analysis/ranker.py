"""Ranks coaching opportunities by estimated lap time impact.

Opportunities arrive pre-sorted from detect_opportunities(), but this module
provides an explicit ranking function for re-sorting or filtering as needed.
"""

from driver_toolkit.analysis.opportunity_detector import Opportunity


def rank_opportunities(opportunities: list[Opportunity]) -> list[Opportunity]:
    """Return opportunities sorted by time_impact descending.

    The highest-impact opportunity appears first, matching the product vision's
    output philosophy of prioritising largest gains.
    """
    return sorted(opportunities, key=lambda o: o.time_impact, reverse=True)
