import re

from pyspark.sql import DataFrame

class WriterStream:
    def __init__(self, settings):
      self.settings = settings

    def write_stream(self, df: DataFrame, path, partition=None):
              checkpoint_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", path.strip("/"))
              writer=(
               df.writeStream
                .format("parquet")
                .option("path", path)
                .option(
                    "checkpointLocation",
                    f"{self.settings.path_checkpoint}/{checkpoint_name}",
                )
                .trigger(availableNow=True)
             )

              if partition:
                   writer.partitionBy(*partition)

              return writer.start()

    # Backward-compatible alias for existing jobs.
    def write_strem(self, df: DataFrame, path, partition=None):
        return self.write_stream(df, path, partition)

