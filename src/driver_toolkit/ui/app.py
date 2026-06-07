"""Driver Development Toolkit – Streamlit application entry point.

Launch with: uv run streamlit run src/driver_toolkit/ui/app.py

The application is coaching-first: the user sees ranked coaching opportunities
and recommendations immediately. Telemetry evidence is available on demand.

Architecture note: this module contains only UI routing and state management.
All analysis logic lives in driver_toolkit.analysis and driver_toolkit.coaching.
"""

import streamlit as st

from driver_toolkit.analysis.comparator import compare_to_reference, compute_session_consistency
from driver_toolkit.analysis.opportunity_detector import detect_opportunities
from driver_toolkit.analysis.ranker import rank_opportunities
from driver_toolkit.coaching.rules import get_coaching
from driver_toolkit.models import Session
from driver_toolkit.parsing.synthetic import generate_synthetic_session
from driver_toolkit.ui.components.evidence import render_evidence
from driver_toolkit.ui.components.summary import render_session_summary, render_coaching_opportunities


def main() -> None:
    st.set_page_config(
        page_title="Driver Development Toolkit",
        page_icon="🏎",
        layout="wide",
    )

    st.title("Driver Development Toolkit")
    st.caption("iRacing telemetry coaching — identify where you're losing time and what to do about it.")

    session = _get_session()
    if session is None:
        return

    if session.valid_lap_count < 2:
        st.error(
            f"This session contains {session.valid_lap_count} valid lap(s). "
            "At least 2 valid laps are required for comparison analysis."
        )
        return

    with st.spinner("Analysing session..."):
        coaching_results = _run_analysis(session)

    consistency = compute_session_consistency(session)
    render_session_summary(session, consistency)
    st.divider()

    selected_corner_id = render_coaching_opportunities(coaching_results)

    if selected_corner_id is not None:
        st.divider()
        result = next(
            (r for r in coaching_results if r.opportunity.corner_id == selected_corner_id),
            None,
        )
        if result:
            render_evidence(result)


def _get_session() -> Session | None:
    """Return a Session from file upload or demo data."""
    st.sidebar.header("Session Source")

    mode = st.sidebar.radio(
        "Load session from",
        options=["Demo Session", "Upload .ibt File"],
        index=0,
    )

    if mode == "Demo Session":
        st.sidebar.success("Using synthetic demo session.")
        st.sidebar.caption(
            "The demo session simulates 10 laps on a 4-corner oval with deliberate "
            "coaching opportunities planted at specific corners."
        )
        return generate_synthetic_session()

    uploaded = st.sidebar.file_uploader(
        "Select .ibt file",
        type=["ibt"],
        help="iRacing telemetry files are stored in Documents/iRacing/telemetry/",
    )

    if uploaded is None:
        st.sidebar.info("Upload a .ibt file to begin analysis.")
        st.info("Select **Demo Session** in the sidebar to explore the toolkit without a real file.")
        return None

    try:
        import tempfile
        import os
        from driver_toolkit.parsing.ibt_reader import load_ibt

        with tempfile.NamedTemporaryFile(suffix=".ibt", delete=False) as tmp:
            tmp.write(uploaded.read())
            tmp_path = tmp.name

        session = load_ibt(tmp_path)
        os.unlink(tmp_path)
        return session

    except ImportError:
        st.error(
            "pyirsdk is not installed. Install it with `uv add pyirsdk` to load real .ibt files. "
            "Use Demo Session to explore the toolkit without it."
        )
        return None
    except Exception as exc:
        st.error(f"Could not load telemetry file: {exc}")
        return None


def _run_analysis(session: Session) -> list:
    """Execute the full analysis pipeline and return ranked coaching results."""
    try:
        _reference, comparisons = compare_to_reference(session)
        opportunities = detect_opportunities(comparisons)
        ranked = rank_opportunities(opportunities)
        return [get_coaching(opp) for opp in ranked]
    except ValueError as exc:
        st.error(f"Analysis failed: {exc}")
        return []


if __name__ == "__main__":
    main()
