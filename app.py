import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MOIL AI",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SHARED MANGANESE DATA
# ============================================================

MANGANESE_STORAGE_DIR = Path("data")
MANGANESE_STORAGE_FILE = MANGANESE_STORAGE_DIR / "manganese_uploaded_latest.csv"

if "manganese_data" not in st.session_state:
    st.session_state["manganese_data"] = None

if "manganese_filename" not in st.session_state:
    st.session_state["manganese_filename"] = None

# Restore the latest uploaded dataset after a Streamlit restart, if available.
if st.session_state["manganese_data"] is None and MANGANESE_STORAGE_FILE.exists():
    try:
        restored_df = pd.read_csv(MANGANESE_STORAGE_FILE)
        if not restored_df.empty:
            st.session_state["manganese_data"] = restored_df
            st.session_state["manganese_filename"] = MANGANESE_STORAGE_FILE.name
    except Exception:
        # A broken stored file should not prevent the application from starting.
        pass


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    color: #9aa4b2;
    font-size: 17px;
    margin-bottom: 25px;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 10px;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# DEMO DATA
# ============================================================

# ============================================================
# DATA MANAGEMENT
# ============================================================

# Default demo dataset
default_data = pd.DataFrame({
    "Date": pd.date_range(
        datetime.now() - timedelta(days=6),
        periods=7
    ),
    "Production": [
        3100, 3250, 3400, 3600,
        3750, 3900, 4050
    ],
    "Efficiency": [
        88, 89, 91, 92,
        93, 94, 95
    ],
    "Temperature": [
        42, 44, 46, 48,
        51, 53, 55
    ],
    "Vibration": [
        2.1, 2.2, 2.3, 2.4,
        2.6, 2.8, 3.0
    ],
    "Pressure": [
        3.8, 3.9, 4.0, 4.2,
        4.3, 4.5, 4.6
    ]
})


# Load the CSV automatically if it exists
try:

    csv_data = pd.read_csv(
        "data/mining_data.csv"
    )

    csv_data["Date"] = pd.to_datetime(
        csv_data["Date"]
    )

    mining_data = csv_data

except Exception:

    mining_data = default_data.copy()
# Keep compatibility with the dashboard charts
production_df = mining_data.copy()


# ============================================================
# DATA SUMMARY
# ============================================================

total_production = mining_data[
    "Production"
].sum()

average_production = mining_data[
    "Production"
].mean()

average_efficiency = mining_data[
    "Efficiency"
].mean()

average_temperature = mining_data[
    "Temperature"
].mean()

average_vibration = mining_data[
    "Vibration"
].mean()

