from driver_development_toolkit.analysis import analyze_session
from driver_development_toolkit.reporting import render_markdown_report
from driver_development_toolkit.synthetic import demo_session


def test_report_answers_coaching_questions():
    session = demo_session()
    report = render_markdown_report(session, analyze_session(session))

    assert "## Ranked Opportunities" in report
    assert "Where:" in report
    assert "Why:" in report
    assert "What to change:" in report
    assert "How to practice:" in report
    assert "Evidence:" in report
