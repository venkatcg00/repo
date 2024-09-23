import pandas as pd
from hashkey_generator import generate_md5
import mysql.connector

def get_last_loaded_record_id(db_config, source_name):
    try:
        connection  = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute(f"SELECT LAST_LOADED_RECORD_ID FROM CSD_SOURCES WHERE SOURCE_NAME = '{source_name}'")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result[0] if result else 0
    except mysql.connector.Error as e:
        print(f"Error connecting MySQl: {e}")
        return None
    

def incremental_dataframe(dataframe, column_name, record_id):
    dataframe['MD5_HASH'] = dataframe.apply(generate_md5, axis = 1)
    return dataframe[dataframe[column_name] > record_id]