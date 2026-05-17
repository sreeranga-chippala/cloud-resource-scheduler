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

    background-image: url("https://images.unsplash.com/photo-1451187580459-43490279c0fa");

    background-size: cover;

    background-attachment: fixed;

    background-position: center;

    color: white;
}

/* overlay */

.stApp::before {

    content: "";

    position: fixed;

    top: 0;

    left: 0;

    width: 100%;

    height: 100%;

    background: rgba(0, 0, 0, 0.72);

    z-index: -1;
}

/* sidebar */

section[data-testid="stSidebar"] {

    background: rgba(15, 23, 42, 0.85);

    backdrop-filter: blur(14px);

    border-right: 1px solid rgba(255,255,255,0.08);
}

/* cards */

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

/* metric title */

.metric-title {

    color: #cbd5e1;

    font-size: 15px;

    margin-bottom: 10px;
}

/* metric value */

.metric-value {

    color: white;

    font-size: 34px;

    font-weight: bold;
}

/* charts */

.chart-container {

    background: rgba(255,255,255,0.06);

    backdrop-filter: blur(12px);

    border-radius: 20px;

    padding: 20px;

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}

/* text */

h1 {

    font-size: 48px !important;

    font-weight: 800 !important;

    color: white !important;
}

h2, h3 {

    color: white !important;
}

/* hide streamlit */

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
st.markdown("""
<div style="
padding:40px;
border-radius:25px;
background:rgba(255,255,255,0.08);
backdrop-filter:blur(14px);
margin-bottom:30px;
">

<h1 style="margin-bottom:10px;">
☁️ AI Cloud Resource Scheduler
</h1>

<p style="
font-size:20px;
color:#cbd5e1;
">
Real-Time Infrastructure Monitoring and Intelligent Cloud Scheduling Platform
</p>

</div>
""", unsafe_allow_html=True)

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