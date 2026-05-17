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

        try:
            generate_charts()
        except Exception as e:
            st.error(f"Chart generation failed: {e}")
            st.stop()

        # Store timestamp so image loader knows to bust cache
        st.session_state["sim_ts"] = time.time()

    st.success("Simulation completed successfully")
    st.rerun()

# ==========================================
# LOAD METRICS
# ==========================================

metrics_path = os.path.join(APP_DIR, "outputs", "metrics", "metrics.csv")

if os.path.exists(metrics_path):
    # Re-read fresh from disk every time (no caching)
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
    """Force fresh read from disk, bypassing any Streamlit cache."""
    with open(path, "rb") as f:
        return f.read()

top_charts = [
    ("Revenue Growth",              "revenue_growth.png"),
    ("Greedy Resource Utilization", "greedy_resource_utilization.png"),
    ("Online Resource Utilization", "online_resource_utilization.png"),
    ("Queue Pressure",              "queue_pressure.png"),
]

for i in range(0, len(top_charts), 2):
    col1, col2 = st.columns(2)

    with col1:
        title, fname = top_charts[i]
        path = os.path.join(VIZ, fname)
        if os.path.exists(path):
            st.subheader(title)
            st.image(load_image(path), use_container_width=True)
        else:
            st.warning(f"{title} not available.")

    with col2:
        title, fname = top_charts[i + 1]
        path = os.path.join(VIZ, fname)
        if os.path.exists(path):
            st.subheader(title)
            st.image(load_image(path), use_container_width=True)
        else:
            st.warning(f"{title} not available.")

    st.divider()

# PIE CHART
st.subheader("Job Distribution")
_, center_col, _ = st.columns([1, 2, 1])

with center_col:
    pie_path = os.path.join(VIZ, "job_distribution.png")
    if os.path.exists(pie_path):
        st.image(load_image(pie_path), use_container_width=True)
    else:
        st.warning("Job distribution chart not available.")