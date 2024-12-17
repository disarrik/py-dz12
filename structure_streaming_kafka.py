from pyspark.sql import SparkSession
from time import sleep
from pyspark.sql.functions import col, from_json, to_timestamp, to_number, hour, minute, cast
from pyspark.sql.types import StructType, StringType, IntegerType, DecimalType, DateType, TimestampType, LongType
from datetime import datetime
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'

# явным образом задаем структуру json-контента
schema = StructType() \
  .add("transaction_id",IntegerType()) \
  .add("user_id", StringType()) \
  .add("amount", DecimalType()) \
  .add("timestamp", TimestampType()) \
  .add("location", StringType())

# users_schema = StructType() \
#   .add("id",IntegerType()) \
#   .add("name", StringType()) \
#   .add("registration_address", StringType()) \
#   .add("last_known_location", StringType())

spark = SparkSession.builder.appName("SparkStreamingKafka") \
  .config("spark.driver.extraClassPath", "postgresql-42.7.3.jar") \
  .getOrCreate()

users = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/db") \
    .option("user", "user") \
    .option("password", "password") \
    .option("dbtable", "users") \
    .load()

input_stream = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "transactions") \
  .option("startingOffsets", "earliest") \
  .option("failOnDataLoss", False) \
  .load() \
  .selectExpr("CAST(value AS STRING)") \
  .select(from_json(col("value"), schema).alias("parsed_value")) \
  .select("parsed_value.*")

join_stream = input_stream.join(users, input_stream.user_id == users.id, "left_outer") \
  .filter(
        (col("amount") > 1000) | \
        (col("registration_address") != col("location")) | \
        (col("last_known_location") != col("location")) | \
        (
            (hour(col("timestamp")) >= 23) &  # Больше или равно 23:00
            (hour(col("timestamp")) <= 5) &  # Меньше или равно 5:00
            (minute(col("timestamp")) >= 0) &  # Больше или равно 0 минут
            (minute(col("timestamp")) < 60)   # Меньше 60 минут
        )
  ) \
  .withColumnRenamed("transaction_id", "value") \
  .selectExpr("CAST(value as STRING)") \
  .writeStream.format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("topic", "suspicious") \
  .option("checkpointLocation", "checkpoints") \
  .start() \
  .awaitTermination()


