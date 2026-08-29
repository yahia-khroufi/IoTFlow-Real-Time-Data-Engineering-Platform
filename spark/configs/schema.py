"""Spark schemas shared by the IoT pipeline jobs."""

from pyspark.sql.types import (
    DoubleType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)


# Values arrive from Kafka as JSON strings. The processing job is responsible
# for validating them and converting dates and numeric measurements.
iot_schema_spark = StructType(
    [
        StructField("device_id", StringType(), nullable=True),
        StructField("event_id", StringType(), nullable=True),
        StructField("event_date", StringType(), nullable=True),
        StructField("event_time", StringType(), nullable=True),
        StructField("cpu_percent", StringType(), nullable=True),
        StructField("ram_percent", StringType(), nullable=True),
        StructField("temperature", StringType(), nullable=True),
        StructField("status", StringType(), nullable=True),
    ]
)

# Columns consumed by the Silver -> Gold aggregation. Extra Silver quality
# columns are intentionally ignored by this projection schema.
processed_iot_schema_spark = StructType(
    [
        StructField("device_id", StringType(), nullable=False),
        StructField("event_time", TimestampType(), nullable=False),
        StructField("cpu_percent", DoubleType(), nullable=True),
        StructField("ram_percent", DoubleType(), nullable=True),
        StructField("temperature", DoubleType(), nullable=True),
    ]
)
