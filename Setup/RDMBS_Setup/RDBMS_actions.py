# RDBMS_actions.py

import mysql.connector
from mysql.connector import Error

class MySQLDatabase:
    def __init__(self,
                 host: str,
                 user: str, 
                 password: str, 
                 database: str
                ):
        """
        Initialize the MySQLDatabase class with connection parameters.
        """

        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect(self):
        """
        Establish a connection to the MySQL Database.
        """
        try:
            self.connection = mysql.connector.connect(host = self.host,
                                                      user = self.user,
                                                      password = self.password,
                                                      database = self.database
                                                      )
            if self.connection.is_connected():
                print(f"Connection MySQL database: {self.database}")
        except Error as connection_error:
            print(f"Error while connecting to MySQL: {connection_error}")

    def disconnect(self):
        """
        Close the connection to the MySQL Database.
        """
        if self.connection.is_connected():
            self.connection.close()
            print(f"Disconnected from MySQL database: {self.database}")
        
    def execute_query(self,
                      sql_action: str,
                      table: str,
                      column_data: dict = None,
                      select_columns: list = None,
                      where: str = ""
                      )
        """
        Execute DML/DQL queries based on the action specified

        :param action: Type of SQL action ('SELECT' or 'UPSERT').
        :param table: The table to perform the action on.
        :param column_data: A dictionary of column names and values for UPSERT operations.
        :param select_columns: A list of columns to retreive for SELECT queries.
        :param where: A string representing the WHERE clause for filtering.

        """