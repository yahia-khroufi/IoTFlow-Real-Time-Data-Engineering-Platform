from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import (
    SparkSubmitOperator,
)


SPARK_KAFKA_PACKAGE = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3"
SPARK_CASSANDRA_PACKAGE = "com.datastax.spark:spark-cassandra-connector_2.12:3.5.1"
SPARK_CONFIG = {"spark.master": "local[2]"}
PIPELINE_ENV = {
    "BRONZE_PATH": "/data/pipeline_v2/bronze",
    "SILVER_PATH": "/data/pipeline_v2/silver",
    "GOLD_PATH": "/data/pipeline_v2/gold",
    "REJECTED_PATH": "/data/pipeline_v2/rejected",
    "PATH_CHECK_POINT": "/data/pipeline_v2/checkpoints/iot_metrics",
    "KAFKA_TOPIC_IOT_METRICS": "iot.metrics.raw",
}

with DAG(
    dag_id="iot_pipeline",
    start_date=datetime(2026, 8, 25),
    schedule=timedelta(minutes=5),
    catchup=False,
    max_active_runs=1,
    max_active_tasks=1,
    tags=["iot", "spark"],
) as dag:
    ingestion = SparkSubmitOperator(
        task_id="ingestion_iot",
        application="/opt/airflow/src/jobs/ingestion_pipline.py",
        conf=SPARK_CONFIG,
        packages=SPARK_KAFKA_PACKAGE,
        env_vars=PIPELINE_ENV,
    )

    processing = SparkSubmitOperator(
        task_id="process_iot",
        application="/opt/airflow/src/jobs/iot_pipline.py",
        conf=SPARK_CONFIG,
        env_vars=PIPELINE_ENV,
    )

    gold = SparkSubmitOperator(
        task_id="gold_iot",
        application="/opt/airflow/src/jobs/gold_pipline.py",
        conf=SPARK_CONFIG,
        env_vars=PIPELINE_ENV,
    )

    cassandra = SparkSubmitOperator(
        task_id="cassandra_iot",
        application="/opt/airflow/src/jobs/cassandra_pipline.py",
        conf=SPARK_CONFIG,
        packages=SPARK_CASSANDRA_PACKAGE,
        env_vars=PIPELINE_ENV,
    )

    ingestion >> processing >> gold >> cassandra
