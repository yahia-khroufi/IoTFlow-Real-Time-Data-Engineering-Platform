from pyspark.sql import SparkSession , DataFrame
from pyspark.sql.types import StructType
import logging
from configs.settings import settings
logger=logging.getLogger("__name__")
class ReadStream:
    def __init__(self,spark: SparkSession):
        self.spark=spark
    
    def read(self,path:str,schema:StructType):
             logger.info("start read into %s", path)
             return(
                  self.spark.readStream
                  .schema(schema)
                  .format("parquet")
                  .option("basePath", path)
                  .load(f"{path}/month=*/day=*")
             )

