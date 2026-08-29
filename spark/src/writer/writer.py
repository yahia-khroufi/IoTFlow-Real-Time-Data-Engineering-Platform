import logging
from pyspark.sql import DataFrame

class ParquetWriter:

    def write(self,path:str,df:DataFrame,partition=None):
        writer=(
            df.write
              .mode("append")
              .forma("parquet")
        )

        if partition:
            writer.partitionBy(*partition)
        return writer.save(path)

