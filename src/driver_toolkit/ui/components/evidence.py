"""Telemetry evidence chart for a selected coaching opportunity.

Renders overlaid speed, throttle, and brake traces comparing the reference
lap to the driver's representative lap within the corner zone.
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from driver_toolkit.coaching.rules import CoachingResult
from driver_toolkit.models import TelemetryPoint


def render_evidence(result: CoachingResult) -> None:
    """Render the telemetry evidence panel for one coaching opportunity."""
    opp = result.opportunity

    st.subheader(f"Telemetry Evidence – {opp.corner_label}")
    st.caption(
        f"Reference lap (blue) vs. representative lap (red) "
        f"in the corner zone around {opp.apex_dist_pct * 100:.1f}% track distance."
    )

    ref_pts = opp.ref_telemetry
    lap_pts = opp.lap_telemetry

    if not ref_pts or not lap_pts:
        st.warning(
            "Telemetry evidence is not available for this opportunity. "
            "This may occur when corner detection finds no matching zone in one of the laps."
        )
        return

    fig = _build_overlay_chart(ref_pts, lap_pts, opp.corner_label)
    st.plotly_chart(fig, use_container_width=True)

    _render_metrics_table(result)


def _build_overlay_chart(
    ref_pts: list[TelemetryPoint],
    lap_pts: list[TelemetryPoint],
    label: str,
) -> go.Figure:
    """Build a 3-row Plotly chart: speed / throttle / brake vs. LapDistPct."""
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Speed (km/h)", "Throttle", "Brake"),
        vertical_spacing=0.08,
    )

    ref_x = [pt.lap_dist_pct * 100 for pt in ref_pts]
    lap_x = [pt.lap_dist_pct * 100 for pt in lap_pts]

    # Speed (convert m/s → km/h)
    fig.add_trace(go.Scatter(
        x=ref_x,
        y=[pt.speed * 3.6 for pt in ref_pts],
        name="Reference",
        line={"color": "#2980b9", "width": 2},
        legendgroup="ref",
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=lap_x,
        y=[pt.speed * 3.6 for pt in lap_pts],
        name="Driver",
        line={"color": "#e74c3c", "width": 2, "dash": "dash"},
        legendgroup="lap",
    ), row=1, col=1)

    # Throttle
    fig.add_trace(go.Scatter(
        x=ref_x,
        y=[pt.throttle for pt in ref_pts],
        name="Reference",
        line={"color": "#2980b9", "width": 2},
        legendgroup="ref",
        showlegend=False,
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=lap_x,
        y=[pt.throttle for pt in lap_pts],
        name="Driver",
        line={"color": "#e74c3c", "width": 2, "dash": "dash"},
        legendgroup="lap",
        showlegend=False,
    ), row=2, col=1)

    # Brake
    fig.add_trace(go.Scatter(
        x=ref_x,
        y=[pt.brake for pt in ref_pts],
        name="Reference",
        line={"color": "#2980b9", "width": 2},
        legendgroup="ref",
        showlegend=False,
    ), row=3, col=1)

    fig.add_trace(go.Scatter(
        x=lap_x,
        y=[pt.brake for pt in lap_pts],
        name="Driver",
        line={"color": "#e74c3c", "width": 2, "dash": "dash"},
        legendgroup="lap",
        showlegend=False,
    ), row=3, col=1)

    fig.update_xaxes(title_text="Track Position (%)", row=3, col=1)
    fig.update_yaxes(range=[0, 1.05], row=2, col=1)
    fig.update_yaxes(range=[0, 1.05], row=3, col=1)
    fig.update_layout(
        height=500,
        title_text=f"Telemetry Overlay – {label}",
        hovermode="x unified",
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02},
    )

    return fig


def _render_metrics_table(result: CoachingResult) -> None:
    """Show a compact table of key corner metrics for reference vs. driver."""
    opp = result.opportunity

    if not opp.ref_telemetry or not opp.lap_telemetry:
        return

    ref_min_speed = min(pt.speed for pt in opp.ref_telemetry) * 3.6
    lap_min_speed = min(pt.speed for pt in opp.lap_telemetry) * 3.6

    import pandas as pd
    df = pd.DataFrame({
        "Metric": ["Min Corner Speed (km/h)", "Estimated Time Loss"],
        "Reference Lap": [f"{ref_min_speed:.1f}", "—"],
        "Your Lap": [f"{lap_min_speed:.1f}", opp.impact_label],
    })
    st.dataframe(df, use_container_width=True, hide_index=True)
