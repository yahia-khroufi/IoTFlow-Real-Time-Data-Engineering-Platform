import pandas as pd
import plotly.express as px
import streamlit as st
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from configs.settings import (
    CASSANDRA_HOSTS,
    CASSANDRA_KEYSPACE,
    CASSANDRA_PASSWORD,
    CASSANDRA_PORT,
    CASSANDRA_TABLE,
    CASSANDRA_USER,
)

st.set_page_config(page_title="IoTFlow Nexus", page_icon="📡", layout="wide")


@st.cache_resource
def get_session():
    auth_provider = None
    if CASSANDRA_USER and CASSANDRA_PASSWORD:
        auth_provider = PlainTextAuthProvider(
            username=CASSANDRA_USER,
            password=CASSANDRA_PASSWORD,
        )

    cluster = Cluster(
        contact_points=CASSANDRA_HOSTS,
        port=CASSANDRA_PORT,
        auth_provider=auth_provider,
        connect_timeout=10,
    )
    return cluster.connect(CASSANDRA_KEYSPACE)


@st.cache_data(ttl=30)
def load_devices() -> list[str]:
    rows = get_session().execute(
        f"SELECT DISTINCT device_id FROM {CASSANDRA_TABLE}"
    )
    return sorted(row.device_id for row in rows if row.device_id)


@st.cache_data(ttl=30)
def load_metrics(device_id: str | None, limit: int = 500) -> pd.DataFrame:
    session = get_session()
    columns = (
        "device_id, event_time, avg_cpu, avg_ram, avg_temperature, "
        "max_temperature, min_temperature"
    )

    if device_id and device_id != "All":
        rows = session.execute(
            f"SELECT {columns} FROM {CASSANDRA_TABLE} "
            "WHERE device_id = %s LIMIT %s",
            (device_id, limit),
        )
    else:
        rows = session.execute(
            f"SELECT {columns} FROM {CASSANDRA_TABLE} LIMIT %s",
            (limit,),
        )

    df = pd.DataFrame(list(rows))
    if not df.empty:
        df["event_time"] = pd.to_datetime(df["event_time"], utc=True)
        df = df.sort_values("event_time")
    return df


def main() -> None:
    st.title("📡 IoTFlow Nexus — IoT Metrics")
    st.caption(
        f"Source: Cassandra · keyspace `{CASSANDRA_KEYSPACE}` "
        f"· table `{CASSANDRA_TABLE}`"
    )

    with st.sidebar:
        st.header("Filters")
        try:
            devices = load_devices()
        except Exception as exc:
            st.error(f"Cassandra is unavailable: {exc}")
            if st.button("Retry connection"):
                st.cache_resource.clear()
                st.cache_data.clear()
                st.rerun()
            st.stop()

        device_choice = st.selectbox("Device", ["All", *devices])
        limit = st.slider("Maximum rows", 50, 5000, 500, 50)
        if st.button("Refresh data"):
            st.cache_data.clear()

    try:
        df = load_metrics(device_choice, limit)
    except Exception as exc:
        st.error(f"Unable to read Cassandra data: {exc}")
        return

    if df.empty:
        st.info("No Gold metrics are available yet. Run the Spark pipeline first.")
        return

    latest = df.groupby("device_id", as_index=False).tail(1)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Devices", df["device_id"].nunique())
    col2.metric("Latest average CPU", f"{latest['avg_cpu'].mean():.1f}%")
    col3.metric("Latest average RAM", f"{latest['avg_ram'].mean():.1f}%")
    col4.metric("Latest temperature", f"{latest['avg_temperature'].mean():.1f}°C")

    st.subheader("CPU and RAM usage")
    cpu_ram_df = df.melt(
        id_vars=["device_id", "event_time"],
        value_vars=["avg_cpu", "avg_ram"],
        var_name="metric",
        value_name="value",
    )
    cpu_ram = px.line(
        cpu_ram_df,
        x="event_time",
        y="value",
        color="device_id" if device_choice == "All" else "metric",
        line_dash="metric" if device_choice == "All" else None,
        labels={"value": "%", "event_time": "Time", "metric": "Metric"},
    )
    st.plotly_chart(cpu_ram, use_container_width=True)

    st.subheader("Temperature")
    temperature_df = df.melt(
        id_vars=["device_id", "event_time"],
        value_vars=["avg_temperature", "min_temperature", "max_temperature"],
        var_name="metric",
        value_name="value",
    )
    temperature = px.line(
        temperature_df,
        x="event_time",
        y="value",
        color="device_id" if device_choice == "All" else "metric",
        line_dash="metric" if device_choice == "All" else None,
        labels={"value": "°C", "event_time": "Time", "metric": "Metric"},
    )
    st.plotly_chart(temperature, use_container_width=True)

    st.subheader("Gold data")
    st.dataframe(df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