average_pressure = mining_data[
    "Pressure"
].mean()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⛏️ MOIL AI")

    st.caption("Mining Intelligence Platform")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "🤖 AI Prediction",
            "🗺️ Manganese Exploration",
            "⚠️ Risk Detection",
            "📁 Data Analysis",
            "⚙️ System"
        ]
    )

    st.divider()

    st.markdown("### ⛏️ Mine Configuration")

    mine = st.selectbox(
        "Mining Site",
        [
            "Site A",
            "Site B",
            "Site C",
            "All Sites"
        ],
        key="sidebar_mining_site"
    )

    shift = st.selectbox(
        "Shift",
        [
            "All Shifts",
            "Morning",
            "Afternoon",
            "Night"
        ],
        key="sidebar_shift"
    )

    st.divider()

    st.success("● AI System Online")

    st.caption(
        f"Last updated: {datetime.now().strftime('%H:%M:%S')}"
    )


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.markdown(
        '<div class="main-title">⛏️ MOIL AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-Powered Mining Intelligence Platform'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # DASHBOARD FILTERS
    # --------------------------------------------------------

    f1, f2, f3 = st.columns(3)

    with f1:

        period = st.selectbox(
            "Time Period",
            [
                "Last 7 Days",
                "Last 14 Days",
                "Last 30 Days"
            ],
            key="dashboard_period"
        )

    with f2:

        metric = st.selectbox(
            "Chart Metric",
            [
                "Production",
                "Efficiency",
                "Temperature",
                "Vibration"
            ],
            key="dashboard_metric"
        )

    with f3:

        st.write("Dashboard")

        refresh = st.button(
            "🔄 Refresh Dashboard",
            width="stretch",
            key="dashboard_refresh"
        )
        # --------------------------------------------------------
        # FILTER DATA BY TIME PERIOD
        # --------------------------------------------------------

        if period == "Last 7 Days":
            days_to_show = 7

        elif period == "Last 14 Days":
            days_to_show = 14

        else:
            days_to_show = 30

        filtered_data = mining_data.sort_values(
            "Date"
        ).tail(days_to_show)

        # Recalculate dashboard values
        total_production = filtered_data["Production"].sum()
        average_efficiency = filtered_data["Efficiency"].mean()
        average_temperature = filtered_data["Temperature"].mean()
        average_vibration = filtered_data["Vibration"].mean()
        average_pressure = filtered_data["Pressure"].mean()

    st.divider()

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(

            "⛏️ Production",
            f"{total_production:,.0f} T"
       )

    with k2:

        st.metric(
            "⚙️ Efficiency",
            f"{average_efficiency:.1f}%"
       )

    with k3:

        if average_temperature < 55:

            risk_level = "LOW"

        elif average_temperature < 70:

            risk_level = "MEDIUM"

        else:

            risk_level = "HIGH"

        st.metric(
            "🌡️ Avg Temperature",
            f"{average_temperature:.1f}°C",
            risk_level
        )

    with k4:

        st.metric(
            "📳 Avg Vibration",
            f"{average_vibration:.2f} mm/s"
        )
    st.divider()

    # ========================================================
    # LIVE MINING CONTROL ROOM
    # ========================================================

    st.subheader("🎛️ Live Mining Control Room")

    st.caption(
        "Adjust operating conditions and run the AI analysis."
    )

    # --------------------------------------------------------
    # EQUIPMENT + PRODUCTION + EFFICIENCY
    # --------------------------------------------------------

    control1, control2, control3 = st.columns(3)

    with control1:

        selected_equipment = st.selectbox(
            "⚙️ Select Equipment",
            [
                "Excavator E-01",
                "Excavator E-02",
                "Dumper D-01",
                "Dumper D-02",
                "Drill DR-01"
            ],
            key="dashboard_equipment"
        )

    with control2:

        production = st.slider(
            "⛏️ Current Production (T/hr)",
            min_value=1000,
            max_value=5000,
            value=3500,
            step=100,
            key="dashboard_production_slider"
        )

    with control3:

        efficiency = st.slider(
            "⚙️ Efficiency (%)",
            min_value=50,
            max_value=100,
            value=92,
            key="dashboard_efficiency_slider"
        )

    # --------------------------------------------------------
    # SENSORS
    # --------------------------------------------------------

    sensor1, sensor2, sensor3 = st.columns(3)

    with sensor1:

        temperature = st.slider(
            "🌡️ Temperature (°C)",
            20,
            90,
            48,
            key="dashboard_temperature_slider"
        )

    with sensor2:

        vibration = st.slider(
            "📳 Vibration (mm/s)",
            0.0,
            10.0,
            2.4,
            0.1,
            key="dashboard_vibration_slider"
        )

    with sensor3:

        pressure = st.slider(
            "💨 Pressure (bar)",
            1.0,
            8.0,
            4.2,
            0.1,
            key="dashboard_pressure_slider"
        )

    st.divider()

    # --------------------------------------------------------
    # AI ANALYSIS BUTTON
    # --------------------------------------------------------

    analyze = st.button(
        "🧠 ANALYZE CURRENT CONDITIONS",
        width="stretch",
        key="dashboard_analyze"
    )

    if analyze:

        # ====================================================
        # RISK CALCULATION
        # ====================================================

        risk_score = 0

        warnings = []

        normal_conditions = []

        # ----------------------------------------------------
        # TEMPERATURE
        # ----------------------------------------------------

        if temperature >= 70:

            risk_score += 35

            warnings.append(
                "🌡️ High temperature detected"
            )

        elif temperature >= 55:

            risk_score += 15

            warnings.append(
                "🌡️ Temperature above preferred range"
            )

        else:

            normal_conditions.append(
                "✓ Temperature normal"
            )

        # ----------------------------------------------------
        # VIBRATION
        # ----------------------------------------------------

        if vibration >= 7:

            risk_score += 35

            warnings.append(
                "📳 Excessive vibration detected"
            )

        elif vibration >= 4:

            risk_score += 15

            warnings.append(
                "📳 Elevated vibration detected"
            )

        else:

            normal_conditions.append(
                "✓ Vibration normal"
            )

        # ----------------------------------------------------
        # EFFICIENCY
        # ----------------------------------------------------

        if efficiency < 70:

            risk_score += 25

            warnings.append(
                "⚙️ Low operational efficiency"
            )

        elif efficiency < 85:

            risk_score += 10

            warnings.append(
                "⚙️ Efficiency below optimal level"
            )

        else:

            normal_conditions.append(
                "✓ Efficiency optimal"
            )

        # ----------------------------------------------------
        # PRESSURE
        # ----------------------------------------------------

        if pressure >= 7:

            risk_score += 20

            warnings.append(
                "💨 High pressure detected"
            )

        elif pressure >= 5.5:

            risk_score += 10

            warnings.append(
                "💨 Pressure slightly elevated"
            )

        else:

            normal_conditions.append(
                "✓ Pressure normal"
            )

        risk_score = min(
            risk_score,
            100
        )

        # ====================================================
        # PREDICTED OUTPUT
        # ====================================================

        predicted_output = production * (
            efficiency / 100
        )

        # ====================================================
        # AI CONFIDENCE
        # ====================================================

        confidence = max(
            70,
            98 - (risk_score * 0.25)
        )

        # ====================================================
        # STATUS
        # ====================================================

        if risk_score < 30:

            status = "NORMAL"

            recommendation = (
                "Continue normal operation. "
                "No immediate intervention is required."
            )

        elif risk_score < 70:

            status = "WARNING"

            recommendation = (
                "Continue operation with increased "
                "monitoring. Inspect affected parameters."
            )

        else:

            status = "CRITICAL"

            recommendation = (
                "Immediate equipment inspection is "
                "recommended before continuing normal operation."
            )

        # ====================================================
        # AI DIAGNOSTIC
        # ====================================================

        st.divider()

        st.subheader(
            "🧠 AI Diagnostic Result"
        )

        st.caption(
            f"Analysis generated for {selected_equipment}"
        )

        # ----------------------------------------------------
        # RESULT CARDS
        # ----------------------------------------------------

        result1, result2, result3, result4 = st.columns(4)

        with result1:

            st.metric(
                "AI Risk Score",
                f"{risk_score}/100"
            )

        with result2:

            if status == "NORMAL":

                st.success(
                    "🟢 NORMAL"
                )

            elif status == "WARNING":

                st.warning(
                    "🟡 WARNING"
                )

            else:

                st.error(
                    "🔴 CRITICAL"
                )

        with result3:

            st.metric(
                "Predicted Output",
                f"{predicted_output:,.0f} T/hr"
            )

        with result4:

            st.metric(
                "AI Confidence",
                f"{confidence:.1f}%"
            )

        # ----------------------------------------------------
        # RISK BAR
        # ----------------------------------------------------

        st.write("### Risk Level")

        st.progress(
            risk_score / 100
        )

        # ----------------------------------------------------
        # FINDINGS
        # ----------------------------------------------------

        detail1, detail2 = st.columns(2)

        with detail1:

            st.markdown(
                "### 🔍 AI Findings"
            )

            if warnings:

                for warning in warnings:

                    st.warning(
                        warning
                    )

            else:

                st.success(
                    "No abnormal operating conditions detected."
                )

        with detail2:

            st.markdown(
                "### ✅ Normal Parameters"
            )

            if normal_conditions:

                for condition in normal_conditions:

                    st.success(
                        condition
                    )

            else:

                st.info(
                    "No parameters are currently in the normal range."
                )

        # ----------------------------------------------------
        # RECOMMENDATION
        # ----------------------------------------------------

        st.markdown(
            "### 💡 AI Recommendation"
        )

        if status == "NORMAL":

            st.success(
                f"🟢 {recommendation}"
            )

        elif status == "WARNING":

            st.warning(
                f"🟡 {recommendation}"
            )

        else:

            st.error(
                f"🔴 {recommendation}"
            )

    # ========================================================
    # PRODUCTION ANALYTICS
    # ========================================================

    st.divider()

    st.subheader(
        "📈 Operational Analytics"
    )

    chart_col, prediction_col = st.columns(
        [1.7, 1]
    )

    with chart_col:

        chart_data = filtered_data.copy()

        fig = px.line(
            chart_data,
            x="Date",
            y=metric,
            markers=True,
            template="plotly_dark"
        )

        

        fig.update_layout(
            height=420,
            margin=dict(
                l=10,
                r=10,
                t=30,
                b=10
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            width="stretch",
            key="operational_analytics_chart"
        )

    # ========================================================
    # AI OPERATIONAL STATUS
    # ========================================================

    with prediction_col:

        st.subheader(
            "🤖 AI Operational Status"
        )

        st.info("⏳ Trained model not connected")

        st.metric("Predicted Production", "—")
        st.write("Model Confidence")
        st.progress(0.0)
        st.caption("Waiting for trained Laptop 1 model")

        st.divider()

        st.write(
            "### Current Conditions"
        )

        condition1, condition2 = st.columns(2)

        with condition1:

            st.metric(
                "Temperature",
                f"{temperature:.1f}°C"
            )

        with condition2:

            st.metric(
                "Vibration",
                f"{vibration:.2f} mm/s"
            )

    # ========================================================
    # SYSTEM STATUS
    # ========================================================

    st.divider()

    st.subheader(
        "🛰️ Real-Time System Status"
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.success(
            "🟢 Equipment\n\nNormal"
        )

    with s2:

        st.success(
            "🟢 Sensors\n\nOnline"
        )

    with s3:

        st.warning(
            "🟡 Production\n\nMinor deviation"
        )

    with s4:

        st.success(
            "🟢 Safety\n\nNormal"
        )

    # ========================================================
    # 3D MINE CONTROL VIEW
    # ========================================================

    st.divider()

    st.subheader(
        "🛰️ 3D Mine Control View"
    )

    st.caption(
        "Interactive visualization of monitored mining equipment."
    )

    equipment_positions = {

        "Excavator E-01": (2, 3, 1),

        "Excavator E-02": (7, 5, 2),

        "Dumper D-01": (4, 8, 1),

        "Dumper D-02": (9, 2, 1),

        "Drill DR-01": (6, 7, 3)
    }

    x = []

    y = []

    z = []

    names = []

    statuses = []

    # Use the current analysis status if analysis was performed
    current_status = "NORMAL"

    if analyze:

        current_status = status

    for name, position in equipment_positions.items():

        x.append(position[0])

        y.append(position[1])

        z.append(position[2])

        names.append(name)

        if name == selected_equipment:

            statuses.append(
                current_status
            )

        else:

            statuses.append(
                "NORMAL"
            )

    # --------------------------------------------------------
    # STATUS NUMBERS
    # --------------------------------------------------------

    status_values = []

    for item in statuses:

        if item == "CRITICAL":

            status_values.append(3)

        elif item == "WARNING":

            status_values.append(2)

        else:

            status_values.append(1)

    # --------------------------------------------------------
    # 3D FIGURE
    # --------------------------------------------------------

    fig3d = go.Figure()

    fig3d.add_trace(
        go.Scatter3d(

            x=x,
            y=y,
            z=z,

            mode="markers+text",

            text=names,

            textposition="top center",

            marker=dict(
                size=14,
                color=status_values,
                colorscale=[
                    [0.0, "#22c55e"],
                    [0.5, "#f59e0b"],
                    [1.0, "#ef4444"]
                ],
                cmin=1,
                cmax=3,
                line=dict(
                    width=2,
                    color="white"
                )
            ),

            hovertemplate=
            "<b>%{text}</b><br>" +
            "X: %{x}<br>" +
            "Y: %{y}<br>" +
            "Elevation: %{z}<br>" +
            "<extra></extra>"
        )
    )

    # --------------------------------------------------------
    # MINE BOUNDARY
    # --------------------------------------------------------

    fig3d.add_trace(
        go.Scatter3d(

            x=[0, 10, 10, 0, 0],

            y=[0, 0, 10, 10, 0],

            z=[0, 0, 0, 0, 0],

            mode="lines",

            line=dict(
                width=5
            ),

            name="Mine Boundary"
        )
    )

    fig3d.update_layout(

        height=600,

        scene=dict(

            xaxis_title="Mine X",

            yaxis_title="Mine Y",

            zaxis_title="Elevation",

            bgcolor="rgba(0,0,0,0)"
        ),

        paper_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=0,
            r=0,
            t=20,
            b=0
        ),

        showlegend=False
    )

    st.plotly_chart(
        fig3d,
        width="stretch",
        key="dashboard_3d_mine_view"
    )

    legend1, legend2, legend3 = st.columns(3)

    with legend1:

        st.success(
            "🟢 Normal"
        )

    with legend2:

        st.warning(
            "🟡 Warning"
        )

    with legend3:

        st.error(
            "🔴 Critical"
        )

    # ========================================================
    # RECENT EVENTS
    # ========================================================

    st.divider()

    st.subheader(
        "📋 Recent Events"
    )

    events = pd.DataFrame({

        "Time": [
            "10:42",
            "10:18",
            "09:55",
            "09:31",
            "09:05"
        ],

        "Event": [
            "Production deviation detected",
            "Equipment health check completed",
            "Sensor data received",
            "AI prediction generated",
            "Safety check completed"
        ],

        "Severity": [
            "Medium",
            "Low",
            "Low",
            "Low",
            "Low"
        ],

        "Status": [
            "Monitoring",
            "Normal",
            "Normal",
            "Completed",
            "Normal"
        ]
    })

    st.dataframe(
        events,
        width="stretch",
        hide_index=True
    )


# ============================================================
# AI PREDICTION PAGE
# ============================================================

elif page == "🤖 AI Prediction":

    st.title(
        "🤖 AI Prediction Engine"
    )

    st.write(
        "Generate operational predictions using the machine-learning model."
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:

        production_input = st.slider(
            "Current Production (T)",
            1000,
            5000,
            3500,
            key="ai_prediction_production"
        )

    with c2:

        efficiency_input = st.slider(
            "Efficiency (%)",
            50,
            100,
            92,
            key="ai_prediction_efficiency"
        )

    with c3:

        temperature_input = st.slider(
            "Temperature (°C)",
            20,
            80,
            48,
            key="ai_prediction_temperature"
        )

    if st.button(
        "🚀 Run AI Prediction",
        width="stretch",
        key="ai_prediction_run"
    ):

        st.divider()

        st.subheader("📥 Prediction Inputs")
        input_data = pd.DataFrame({
            "Parameter": ["Production", "Efficiency", "Temperature"],
            "Value": [production_input, efficiency_input, temperature_input],
            "Unit": ["T", "%", "°C"]
        })
        st.dataframe(input_data, width="stretch", hide_index=True)

        st.warning(
            "⚠️ No trained prediction model is connected yet. "
            "The application will not generate a fabricated prediction or confidence value."
        )

        st.info(
            "These inputs are ready for the Laptop 1 ML pipeline. "
            "Connect the trained model here to produce the real prediction."
        )

elif page == "🗺️ Manganese Exploration":

    st.title("🗺️ Manganese Exploration")
    st.caption(
        "Prepare, inspect and hand off manganese exploration data to the Laptop 1 processing pipeline. "
        "No fabricated prediction is generated on this page."
    )

    st.divider()

    # ------------------------------------------------------------
    # UPLOAD / STORAGE
    # ------------------------------------------------------------
    st.subheader("📁 Exploration Dataset")

    uploaded_manganese = st.file_uploader(
        "Upload a manganese exploration CSV",
        type=["csv"],
        key="manganese_dataset_upload"
    )

    if uploaded_manganese is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_manganese)
            if uploaded_df.empty:
                st.error("The uploaded CSV is empty. Please upload a dataset containing rows and columns.")
            else:
                st.session_state["manganese_data"] = uploaded_df.copy()
                st.session_state["manganese_filename"] = uploaded_manganese.name
                MANGANESE_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
                uploaded_df.to_csv(MANGANESE_STORAGE_FILE, index=False)
                st.success(f"✅ Loaded and stored: {uploaded_manganese.name}")
        except Exception as exc:
            st.error(f"Could not read the CSV file: {exc}")

    manganese_data = st.session_state.get("manganese_data")

    if manganese_data is None:
        st.info("Upload a CSV dataset to start the manganese exploration workflow.")
    else:
        # --------------------------------------------------------
        # OVERVIEW
        # --------------------------------------------------------
        st.subheader("📊 Dataset Overview")
        o1, o2, o3, o4, o5 = st.columns(5)
        with o1:
            st.metric("Rows", f"{len(manganese_data):,}")
        with o2:
            st.metric("Columns", len(manganese_data.columns))
        with o3:
            st.metric("Numeric Features", len(manganese_data.select_dtypes(include=np.number).columns))
        with o4:
            st.metric("Missing Values", int(manganese_data.isna().sum().sum()))
        with o5:
            st.metric("Duplicate Rows", int(manganese_data.duplicated().sum()))

        st.caption(f"Current dataset: {st.session_state.get('manganese_filename', 'Unknown')}")

        tab_data, tab_quality, tab_visuals, tab_handoff = st.tabs(
            ["📋 Data", "🧪 Quality", "📈 Exploration", "🔗 Laptop 1 Handoff"]
        )

        with tab_data:
            st.dataframe(
                manganese_data,
                width="stretch",
                hide_index=True,
                height=420
            )

            numeric_columns = list(manganese_data.select_dtypes(include=np.number).columns)
            if numeric_columns:
                st.subheader("📐 Numeric Summary")
                st.dataframe(
                    manganese_data[numeric_columns].describe().T.round(3),
                    width="stretch"
                )
            else:
                st.info("No numeric columns were detected.")

        # --------------------------------------------------------
        # COLUMN DETECTION / QUALITY
        # --------------------------------------------------------
        columns_lower = {str(col).strip().lower(): col for col in manganese_data.columns}

        latitude_col = next(
            (columns_lower[key] for key in columns_lower if key in {"latitude", "lat", "y", "lat_deg"}),
            None
        )
        longitude_col = next(
            (columns_lower[key] for key in columns_lower if key in {"longitude", "lon", "lng", "x", "long", "lon_deg"}),
            None
        )
        manganese_cols = [
            col for col in manganese_data.columns
            if any(token in str(col).lower() for token in ["mn", "manganese"])
        ]
        numeric_columns = list(manganese_data.select_dtypes(include=np.number).columns)

        with tab_quality:
            q1, q2, q3, q4 = st.columns(4)
            with q1:
                st.metric("Latitude", str(latitude_col) if latitude_col else "Not detected")
            with q2:
                st.metric("Longitude", str(longitude_col) if longitude_col else "Not detected")
            with q3:
                st.metric("Mn Columns", len(manganese_cols))
            with q4:
                st.metric("Numeric Features", len(numeric_columns))

            quality = pd.DataFrame({
                "Check": [
                    "Rows available",
                    "Missing values",
                    "Duplicate rows",
                    "Numeric features",
                    "Latitude detected",
                    "Longitude detected",
                    "Manganese-related column"
                ],
                "Result": [
                    "PASS" if len(manganese_data) > 0 else "FAIL",
                    "PASS" if int(manganese_data.isna().sum().sum()) == 0 else "CHECK",
                    "PASS" if int(manganese_data.duplicated().sum()) == 0 else "CHECK",
                    "PASS" if numeric_columns else "CHECK",
                    "PASS" if latitude_col else "NOT FOUND",
                    "PASS" if longitude_col else "NOT FOUND",
                    "FOUND" if manganese_cols else "NOT FOUND"
                ]
            })
            st.dataframe(quality, width="stretch", hide_index=True)

            missing = manganese_data.isna().sum()
            missing = missing[missing > 0].sort_values(ascending=False)
            if not missing.empty:
                st.subheader("⚠️ Missing Data by Column")
                st.dataframe(
                    missing.rename("Missing Values").to_frame(),
                    width="stretch"
                )
            else:
                st.success("✅ No missing values detected.")

        # --------------------------------------------------------
        # EXPLORATION VISUALS
        # --------------------------------------------------------
        with tab_visuals:
            st.subheader("📈 Feature Exploration")

            if numeric_columns:
                selected_feature = st.selectbox(
                    "Select numeric feature",
                    numeric_columns,
                    key="mn_exploration_feature"
                )

                fig_feature = px.histogram(
                    manganese_data,
                    x=selected_feature,
                    nbins=30,
                    template="plotly_dark",
                    title=f"Distribution of {selected_feature}"
                )
                st.plotly_chart(
                    fig_feature,
                    width="stretch",
                    key="mn_exploration_histogram"
                )

                if len(numeric_columns) >= 2:
                    c1, c2 = st.columns(2)
                    with c1:
                        x_feature = st.selectbox(
                            "X-axis feature",
                            numeric_columns,
                            key="mn_exploration_x"
                        )
                    with c2:
                        y_feature = st.selectbox(
                            "Y-axis feature",
                            numeric_columns,
                            index=1 if len(numeric_columns) > 1 else 0,
                            key="mn_exploration_y"
                        )

                    scatter_df = manganese_data[[x_feature, y_feature]].dropna()
                    fig_scatter = px.scatter(
                        scatter_df,
                        x=x_feature,
                        y=y_feature,
                        template="plotly_dark",
                        title=f"{x_feature} vs {y_feature}"
                    )
                    st.plotly_chart(
                        fig_scatter,
                        width="stretch",
                        key="mn_exploration_scatter"
                    )

            else:
                st.info("Numeric exploration features are required for these charts.")

            if latitude_col and longitude_col:
                map_df = manganese_data[[latitude_col, longitude_col]].copy()
                map_df[latitude_col] = pd.to_numeric(map_df[latitude_col], errors="coerce")
                map_df[longitude_col] = pd.to_numeric(map_df[longitude_col], errors="coerce")
                map_df = map_df.dropna()

                if not map_df.empty:
                    st.subheader("📍 Exploration Coordinates")
                    fig_coordinates = px.scatter_map(
                        map_df,
                        lat=latitude_col,
                        lon=longitude_col,
                        zoom=5,
                        height=480,
                        template="plotly_dark",
                        title="Uploaded Exploration Locations"
                    )
                    fig_coordinates.update_layout(map_style="open-street-map")
                    st.plotly_chart(
                        fig_coordinates,
                        width="stretch",
                        key="mn_exploration_coordinates"
                    )
                else:
                    st.warning("Latitude and longitude columns were detected, but no valid coordinate pairs were found.")
            else:
                st.info("Latitude/longitude columns were not detected, so a coordinate view cannot be generated yet.")

        # --------------------------------------------------------
        # PROSPECTIVITY MAP
        # --------------------------------------------------------
        st.divider()
        st.subheader("🗺️ Manganese Prospectivity Map")
        st.caption(
            "Spatial visualization of the actual Laptop 1 exploration inputs. "
            "No artificial prospectivity score is generated here."
        )

        if latitude_col and longitude_col:
            prospectivity_options = [
                col for col in manganese_cols
                if col in numeric_columns
            ]

            if prospectivity_options:
                prospectivity_field = st.selectbox(
                    "Manganese exploration field",
                    prospectivity_options,
                    key="mn_prospectivity_field"
                )

                prospectivity_df = manganese_data[
                    [latitude_col, longitude_col, prospectivity_field]
                ].copy()

                prospectivity_df["__lat"] = pd.to_numeric(
                    prospectivity_df[latitude_col], errors="coerce"
                )
                prospectivity_df["__lon"] = pd.to_numeric(
                    prospectivity_df[longitude_col], errors="coerce"
                )
                prospectivity_df["__mn"] = pd.to_numeric(
                    prospectivity_df[prospectivity_field], errors="coerce"
                )
                prospectivity_df = prospectivity_df.dropna(
                    subset=["__lat", "__lon", "__mn"]
                )

                if not prospectivity_df.empty:
                    fig_prospectivity = px.scatter_map(
                        prospectivity_df,
                        lat="__lat",
                        lon="__lon",
                        color="__mn",
                        hover_data={
                            "__lat": False,
                            "__lon": False,
                            prospectivity_field: True
                        },
                        zoom=5,
                        height=520,
                        template="plotly_dark",
                        title=f"Uploaded {prospectivity_field} Distribution"
                    )
                    fig_prospectivity.update_layout(
                        map_style="open-street-map",
                        margin=dict(l=0, r=0, t=50, b=0)
                    )
                    st.plotly_chart(
                        fig_prospectivity,
                        width="stretch",
                        key="mn_prospectivity_map"
                    )
                    st.success(
                        "Prospectivity view generated from the uploaded "
                        f"Laptop 1 field: {prospectivity_field}"
                    )
                else:
                    st.warning(
                        "The selected manganese field has no valid coordinate/value pairs."
                    )
            else:
                st.info(
                    "No numeric manganese field was detected. Upload a dataset "
                    "with latitude/longitude and a numeric Mn/manganese field "
                    "to enable this map."
                )
        else:
            st.info(
                "Latitude/longitude columns are required for the prospectivity map."
            )

        # --------------------------------------------------------
        # MANGANESE PRIORITY MAP
        # --------------------------------------------------------
        st.divider()
        st.subheader("🎯 Manganese Priority Map")
        st.caption(
            "Displays a priority/prospectivity field supplied by Laptop 1. "
            "The interface does not invent a priority score."
        )

        priority_candidates = [
            col for col in manganese_data.columns
            if any(
                token in str(col).strip().lower()
                for token in (
                    "priority",
                    "prospectivity",
                    "priority_score",
                    "prospectivity_score",
                    "target_score"
                )
            )
        ]

        if latitude_col and longitude_col:
            if priority_candidates:
                priority_field = st.selectbox(
                    "Laptop 1 priority field",
                    priority_candidates,
                    key="mn_priority_field"
                )

                priority_df = manganese_data[
                    [latitude_col, longitude_col, priority_field]
                ].copy()

                priority_df["__lat"] = pd.to_numeric(
                    priority_df[latitude_col], errors="coerce"
                )
                priority_df["__lon"] = pd.to_numeric(
                    priority_df[longitude_col], errors="coerce"
                )
                priority_df["__priority"] = pd.to_numeric(
                    priority_df[priority_field], errors="coerce"
                )
                priority_df = priority_df.dropna(
                    subset=["__lat", "__lon", "__priority"]
                )

                if not priority_df.empty:
                    fig_priority = px.scatter_map(
                        priority_df,
                        lat="__lat",
                        lon="__lon",
                        color="__priority",
                        hover_data={
                            "__lat": False,
                            "__lon": False,
                            priority_field: True
                        },
                        zoom=5,
                        height=520,
                        template="plotly_dark",
                        title=f"Laptop 1 Priority: {priority_field}"
                    )
                    fig_priority.update_layout(
                        map_style="open-street-map",
                        margin=dict(l=0, r=0, t=50, b=0)
                    )
                    st.plotly_chart(
                        fig_priority,
                        width="stretch",
                        key="mn_priority_map"
                    )
                else:
                    st.warning(
                        "The selected priority field has no valid geographic records."
                    )
            else:
                st.info(
                    "No priority/prospectivity output is present in the current "
                    "Laptop 1 dataset. Once Laptop 1 supplies a field such as "
                    "'priority_score' or 'prospectivity_score', it will appear here."
                )
        else:
            st.info(
                "Latitude/longitude columns are required for the priority map."
            )

        # --------------------------------------------------------
        # LAPTOP 1 HANDOFF
        # --------------------------------------------------------
        with tab_handoff:
            st.subheader("🔗 Laptop 1 Processing Handoff")

            h1, h2, h3 = st.columns(3)
            with h1:
                st.success("🟢 DATA LOADED")
            with h2:
                st.info("⏳ MODEL INPUT READY")
            with h3:
                st.info("⏳ PREDICTION WAITING")

            if numeric_columns:
                st.write("**Numeric features available to the future model pipeline:**")
                st.write(", ".join(map(str, numeric_columns)))
            else:
                st.warning("No numeric features are available for model processing.")

            if st.button(
                "📤 Set as Active Laptop 1 Dataset",
                width="stretch",
                key="activate_manganese_dataset"
            ):
                st.session_state["active_manganese_data"] = manganese_data.copy()
                st.session_state["active_manganese_filename"] = st.session_state.get("manganese_filename")
                st.success("✅ This dataset is now the active Laptop 1 input.")

            active_name = st.session_state.get("active_manganese_filename")
            if active_name:
                st.success(f"Active dataset: {active_name}")
            else:
                st.caption("No dataset has been activated for the Laptop 1 pipeline yet.")

            st.download_button(
                "⬇️ Download Current Dataset",
                data=manganese_data.to_csv(index=False).encode("utf-8"),
                file_name="manganese_exploration_export.csv",
                mime="text/csv",
                width="stretch",
                key="mn_download_dataset"
            )

            st.info(
                "The interface prepares and stores the exploration data, but it does not claim to produce a manganese prospectivity prediction until the trained Laptop 1 model is connected."
            )


# ============================================================
# RISK DETECTION PAGE
# ============================================================

if page == "⚠️ Risk Detection":

    st.title("⚠️ Risk & Anomaly Detection")

    st.write(
        "Monitor operational conditions and identify potential anomalies."
    )

    st.divider()

    # ========================================================
    # RISK SCORE
    # ========================================================

    risk_score = st.slider(
        "Risk Threshold",
        0,
        100,
        24,
        key="risk_score_slider"
    )

    if risk_score < 30:

        st.success("🟢 LOW RISK")

    elif risk_score < 70:

        st.warning("🟡 MEDIUM RISK")

    else:

        st.error("🔴 HIGH RISK")

    st.progress(risk_score / 100)

    st.divider()

    # ========================================================
    # SENSOR MONITORING
    # ========================================================

    st.subheader("📡 Sensor Monitoring")

    sensor1, sensor2, sensor3, sensor4 = st.columns(4)

    with sensor1:
        st.metric(
            "Temperature",
            f"{average_temperature:.1f} °C"
        )

    with sensor2:
        st.metric(
            "Vibration",
            f"{average_vibration:.2f} mm/s"
        )

    with sensor3:
        st.metric(
            "Pressure",
            f"{average_pressure:.2f} bar"
        )

    with sensor4:
        st.metric(
            "Efficiency",
            f"{average_efficiency:.1f}%"
        )

    st.divider()

    # ========================================================
    # ANOMALY STATUS
    # ========================================================

    st.subheader("🔎 Detected Anomalies")

    anomaly_data = pd.DataFrame({
        "Parameter": [
            "Temperature",
            "Vibration",
            "Pressure",
            "Efficiency"
        ],

        "Current Value": [
            f"{average_temperature:.1f} °C",
            f"{average_vibration:.2f} mm/s",
            f"{average_pressure:.2f} bar",
            f"{average_efficiency:.1f}%"
        ],

        "Status": [
            "Monitoring",
            "Monitoring",
            "Monitoring",
            "Monitoring"
        ],

        "AI Status": [
            "Waiting for model",
            "Waiting for model",
            "Waiting for model",
            "Waiting for model"
        ]
    })

    st.dataframe(
        anomaly_data,
        width="stretch",
        hide_index=True
    )

    st.info(
        "Actual anomaly detection will be connected to "
        "the trained model from Laptop 1."
    )


# ============================================================
# DATA ANALYSIS PAGE
# ============================================================

elif page == "📁 Data Analysis":

    st.title(
        "📁 Mining Data Analysis"
    )

    st.write(
        "Upload operational data and automatically explore the dataset."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"],
        key="data_analysis_upload"
    )

    if uploaded_file:

        data = pd.read_csv(
            uploaded_file
        )

        st.success(
            f"Successfully loaded {uploaded_file.name}"
        )

        st.divider()

        d1, d2, d3, d4 = st.columns(4)

        with d1:

            st.metric(
                "Rows",
                f"{len(data):,}"
            )

        with d2:

            st.metric(
                "Columns",
                len(data.columns)
            )

        with d3:

            st.metric(
                "Missing Values",
                int(
                    data.isna().sum().sum()
                )
            )

        with d4:

            st.metric(
                "Numeric Columns",
                len(
                    data.select_dtypes(
                        include=np.number
                    ).columns
                )
            )

        st.divider()

        tab1, tab2, tab3 = st.tabs(
            [
                "📋 Dataset",
                "📊 Statistics",
                "📈 Visualization"
            ]
        )

        with tab1:

            st.dataframe(
                data,
                width="stretch",
                hide_index=True
            )

        with tab2:

            st.dataframe(
                data.describe(),
                width="stretch"
            )

        with tab3:

            numeric_columns = list(
                data.select_dtypes(
                    include=np.number
                ).columns
            )

            if numeric_columns:

                selected_column = st.selectbox(
                    "Select variable",
                    numeric_columns,
                    key="data_analysis_variable"
                )

                fig = px.histogram(
                    data,
                    x=selected_column,
                    template="plotly_dark"
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                    key="data_analysis_histogram"
                )

            else:

                st.info(
                    "No numerical columns found."
                )

    else:

        st.info(
            "Upload a CSV file to begin analysis."
        )


# ============================================================
# SYSTEM PAGE
# ============================================================

elif page == "⚙️ System":

    st.title(
        "⚙️ System Information"
    )

    st.divider()

    st.subheader(
        "🟢 Platform Status"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.success(
            "AI Engine\n\nONLINE"
        )

    with c2:

        st.success(
            "Data Pipeline\n\nONLINE"
        )

    with c3:

        st.success(
            "Dashboard\n\nONLINE"
        )

    st.divider()

    st.subheader(
        "🤖 Model Information"
    )

    model_info = pd.DataFrame({

        "Property": [
            "Model Status",
            "Model Version",
            "Prediction Mode",
            "Confidence",
            "Data Source"
        ],

        "Value": [
            "Not connected",
            "Not loaded",
            "Awaiting trained model",
            "—",
            st.session_state.get("manganese_filename") or "Built-in operational dataset"
        ]
    })

    st.dataframe(
        model_info,
        width="stretch",
        hide_index=True
    )

    st.divider()

    st.info(
        "⚠️ The current prediction engine is running in "
        "DEMO mode. The trained ML model from Laptop 1 "
        "will be connected here during final integration."
    )