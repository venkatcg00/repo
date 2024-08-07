# RDBMS_actions.py

import mysql.connector
from mysql.connector import Error

class MySQLDatabase:
    def __init__(self, host: str, , user: str, password: str, database: str):
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
        
    def execute_query(self, action: str, table: str, data: dict = None, where: dict = None, columns: list = None, ssi_key: str = None, ssi_value: str = None):
        """
        Execute DML/DQL queries based on the action specified

        :param action: Type of SQL action ('SELECT', 'INSERT', 'UPDATE', 'DELETE')
        """