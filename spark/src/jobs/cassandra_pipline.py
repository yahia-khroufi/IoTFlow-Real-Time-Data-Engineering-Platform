from pyspark.sql import SparkSession
from configs.settings import settings
from writer.writer_cassandra import CassandraWriter
import logging

def main():
    session=(
      SparkSession.builder
      .appName(settings.app_name)
      .getOrCreate()
    )
    #================
    
    df=session.read.parquet(settings.path_gold)

    #================

    writer=CassandraWriter(settings)
    writer.write_metrics_by_gold(df)
    
if __name__ == "__main__":
    main()
