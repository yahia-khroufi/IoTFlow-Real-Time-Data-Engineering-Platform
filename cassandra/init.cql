CREATE KEYSPACE IF NOT EXISTS iot_metrics
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE iot_metrics;

CREATE TABLE IF NOT EXISTS metrics_by_devices (
    device_id text,
    event_date date,
    event_time timestamp,
    cpu_percent double,
    ram_percent double,
    temperature double,
    status text,
    event_id text,
    PRIMARY KEY ((device_id, event_date), event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

CREATE TABLE IF NOT EXISTS processed_events (
    event_id text PRIMARY KEY,
    processed_at timestamp
);

CREATE TABLE IF NOT EXISTS gold_table (
    device_id TEXT,
    event_time TIMESTAMP,
    avg_temperature DOUBLE,
    max_temperature DOUBLE,
    min_temperature DOUBLE,
    avg_cpu DOUBLE,
    avg_ram DOUBLE,
    PRIMARY KEY (device_id, event_time)
);

-- 4. Vérifier
DESCRIBE TABLES;