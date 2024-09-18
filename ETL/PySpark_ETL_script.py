import os
from file_to_dataframe import read_csv, read_json, read_xml
from full_refresh import dataframe_full_refresh
from typing import List, Dict
import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor


def get_parameters(parameter_file_path: str) -> Dict[str, str]:
    """
    Fetch the setup parameters from the parameter file.
    
    Parameters:
    parameter_file_path (str): The path to the setup parameter file.

    Returns:
    Dict[str, str]: A dictionary containing parameter names and values
    """
    parameters = {}

    # Read the file and extract the parameters
    with open(parameter_file_path, 'r') as parameter_file:
        for line in parameter_file:
            # Strip any extra spaces or new line characters
            line = line.strip()

            # Ignore empty lines
            if line:
                # Split each line by "=" to get key and value
                key, value = line.split("=", 1)
                parameters[key.strip()] = value.strip()
    
    return parameters

# Get the directory where the current Python script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Navigate to the parent directory
project_directory = os.path.dirname(current_directory)

# Construct the path to the parameter file
parameter_file_path = os.path.join(project_directory, 'Application_Setup', 'Setup_parameters.txt')

parameters = get_parameters(parameter_file_path)

csv_df = read_csv(parameters['CSV_FILE'])
print(csv_df.info())

json_df = read_json(parameters['JSON_FILE'])
print(json_df.info())

xml_df = read_xml(parameters['XML_FILE'])
print(xml_df.info())

source_list = parameters['SOURCES_LIST'].split(',')

# MySQL database configuration
db_config = {
    'user' : parameters['DB_USER'],
    'password' : parameters['DB_PASSWORD'],
    'host' : parameters['DB_HOST'],
    'database' : parameters['DB_NAME']
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

for source in source_list:
    query = f"SELECT DISTINCT DATA_LOAD_STRATEGY FROM CSD_SOURCES WHERE UPPER(SOURCE_NAME) = UPPER('{source}')"
    cursor.execute(f"SELECT DISTINCT DATA_LOAD_STRATEGY FROM CSD_SOURCES WHERE UPPER(SOURCE_NAME) = UPPER('{source}')")
    data_load_strategy_list = cursor.fetchone()
    data_load_strategy = data_load_strategy_list[0]
    print(f'Data load strategy for source [{source}] = {data_load_strategy}')