# Cloud Resource Scheduler with DevOps Automation

## Overview

This project simulates a real-world cloud resource scheduling system using advanced scheduling algorithms, workload simulation, runtime analytics, Docker containerization, and CI/CD automation.

The system dynamically allocates CPU, RAM, Storage, and Bandwidth resources to incoming jobs while maximizing revenue and utilization efficiency.


## Features

- Static Greedy Scheduling
- Online Discrete Event Scheduling
- Dynamic Workload Generation
- Resource Utilization Analytics
- Revenue Optimization
- Queue Congestion Monitoring
- Automated Visualization Generation
- Dockerized Execution
- GitHub Actions CI/CD
- Artifact Upload Automation


## Tech Stack

| Layer | Technology |
|---|---|
| Core Algorithms | C++ |
| Visualization | Python |
| Analytics | Pandas |
| Graphs | Matplotlib / Seaborn |
| Containerization | Docker |
| Version Control | Git + GitHub |
| CI/CD | GitHub Actions |


## System Workflow

```text
Workload Generator
        ↓
Input Dataset Generation
        ↓
Online Cloud Scheduler
        ↓
Resource Allocation
        ↓
Metrics Collection
        ↓
Visualization Generation
        ↓
CI/CD Artifact Upload



---

# DOCKER EXECUTION

Add:

```md id="n2m4vu"
## Docker Execution

### Build Image

```bash
docker build -t cloud-scheduler .

Run Project
docker run --rm -v $(pwd):/app cloud-scheduler



---

# CI/CD SECTION

Add:

```md id="2nmh2r"
## CI/CD Pipeline

GitHub Actions automatically:

- Builds the project
- Generates workloads
- Executes scheduling simulation
- Produces runtime metrics
- Generates visual analytics
- Uploads artifacts automatically


## Complexity Analysis

| Component | Complexity |
|---|---|
| Workload Generation | O(n) |
| Greedy Sorting | O(n log n) |
| Online Scheduling | O(n log n) |
| Priority Queue Operations | O(log n) |
| Visualization Generation | O(n) |


## Folder Structure

```text
cloud-scheduler/
│
├── builds/
├── outputs/
│   ├── logs/
│   ├── metrics/
│   └── visualizations/
│
├── .github/workflows/
├── charts.py
├── input_generator.c
├── main.cpp
├── Dockerfile
└── README.md