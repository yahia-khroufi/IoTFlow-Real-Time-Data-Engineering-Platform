from pyspark.sql import SparkSession
from transformations.transform_gold import GoldTransform
from configs.settings import settings
from configs.schema import processed_iot_schema_spark
from quality.gold_quality import GoldQualite

def main():
    session=(
      SparkSession.builder
      .appName(settings.app_name)
      .getOrCreate()
    )
    #================
    
    df=(session.read
        .schema(processed_iot_schema_spark)
        .option("basePath", settings.path_silver)
        .parquet(f"{settings.path_silver}/month=*/day=*"))

    #================

    transform=GoldTransform()
    df=transform.transform(df)
    df=transform.add_partition(df)
    #================
    quality=GoldQualite()
    df_clean=quality.virifie(df)

    #================

    (df_clean.write
        .mode("overwrite")
        .partitionBy("month", "day")
        .parquet(settings.path_gold))

if __name__ == "__main__":
    main()
     
