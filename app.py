import os
import time
import streamlit as st
from PIL import Image
import pandas as pd
from charts import generate_charts

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Cloud Resource Scheduler",
    layout="wide"
)

# ==========================================
# SESSION STATE
# ==========================================

if "run_id" not in st.session_state:
    st.session_state["run_id"] = "default"

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

st.caption(
    "Cloud-native resource scheduling simulation with analytics and DevOps automation."
)

st.divider()

# ==========================================
# RUN BUTTON
# ==========================================

if st.button("Run Simulation"):

    run_id = str(int(time.time()))

    st.session_state["run_id"] = run_id

    with st.spinner("Running cloud scheduling simulation..."):

        os.system("gcc input_generator.c -o builds/gen")

        os.system("g++ -std=c++17 main.cpp -o builds/run")

        os.system("./builds/gen")

        os.system("./builds/run")

        generate_charts(run_id)

    st.success("Simulation completed successfully")

# ==========================================
# LOAD METRICS
# ==========================================

metrics_path = "outputs/metrics/metrics.csv"

if os.path.exists(metrics_path):

    metrics = pd.read_csv(metrics_path)

    online = metrics.iloc[1]

    # ======================================
    # KPI METRICS
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
            "CPU Utilization",
            f"{online['CPU']:.2f}%"
        )

    col5, col6, col7 = st.columns(3)

    with col5:
        st.metric(
            "Storage Utilization",
            f"{online['Storage']:.2f}%"
        )

    with col6:
        st.metric(
            "RAM Utilization",
            f"{online['RAM']:.2f}%"
        )

    with col7:
        st.metric(
            "Bandwidth Utilization",
            f"{online['BW']:.2f}%"
        )

    st.divider()

    # ======================================
    # METRICS TABLE
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

import time

timestamp = int(time.time())

top_charts = [

    (
        "Revenue Growth",
        "outputs/visualizations/revenue_growth.png"
    ),

    (
        "Greedy Resource Utilization",
        "outputs/visualizations/greedy_resource_utilization.png"
    ),

    (
        "Online Resource Utilization",
        "outputs/visualizations/online_resource_utilization.png"
    ),

    (
        "Queue Pressure",
        "outputs/visualizations/queue_pressure.png"
    )
]

for i in range(0, len(top_charts), 2):

    col1, col2 = st.columns(2)

    with col1:

        title, path = top_charts[i]

        if os.path.exists(path):

            st.subheader(title)

            with open(path, "rb") as img:
                st.image(
                    img.read(),
                    width="stretch"
                )

    with col2:

        title, path = top_charts[i + 1]

        if os.path.exists(path):

            st.subheader(title)

            with open(path, "rb") as img:
                st.image(
                    img.read(),
                    width="stretch"
                )

    st.divider()

# ==========================================
# PIE CHART
# ==========================================

st.subheader("Job Distribution")

center1, center2, center3 = st.columns([1,2,1])

with center2:

    pie_chart = "outputs/visualizations/job_distribution.png"

    if os.path.exists(pie_chart):

        with open(pie_chart, "rb") as img:
            st.image(
                img.read(),
                width="stretch"
            )

    else:

        st.warning("Job distribution chart not available.")