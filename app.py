import os
import sys
import time
import streamlit as st
from PIL import Image
import pandas as pd

# Fix working directory on EC2
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
# CSS
# ==========================================

st.markdown("""
<style>

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
[data-testid="stToolbar"] { visibility: hidden; }

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.stApp {
    background-color: white;
}

/* Fix metric label, value and delta all black on white */
[data-testid="stMetric"] {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px;
}

[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-size: 14px !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] > div {
    color: #0f172a !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* Dataframe text */
.dataframe { color: black !important; }

/* All general text black */
p, h1, h2, h3, h4, label {
    color: #0f172a !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Cloud Scheduler")
st.sidebar.markdown("""
### Features
- Greedy Scheduling
- Online Scheduling
- Queue Simulation
- Resource Allocation
- Runtime Analytics
- Docker Deployment
- CI/CD Automation
""")

# ==========================================
# TITLE
# ==========================================

st.title("Cloud Resource Scheduler Dashboard")
st.caption("Dynamic cloud resource scheduling simulation using Greedy and Online algorithms.")
st.divider()

# ==========================================
# RUN BUTTON
# ==========================================

VIZ_DIR = os.path.join(APP_DIR, "outputs", "visualizations")

if st.button("▶ Run Simulation"):
    with st.spinner("Running simulation..."):

        # Clear old charts
        if os.path.exists(VIZ_DIR):
            for f in os.listdir(VIZ_DIR):
                if f.endswith(".png"):
                    os.remove(os.path.join(VIZ_DIR, f))

        os.system("gcc input_generator.c -o builds/gen")
        os.system("g++ -std=c++17 main.cpp -o builds/run")
        os.system("./builds/gen")
        os.system("./builds/run")

        run_id = str(int(time.time()))
        try:
            generate_charts()
        except Exception as e:
            st.error(f"Chart generation failed: {e}")
            st.stop()

        st.session_state["run_id"] = run_id
        st.cache_data.clear()
        st.cache_resource.clear()

    st.success("✅ Simulation completed")
    st.rerun()

# ==========================================
# HELPER
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
    return max(candidates, key=os.path.getmtime) if candidates else None

# ==========================================
# LOAD METRICS
# ==========================================

metrics_path = os.path.join(APP_DIR, "outputs", "metrics", "metrics.csv")

if os.path.exists(metrics_path):
    metrics = pd.read_csv(metrics_path)
    online  = metrics.iloc[1]

    st.header("System Metrics")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Revenue",       f"${int(online['Revenue'])}")
    with col2:
        st.metric("✅ Accepted Jobs", int(online["Accepted"]))
    with col3:
        st.metric("❌ Rejected Jobs", int(online["Rejected"]))
    with col4:
        st.metric("🖥️ CPU Usage",    f"{online['CPU']:.2f}%")

    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("💾 Storage",   f"{online['Storage']:.2f}%")
    with col6:
        st.metric("🧠 RAM",       f"{online['RAM']:.2f}%")
    with col7:
        st.metric("📡 Bandwidth", f"{online['BW']:.2f}%")

    st.divider()

    st.header("Detailed Metrics")
    st.dataframe(metrics, use_container_width=True)
    st.divider()

# ==========================================
# VISUAL ANALYTICS
# ==========================================

st.header("Visual Analytics")

charts = [
    ("Revenue Growth",              "revenue_growth"),
    ("Queue Pressure",              "queue_pressure"),
    ("Greedy Resource Utilization", "greedy_resource_utilization"),
    ("Online Resource Utilization", "online_resource_utilization"),
]

for i in range(0, len(charts), 2):
    col1, col2 = st.columns(2)

    with col1:
        title, base = charts[i]
        path = get_chart_path(base)
        if path:
            st.subheader(title)
            st.image(load_image(path), use_container_width=True)

    with col2:
        title, base = charts[i + 1]
        path = get_chart_path(base)
        if path:
            st.subheader(title)
            st.image(load_image(path), use_container_width=True)

    st.divider()

# ==========================================
# JOB DISTRIBUTION
# ==========================================

st.header("Job Distribution")

pie_path = get_chart_path("job_distribution")
if pie_path:
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.image(load_image(pie_path), width=500)
else:
    st.warning("Job distribution chart not found.")