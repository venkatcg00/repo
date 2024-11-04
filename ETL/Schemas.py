from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

csv_schema = StructType([
    StructField("TICKET_IDENTIFIER", IntegerType(), True),
    StructField("SUPPORT_CATEGORY", StringType(), True),
    StructField("AGENT_NAME", StringType(), True),
    StructField("DATE_OF_CALL", StringType(), True),  # Initially read as StringType
    StructField("CALL_STATUS", StringType(), True),
    StructField("CALL_TYPE", StringType(), True),
    StructField("TYPE_OF_CUSTOMER", StringType(), True),
    StructField("DURATION", IntegerType(), True),
    StructField("TICKET_STATUS", IntegerType(), True),
    StructField("RESOLVED_IN_FIRST_CONTACT", StringType(), True),
    StructField("RESOLUTION_CATEGORY", IntegerType(), True),
    StructField("RATING", StringType(), True)
])

json_schema = StructType([
    StructField("RECORD_ID", IntegerType(), True),
    StructField("INTERACTION_ID", IntegerType(), True),
    StructField("SUPPORT_CATEGORY", StringType(), True),
    StructField("AGENT_PSEUDO_NAME", StringType(), True),
    StructField("CONTACT_DATE", StringType(), True),  # Initially read as StringType
    StructField("INTERACTION_STATUS", StringType(), True),
    StructField("INTERACTION_TYPE", StringType(), True),
    StructField("TYPE_OF_CUSTOMER", StringType(), True),
    StructField("INTERACTION_DURATION", IntegerType(), True),
    StructField("TOTAL_TIME", IntegerType(), True),
    StructField("STATUS_OF_CUSTOMER_INCIDENT", StringType(), True),
    StructField("RESOLVED_IN_FIRST_CONTACT", StringType(), True),
    StructField("SOLUTION_TYPE", StringType(), True),
    StructField("RATING", IntegerType(), True)
])

xml_schema = StructType([
    StructField("SUPPORT_IDENTIFIER", IntegerType(), True),
    StructField("CONTACT_REGARDING", StringType(), True),
    StructField("AGENT_NAME", StringType(), True),
    StructField("DATE_OF_INTERACTION", StringType(), True),  # Initially read as StringType
    StructField("STATUS_OF_INTERACTION", StringType(), True),
    StructField("TYPE_OF_INTERACTION", StringType(), True),
    StructField("CUSTOMER_TYPE", StringType(), True),
    StructField("CONTACT_DURATION", StringType(), True),  # Read as StringType to handle "HH:MM:SS" format
    StructField("AFTER_CONTACT_WORK_TIME", StringType(), True),  # Read as StringType to handle "HH:MM:SS" format
    StructField("INCIDENT_STATUS", StringType(), True),
    StructField("FIRST_CONTACT_SOLVE", StringType(), True),
    StructField("TYPE_OF_RESOLUTION", StringType(), True),
    StructField("SUPPORT_RATING", IntegerType(), True),
    StructField("TIME_STAMP", StringType(), True)  # Initially read as StringType
])
