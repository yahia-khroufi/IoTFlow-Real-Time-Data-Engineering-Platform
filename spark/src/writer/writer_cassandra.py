import logging

class CassandraWriter:

    def __init__(self, settings):
        self.settings = settings

         
    def write_metrics_by_gold(self, df):
         query=   (
            df.write
            .format("org.apache.spark.sql.cassandra")
            .option(
                "spark.cassandra.connection.host",
                self.settings.CASSANDRA_HOSTS
            )
            .options(
                table=self.settings.table1_processed_gold,
                keyspace=self.settings.cassandra_keyspace
            )
            .mode("append")
            .save()
                 ) 
         return query

    