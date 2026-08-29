from pyspark.sql import SparkSession
from readers.kafka_reader import KafkaReader
from transformations.transform_kafka import KafkaTransformer
from configs.settings import settings
from configs.schema import iot_schema_spark
from writer.writer_stream import WriterStream
import logging



def main():
    session=(
      SparkSession.builder
      .appName(settings.app_name)
      .getOrCreate()
    )
    #================
    
    reader=KafkaReader(session, settings)
    df=reader.read_stream()

    #================

    transform=KafkaTransformer()
    df=transform.parse_json(df,iot_schema_spark)
    df=transform.add_ingestion_time(df)

    #================
    write=WriterStream(settings)
    query=write.write_stream(df,settings.path_bronze,["month","day"])

    query.awaitTermination()

if __name__ == "__main__":
    main()
     
