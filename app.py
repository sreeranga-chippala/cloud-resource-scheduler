import os
import time
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

/* =========================
MAIN BACKGROUND
========================= */

.stApp {

    background: #0f172a;
    color: white;
}

/* =========================
REMOVE STREAMLIT BRANDING
========================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* =========================
TOP HEADER
========================= */

.main-title {

    font-size: 52px;
    font-weight: 800;
    color: white;
    margin-bottom: 10px;
}

.sub-title {

    font-size: 20px;
    color: #cbd5e1;
    margin-bottom: 25px;
}

/* =========================
GLASS CARDS
========================= */

.metric-card {

    background: linear-gradient(
        145deg,
        rgba(30,41,59,0.95),
        rgba(15,23,42,0.95)
    );

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 22px;

    padding: 24px;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.35);

    transition: 0.3s ease;
}

.metric-card:hover {

    transform: translateY(-4px);

    border: 1px solid #3b82f6;
}

/* =========================
METRIC TEXT
========================= */

.metric-title {

    font-size: 16px;
    color: #94a3b8;
    margin-bottom: 12px;
}

.metric-value {

    font-size: 36px;
    font-weight: 700;
    color: white;
}

/* =========================
SECTION HEADERS
========================= */

.section-title {

    font-size: 34px;
    font-weight: 700;
    color: white;
    margin-top: 25px;
    margin-bottom: 20px;
}

/* =========================
CHART CONTAINERS
========================= */

.chart-card {

    background: rgba(15,23,42,0.96);

    border-radius: 24px;

    padding: 18px;

    border: 1px solid rgba(255,255,255,0.08);

    margin-bottom: 20px;
}

/* =========================
BUTTONS
========================= */

.stButton>button {

    background: linear-gradient(
        90deg,
        #2563eb,
        #3b82f6
    );

    color: white;

    font-size: 18px;

    font-weight: 600;

    border-radius: 14px;

    border: none;

    padding: 12px 28px;

    transition: 0.3s ease;
}

.stButton>button:hover {

    transform: scale(1.03);

    background: linear-gradient(
        90deg,
        #1d4ed8,
        #2563eb
    );
}

/* =========================
DATAFRAME
========================= */

[data-testid="stDataFrame"] {

    border-radius: 20px;

    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.08);
}

/* =========================
SIDEBAR
========================= */

section[data-testid="stSidebar"] {

    background: #111827;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("☁️ Cloud Scheduler")

st.sidebar.markdown("""
### Features

- Static Greedy Packing
- Online Event Scheduling
- Resource Optimization
- Queue Management
- Aging-Based Priority
- Runtime Analytics
- AWS Cloud Deployment
- CI/CD Automation
""")

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="main-title">
☁️ Cloud Resource Scheduler
</div>

<div class="sub-title">
Dynamic Resource Allocation and Online Scheduling Simulator
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# RUN SIMULATION
# ==========================================

if st.button("🚀 Run Simulation"):

    with st.spinner("Running scheduling simulation..."):

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

    st.markdown(
        '<div class="section-title">📊 System Metrics</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    cards = [

        ("💰 Revenue",
         f"${int(online['Revenue'])}"),

        ("✅ Accepted Jobs",
         int(online["Accepted"])),

        ("❌ Rejected Jobs",
         int(online["Rejected"])),

        ("🖥️ CPU Utilization",
         f"{online['CPU']:.2f}%")
    ]

    for col, (title, value) in zip(
        [c1, c2, c3, c4],
        cards
    ):

        with col:

            st.markdown(f"""
            <div class="metric-card">

                <div class="metric-title">
                    {title}
                </div>

                <div class="metric-value">
                    {value}
                </div>

            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c5, c6, c7 = st.columns(3)

    more_cards = [

        ("💾 Storage",
         f"{online['Storage']:.2f}%"),

        ("🧠 RAM",
         f"{online['RAM']:.2f}%"),

        ("📡 Bandwidth",
         f"{online['BW']:.2f}%")
    ]

    for col, (title, value) in zip(
        [c5, c6, c7],
        more_cards
    ):

        with col:

            st.markdown(f"""
            <div class="metric-card">

                <div class="metric-title">
                    {title}
                </div>

                <div class="metric-value">
                    {value}
                </div>

            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ======================================
    # RESOURCE UTILIZATION
    # ======================================

    st.markdown(
        '<div class="section-title">📈 Resource Utilization</div>',
        unsafe_allow_html=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=timeline["Time"],
            y=timeline["CPU"],
            mode="lines",
            name="CPU",
            line=dict(color="#3b82f6", width=3)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=timeline["Time"],
            y=timeline["RAM"],
            mode="lines",
            name="RAM",
            line=dict(color="#10b981", width=3)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=timeline["Time"],
            y=timeline["Storage"],
            mode="lines",
            name="Storage",
            line=dict(color="#f59e0b", width=3)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=timeline["Time"],
            y=timeline["BW"],
            mode="lines",
            name="Bandwidth",
            line=dict(color="#ef4444", width=3)
        )
    )

    fig.update_layout(

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font=dict(color="white"),

        height=520,

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displaylogo": False}
    )

    st.divider()

    # ======================================
    # REVENUE + QUEUE
    # ======================================

    left, right = st.columns(2)

    # ======================================
    # REVENUE
    # ======================================

    with left:

        st.markdown(
            '<div class="section-title">💰 Revenue Growth</div>',
            unsafe_allow_html=True
        )

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
                fill='tozeroy'
            )
        )

        fig2.update_layout(

            paper_bgcolor="#0f172a",

            plot_bgcolor="#0f172a",

            font=dict(color="white"),

            height=420,

            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            )
        )

        st.plotly_chart(
            fig2,
            use_container_width=True,
            config={"displaylogo": False}
        )

    # ======================================
    # QUEUE
    # ======================================

    with right:

        st.markdown(
            '<div class="section-title">⏳ Queue Pressure</div>',
            unsafe_allow_html=True
        )

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
                fill='tozeroy'
            )
        )

        fig3.update_layout(

            paper_bgcolor="#0f172a",

            plot_bgcolor="#0f172a",

            font=dict(color="white"),

            height=420,

            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            )
        )

        st.plotly_chart(
            fig3,
            use_container_width=True,
            config={"displaylogo": False}
        )

    st.divider()

    # ======================================
    # JOB DISTRIBUTION
    # ======================================

    st.markdown(
        '<div class="section-title">🧩 Job Distribution</div>',
        unsafe_allow_html=True
    )

    pie = px.pie(

        values=[
            online["Accepted"],
            online["Rejected"]
        ],

        names=[
            "Accepted",
            "Rejected"
        ],

        hole=0.55,

        color_discrete_sequence=[
            "#10b981",
            "#ef4444"
        ]
    )

    pie.update_layout(

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font=dict(color="white"),

        height=500
    )

    st.plotly_chart(
        pie,
        use_container_width=True,
        config={"displaylogo": False}
    )

    st.divider()

    # ======================================
    # TABLE
    # ======================================

    st.markdown(
        '<div class="section-title">🗂️ Detailed Metrics</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        metrics,
        width="stretch"
    )