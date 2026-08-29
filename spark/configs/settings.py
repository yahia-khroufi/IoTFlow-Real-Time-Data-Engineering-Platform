from dotenv import load_dotenv
from dataclasses import dataclass
import os

load_dotenv()


@dataclass
class Settings:
    path_bronze: str
    path_silver: str
    path_gold: str
    path_reject: str
    path_checkpoint: str

    app_name: str

    kafka_bootstrap_servers: str
    kafka_topic: str

    CASSANDRA_HOSTS: str
    cassandra_keyspace: str
    table1_processed_gold: str


def get_settings() -> Settings:

    return Settings(
        path_bronze=os.getenv("BRONZE_PATH"),
        path_silver=os.getenv("SILVER_PATH"),
        path_gold=os.getenv("GOLD_PATH"),
        path_reject=os.getenv("REJECTED_PATH"),
        path_checkpoint=os.getenv("PATH_CHECK_POINT"),

        app_name=os.getenv("SPARK_APP_NAME"),

        kafka_bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        kafka_topic=os.getenv("KAFKA_TOPIC_IOT_METRICS"),

        CASSANDRA_HOSTS=os.getenv("CASSANDRA_HOSTS"),
        cassandra_keyspace=os.getenv("CASSANDRA_KEYSPACE"),
        table1_processed_gold=os.getenv("TABLE1"),
    )

settings = get_settings()
