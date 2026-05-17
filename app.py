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
    background-image: url("https://images.unsplash.com/photo-1516321318423-f06f85e504b3");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}

/* DARK OVERLAY */

.stApp::before {

    content: "";

    position: fixed;

    top: 0;
    left: 0;

    width: 100%;
    height: 100%;

    background: rgba(0,0,0,0.72);

    z-index: -1;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {

    background: rgba(15,23,42,0.88);

    backdrop-filter: blur(16px);

    border-right: 1px solid rgba(255,255,255,0.08);
}

/* HERO */

.hero {

    padding: 45px;

    border-radius: 28px;

    background: linear-gradient(
        135deg,
        rgba(59,130,246,0.22),
        rgba(15,23,42,0.88)
    );

    backdrop-filter: blur(18px);

    border: 1px solid rgba(255,255,255,0.08);

    margin-top: 20px;

    margin-bottom: 35px;

    box-shadow: 0 15px 40px rgba(0,0,0,0.35);
}

/* METRIC CARDS */

.metric-card {

    background: rgba(255,255,255,0.08);

    backdrop-filter: blur(14px);

    border-radius: 22px;

    padding: 24px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow: 0 8px 30px rgba(0,0,0,0.3);

    transition: 0.3s ease;
}

.metric-card:hover {

    transform: translateY(-5px);

    border: 1px solid #60a5fa;

    box-shadow: 0 15px 40px rgba(59,130,246,0.3);
}

.metric-title {

    color: #cbd5e1;

    font-size: 15px;

    margin-bottom: 10px;
}

.metric-value {

    color: white;

    font-size: 34px;

    font-weight: bold;
}

/* CHART CONTAINER */

.chart-container {

    background: rgba(255,255,255,0.06);

    backdrop-filter: blur(14px);

    border-radius: 24px;

    padding: 20px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow: 0 8px 30px rgba(0,0,0,0.3);

    margin-bottom: 25px;
}

/* TEXT */

h1, h2, h3 {

    color: white !important;
}

/* REMOVE STREAMLIT */

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("☁️ Cloud Scheduler")

st.sidebar.markdown("""
### Features

- AI Scheduling
- Runtime Analytics
- Queue Optimization
- AWS EC2 Deployment
- GitHub Actions CI/CD
- Real-Time Monitoring
""")

# ==========================================
# TITLE
# ==========================================

st.title("☁️ Cloud Resource Scheduler")

st.caption(
    "Real-Time Infrastructure Scheduling and Cloud Analytics Dashboard"
)

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">

<div style="
font-size:54px;
font-weight:800;
margin-bottom:12px;
">
☁️ AI Cloud Resource Scheduler
</div>

<div style="
font-size:22px;
color:#cbd5e1;
line-height:1.6;
max-width:900px;
">
Real-Time Cloud Infrastructure Monitoring, Intelligent Resource Allocation,
Queue Optimization, Revenue Analytics, and AI-Based Scheduling Simulation
Platform deployed on AWS EC2 with CI/CD automation.
</div>

</div>
""", unsafe_allow_html=True)

# ==========================================
# STATUS BAR
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🟢 EC2 Deployment Active")

with col2:
    st.info("⚡ GitHub Actions CI/CD Connected")

with col3:
    st.warning("☁️ AWS Cloud Environment")

st.divider()

# ==========================================
# RUN BUTTON
# ==========================================

if st.button("🚀 Run Simulation"):

    with st.spinner("Running simulation..."):

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
    # METRICS
    # ======================================

    st.subheader("📊 System Metrics")

    cols = st.columns(4)

    metric_data = [

        ("💰 Revenue", f"${int(online['Revenue'])}"),

        ("✅ Accepted", int(online["Accepted"])),

        ("❌ Rejected", int(online["Rejected"])),

        ("🖥️ CPU Usage", f"{online['CPU']:.2f}%")
    ]

    for col, (title, value) in zip(cols, metric_data):

        with col:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cols2 = st.columns(3)

    metric_data2 = [

        ("💾 Storage", f"{online['Storage']:.2f}%"),

        ("🧠 RAM", f"{online['RAM']:.2f}%"),

        ("📡 Bandwidth", f"{online['BW']:.2f}%")
    ]

    for col, (title, value) in zip(cols2, metric_data2):

        with col:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ======================================
    # RESOURCE CHART
    # ======================================

    st.subheader("📈 Resource Utilization")

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=timeline["Time"],
        y=timeline["CPU"],
        mode="lines",
        name="CPU",
        line=dict(color="#3b82f6", width=3)
    ))

    fig1.add_trace(go.Scatter(
        x=timeline["Time"],
        y=timeline["RAM"],
        mode="lines",
        name="RAM",
        line=dict(color="#10b981", width=3)
    ))

    fig1.add_trace(go.Scatter(
        x=timeline["Time"],
        y=timeline["Storage"],
        mode="lines",
        name="Storage",
        line=dict(color="#f59e0b", width=3)
    ))

    fig1.add_trace(go.Scatter(
        x=timeline["Time"],
        y=timeline["BW"],
        mode="lines",
        name="Bandwidth",
        line=dict(color="#ef4444", width=3)
    ))

    fig1.update_layout(

        template="none",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(color="white"),

        height=500,

        xaxis=dict(
            gridcolor="rgba(255,255,255,0.08)"
        ),

        yaxis=dict(
            gridcolor="rgba(255,255,255,0.08)"
        )
    )

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ======================================
    # REVENUE + QUEUE
    # ======================================

    colA, colB = st.columns(2)

    with colA:

        st.subheader("💰 Revenue Growth")

        fig2 = px.line(
            timeline,
            x="Time",
            y="Revenue"
        )

        fig2.update_traces(
            line=dict(color="#3b82f6", width=3)
        )

        fig2.update_layout(

            template="none",

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(color="white"),

            height=400
        )

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with colB:

        st.subheader("⏳ Queue Pressure")

        fig3 = px.line(
            timeline,
            x="Time",
            y="Queue"
        )

        fig3.update_traces(
            line=dict(color="#ef4444", width=3)
        )

        fig3.update_layout(

            template="none",

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(color="white"),

            height=400
        )

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        st.plotly_chart(fig3, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

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
        color_discrete_sequence=["#10b981", "#ef4444"]
    )

    fig4.update_layout(

        template="none",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(color="white"),

        height=500
    )

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # ======================================
    # TABLE
    # ======================================

    with st.expander("🗂️ View Detailed Metrics"):

        st.dataframe(
            metrics,
            use_container_width=True
        )