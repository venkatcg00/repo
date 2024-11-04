from pyspark.sql.functions import col, to_timestamp
from Schemas import csv_schema, json_schema, xml_schema
import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor

def read_csv(spark, file_path):
    df = spark.read.option("delimiter", "|").schema(csv_schema).csv(file_path, header=True)
    df = df.withColumn("DATE_OF_CALL", to_timestamp(col("DATE_OF_CALL"), "MMddyyyyHHmmss"))
    return df

def read_json(spark, file_path):
    df = spark.read.schema(json_schema).json(file_path)
    df = df.withColumn("CONTACT_DATE", to_timestamp(col("CONTACT_DATE"), "dd/MM/yyyy HH:mm:ss"))
    return df

def read_xml(spark, file_path):
    df = spark.read.format("com.databricks.spark.xml").option("rowTag", "RECORD").schema(xml_schema).load(file_path)
    df = df.withColumn("DATE_OF_INTERACTION", to_timestamp(col("DATE_OF_INTERACTION"), "yyyyMMddHHmmss"))
    df = df.withColumn("TIME_STAMP", to_timestamp(col("TIME_STAMP"), "yyyy/MM/dd HH:mm:ss"))
    return df