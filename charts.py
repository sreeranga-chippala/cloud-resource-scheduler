import pandas as pd
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import os

# ============================================
# CHART GENERATOR FUNCTION
# ============================================

def generate_charts():

    # ============================================
    # BASE PATHS
    # ============================================

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    VISUAL_DIR = os.path.join(
        BASE_DIR,
        "outputs",
        "visualizations"
    )

    METRICS_DIR = os.path.join(
        BASE_DIR,
        "outputs",
        "metrics"
    )

    BUILDS_DIR = os.path.join(
        BASE_DIR,
        "builds"
    )

    os.makedirs(VISUAL_DIR, exist_ok=True)

    # ============================================
    # FILE PATHS
    # ============================================

    TIMELINE_CSV = os.path.join(
        METRICS_DIR,
        "timeline.csv"
    )

    METRICS_CSV = os.path.join(
        METRICS_DIR,
        "metrics.csv"
    )

    INPUT_TXT = os.path.join(
        BUILDS_DIR,
        "input.txt"
    )

    # ============================================
    # LOAD DATA
    # ============================================

    timeline = pd.read_csv(TIMELINE_CSV)

    metrics = pd.read_csv(METRICS_CSV)

    greedy = metrics.iloc[0]

    online = metrics.iloc[1]

    # ============================================
    # READ CLUSTER CAPACITY
    # ============================================

    with open(INPUT_TXT, "r") as f:

        first = f.readline().split()

        MAX_CPU = int(first[0])
        MAX_RAM = int(first[1])
        MAX_STORAGE = int(first[2])
        MAX_BW = int(first[3])

    # ============================================
    # STYLE
    # ============================================

    sns.set_theme(
        style="whitegrid",
        palette="deep"
    )

    # ============================================
    # NORMALIZED UTILIZATION
    # ============================================

    cpu_percent = (timeline["CPU"] / MAX_CPU) * 100
    ram_percent = (timeline["RAM"] / MAX_RAM) * 100
    storage_percent = (timeline["Storage"] / MAX_STORAGE) * 100
    bw_percent = (timeline["BW"] / MAX_BW) * 100

    WINDOW = 20

    cpu_smooth = cpu_percent.rolling(WINDOW).mean()
    ram_smooth = ram_percent.rolling(WINDOW).mean()
    storage_smooth = storage_percent.rolling(WINDOW).mean()
    bw_smooth = bw_percent.rolling(WINDOW).mean()
    queue_smooth = timeline["Queue"].rolling(WINDOW).mean()

    # ============================================
    # ONLINE RESOURCE UTILIZATION
    # ============================================

    plt.figure(figsize=(14, 7))

    sns.lineplot(x=timeline["Time"], y=cpu_smooth, label="CPU")
    sns.lineplot(x=timeline["Time"], y=ram_smooth, label="RAM")
    sns.lineplot(x=timeline["Time"], y=storage_smooth, label="Storage")
    sns.lineplot(x=timeline["Time"], y=bw_smooth, label="Bandwidth")

    plt.title("Online Resource Utilization")
    plt.xlabel("Time")
    plt.ylabel("Utilization (%)")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            VISUAL_DIR,
            "online_resource_utilization.png"
        )
    )

    plt.close()

    # ============================================
    # GREEDY RESOURCE UTILIZATION
    # ============================================

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=["CPU", "RAM", "Storage", "Bandwidth"],
        y=[
            greedy["CPU"],
            greedy["RAM"],
            greedy["Storage"],
            greedy["BW"]
        ]
    )

    plt.title("Greedy Resource Utilization")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            VISUAL_DIR,
            "greedy_resource_utilization.png"
        )
    )

    plt.close()

    # ============================================
    # REVENUE GROWTH
    # ============================================

    revenue_rate = (
        timeline["Revenue"]
        .diff()
        .fillna(0)
    )

    revenue_rate_smooth = (
        revenue_rate
        .rolling(WINDOW)
        .mean()
    )

    plt.figure(figsize=(14, 7))

    sns.lineplot(
        x=timeline["Time"],
        y=revenue_rate_smooth
    )

    plt.title("Revenue Growth")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            VISUAL_DIR,
            "revenue_growth.png"
        )
    )

    plt.close()

    # ============================================
    # QUEUE PRESSURE
    # ============================================

    plt.figure(figsize=(14, 7))

    sns.lineplot(
        x=timeline["Time"],
        y=queue_smooth
    )

    plt.title("Queue Pressure")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            VISUAL_DIR,
            "queue_pressure.png"
        )
    )

    plt.close()

    # ============================================
    # JOB DISTRIBUTION PIE CHART
    # ============================================

    plt.figure(figsize=(8, 8))

    plt.pie(
        [online["Accepted"], online["Rejected"]],
        labels=["Accepted", "Rejected"],
        autopct="%1.1f%%"
    )

    plt.title("Job Distribution")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            VISUAL_DIR,
            "job_distribution.png"
        )
    )

    plt.close()

# ============================================
# DIRECT EXECUTION
# ============================================

if __name__ == "__main__":

    generate_charts()