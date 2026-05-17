import os
import sys
import time
import streamlit as st
from PIL import Image
import pandas as pd

# ==========================================
# FIX WORKING DIRECTORY
# ==========================================

APP_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

os.chdir(APP_DIR)

sys.path.insert(0, APP_DIR)

from charts import generate_charts

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Cloud Resource Scheduler",
    page_icon="☁️",
    layout="wide"
)

# ==========================================
# CLEAN LIGHT THEME
# ==========================================

st.markdown("""
<style>

/* Hide Streamlit UI */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    visibility: hidden;
}

/* Main App */

.stApp {
    background-color: #ffffff;
}

/* Padding */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Titles */

h1, h2, h3, h4, p, label {
    color: #111827 !important;
}

/* Metric Cards */

[data-testid="stMetric"] {

    background-color: #f8fafc;

    border: 1px solid #dbeafe;

    border-radius: 12px;

    padding: 18px;
}

/* Metric Labels */

[data-testid="stMetricLabel"] {

    color: #475569 !important;

    font-size: 14px !important;

    font-weight: 600 !important;
}

/* Metric Values */

[data-testid="stMetricValue"] {

    color: #111827 !important;

    font-size: 30px !important;

    font-weight: bold !important;
}

/* Dataframe */

[data-testid="stDataFrame"] {

    border: 1px solid #e5e7eb;

    border-radius: 10px;
}

/* Buttons */

.stButton > button {

    background-color: #2563eb;

    color: white;

    border: none;

    border-radius: 8px;

    padding: 10px 22px;

    font-size: 16px;

    font-weight: 600;
}

/* Button Hover */

.stButton > button:hover {

    background-color: #1d4ed8;

    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================

st.title(
    "Cloud Resource Scheduler Dashboard"
)

st.caption(
    "Dynamic cloud resource scheduling simulation using Greedy and Online algorithms."
)

st.divider()

# ==========================================
# RUN BUTTON
# ==========================================

VIZ_DIR = os.path.join(
    APP_DIR,
    "outputs",
    "visualizations"
)

if st.button("Run Simulation"):

    with st.spinner(
        "Running simulation..."
    ):

        # CLEAR OLD CHARTS

        if os.path.exists(VIZ_DIR):

            for file in os.listdir(VIZ_DIR):

                if file.endswith(".png"):

                    os.remove(
                        os.path.join(
                            VIZ_DIR,
                            file
                        )
                    )

        # COMPILE INPUT GENERATOR

        os.system(
            "gcc input_generator.c -o builds/gen"
        )

        # COMPILE MAIN PROGRAM

        os.system(
            "g++ -std=c++17 main.cpp -o builds/run"
        )

        # GENERATE INPUT

        os.system("./builds/gen")

        # RUN SCHEDULER

        os.system("./builds/run")

        # GENERATE CHARTS

        run_id = str(
            int(time.time())
        )

        generate_charts(run_id)

        st.cache_data.clear()

        st.cache_resource.clear()

    st.success(
        "Simulation completed successfully"
    )

    st.rerun()

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def load_image(path):

    with open(path, "rb") as f:

        return f.read()

def get_chart_path(base_name):

    if not os.path.exists(VIZ_DIR):

        return None

    candidates = [

        os.path.join(VIZ_DIR, file)

        for file in os.listdir(VIZ_DIR)

        if file.startswith(base_name)

        and file.endswith(".png")
    ]

    if not candidates:

        return None

    return max(
        candidates,
        key=os.path.getmtime
    )

# ==========================================
# LOAD METRICS
# ==========================================

metrics_path = os.path.join(
    APP_DIR,
    "outputs",
    "metrics",
    "metrics.csv"
)

if os.path.exists(metrics_path):

    metrics = pd.read_csv(metrics_path)

    online = metrics.iloc[1]

    # ======================================
    # SYSTEM METRICS
    # ======================================

    st.header("System Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Revenue",
            f"${int(online['Revenue'])}"
        )

    with col2:

        st.metric(
            "Accepted Jobs",
            int(online["Accepted"])
        )

    with col3:

        st.metric(
            "Rejected Jobs",
            int(online["Rejected"])
        )

    with col4:

        st.metric(
            "CPU Usage",
            f"{online['CPU']:.2f}%"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col5, col6, col7 = st.columns(3)

    with col5:

        st.metric(
            "Storage Usage",
            f"{online['Storage']:.2f}%"
        )

    with col6:

        st.metric(
            "RAM Usage",
            f"{online['RAM']:.2f}%"
        )

    with col7:

        st.metric(
            "Bandwidth Usage",
            f"{online['BW']:.2f}%"
        )

    st.divider()

    # ======================================
    # TABLE
    # ======================================

    st.header("Detailed Metrics")

    st.dataframe(
        metrics,
        use_container_width=True
    )

    st.divider()

# ==========================================
# VISUAL ANALYTICS
# ==========================================

st.header("Visual Analytics")

charts = [

    (
        "Revenue Growth",
        "revenue_growth"
    ),

    (
        "Queue Pressure",
        "queue_pressure"
    ),

    (
        "Greedy Resource Utilization",
        "greedy_resource_utilization"
    ),

    (
        "Online Resource Utilization",
        "online_resource_utilization"
    )
]

# ==========================================
# DISPLAY CHARTS
# ==========================================

for i in range(0, len(charts), 2):

    col1, col2 = st.columns(2)

    # LEFT CHART

    with col1:

        title, base = charts[i]

        path = get_chart_path(base)

        if path:

            st.subheader(title)

            st.image(
                load_image(path),
                use_container_width=True
            )

    # RIGHT CHART

    with col2:

        title, base = charts[i + 1]

        path = get_chart_path(base)

        if path:

            st.subheader(title)

            st.image(
                load_image(path),
                use_container_width=True
            )

    st.divider()

# ==========================================
# JOB DISTRIBUTION
# ==========================================

st.header("Job Distribution")

pie_path = get_chart_path(
    "job_distribution"
)

if pie_path:

    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:

        st.image(
            load_image(pie_path),
            width=450
        )

else:

    st.warning(
        "Job distribution chart not found."
    )