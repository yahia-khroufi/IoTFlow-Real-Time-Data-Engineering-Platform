from pyspark.sql import functions as F

class GoldQualite:

    def virifie(self,df):
        return df.filter(
            F.col("avg_temperature").isNotNull()
            &F.col("max_temperature").isNotNull()
            &F.col("min_temperature").isNotNull()
            &F.col("avg_cpu").isNotNull()
            &F.col("avg_ram").isNotNull()
        )
      
       
