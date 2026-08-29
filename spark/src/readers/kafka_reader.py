import logging

from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)


class KafkaReader:
    def __init__(self, spark: SparkSession, settings):
        self.spark = spark
        self.settings = settings

    def read_stream(self):
        logger.info(
            "Reading Kafka topic %s from %s",
            self.settings.kafka_topic,
            self.settings.kafka_bootstrap_servers,
        )
        return (
            self.spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", self.settings.kafka_bootstrap_servers)
            .option("subscribe", self.settings.kafka_topic)
            .option("startingOffsets", "earliest")
            .option("failOnDataLoss", "false")
            .load()
        )
