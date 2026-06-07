from driver_development_toolkit.analysis import AnalysisConfig, analyze_session, analyze_session_with_summary
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


def test_repeated_segment_findings_are_consolidated():
    opportunities = analyze_session(demo_session())
    pace_segments = [
        opportunity.segment.name
        for opportunity in opportunities
        if opportunity.kind != OpportunityKind.CONSISTENCY
    ]

    assert len(pace_segments) == len(set(pace_segments))
    assert any(
        evidence.metric == "Repeated opportunity"
        for opportunity in opportunities
        for evidence in opportunity.evidence
    )


def test_analysis_config_can_limit_reported_opportunities():
    opportunities = analyze_session(demo_session(), config=AnalysisConfig(max_opportunities=3))

    assert len(opportunities) == 3


def test_analysis_summary_exposes_reference_and_validation_notes():
    opportunities, summary = analyze_session_with_summary(demo_session())

    assert opportunities
    assert summary.reference_lap == 2
    assert summary.minimum_impact_s == 0.03
    assert any("synthetic" in note for note in summary.validation_notes)
