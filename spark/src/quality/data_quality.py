from pyspark.sql import DataFrame
from pyspark.sql import functions as F


class DataQuality:

    def add_flags(self, df: DataFrame) -> DataFrame:

        return (
            df
            .withColumn(
                "invalid_device_id",
                F.col("device_id").isNull()
                | (F.col("device_id") == "")
            )
            .withColumn(
                "invalid_event_time",
                F.col("event_time").isNull()
            )
            .withColumn(
                "invalid_event_date",
                F.col("event_date").isNull()
            )
            .withColumn(
                "invalid_temperature",
                F.col("temperature").isNull()
                | (~F.col("temperature").between(-40, 100))
            )
            .withColumn(
                "invalid_cpu",
                F.col("cpu_percent").isNull()
                | (~F.col("cpu_percent").between(0, 100))
            )
            .withColumn(
                "invalid_ram",
                F.col("ram_percent").isNull()
                | (~F.col("ram_percent").between(0, 100))
            )
        )
    
    def split(self,df:DataFrame) ->tuple:

        condition = (
            ~F.col("invalid_device_id")
            &
            ~F.col("invalid_event_time")
            &
            ~F.col("invalid_temperature")
            &
            ~F.col("invalid_cpu")
            &
            ~F.col("invalid_ram")
        )

        valide=df.filter(condition)
        invalid=df.filter(~condition)
        return valide , invalid

    