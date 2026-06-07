"""Session summary and ranked coaching opportunity display.

Renders the coaching-first primary view: session overview at the top,
ranked opportunities below with cause, recommendation, and drill.
"""

import streamlit as st

from driver_toolkit.analysis.comparator import SessionConsistency
from driver_toolkit.coaching.rules import CoachingResult
from driver_toolkit.models import Session


OPPORTUNITY_TYPE_LABELS = {
    "over_slowing": "Over-Slowing",
    "late_throttle": "Late Throttle",
    "early_brake": "Early Brake",
    "inconsistent_braking": "Inconsistent Braking",
    "general_corner": "General Corner",
}

OPPORTUNITY_TYPE_COLORS = {
    "over_slowing": "#e74c3c",
    "late_throttle": "#f39c12",
    "early_brake": "#3498db",
    "inconsistent_braking": "#9b59b6",
    "general_corner": "#7f8c8d",
}


def render_session_summary(session: Session, consistency: SessionConsistency) -> None:
    """Render the session header with key metrics."""
    st.header("Session Summary")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Car", session.car or "Unknown")
    with col2:
        st.metric("Track", session.track or "Unknown")
    with col3:
        st.metric("Best Lap", _format_lap_time(consistency.best_lap_time))
    with col4:
        st.metric(
            "Consistency",
            f"{consistency.consistency_score:.0f}/100",
            help="100 = perfectly consistent lap times. Lower = more variation.",
        )

    with st.expander("Lap Time Summary"):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Valid Laps", session.valid_lap_count)
        with col_b:
            st.metric("Average Lap", _format_lap_time(consistency.average_lap_time))
        with col_c:
            st.metric("Std Dev", f"{consistency.std_dev:.3f}s")

        if consistency.lap_times:
            import pandas as pd
            df = pd.DataFrame({
                "Lap": range(1, len(consistency.lap_times) + 1),
                "Lap Time (s)": consistency.lap_times,
            })
            st.dataframe(df, use_container_width=True, hide_index=True)


def render_coaching_opportunities(results: list[CoachingResult]) -> int | None:
    """Render the ranked coaching opportunity list.

    Returns the corner_id of the selected opportunity for evidence drill-down,
    or None if no selection was made.
    """
    st.header("Coaching Opportunities")

    if not results:
        st.info("No significant coaching opportunities detected in this session.")
        return None

    st.caption(
        f"{len(results)} opportunity{'s' if len(results) != 1 else ''} identified, "
        "ranked by estimated lap time impact."
    )

    selected_corner_id = None

    for rank, result in enumerate(results, start=1):
        opp = result.opportunity
        type_key = opp.opportunity_type.value
        color = OPPORTUNITY_TYPE_COLORS.get(type_key, "#7f8c8d")
        type_label = OPPORTUNITY_TYPE_LABELS.get(type_key, type_key)

        with st.container(border=True):
            header_col, badge_col, impact_col, btn_col = st.columns([3, 2, 2, 1])

            with header_col:
                st.markdown(f"**#{rank} – {opp.corner_label}**")

            with badge_col:
                st.markdown(
                    f'<span style="background:{color};color:white;padding:2px 8px;'
                    f'border-radius:4px;font-size:0.8em">{type_label}</span>',
                    unsafe_allow_html=True,
                )

            with impact_col:
                st.markdown(f"**{opp.impact_label}** per lap")

            with btn_col:
                if st.button("Evidence", key=f"evidence_{opp.corner_id}"):
                    selected_corner_id = opp.corner_id

            tab_why, tab_what, tab_how = st.tabs(["Why", "What to Change", "How to Practice"])
            with tab_why:
                st.write(result.cause)
            with tab_what:
                st.write(result.recommendation)
            with tab_how:
                st.write(result.drill)

    return selected_corner_id


def _format_lap_time(seconds: float) -> str:
    if seconds <= 0:
        return "—"
    minutes = int(seconds // 60)
    secs = seconds % 60
    if minutes > 0:
        return f"{minutes}:{secs:06.3f}"
    return f"{secs:.3f}s"
