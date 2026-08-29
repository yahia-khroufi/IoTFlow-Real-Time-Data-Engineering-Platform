from pyspark.sql import SparkSession

from readers.read_stream import ReadStream
from transformations.transform import IotTransformer
from configs.settings import settings
from quality.data_quality import DataQuality
from configs.schema import iot_schema_spark
from writer.writer_stream import WriterStream


def main():

    spark = (
        SparkSession.builder
        .appName(settings.app_name)
        .getOrCreate()
    )

    reader = ReadStream(spark)
    transformer = IotTransformer()
    quality = DataQuality()
    writer = WriterStream(settings)

    # nbronze--=> silver
    df = reader.read(
        settings.path_bronze,
         iot_schema_spark
    )
    df = transformer.clean(df)
    df = transformer.convert_type(df)
    df = quality.add_flags(df)
    df = transformer.add_partition(df)

    valid, invalide = quality.split(df)

    query_valid=writer.write_stream(
        valid,
        settings.path_silver,
        ["month", "day"]
    )

    query_invalid=writer.write_stream(
        invalide,
        settings.path_reject,
        ["month", "day"]
    )
    query_valid.awaitTermination()
    query_invalid.awaitTermination()
  

if __name__ == "__main__":
    main()
