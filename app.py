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

st.set_page_config(page_title="Cloud Resource Scheduler", layout="wide")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("Cloud Scheduler")
st.sidebar.markdown("""
### Features
- Online Scheduling
- Greedy Scheduling
- Runtime Analytics
- Docker Deployment
- GitHub Actions CI/CD
- Cloud Deployment
""")

# ==========================================
# TITLE
# ==========================================

st.title("Cloud Resource Scheduler Dashboard")
st.caption("Cloud-native resource scheduling simulation with analytics and DevOps automation.")
st.divider()

# ==========================================
# RUN BUTTON
# ==========================================

if st.button("Run Simulation"):
    with st.spinner("Running cloud scheduling simulation..."):

        ret1 = os.system("gcc input_generator.c -o builds/gen")
        ret2 = os.system("g++ -std=c++17 main.cpp -o builds/run")

        if ret1 != 0 or ret2 != 0:
            st.error("Compilation failed. Check gcc/g++ and source files.")
            st.stop()

        os.system("./builds/gen")
        os.system("./builds/run")

        # Use timestamp as run_id — matches what charts.py saves
        run_id = str(int(time.time()))

        try:
            generate_charts(run_id)
        except Exception as e:
            st.error(f"Chart generation failed: {e}")
            st.stop()

        st.session_state["run_id"] = run_id

    st.success("Simulation completed successfully")
    st.rerun()

# ==========================================
# LOAD METRICS
# ==========================================

metrics_path = os.path.join(APP_DIR, "outputs", "metrics", "metrics.csv")

if os.path.exists(metrics_path):
    metrics = pd.read_csv(metrics_path)
    online = metrics.iloc[1]

    st.header("System Metrics")

    col1, col2, col3, _ = st.columns(4)
    with col1:
        st.metric("Revenue", f"${int(online['Revenue'])}")
    with col2:
        st.metric("Accepted Jobs", int(online["Accepted"]))
    with col3:
        st.metric("Rejected Jobs", int(online["Rejected"]))

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("CPU Utilization", f"{online['CPU']:.2f}%")
    with col6:
        st.metric("Storage Utilization", f"{online['Storage']:.2f}%")
    with col7:
        st.metric("RAM Utilization", f"{online['RAM']:.2f}%")
    with col8:
        st.metric("Bandwidth Utilization", f"{online['BW']:.2f}%")

    st.divider()

    st.header("Detailed Metrics")
    st.dataframe(metrics, use_container_width=True)
    st.divider()

# ==========================================
# VISUAL ANALYTICS
# ==========================================

st.header("Visual Analytics")

VIZ = os.path.join(APP_DIR, "outputs", "visualizations")

def load_image(path):
    with open(path, "rb") as f:
        return f.read()

# Use the run_id from this session, else fall back to latest file on disk
run_id = st.session_state.get("run_id", None)

def get_path(base_name):
    """Return timestamped path if available, else fall back to any match."""
    if run_id:
        p = os.path.join(VIZ, f"{base_name}_{run_id}.png")
        if os.path.exists(p):
            return p
    # Fallback: find the most recently modified matching file
    candidates = [
        os.path.join(VIZ, f) for f in os.listdir(VIZ)
        if f.startswith(base_name) and f.endswith(".png")
    ]
    if candidates:
        return max(candidates, key=os.path.getmtime)
    return None

top_charts = [
    ("Revenue Growth",              "revenue_growth"),
    ("Greedy Resource Utilization", "greedy_resource_utilization"),
    ("Online Resource Utilization", "online_resource_utilization"),
    ("Queue Pressure",              "queue_pressure"),
]

for i in range(0, len(top_charts), 2):
    col1, col2 = st.columns(2)

    with col1:
        title, base = top_charts[i]
        path = get_path(base)
        if path:
            st.subheader(title)
            st.image(load_image(path), use_container_width=True)
        else:
            st.warning(f"{title} not available.")

    with col2:
        title, base = top_charts[i + 1]
        path = get_path(base)
        if path:
            st.subheader(title)
            st.image(load_image(path), use_container_width=True)
        else:
            st.warning(f"{title} not available.")

    st.divider()

# PIE CHART
st.subheader("Job Distribution")
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    path = get_path("job_distribution")
    if path:
        st.image(load_image(path), use_container_width=True)
    else:
        st.warning("Job distribution chart not available.")