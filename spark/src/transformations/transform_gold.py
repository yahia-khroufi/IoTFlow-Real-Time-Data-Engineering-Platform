from pyspark.sql import functions as F

class GoldTransform:

    def transform(self, df):

        return (
            df.groupBy(
            "device_id",
            "event_time"
                ).agg(
                    F.avg("temperature").alias("avg_temperature"),
                    F.max("temperature").alias("max_temperature"),
                    F.min("temperature").alias("min_temperature"),
                    F.avg("cpu_percent").alias("avg_cpu"),
                    F.avg("ram_percent").alias("avg_ram")
                )
        )


    def add_partition(self,df):
         return (df.withColumn("year", F.year("event_time"))
                .withColumn("month", F.month("event_time"))
                .withColumn("day", F.dayofmonth("event_time")))
                  
      
