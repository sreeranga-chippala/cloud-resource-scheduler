import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Cloud Resource Scheduler",
    page_icon="☁️",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* MAIN APP */

.stApp {

    background-image:
    linear-gradient(
        rgba(5,10,20,0.80),
        rgba(5,10,20,0.85)
    ),
    url("https://images.unsplash.com/photo-1462331940025-496dfbfc7564");

    background-size: cover;

    background-position: center;

    background-attachment: fixed;

    color: white;
}

/* MAIN CONTAINER */

.block-container {

    max-width: 1450px;

    padding-top: 2rem;

    padding-bottom: 2rem;
}

/* HERO SECTION */

.hero {

    padding: 55px;

    border-radius: 30px;

    background: rgba(15,23,42,0.72);

    backdrop-filter: blur(16px);

    border: 1px solid rgba(255,255,255,0.08);

    margin-bottom: 40px;

    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
}

/* METRIC CARDS */

.metric-card {

    background: rgba(15,23,42,0.78);

    border-radius: 24px;

    padding: 30px;

    border: 1px solid rgba(255,255,255,0.06);

    backdrop-filter: blur(12px);

    min-height: 150px;

    box-shadow: 0 10px 30px rgba(0,0,0,0.25);

    transition: 0.3s;
}

.metric-card:hover {

    transform: translateY(-6px);

    border: 1px solid #3b82f6;
}

.metric-title {

    color: #cbd5e1;

    font-size: 18px;

    margin-bottom: 15px;
}

.metric-value {

    font-size: 38px;

    font-weight: 800;

    color: white;
}

/* CHART CONTAINER */

.chart-container {

    background: rgba(15,23,42,0.82);

    border-radius: 24px;

    padding: 25px;

    margin-bottom: 35px;

    border: 1px solid rgba(255,255,255,0.06);

    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

/* SIDEBAR */

section[data-testid="stSidebar"] {

    background: rgba(15,23,42,0.94);

    border-right: 1px solid rgba(255,255,255,0.05);
}

/* TITLES */

h1 {

    font-size: 58px !important;

    font-weight: 800 !important;

    color: white !important;
}

h2, h3 {

    color: white !important;
}

/* BUTTON */

.stButton>button {

    background: linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );

    color: white;

    border-radius: 14px;

    border: none;

    padding: 14px 26px;

    font-size: 18px;

    font-weight: 600;

    transition: 0.3s;

    box-shadow: 0 8px 20px rgba(37,99,235,0.35);
}

.stButton>button:hover {

    transform: translateY(-2px);

    background: linear-gradient(
        135deg,
        #3b82f6,
        #2563eb
    );
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

- AI Resource Scheduling
- Runtime Analytics
- Queue Optimization
- AWS EC2 Deployment
- CI/CD Automation
- Cloud Monitoring
""")

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">

<div style="
font-size:62px;
font-weight:800;
margin-bottom:15px;
">
☁️ AI Cloud Resource Scheduler
</div>

<div style="
font-size:24px;
color:#cbd5e1;
line-height:1.7;
max-width:1000px;
">
Real-Time Cloud Infrastructure Monitoring,
Intelligent Scheduling,
Revenue Analytics,
Queue Optimization,
and AI-Based Resource Allocation Platform deployed on AWS EC2 with CI/CD automation.
</div>

</div>
""", unsafe_allow_html=True)

# ==========================================
# STATUS BAR
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🟢 AWS EC2 Active")

with col2:
    st.info("⚡ GitHub Actions Connected")

with col3:
    st.warning("☁️ Cloud Deployment Enabled")

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
    # METRICS
    # ======================================

    st.subheader("📊 System Metrics")

    cols = st.columns(4)

    metric_data = [

        ("💰 Revenue", f"${int(online['Revenue'])}"),

        ("✅ Accepted Jobs", int(online["Accepted"])),

        ("❌ Rejected Jobs", int(online["Rejected"])),

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
    # RESOURCE UTILIZATION
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

        template="plotly",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(color="white"),

        height=420,

        margin=dict(l=20, r=20, t=40, b=20),

        xaxis=dict(
            gridcolor="rgba(255,255,255,0.08)"
        ),

        yaxis=dict(
            gridcolor="rgba(255,255,255,0.08)"
        )
    )

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    st.plotly_chart(
        fig1,
        use_container_width=True,
        config={"displayModeBar": False}
    )

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

            template="plotly",

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(color="white"),

            height=350,

            margin=dict(l=20, r=20, t=40, b=20)
        )

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        st.plotly_chart(
            fig2,
            use_container_width=True,
            config={"displayModeBar": False}
        )

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

            template="plotly",

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(color="white"),

            height=350,

            margin=dict(l=20, r=20, t=40, b=20)
        )

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)

        st.plotly_chart(
            fig3,
            use_container_width=True,
            config={"displayModeBar": False}
        )

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

    fig4.update_traces(
        textfont_size=18
    )

    fig4.update_layout(

        template="plotly",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(color="white"),

        height=450,

        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    st.plotly_chart(
        fig4,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ======================================
    # TABLE
    # ======================================

    st.divider()

    with st.expander("🗂️ View Detailed Metrics"):

        st.dataframe(
            metrics,
            use_container_width=True
        )