import os
import streamlit as st
from PIL import Image
import pandas as pd

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Cloud Resource Scheduler",
    layout="wide"
)

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

    with st.spinner("Running cloud scheduling simulation..."):

        os.system("gcc input_generator.c -o builds/gen")

        os.system("g++ -std=c++17 main.cpp -o builds/run")

        os.system("./builds/gen")

        os.system("./builds/run")

        python_exec = "venv/bin/python"

        if not os.path.exists(python_exec):
            python_exec = "python3"

        os.system(f"{python_exec} charts.py")

    st.success("Simulation completed successfully")

    st.rerun()
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

    col5, col6, col7, col8 = st.columns(4)
    with col5:

        st.metric(
            "CPU Utilization",
            f"{online['CPU']:.2f}%"
        )


    with col6:

        st.metric(
            "Storage Utilization",
            f"{online['Storage']:.2f}%"
        )
    with col7:

        st.metric(
            "RAM Utilization",
            f"{online['RAM']:.2f}%"
        )
    with col8:

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
        width="stretch"
    )

    st.divider()

# ==========================================
# VISUAL ANALYTICS
# ==========================================

st.header("Visual Analytics")

# ==========================================
# TOP GRID CHARTS
# ==========================================

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

    # ======================================
    # LEFT CHART
    # ======================================

    with col1:

        title, path = top_charts[i]

        if os.path.exists(path):

            st.subheader(title)

            image = Image.open(path)

            st.image(
                image,
                width="stretch"
            )

    # ======================================
    # RIGHT CHART
    # ======================================

    with col2:

        title, path = top_charts[i + 1]

        if os.path.exists(path):

            st.subheader(title)

            image = Image.open(path)

            st.image(
                image,
                width="stretch"
            )
            st.divider()

# ==========================================
# PIE CHART SEPARATELY
# ==========================================

st.subheader("Job Distribution")

center_col1, center_col2, center_col3 = st.columns([1, 2, 1])

with center_col2:

    pie_chart = "outputs/visualizations/job_distribution.png"

    if os.path.exists(pie_chart):

        image = Image.open(pie_chart)

        st.image(
            image,
            width="stretch"
        )

    else:

        st.warning("Job distribution chart not available.")