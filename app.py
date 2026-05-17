import os
import sys
import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Fix working directory on EC2
APP_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(APP_DIR)
sys.path.insert(0, APP_DIR)

from charts import generate_charts

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

.stApp {
    background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    color: white;
}

.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.72);
    z-index: -1;
}

section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.metric-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 24px;
    transition: 0.3s ease;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
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

h1, h2, h3 { color: white !important; }

#MainMenu          { visibility: hidden; }
footer             { visibility: hidden; }
header             { visibility: hidden; }
[data-testid="stToolbar"] { visibility: hidden; }

</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER — only one, using markdown (no st.title duplicate)
# ==========================================

st.markdown("""
<div style="
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 32px;
">
    <h1 style="font-size:48px; font-weight:800; margin:0;">☁️ AI Cloud Resource Scheduler</h1>
    <p style="color:#94a3b8; font-size:18px; margin-top:12px;">
        Real-Time Infrastructure Monitoring and Intelligent Cloud Scheduling Platform
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# RUN SIMULATION
# ==========================================

if st.button("🚀 Run Simulation"):
    with st.spinner("Running simulation..."):

        ret1 = os.system("gcc input_generator.c -o builds/gen")
        ret2 = os.system("g++ -std=c++17 main.cpp -o builds/run")

        if ret1 != 0 or ret2 != 0:
            st.error("Compilation failed.")
            st.stop()

        os.system("./builds/gen")
        os.system("./builds/run")

        run_id = str(int(time.time()))

        try:
            generate_charts(run_id)
        except Exception as e:
            st.error(f"Chart generation failed: {e}")
            st.stop()

        st.session_state["run_id"] = run_id

    st.success("✅ Simulation completed successfully")
    st.rerun()

# ==========================================
# LOAD CSV FILES
# ==========================================

metrics_path  = os.path.join(APP_DIR, "outputs", "metrics", "metrics.csv")
timeline_path = os.path.join(APP_DIR, "outputs", "metrics", "timeline.csv")
input_path    = os.path.join(APP_DIR, "builds", "input.txt")

if os.path.exists(metrics_path) and os.path.exists(timeline_path):

    metrics  = pd.read_csv(metrics_path)
    timeline = pd.read_csv(timeline_path)
    online   = metrics.iloc[1]

    # ======================================
    # KPI SECTION
    # ======================================

    st.subheader("📊 System Metrics")

    col1, col2, col3, col4 = st.columns(4)

    for col, (title, value) in zip(
        [col1, col2, col3, col4],
        [
            ("💰 Revenue",       f"${int(online['Revenue'])}"),
            ("✅ Accepted Jobs", int(online["Accepted"])),
            ("❌ Rejected Jobs", int(online["Rejected"])),
            ("🖥️ CPU Usage",    f"{online['CPU']:.2f}%"),
        ]
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

    for col, (title, value) in zip(
        [col5, col6, col7],
        [
            ("💾 Storage",    f"{online['Storage']:.2f}%"),
            ("🧠 RAM",        f"{online['RAM']:.2f}%"),
            ("📡 Bandwidth",  f"{online['BW']:.2f}%"),
        ]
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
    # RESOURCE UTILIZATION — normalized to %
    # ======================================

    st.subheader("📈 Resource Utilization")

    # Read cluster max capacity to normalize
    if os.path.exists(input_path):
        with open(input_path) as f:
            parts       = f.readline().split()
            MAX_CPU     = int(parts[0])
            MAX_RAM     = int(parts[1])
            MAX_STORAGE = int(parts[2])
            MAX_BW      = int(parts[3])

        cpu_pct     = (timeline["CPU"]     / MAX_CPU)     * 100
        ram_pct     = (timeline["RAM"]     / MAX_RAM)     * 100
        storage_pct = (timeline["Storage"] / MAX_STORAGE) * 100
        bw_pct      = (timeline["BW"]      / MAX_BW)      * 100
    else:
        # Fallback: use raw values if input.txt not found
        cpu_pct     = timeline["CPU"]
        ram_pct     = timeline["RAM"]
        storage_pct = timeline["Storage"]
        bw_pct      = timeline["BW"]

    fig1 = go.Figure()
    for y, name, color in [
        (cpu_pct,     "CPU",       "#3b82f6"),
        (ram_pct,     "RAM",       "#10b981"),
        (storage_pct, "Storage",   "#f59e0b"),
        (bw_pct,      "Bandwidth", "#ef4444"),
    ]:
        fig1.add_trace(go.Scatter(
            x=timeline["Time"], y=y,
            mode="lines", name=name,
            line=dict(color=color, width=2)
        ))

    fig1.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        yaxis_title="Utilization (%)",
        yaxis=dict(range=[0, 105]),
        height=500,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()

    # ======================================
    # REVENUE + QUEUE
    # ======================================

    colA, colB = st.columns(2)

    with colA:
        st.subheader("💰 Revenue Growth")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=timeline["Time"], y=timeline["Revenue"],
            mode="lines", line=dict(color="#3b82f6", width=3), name="Revenue"
        ))
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"), height=400
        )
        st.plotly_chart(fig2, use_container_width=True)

    with colB:
        st.subheader("⏳ Queue Pressure")
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=timeline["Time"], y=timeline["Queue"],
            mode="lines", line=dict(color="#ef4444", width=3), name="Queue"
        ))
        fig3.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"), height=400
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # ======================================
    # PIE CHART — fixed colors (green=Accepted, red=Rejected)
    # ======================================

    st.subheader("🧩 Job Distribution")

    _, pie_col, _ = st.columns([1, 2, 1])

    with pie_col:
        fig4 = px.pie(
            pd.DataFrame({
                "Status": ["Accepted", "Rejected"],
                "Count":  [online["Accepted"], online["Rejected"]]
            }),
            names="Status",
            values="Count",
            hole=0.45,
            color="Status",
            color_discrete_map={
                "Accepted": "#10b981",   # green
                "Rejected": "#ef4444"    # red
            }
        )
        fig4.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=500
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # ======================================
    # METRICS TABLE
    # ======================================

    st.subheader("🗂️ Detailed Metrics")
    st.dataframe(metrics, use_container_width=True)