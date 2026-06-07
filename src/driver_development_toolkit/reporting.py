"""Coaching-first report rendering."""

from __future__ import annotations

from driver_development_toolkit.models import Opportunity, TelemetrySession


def render_markdown_report(session: TelemetrySession, opportunities: list[Opportunity]) -> str:
    """Render a Markdown coaching report."""

    lines = [
        "# Driver Development Toolkit Coaching Report",
        "",
        f"Source: `{session.source}`",
        f"Car: {session.car}",
        f"Track: {session.track}",
        f"Valid laps analyzed: {sum(1 for lap in session.laps if lap.valid)}",
        "",
        "## Ranked Opportunities",
        "",
    ]

    if not opportunities:
        lines.extend(
            [
                "No significant opportunities were detected with the current analysis thresholds.",
                "",
            ]
        )
        return "\n".join(lines)

    for index, opportunity in enumerate(opportunities, start=1):
        lines.extend(
            [
                f"### {index}. {opportunity.segment.name} (+{opportunity.impact_s:.3f}s)",
                "",
                f"- Where: {opportunity.segment.start_pct:.0%}-{opportunity.segment.end_pct:.0%} lap distance.",
                _comparison_line(opportunity),
                f"- Why: {opportunity.cause}",
                f"- What to change: {opportunity.recommendation}",
                f"- How to practice: {opportunity.practice}",
                "- Evidence:",
            ]
        )
        for item in opportunity.evidence:
            lines.append(f"  - {item.metric}: {item.observed}. {item.interpretation}")
        lines.append("")

    return "\n".join(lines)


def _comparison_line(opportunity: Opportunity) -> str:
    if opportunity.comparison_lap is None or opportunity.reference_lap is None:
        return "- Compared: consistency across valid laps."
    return f"- Compared: lap {opportunity.comparison_lap} against reference lap {opportunity.reference_lap}."
