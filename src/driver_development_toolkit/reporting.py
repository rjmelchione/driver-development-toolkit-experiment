"""Coaching-first report rendering."""

from __future__ import annotations

from driver_development_toolkit.models import AnalysisSummary, Opportunity, TelemetrySession


def render_markdown_report(
    session: TelemetrySession,
    opportunities: list[Opportunity],
    summary: AnalysisSummary | None = None,
) -> str:
    """Render a Markdown coaching report."""

    lines = [
        "# Driver Development Toolkit Coaching Report",
        "",
        f"Source: `{session.source}`",
        f"Source type: {session.source_type}",
        f"Car: {session.car}",
        f"Track: {session.track}",
        f"Valid laps analyzed: {sum(1 for lap in session.laps if lap.valid)}",
        "",
    ]

    if summary is not None:
        lines.extend(_summary_lines(summary))

    lines.extend(
        [
            "## Ranked Opportunities",
            "",
        ]
    )

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


def _summary_lines(summary: AnalysisSummary) -> list[str]:
    max_opportunities = (
        "unlimited" if summary.max_opportunities is None else str(summary.max_opportunities)
    )
    lines = [
        "## Analysis Provenance",
        "",
        f"- Reference lap: lap {summary.reference_lap} ({summary.reference_lap_time_s:.3f}s).",
        f"- Valid laps: {summary.valid_lap_count}.",
        f"- Segments analyzed: {summary.segment_count}.",
        f"- Minimum impact threshold: {summary.minimum_impact_s:.3f}s.",
        f"- Throttle classification threshold: {summary.throttle_delta_threshold_pct:.1f} percentage points.",
        f"- Brake classification threshold: {summary.brake_delta_threshold_pct:.1f} percentage points.",
        f"- Consistency opportunities included: {summary.consistency_included}.",
        f"- Max opportunities: {max_opportunities}.",
        "- Validation notes:",
    ]
    for note in summary.validation_notes:
        lines.append(f"  - {note}")
    lines.append("")
    return lines


def _comparison_line(opportunity: Opportunity) -> str:
    if opportunity.comparison_lap is None or opportunity.reference_lap is None:
        return "- Compared: consistency across valid laps."
    return f"- Compared: lap {opportunity.comparison_lap} against reference lap {opportunity.reference_lap}."
