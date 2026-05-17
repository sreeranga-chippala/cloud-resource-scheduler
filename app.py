import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    background-color: #0b1220;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1f2937;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.metric-card {
    background-color: #111827;
    border: 1px solid #1f2937;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
}

.metric-title {
    color: #9ca3af;
    font-size: 15px;
}

.metric-value {
    color: white;
    font-size: 32px;
    font-weight: bold;
}

.chart-card {
    background-color: #111827;
    border: 1px solid #1f2937;
    border-radius: 16px;
    padding: 10px;
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
# RUN BUTTON
# ==========================================

if st.button("🚀 Run Simulation"):

    with st.spinner("Running cloud scheduling simulation..."):

        os.system("gcc input_generator.c -o builds/gen")

        os.system("g++ -std=c++17 main.cpp -o builds/run")

        os.system("./builds/gen")

        os.system("./builds/run")

    st.success("Simulation completed successfully")

# ==========================================
# LOAD DATA
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

    cards = [

        ("💰 Revenue", f"${int(online['Revenue'])}"),

        ("✅ Accepted Jobs", int(online["Accepted"])),

        ("❌ Rejected Jobs", int(online["Rejected"])),

        ("🖥️ CPU Usage", f"{online['CPU']:.2f}%")
    ]

    for col, (title, value) in zip(
        [col1, col2, col3, col4],
        cards
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

    more_cards = [

        ("💾 Storage Usage", f"{online['Storage']:.2f}%"),

        ("🧠 RAM Usage", f"{online['RAM']:.2f}%"),

        ("📡 Bandwidth Usage", f"{online['BW']:.2f}%")
    ]

    for col, (title, value) in zip(
        [col5, col6, col7],
        more_cards
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
    # RESOURCE UTILIZATION CHART
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
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="white"),
        height=500,
        margin=dict(l=20, r=20, t=50, b=20)
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

    with colA:

        st.subheader("💰 Revenue Growth")

        fig2 = px.line(
            timeline,
            x="Time",
            y="Revenue",
            template="plotly_dark"
        )

        fig2.update_traces(
            line=dict(color="#3b82f6", width=3)
        )

        fig2.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="white"),
            height=400
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    with colB:

        st.subheader("⏳ Queue Pressure")

        fig3 = px.line(
            timeline,
            x="Time",
            y="Queue",
            template="plotly_dark"
        )

        fig3.update_traces(
            line=dict(color="#ef4444", width=3)
        )

        fig3.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="white"),
            height=400
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    st.divider()

    # ======================================
    # JOB DISTRIBUTION
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
        template="plotly_dark",
        hole=0.4,
        color_discrete_sequence=[
            "#10b981",
            "#ef4444"
        ]
    )

    fig4.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
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