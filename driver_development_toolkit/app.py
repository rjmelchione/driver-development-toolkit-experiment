import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tempfile

from driver_development_toolkit.parser import (
    parse_ibt_file,
    SyntheticTelemetryGenerator,
    TelemetrySession,
    PYIRSDK_AVAILABLE
)
from driver_development_toolkit.analyzer import OvalSectorer, TelemetryComparer
from driver_development_toolkit.coaching import CoachingEngine

# Page configuration
st.set_page_config(
    page_title="Driver Development Toolkit - iRacing Coach",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium styling
st.markdown("""
<style>
    .reportview-container {
        background-color: #0f1116;
    }
    .card {
        background-color: #1e222b;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #ff4b4b;
    }
    .card-title {
        color: #ff4b4b;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #00e676;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #8a9ba8;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.title("🏁 iRacing Driver Development Toolkit")
st.subheader("Data-driven driving coach for improving Late Model lap times")

# Sidebar for session configuration
st.sidebar.header("Session Loader")

# Option to use demo data or upload file
data_source = st.sidebar.radio(
    "Select Telemetry Source:",
    ("Use Synthetic Demo Session", "Upload iRacing .ibt File")
)

session = None

if data_source == "Use Synthetic Demo Session":
    st.sidebar.info("Loading Charlotte Motor Speedway Oval demo...")
    generator = SyntheticTelemetryGenerator(track_length=1000.0, dt=1/60.0)
    session = generator.generate_session()
else:
    if not PYIRSDK_AVAILABLE:
        st.sidebar.error("pyirsdk is not available. Uploading physical .ibt files is disabled in this environment. Please run the Demo Session instead.")
    else:
        uploaded_file = st.sidebar.file_uploader("Upload .ibt file:", type=["ibt"])
        if uploaded_file is not None:
            # Save bytes to a temp file on Windows
            with tempfile.NamedTemporaryFile(delete=False, suffix=".ibt") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            try:
                with st.spinner("Parsing telemetry file..."):
                    session = parse_ibt_file(tmp_path)
                st.sidebar.success("Telemetry loaded successfully!")
            except Exception as e:
                st.sidebar.error(f"Error parsing file: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

if session is not None:
    # Sidebar session info display
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Track:** {session.track_name}")
    st.sidebar.markdown(f"**Car:** {session.car_name}")
    st.sidebar.markdown(f"**Driver:** {session.driver_name}")
    
    # List valid laps for selectors
    laps_dict = {f"Lap {l.lap_number} ({l.lap_time:.3f}s)": l for l in session.laps}
    valid_laps_dict = {f"Lap {l.lap_number} ({l.lap_time:.3f}s)": l for l in session.laps if l.is_valid}
    
    if not laps_dict:
        st.error("No laps could be parsed from the telemetry data.")
    else:
        # Lap Selection
        st.sidebar.markdown("---")
        st.sidebar.header("Lap Comparison Selection")
        
        # Default target lap to the slowest or second lap if available
        lap_keys = list(laps_dict.keys())
        default_target_idx = min(1, len(lap_keys) - 1) if len(lap_keys) > 1 else 0
        
        target_lap_key = st.sidebar.selectbox(
            "Select Target Lap (Driver):",
            lap_keys,
            index=default_target_idx
        )
        target_lap = laps_dict[target_lap_key]
        
        # Default reference to the fastest valid lap
        fastest = session.fastest_lap
        default_ref_idx = 0
        if fastest:
            fastest_key = f"Lap {fastest.lap_number} ({fastest.lap_time:.3f}s)"
            if fastest_key in lap_keys:
                default_ref_idx = lap_keys.index(fastest_key)
                
        ref_lap_key = st.sidebar.selectbox(
            "Select Reference Lap (Coach):",
            lap_keys,
            index=default_ref_idx
        )
        ref_lap = laps_dict[ref_lap_key]
        
        # Comparison Header Dashboard
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Target Lap", f"{target_lap.lap_time:.3f}s", f"Lap {target_lap.lap_number}")
        with col2:
            st.metric("Reference Lap", f"{ref_lap.lap_time:.3f}s", f"Lap {ref_lap.lap_number}")
        with col3:
            time_diff = target_lap.lap_time - ref_lap.lap_time
            diff_color = "inverse" if time_diff > 0 else "normal"
            st.metric("Time Delta", f"{time_diff:+.3f}s", delta_color=diff_color)
        with col4:
            valid_status = "Valid" if target_lap.is_valid else "Invalid/Partial"
            st.metric("Lap Validity", valid_status)
            
        # Perform segmenting and comparison
        sectorer = OvalSectorer()
        sectors = sectorer.segment_lap(ref_lap)
        
        comparer = TelemetryComparer(step_meters=1.0)
        comparison = comparer.compare_laps(target_lap, ref_lap, sectors)
        
        # Heuristics Coaching Engine
        engine = CoachingEngine(time_loss_threshold=0.15)
        opportunities = engine.generate_opportunities(comparison)
        
        # Render Coaching opportunities
        st.markdown("---")
        st.header("🎯 Coaching Analysis & Recommendations")
        
        if not opportunities:
            st.success("🎉 Excellent consistency! No major performance opportunities detected compared to the reference lap. Keep rolling that speed!")
        else:
            # Display ranked coaching opportunities
            for idx, opp in enumerate(opportunities):
                severity_color = "#ff1744" if opp.time_lost > 1.0 else "#ff9100"
                
                # HTML template card for premium visual aesthetics
                st.markdown(f"""
                <div class="card" style="border-left-color: {severity_color}">
                    <div class="card-title" style="color: {severity_color}">{idx + 1}. {opp.opportunity_name}</div>
                    <p><b>Diagnosis:</b> {opp.diagnosis}</p>
                    <p><b>Corrective Action:</b> {opp.advice}</p>
                    <p style="background-color: #272c36; padding: 10px; border-radius: 4px; border-left: 3px solid #00e676;">
                        <b>🛠️ Focused Practice Drill:</b> {opp.drill}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # Plotly Telemetry Overlay Viewer
        st.markdown("---")
        st.header("📊 Telemetry Overlay Viewer")
        st.caption("Distance-aligned traces. Hover over the chart to inspect target vs. reference inputs at any track location.")
        
        common_dist = comparison['common_dist']
        target_ch = comparison['target_data']
        ref_ch = comparison['ref_data']
        delta_t = comparison['delta_t']
        
        # Construct 3-panel figure
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.06,
            row_heights=[0.4, 0.2, 0.4],
            subplot_titles=(
                "Speed Trace (m/s) - Shows where corner entry & apex speeds drop",
                "Cumulative Time Delta (Seconds) - Slope climbing indicates time loss",
                "Pedal Inputs - Throttle (solid/dash red) & Brake (solid/dash brown)"
            )
        )
        
        # 1. Speed Traces
        fig.add_trace(
            go.Scatter(x=common_dist, y=ref_ch['Speed'], name="Ref Speed", line=dict(color="#00e676", width=2, dash="dash")),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=common_dist, y=target_ch['Speed'], name="Target Speed", line=dict(color="#ff1744", width=2)),
            row=1, col=1
        )
        
        # Add sector shaded regions to row 1
        for sec in sectors:
            if sec['type'] == 'turn':
                fig.add_vrect(
                    x0=sec['start_dist'], x1=sec['end_dist'],
                    fillcolor="rgba(255, 255, 255, 0.05)",
                    layer="below", line_width=0,
                    annotation_text=sec['name'], annotation_position="top left",
                    row=1, col=1
                )
                
        # 2. Delta-T Time Slip
        fig.add_trace(
            go.Scatter(x=common_dist, y=delta_t, name="Time Slip (Delta-T)", line=dict(color="#2979ff", width=2.5)),
            row=2, col=1
        )
        fig.add_hline(y=0.0, line_dash="dash", line_color="#8a9ba8", row=2, col=1)
        
        # 3. Pedals overlay
        # Throttle
        fig.add_trace(
            go.Scatter(x=common_dist, y=ref_ch['Throttle'] * 100, name="Ref Throttle", line=dict(color="#00e676", width=1.5, dash="dash")),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(x=common_dist, y=target_ch['Throttle'] * 100, name="Target Throttle", line=dict(color="#ff1744", width=2)),
            row=3, col=1
        )
        # Brake
        fig.add_trace(
            go.Scatter(x=common_dist, y=ref_ch['Brake'] * 100, name="Ref Brake", line=dict(color="#e0a96d", width=1.5, dash="dash")),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(x=common_dist, y=target_ch['Brake'] * 100, name="Target Brake", line=dict(color="#b85d06", width=2)),
            row=3, col=1
        )
        
        # Update styling
        fig.update_layout(
            template="plotly_dark",
            height=800,
            hovermode="x unified",
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Y-axes label configuration
        fig.update_yaxes(title_text="Speed (m/s)", row=1, col=1)
        fig.update_yaxes(title_text="Delta-T (s)", row=2, col=1)
        fig.update_yaxes(title_text="Pedal %", row=3, col=1)
        fig.update_xaxes(title_text="Distance along track (Meters)", row=3, col=1)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Details segment listing
        st.markdown("---")
        st.header("📋 Sector Comparison Breakdown")
        sector_df = pd.DataFrame(comparison['sectors'])
        sector_df.columns = ["Sector Name", "Start Distance (m)", "End Distance (m)", "Sector Type", "Time Gained/Lost (s)"]
        
        # Highlight time lost cells
        def color_sectors(val):
            if isinstance(val, float):
                if val > 0.15:
                    return 'background-color: rgba(255, 23, 68, 0.2); color: #ff1744; font-weight: bold;'
                elif val < -0.05:
                    return 'background-color: rgba(0, 230, 118, 0.2); color: #00e676;'
            return ''
            
        st.table(sector_df.style.map(color_sectors, subset=["Time Gained/Lost (s)"]).format({"Time Gained/Lost (s)": "{:+.3f}s"}))

else:
    st.info("👈 Please load a session to begin. You can use the Synthetic Demo Session or upload an iRacing .ibt file.")
