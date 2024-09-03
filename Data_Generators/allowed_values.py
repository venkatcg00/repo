import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from typing import List, Dict, Tuple

def connect_to_database(db_config: Dict[str, str]) -> tuple:
    """
    Establish a connection to the database.

    Parameters:
    db_config (Dict[str, str]): A dictionary with databse connection parameters.

    Returns:
    Tuple: A tuple contaning the MySQL connection and cursor objects.
    """

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    return connection, cursor


def fetch_allowed_values(cursor: MySQLCursor, 
                         table_name: str, 
                         source_name: str, 
                         column_name: str
                         ) -> List[str]:
    """
    Fetch allowed values from a specific column in a MySQL table.

    Parameters: 
    cursor (MySQLCursor): The MySQL cursor object.
    table_name (str): The name of the table to query.
    source_name (str): The name of source for which values are to be retreived.
    column_name (str): The name of the column that stores the allowed values.

    Returns:
    List[str]: A list of allowed values from the specified column.
    """
    query = f"SELECT DISTINCT {column_name} FROM {table_name} WHERE SOURCE_ID = (SELECT SOURCE_ID FROM CSD_SOURCES WHERE SOURCE_NAME = {source_name})"
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]

def close_database_connection(connection: MySQLConnection, cursor: MySQLCursor) -> None:
    """
    Close the connection to the MySQL database.

    Parameters:
    connection (MySQLConnection): The MySQL connection object.
    cursor (MySQLCursor): The MySQL cursor object.
    """
    cursor.close()
    connection.close()
    