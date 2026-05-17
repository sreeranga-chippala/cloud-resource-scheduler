import os
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

METRICS_PATH = os.path.join(
    BASE_DIR,
    "outputs",
    "metrics",
    "metrics.csv"
)

TIMELINE_PATH = os.path.join(
    BASE_DIR,
    "outputs",
    "metrics",
    "timeline.csv"
)

VIZ_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "visualizations"
)

os.makedirs(VIZ_DIR, exist_ok=True)

# ==========================================
# GLOBAL STYLE
# ==========================================

plt.style.use("default")

plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"

# ==========================================
# GENERATE CHARTS
# ==========================================

def generate_charts():

    # =========================
    # LOAD DATA
    # =========================

    metrics = pd.read_csv(METRICS_PATH)
    timeline = pd.read_csv(TIMELINE_PATH)

    online = metrics.iloc[1]

    # ======================================
    # GREEDY RESOURCE UTILIZATION
    # ======================================

    fig, ax = plt.subplots(
        figsize=(10, 6),
        facecolor="white"
    )

    resources = [
        "CPU",
        "RAM",
        "Storage",
        "Bandwidth"
    ]

    values = [
        online["CPU"],
        online["RAM"],
        online["Storage"],
        online["BW"]
    ]

    ax.bar(resources, values)

    ax.set_title("Greedy Resource Utilization")
    ax.set_ylabel("Utilization (%)")
    ax.set_ylim(0, 105)

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            VIZ_DIR,
            "greedy_resource_utilization.png"
        )
    )

    plt.close()

    # ======================================
    # JOB DISTRIBUTION PIE CHART
    # ======================================

    fig, ax = plt.subplots(
        figsize=(8, 8),
        facecolor="white"
    )

    jobs = [
        online["Accepted"],
        online["Rejected"]
    ]

    labels = [
        "Accepted",
        "Rejected"
    ]

    ax.pie(
        jobs,
        labels=labels,
        autopct="%1.1f%%"
    )

    ax.set_title("Job Distribution")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            VIZ_DIR,
            "job_distribution.png"
        )
    )

    plt.close()

    # ======================================
    # ONLINE RESOURCE UTILIZATION
    # ======================================

    fig, ax = plt.subplots(
        figsize=(14, 7),
        facecolor="white"
    )

    ax.plot(
        timeline["Time"],
        timeline["CPU"],
        label="CPU"
    )

    ax.plot(
        timeline["Time"],
        timeline["RAM"],
        label="RAM"
    )

    ax.plot(
        timeline["Time"],
        timeline["Storage"],
        label="Storage"
    )

    ax.plot(
        timeline["Time"],
        timeline["BW"],
        label="Bandwidth"
    )

    ax.set_title("Online Resource Utilization")
    ax.set_xlabel("Time")
    ax.set_ylabel("Utilization (%)")

    ax.legend()

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            VIZ_DIR,
            "online_resource_utilization.png"
        )
    )

    plt.close()

    # ======================================
    # QUEUE PRESSURE
    # ======================================

    fig, ax = plt.subplots(
        figsize=(14, 7),
        facecolor="white"
    )

    ax.plot(
        timeline["Time"],
        timeline["Queue"]
    )

    ax.set_title("Queue Pressure")
    ax.set_xlabel("Time")
    ax.set_ylabel("Queue")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            VIZ_DIR,
            "queue_pressure.png"
        )
    )

    plt.close()

    # ======================================
    # REVENUE GROWTH
    # ======================================

    fig, ax = plt.subplots(
        figsize=(14, 7),
        facecolor="white"
    )

    ax.plot(
        timeline["Time"],
        timeline["Revenue"]
    )

    ax.set_title("Revenue Growth")
    ax.set_xlabel("Time")
    ax.set_ylabel("Revenue")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            VIZ_DIR,
            "revenue_growth.png"
        )
    )

    plt.close()