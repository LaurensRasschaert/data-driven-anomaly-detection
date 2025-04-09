import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuratie
n_normal = 10000
n_vertical_scans = 100
n_horizontal_scans = 100
n_dst_ip_spikes = 100
n_unusual_pairs = 100

# IP en poorten pool
source_ips = [f"10.0.0.{i}" for i in range(1, 51)]
destination_ips = [f"192.168.1.{i}" for i in range(1, 51)]
ports = list(range(1024, 1100))

def generate_timestamp(start_time, n):
    return [start_time + timedelta(seconds=random.randint(0, 3600)) for _ in range(n)]

def generate_records(n, label, pattern_func):
    return pattern_func(n, label)

def normal_traffic(n, label):
    return pd.DataFrame({
        "@timestamp": generate_timestamp(datetime.now(), n),
        "source.ip": np.random.choice(source_ips, n),
        "destination.ip": np.random.choice(destination_ips, n),
        "source.port": np.random.randint(10000, 65000, n),
        "destination.port": np.random.choice(ports, n),
        "network.transport": np.random.choice(["tcp", "udp"], n),
        "session.iflow_bytes": np.random.randint(100, 20000, n),
        "session.iflow_pkts": np.random.randint(1, 100, n),
        "event.action": "flow_create",
        "session.id": np.random.randint(100000, 999999, n),
        "label": label
    })


def vertical_scan(n, label):
    src_ip = np.random.choice(source_ips)
    dst_ip = np.random.choice(destination_ips)
    timestamps = generate_timestamp(datetime.now(), n)
    dst_ports = np.random.choice(ports, n, replace=True)  # allow duplicate ports
    return pd.DataFrame({
        "@timestamp": timestamps,
        "source.ip": [src_ip] * n,
        "destination.ip": [dst_ip] * n,
        "source.port": np.random.randint(10000, 65000, n),
        "destination.port": dst_ports,
        "network.transport": ["tcp"] * n,
        "session.iflow_bytes": [0] * n,
        "session.iflow_pkts": [1] * n,
        "event.action": ["flow_create"] * n,
        "session.id": np.random.randint(100000, 999999, n),
        "label": [label] * n
    })



def horizontal_scan(n, label):
    src_ip = np.random.choice(source_ips)
    dst_port = np.random.choice(ports)
    dst_ips_sample = np.random.choice(destination_ips, n)
    timestamps = generate_timestamp(datetime.now(), n)
    return pd.DataFrame({
        "@timestamp": timestamps,
        "source.ip": [src_ip] * n,
        "destination.ip": dst_ips_sample,
        "source.port": np.random.randint(10000, 65000, n),
        "destination.port": [dst_port] * n,
        "network.transport": ["tcp"] * n,
        "session.iflow_bytes": [0] * n,
        "session.iflow_pkts": [1] * n,
        "event.action": ["flow_create"] * n,
        "session.id": np.random.randint(100000, 999999, n),
        "label": [label] * n
    })

def dst_ip_spike(n, label):
    dst_ip = np.random.choice(destination_ips)
    timestamps = [datetime.now()] * n
    return pd.DataFrame({
        "@timestamp": timestamps,
        "source.ip": np.random.choice(source_ips, n),
        "destination.ip": [dst_ip] * n,
        "source.port": np.random.randint(10000, 65000, n),
        "destination.port": np.random.choice(ports, n),
        "network.transport": ["tcp"] * n,
        "session.iflow_bytes": np.random.randint(50, 500, n),
        "session.iflow_pkts": np.random.randint(1, 10, n),
        "event.action": ["flow_create"] * n,
        "session.id": np.random.randint(100000, 999999, n),
        "label": [label] * n
    })

def unusual_pairs(n, label):
    timestamps = generate_timestamp(datetime.now(), n)
    return pd.DataFrame({
        "@timestamp": timestamps,
        "source.ip": [f"172.16.0.{i}" for i in range(n)],
        "destination.ip": [f"172.31.0.{i}" for i in range(n)],
        "source.port": np.random.randint(10000, 65000, n),
        "destination.port": np.random.choice(ports, n),
        "network.transport": ["udp"] * n,
        "session.iflow_bytes": np.random.randint(10, 100, n),
        "session.iflow_pkts": [1] * n,
        "event.action": ["flow_create"] * n,
        "session.id": np.random.randint(100000, 999999, n),
        "label": [label] * n
    })

#Combinatie
df = pd.concat([
    normal_traffic(n_normal, 0),
    vertical_scan(n_vertical_scans, 1),
    horizontal_scan(n_horizontal_scans, 1),
    dst_ip_spike(n_dst_ip_spikes, 1),
    unusual_pairs(n_unusual_pairs, 1)
]).sample(frac=1).reset_index(drop=True)

df.to_csv(r"C:\Users\laure\PycharmProjects\Data-Driven Anomaly Detection\data\dummy_network_logs.csv", index=False)

