import os
import sys
import time
import streamlit as st
import pandas as pd

# ==========================================
# FIX WORKING DIRECTORY
# ==========================================

APP_DIR = os.path.dirname(os.path.abspath(__file__))
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
# SIMPLE CLEAN CSS
# ==========================================

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================

st.title("☁️ Cloud Resource Scheduler Dashboard")
st.write(
    "Dynamic cloud resource scheduling simulation using Greedy and Online algorithms."
)

st.divider()

# ==========================================
# PATHS
# ==========================================

VIZ_DIR = os.path.join(APP_DIR, "outputs", "visualizations")
METRICS_PATH = os.path.join(APP_DIR, "outputs", "metrics", "metrics.csv")

# ==========================================
# RUN SIMULATION
# ==========================================

if st.button("Run Simulation"):

    with st.spinner("Running simulation..."):

        # Clear old images
        if os.path.exists(VIZ_DIR):
            for f in os.listdir(VIZ_DIR):
                if f.endswith(".png"):
                    os.remove(os.path.join(VIZ_DIR, f))

        # Compile and run
        os.system("gcc input_generator.c -o builds/gen")
        os.system("g++ -std=c++17 main.cpp -o builds/run")

        os.system("./builds/gen")
        os.system("./builds/run")

        try:
            generate_charts()
        except Exception as e:
            st.error(f"Chart generation failed: {e}")
            st.stop()

    st.success("Simulation completed successfully")
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
        os.path.join(VIZ_DIR, f)
        for f in os.listdir(VIZ_DIR)
        if f.startswith(base_name) and f.endswith(".png")
    ]

    if not candidates:
        return None

    return max(candidates, key=os.path.getmtime)

# ==========================================
# METRICS
# ==========================================

if os.path.exists(METRICS_PATH):

    metrics = pd.read_csv(METRICS_PATH)

    if len(metrics) > 1:

        online = metrics.iloc[1]

        st.header("System Metrics")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Revenue", f"${int(online['Revenue'])}")
        c2.metric("Accepted Jobs", int(online["Accepted"]))
        c3.metric("Rejected Jobs", int(online["Rejected"]))
        c4.metric("CPU Usage", f"{online['CPU']:.2f}%")

        c5, c6, c7 = st.columns(3)

        c5.metric("Storage", f"{online['Storage']:.2f}%")
        c6.metric("RAM", f"{online['RAM']:.2f}%")
        c7.metric("Bandwidth", f"{online['BW']:.2f}%")

        st.divider()

        st.header("Detailed Metrics")
        st.dataframe(metrics, use_container_width=True)

        st.divider()

# ==========================================
# VISUAL ANALYTICS
# ==========================================

st.header("Visual Analytics")

charts = [
    ("Revenue Growth", "revenue_growth"),
    ("Queue Pressure", "queue_pressure"),
    ("Greedy Resource Utilization", "greedy_resource_utilization"),
    ("Online Resource Utilization", "online_resource_utilization"),
]

for i in range(0, len(charts), 2):

    col1, col2 = st.columns(2)

    # LEFT CHART
    with col1:

        title, base = charts[i]

        path = get_chart_path(base)

        if path:
            st.subheader(title)
            st.image(path, use_container_width=True)

    # RIGHT CHART
    with col2:

        if i + 1 < len(charts):

            title, base = charts[i + 1]

            path = get_chart_path(base)

            if path:
                st.subheader(title)
                st.image(path, use_container_width=True)

    st.divider()

# ==========================================
# JOB DISTRIBUTION
# ==========================================

st.header("Job Distribution")

pie_path = get_chart_path("job_distribution")

if pie_path:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(pie_path, width=400)

else:
    st.warning("Job distribution chart not found.")