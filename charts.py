import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_charts():
    # Anchor all paths to this file's directory — fixes relative path issues
    BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
    VISUAL_DIR   = os.path.join(BASE_DIR, "outputs", "visualizations")
    TIMELINE_CSV = os.path.join(BASE_DIR, "outputs", "metrics", "timeline.csv")
    METRICS_CSV  = os.path.join(BASE_DIR, "outputs", "metrics", "metrics.csv")
    INPUT_TXT    = os.path.join(BASE_DIR, "builds", "input.txt")

    os.makedirs(VISUAL_DIR, exist_ok=True)

    sns.set_theme(style="whitegrid", palette="deep")

    # ============================================
    # LOAD DATA
    # ============================================

    timeline = pd.read_csv(TIMELINE_CSV)
    metrics  = pd.read_csv(METRICS_CSV)

    greedy = metrics.iloc[0]
    online = metrics.iloc[1]

    # ============================================
    # READ CLUSTER CAPACITY
    # ============================================

    with open(INPUT_TXT, "r") as f:
        first       = f.readline().split()
        MAX_CPU     = int(first[0])
        MAX_RAM     = int(first[1])
        MAX_STORAGE = int(first[2])
        MAX_BW      = int(first[3])

    # ============================================
    # NORMALIZED UTILIZATION + SMOOTHING
    # ============================================

    WINDOW = 20

    cpu_smooth     = (timeline["CPU"]     / MAX_CPU     * 100).rolling(WINDOW).mean()
    ram_smooth     = (timeline["RAM"]     / MAX_RAM     * 100).rolling(WINDOW).mean()
    storage_smooth = (timeline["Storage"] / MAX_STORAGE * 100).rolling(WINDOW).mean()
    bw_smooth      = (timeline["BW"]      / MAX_BW      * 100).rolling(WINDOW).mean()
    queue_smooth   = timeline["Queue"].rolling(WINDOW).mean()

    # =========================================================
    # 1. ONLINE RESOURCE UTILIZATION OVER TIME
    # =========================================================

    plt.figure(figsize=(14, 7), dpi=300)
    sns.lineplot(x=timeline["Time"], y=cpu_smooth,     label="CPU (%)",       linewidth=2)
    sns.lineplot(x=timeline["Time"], y=ram_smooth,     label="RAM (%)",       linewidth=2)
    sns.lineplot(x=timeline["Time"], y=storage_smooth, label="Storage (%)",   linewidth=2)
    sns.lineplot(x=timeline["Time"], y=bw_smooth,      label="Bandwidth (%)", linewidth=2)
    plt.title("Online Scheduler Resource Utilization Over Time", fontsize=16, fontweight="bold")
    plt.xlabel("Simulation Time Step")
    plt.ylabel("Utilization (% of Cluster Capacity)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(VISUAL_DIR, "online_resource_utilization.png"), dpi=300, bbox_inches="tight")
    plt.close()

    # =========================================================
    # 2. GREEDY RESOURCE UTILIZATION
    # =========================================================

    plt.figure(figsize=(14, 7), dpi=300)
    sns.barplot(x=["CPU", "RAM", "Storage", "Bandwidth"],
                y=[greedy["CPU"], greedy["RAM"], greedy["Storage"], greedy["BW"]])
    plt.title("Static Baseline Resource Utilization", fontsize=16, fontweight="bold")
    plt.xlabel("Resources")
    plt.ylabel("Utilization (% of Capacity)")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUAL_DIR, "greedy_resource_utilization.png"), dpi=300, bbox_inches="tight")
    plt.close()

    # =========================================================
    # 3. REVENUE GENERATION RATE
    # =========================================================

    revenue_smooth = timeline["Revenue"].diff().fillna(0).rolling(WINDOW).mean()

    plt.figure(figsize=(14, 7), dpi=300)
    sns.lineplot(x=timeline["Time"], y=revenue_smooth, linewidth=2)
    plt.title("Revenue Generation Rate Over Time", fontsize=16, fontweight="bold")
    plt.xlabel("Simulation Time Step")
    plt.ylabel("Revenue Generated ($ per event)")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUAL_DIR, "revenue_growth.png"), dpi=300, bbox_inches="tight")
    plt.close()

    # =========================================================
    # 4. QUEUE PRESSURE
    # =========================================================

    plt.figure(figsize=(14, 7), dpi=300)
    sns.lineplot(x=timeline["Time"], y=queue_smooth, linewidth=2)
    plt.title("Scheduler Congestion Over Time", fontsize=16, fontweight="bold")
    plt.xlabel("Simulation Time Step")
    plt.ylabel("Queued Jobs")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUAL_DIR, "queue_pressure.png"), dpi=300, bbox_inches="tight")
    plt.close()

    # =========================================================
    # 5. JOB DISTRIBUTION PIE CHART
    # =========================================================

    plt.figure(figsize=(8, 8), dpi=300)
    plt.pie(
        [online["Accepted"], online["Rejected"]],
        labels=["Accepted", "Rejected"],
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("deep")
    )
    plt.title("Online Scheduler Job Distribution", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(VISUAL_DIR, "job_distribution.png"), dpi=300, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":
    generate_charts()