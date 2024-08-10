from datetime import date
import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Dict, Any, Union

class RDBMS_Library:
    def __init__(self,
                 host: str,
                 user: str, 
                 password: str, 
                 database: str
                ) -> None:
        """
        Initialize the MySQLDatabase class with connection parameters.
        """
        self.host: str = host
        self.user: str = user
        self.password: str = password
        self.database: str = database
        self.connection: Optional[mysql.connector.connection_cext.CMySQLConnection] = None
        
    def connect(self) -> None:
        """
        Establish a connection to the MySQL Database.
        """
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                      user=self.user,
                                                      password=self.password,
                                                      database=self.database
                                                      )
            if self.connection.is_connected():
                print(f"Connected to MySQL database: {self.database}")
        except Error as connection_error:
            print(f"Error while connecting to MySQL: {connection_error}")

    def disconnect(self) -> None:
        """
        Close the connection to the MySQL Database.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print(f"Disconnected from MySQL database: {self.database}")
        
    def execute_query(self,
                      sql_action: str,
                      table: str,
                      column_data: Optional[Dict[str, Any]] = None,
                      select_columns: Optional[List[str]] = None,
                      where: str = ""
                      ) -> Optional[Union[List[Dict[str, Any]], int]]:
        """
        Execute DML/DQL queries based on the action specified

        :param sql_action: Type of SQL action ('SELECT' or 'UPSERT').
        :param table: The table to perform the action on.
        :param column_data: A dictionary of column names and values for UPSERT operations.
        :param select_columns: A list of columns to retrieve for SELECT queries.
        :param where: A string representing the WHERE clause for filtering.
        :return: Result of SELECT query or affected rows in UPSERT operation.
        """

        if not self.connection or not self.connection.is_connected():
            print("No active database connection.")
            return None

        cursor = self.connection.cursor(dictionary=True)
        try:
            if sql_action.upper() == 'SELECT':
                # Build the SELECT query
                column_str: str = ", ".join(select_columns) if select_columns else "*"
                query: str = f"SELECT {column_str} FROM {table}"

                if where:
                    query += f" WHERE {where}"
                
                cursor.execute(query)
                results: List[Dict[str, Any]] = cursor.fetchall()
                return results
            
            elif sql_action.upper() == "UPSERT":
                # Perform UPSERT operation for SCD Type 2
                if column_data is None:
                    raise ValueError("Column data must be specified for UPSERT operation.")
                
                # Check for existing record.
                select_query: str = f"SELECT * FROM {table} WHERE {where}"
                cursor.execute(select_query)
                existing_record: Optional[Dict[str, Any]] = cursor.fetchone()

                if existing_record:
                    # If the record exists, update the old record and insert a new one.
                    update_query: str = f"UPDATE {table} SET ACTIVE_FLAG = 'N', END_DATE = %s WHERE {where}"
                    cursor.execute(update_query, (date.today(),))

                    # Insert the new record
                    placeholders: str = ", ".join(["%s"] * len(column_data))
                    columns_str: str = ", ".join(column_data.keys())
                    new_values: tuple = tuple(column_data.values()) + ("Y", date.today(), "2999-12-31 00:00:00")
                    insert_query: str = f"INSERT INTO {table} ({columns_str}, ACTIVE_FLAG, START_DATE, END_DATE) VALUES ({placeholders}, %s, %s, %s)"
                    cursor.execute(insert_query, new_values)
                else:
                    # Insert a new record
                    placeholders: str = ", ".join(["%s"] * len(column_data))
                    columns_str: str = ", ".join(column_data.keys())
                    new_values: tuple = tuple(column_data.values()) + ("Y", date.today(), "2999-12-31 00:00:00")
                    insert_query: str = f"INSERT INTO {table} ({columns_str}, ACTIVE_FLAG, START_DATE, END_DATE) VALUES ({placeholders}, %s, %s, %s)"
                    cursor.execute(insert_query, new_values)

                self.connection.commit()
                print(f"Upserted {cursor.rowcount} row(s) in {table}.")
                return cursor.lastrowid
            
            else:
                raise ValueError("Invalid SQL action specified. Use 'SELECT' or 'UPSERT'.")
            
        except Error as e:
            print(f"Error executing {sql_action} query: {e}")
            return None
        
        finally:
            cursor.close()