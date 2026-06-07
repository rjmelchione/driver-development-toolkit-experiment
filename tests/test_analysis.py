from driver_development_toolkit.analysis import analyze_session
from driver_development_toolkit.models import OpportunityKind
from driver_development_toolkit.synthetic import demo_session


def test_analyze_session_ranks_opportunities_by_impact():
    opportunities = analyze_session(demo_session())

    assert len(opportunities) >= 2
    impacts = [opportunity.impact_s for opportunity in opportunities]
    assert impacts == sorted(impacts, reverse=True)


def test_opportunities_include_explainable_coaching_fields():
    opportunity = analyze_session(demo_session())[0]

    assert opportunity.cause
    assert opportunity.recommendation
    assert opportunity.practice
    assert opportunity.evidence


def test_synthetic_session_detects_throttle_or_brake_opportunity():
    kinds = {opportunity.kind for opportunity in analyze_session(demo_session())}

    assert OpportunityKind.THROTTLE_APPLICATION in kinds or OpportunityKind.BRAKE_RELEASE in kinds
