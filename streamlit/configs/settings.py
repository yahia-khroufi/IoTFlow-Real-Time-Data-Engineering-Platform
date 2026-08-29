from dotenv import load_dotenv
import os

load_dotenv()

# ============================================
# Configuration Cassandra
CASSANDRA_HOSTS = [
    host.strip()
    for host in os.getenv(
        "CASSANDRA_HOSTS",
        os.getenv("CASSANDRA_HOST", "cassandra"),
    ).split(",")
    if host.strip()
]
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "iot_metrics")
CASSANDRA_TABLE = os.getenv("CASSANDRA_TABLE", os.getenv("TABLE1", "gold_table"))
CASSANDRA_USER = os.getenv("CASSANDRA_USER", "")
CASSANDRA_PASSWORD = os.getenv("CASSANDRA_PASSWORD", "")
