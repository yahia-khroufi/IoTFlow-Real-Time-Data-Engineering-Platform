from pyspark.sql import DataFrame
from pyspark.sql import functions as F
import logging

logger=logging.getLogger("__name__")
class IotTransformer:

   ##PIPLINE!2

    def clean(self, df: DataFrame) -> DataFrame:
        return (
            df
            .withColumn("device_id", F.trim(F.col("device_id")))
            .withColumn("event_date", F.trim(F.col("event_date")))
            .withColumn("event_time", F.trim(F.col("event_time")))
            .withColumn("cpu_percent", F.trim(F.col("cpu_percent")))
            .withColumn("ram_percent", F.trim(F.col("ram_percent")))
            .withColumn("event_id", F.trim(F.col("event_id")))
            .withColumn("temperature", F.trim(F.col("temperature")))
          )
     
    def convert_type(self,df:DataFrame):
        return (
            df
              .withColumn("event_date", F.to_date("event_date", "dd/MM/yyyy"))
              .withColumn("event_time",F.try_to_timestamp(F.col("event_time")))
              .withColumn("cpu_percent",F.expr("try_cast(cpu_percent as DOUBLE)"))
              .withColumn("ram_percent",F.expr("try_cast(ram_percent as DOUBLE)"))
              .withColumn("temperature",F.expr("try_cast(temperature as DOUBLE)"))
        )

        
    def normalize(self, df: DataFrame) -> DataFrame:

        return  df.select(
        "device_id",
        "event_time",
        "temperature",
        "cpu_percent",
        "ram_percent" 
    )

    def add_partition(self,df):
       return (df.withColumn("year", F.year("event_time"))
              .withColumn("month", F.month("event_time"))
              .withColumn("day", F.dayofmonth("event_time")))
                
    


    
