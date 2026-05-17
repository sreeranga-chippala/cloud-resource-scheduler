import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os

matplotlib.use("Agg")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VISUAL_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "visualizations"
)

os.makedirs(VISUAL_DIR, exist_ok=True)
# ============================================
# SEABORN STYLE
# ============================================

sns.set_theme(
    style="whitegrid",
    palette="deep"
)

# ============================================
# LOAD DATA
# ============================================

timeline = pd.read_csv(
    "outputs/metrics/timeline.csv"
)

metrics = pd.read_csv(
    "outputs/metrics/metrics.csv"
)

greedy = metrics.iloc[0]
online = metrics.iloc[1]

# ============================================
# READ CLUSTER CAPACITY
# ============================================

with open("builds/input.txt", "r") as f:

    first = f.readline().split()

    MAX_CPU = int(first[0])
    MAX_RAM = int(first[1])
    MAX_STORAGE = int(first[2])
    MAX_BW = int(first[3])

# ============================================
# NORMALIZED UTILIZATION
# ============================================

cpu_percent = (
    timeline["CPU"] / MAX_CPU
) * 100

ram_percent = (
    timeline["RAM"] / MAX_RAM
) * 100

storage_percent = (
    timeline["Storage"] / MAX_STORAGE
) * 100

bw_percent = (
    timeline["BW"] / MAX_BW
) * 100

# ============================================
# MOVING AVERAGE SMOOTHING
# ============================================

WINDOW = 20

cpu_smooth = (
    cpu_percent
    .rolling(WINDOW)
    .mean()
)

ram_smooth = (
    ram_percent
    .rolling(WINDOW)
    .mean()
)

storage_smooth = (
    storage_percent
    .rolling(WINDOW)
    .mean()
)

bw_smooth = (
    bw_percent
    .rolling(WINDOW)
    .mean()
)

queue_smooth = (
    timeline["Queue"]
    .rolling(WINDOW)
    .mean()
)

# =========================================================
# 1. ONLINE RESOURCE UTILIZATION OVER TIME
# =========================================================

plt.figure(figsize=(14, 7), dpi=300)

sns.lineplot(
    x=timeline["Time"],
    y=cpu_smooth,
    label="CPU (%)",
    linewidth=2
)

sns.lineplot(
    x=timeline["Time"],
    y=ram_smooth,
    label="RAM (%)",
    linewidth=2
)

sns.lineplot(
    x=timeline["Time"],
    y=storage_smooth,
    label="Storage (%)",
    linewidth=2
)

sns.lineplot(
    x=timeline["Time"],
    y=bw_smooth,
    label="Bandwidth (%)",
    linewidth=2
)

plt.title(
    "Online Scheduler Resource Utilization Over Time",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Simulation Time Step"
)

plt.ylabel(
    "Utilization (% of Cluster Capacity)"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_DIR,
        "online_resource_utilization.png"
    ),
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# =========================================================
# 2. GREEDY RESOURCE UTILIZATION
# =========================================================

resources = [
    "CPU",
    "RAM",
    "Storage",
    "Bandwidth"
]

greedy_values = [
    greedy["CPU"],
    greedy["RAM"],
    greedy["Storage"],
    greedy["BW"]
]

plt.figure(figsize=(14, 7), dpi=300)

sns.barplot(
    x=resources,
    y=greedy_values
)

plt.title(
    "Static Baseline Resource Utilization",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Resources"
)

plt.ylabel(
    "Utilization (% of Capacity)"
)
plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_DIR,
        "greedy_resource_utilization.png"
    ),
    dpi=300,
    bbox_inches="tight"
)
plt.close()
# =========================================================
# 3. REVENUE GENERATION RATE
# =========================================================

# Revenue generated between events

revenue_rate = (
    timeline["Revenue"]
    .diff()
    .fillna(0)
)

# Smooth fluctuations

revenue_rate_smooth = (
    revenue_rate
    .rolling(20)
    .mean()
)

plt.figure(figsize=(14, 7), dpi=300)

sns.lineplot(
    x=timeline["Time"],
    y=revenue_rate_smooth,
    linewidth=2
)

plt.title(
    "Revenue Generation Rate Over Time",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Simulation Time Step"
)

plt.ylabel(
    "Revenue Generated ($ per event)"
)
plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_DIR,
        "revenue_growth.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()
# =========================================================
# 4. QUEUE PRESSURE ANALYSIS
# =========================================================

plt.figure(figsize=(14, 7), dpi=300)

sns.lineplot(
    x=timeline["Time"],
    y=queue_smooth,
    linewidth=2
)

plt.title(
    "Scheduler Congestion Over Time",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel(
    "Simulation Time Step"
)

plt.ylabel(
    "Queued Jobs"
)
plt.tight_layout()

plt.savefig(
    os.path.join(
        VISUAL_DIR,
        "queue_pressure.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()
# =========================================================
# 5. ONLINE DISTRIBUTION PIE CHART
# =========================================================

plt.figure(figsize=(8, 8), dpi=300)

sizes = [
    online["Accepted"],
    online["Rejected"]
]

labels = [
    "Accepted",
    "Rejected"
]

colors = sns.color_palette("deep")

plt.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors
)

plt.title(
    "Online Scheduler Job Distribution",
    fontsize=16,
    fontweight="bold"
)

plt.tight_layout()
plt.savefig(
    os.path.join(
        VISUAL_DIR,
        "job_distribution.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()