import os
import streamlit as st
from PIL import Image
import pandas as pd
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
# SIMPLE CLEAN UI
# ==========================================
st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.stApp {
    background-color: white;
    color: black;
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

st.caption(
    "Dynamic cloud resource scheduling simulation using Greedy and Online algorithms."
)

st.divider()

# ==========================================
# RUN BUTTON
# ==========================================

if st.button("Run Simulation"):

    with st.spinner("Running simulation..."):

        # Clear old charts
        if os.path.exists("outputs/visualizations"):

            for file in os.listdir("outputs/visualizations"):

                if file.endswith(".png"):

                    os.remove(
                        os.path.join(
                            "outputs/visualizations",
                            file
                        )
                    )

        # Compile generator
        os.system(
            "gcc input_generator.c -o builds/gen"
        )

        # Compile scheduler
        os.system(
            "g++ -std=c++17 main.cpp -o builds/run"
        )

        # Generate jobs
        os.system("./builds/gen")

        # Run simulation
        os.system("./builds/run")

        # Generate charts
        generate_charts()

        st.cache_data.clear()
        st.cache_resource.clear()

    st.success("Simulation completed")

    st.rerun()

# ==========================================
# LOAD METRICS
# ==========================================

metrics_path = "outputs/metrics/metrics.csv"

if os.path.exists(metrics_path):

    metrics = pd.read_csv(metrics_path)

    online = metrics.iloc[1]

    # ======================================
    # METRICS
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

    col5, col6, col7 = st.columns(3)

    with col5:
        st.metric(
            "Storage",
            f"{online['Storage']:.2f}%"
        )

    with col6:
        st.metric(
            "RAM",
            f"{online['RAM']:.2f}%"
        )

    with col7:
        st.metric(
            "Bandwidth",
            f"{online['BW']:.2f}%"
        )

    st.divider()

    # ======================================
    # DETAILED TABLE
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
        "outputs/visualizations/revenue_growth.png"
    ),

    (
        "Queue Pressure",
        "outputs/visualizations/queue_pressure.png"
    ),

    (
        "Greedy Resource Utilization",
        "outputs/visualizations/greedy_resource_utilization.png"
    ),

    (
        "Online Resource Utilization",
        "outputs/visualizations/online_resource_utilization.png"
    )
]

# ==========================================
# DISPLAY CHARTS
# ==========================================

for i in range(0, len(charts), 2):

    col1, col2 = st.columns(2)

    with col1:

        title, path = charts[i]

        if os.path.exists(path):

            st.subheader(title)

            image = Image.open(path)

            st.image(
                image,
                use_container_width=True
            )

    with col2:

        title, path = charts[i + 1]

        if os.path.exists(path):

            st.subheader(title)

            image = Image.open(path)

            st.image(
                image,
                use_container_width=True
            )

    st.divider()

# ==========================================
# JOB DISTRIBUTION
# ==========================================

st.header("Job Distribution")

pie_path = (
    "outputs/visualizations/job_distribution.png"
)
if os.path.exists(pie_path):

    image = Image.open(pie_path)

    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:

        st.image(
            image,
            width=500
        )

else:

    st.warning(
        "Job distribution chart not found."
    )