FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    g++ \
    gcc \
    python3 \
    python3-pip

RUN pip3 install pandas matplotlib seaborn

WORKDIR /app

CMD gcc input_generator.c -o builds/gen && \
    g++ -std=c++17 main.cpp -o builds/run && \
    ./builds/gen && \
    ./builds/run && \
    python3 charts.py