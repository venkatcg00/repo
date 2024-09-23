import pandas as pd
from hashkey_generator import generate_md5
import mysql.connector

def get_last_loaded_record_id(db_config):
    try:
        connection  = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT LAST_LOADED_RECORD_ID FROM CSD_SOURCES WHERE SOURCE_NAME = 'AMAZON'")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result[0] if result else 0
    except mysql.connector.Error as e:
        print(f"Error connecting MySQl: {e}")
        return None
    

def incremental_dataframe(dataframe, column_name, record_id):
    return dataframe[dataframe[column_name] > record_id]