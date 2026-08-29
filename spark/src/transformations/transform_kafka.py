import logging

from pyspark.sql import DataFrame, functions as F
from pyspark.sql.types import StructType

logger = logging.getLogger(__name__)


class KafkaTransformer:
    def parse_json(self, df: DataFrame, schema: StructType) -> DataFrame:
        """Decode Kafka's binary value and expose the payload fields."""
        return (
            df.withColumn(
                "data",
                F.from_json(F.col("value").cast("string"), schema),
            )
            .select(
                "data.*",
                F.col("timestamp").alias("kafka_timestamp"),
                F.col("partition").alias("kafka_partition"),
                F.col("offset").alias("kafka_offset"),
            )
        )

    def add_ingestion_time(self, df: DataFrame) -> DataFrame:
        """Add ingestion metadata and the columns used by Bronze partitions."""
        return (
            df.withColumn("time_ingestion", F.current_timestamp())
            .withColumn("month", F.month("time_ingestion"))
            .withColumn("day", F.dayofmonth("time_ingestion"))
        )
