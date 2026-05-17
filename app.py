import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Cloud Resource Scheduler",
    page_icon="☁️",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #020817;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid #1e293b;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.metric-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    transition: 0.3s;
}

.metric-card:hover {
    border: 1px solid #3b82f6;
    transform: translateY(-2px);
}

.metric-title {
    color: #94a3b8;
    font-size: 15px;
    margin-bottom: 10px;
}

.metric-value {
    color: white;
    font-size: 32px;
    font-weight: bold;
}

.chart-container {
    background: #0f172a;
    border: 1px solid #1e293b;
    padding: 15px;
    border-radius: 18px;
}

h1, h2, h3 {
    color: white !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("☁️ Cloud Scheduler")

st.sidebar.markdown("""
### Features

- Online Scheduling
- Greedy Scheduling
- Runtime Analytics
- AWS EC2 Deployment
- GitHub Actions CI/CD
- Real-Time Monitoring
""")

# ==========================================
# HEADER
# ==========================================

st.title("☁️ Cloud Resource Scheduler")

st.caption(
    "Real-Time Infrastructure Scheduling and Cloud Analytics Dashboard"
)

st.divider()

# ==========================================
# RUN SIMULATION
# ==========================================

if st.button("🚀 Run Simulation"):

    with st.spinner("Running simulation..."):

        os.system("gcc input_generator.c -o builds/gen")

        os.system("g++ -std=c++17 main.cpp -o builds/run")

        os.system("./builds/gen")

        os.system("./builds/run")

    st.success("Simulation completed successfully")

# ==========================================
# LOAD CSV FILES
# ==========================================

metrics_path = "outputs/metrics/metrics.csv"
timeline_path = "outputs/metrics/timeline.csv"

if os.path.exists(metrics_path) and os.path.exists(timeline_path):

    metrics = pd.read_csv(metrics_path)

    timeline = pd.read_csv(timeline_path)

    online = metrics.iloc[1]

    # ======================================
    # KPI SECTION
    # ======================================

    st.subheader("📊 System Metrics")

    col1, col2, col3, col4 = st.columns(4)

    metrics_data = [

        ("💰 Revenue", f"${int(online['Revenue'])}"),

        ("✅ Accepted Jobs", int(online["Accepted"])),

        ("❌ Rejected Jobs", int(online["Rejected"])),

        ("🖥️ CPU Usage", f"{online['CPU']:.2f}%")
    ]

    for col, (title, value) in zip(
        [col1, col2, col3, col4],
        metrics_data
    ):

        with col:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col5, col6, col7 = st.columns(3)

    more_metrics = [

        ("💾 Storage", f"{online['Storage']:.2f}%"),

        ("🧠 RAM", f"{online['RAM']:.2f}%"),

        ("📡 Bandwidth", f"{online['BW']:.2f}%")
    ]

    for col, (title, value) in zip(
        [col5, col6, col7],
        more_metrics
    ):

        with col:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ======================================
    # RESOURCE UTILIZATION
    # ======================================

    st.subheader("📈 Resource Utilization")

    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=timeline["Time"],
            y=timeline["CPU"],
            mode="lines",
            name="CPU",
            line=dict(color="#3b82f6", width=3)
        )
    )

    fig1.add_trace(
        go.Scatter(
            x=timeline["Time"],
            y=timeline["RAM"],
            mode="lines",
            name="RAM",
            line=dict(color="#10b981", width=3)
        )
    )

    fig1.add_trace(
        go.Scatter(
            x=timeline["Time"],
            y=timeline["Storage"],
            mode="lines",
            name="Storage",
            line=dict(color="#f59e0b", width=3)
        )
    )

    fig1.add_trace(
        go.Scatter(
            x=timeline["Time"],
            y=timeline["BW"],
            mode="lines",
            name="Bandwidth",
            line=dict(color="#ef4444", width=3)
        )
    )

    fig1.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font=dict(color="white"),

        height=500,

        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.divider()

    # ======================================
    # REVENUE + QUEUE
    # ======================================

    colA, colB = st.columns(2)

    # ======================================
    # REVENUE CHART
    # ======================================

    with colA:

        st.subheader("💰 Revenue Growth")

        fig2 = go.Figure()

        fig2.add_trace(
            go.Scatter(
                x=timeline["Time"],
                y=timeline["Revenue"],
                mode="lines",
                line=dict(
                    color="#3b82f6",
                    width=3
                ),
                name="Revenue"
            )
        )

        fig2.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0f172a",

            plot_bgcolor="#0f172a",

            font=dict(color="white"),

            height=400
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # ======================================
    # QUEUE CHART
    # ======================================

    with colB:

        st.subheader("⏳ Queue Pressure")

        fig3 = go.Figure()

        fig3.add_trace(
            go.Scatter(
                x=timeline["Time"],
                y=timeline["Queue"],
                mode="lines",
                line=dict(
                    color="#ef4444",
                    width=3
                ),
                name="Queue"
            )
        )

        fig3.update_layout(

            template="plotly_dark",

            paper_bgcolor="#0f172a",

            plot_bgcolor="#0f172a",

            font=dict(color="white"),

            height=400
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    st.divider()

    # ======================================
    # PIE CHART
    # ======================================

    st.subheader("🧩 Job Distribution")

    pie_data = pd.DataFrame({

        "Status": ["Accepted", "Rejected"],

        "Count": [
            online["Accepted"],
            online["Rejected"]
        ]
    })

    fig4 = px.pie(

        pie_data,

        names="Status",

        values="Count",

        hole=0.45,

        color_discrete_sequence=[
            "#10b981",
            "#ef4444"
        ]
    )

    fig4.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font=dict(color="white"),

        height=500
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.divider()

    # ======================================
    # METRICS TABLE
    # ======================================

    st.subheader("🗂️ Detailed Metrics")

    st.dataframe(
        metrics,
        use_container_width=True
    )