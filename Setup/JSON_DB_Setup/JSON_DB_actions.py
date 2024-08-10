import json
from pysondb import db
from typing import Dict, Any, List

class PysonDB_Library:
    def __init__(self, config_file: str = 'pysondb_config.json') -> None:
        """
        Initialize the PysonDBLibrary with a configuration file specifying the database path.
        """
        self.db_path: str = self.load_config(config_file)
        self.database = db.getDb(self.db_path)

    @staticmethod
    def load_config(config_file: str) -> str:
        """
        Load the database configuration from a JSON file.

        :param config_file: The path to the configuration file.
        :return: The database path specified in the configuration file.
        :raises: Exception if the configuration file is not found or is incorrectly formatted.
        """
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
                return config['database_path']
        except FileNotFoundError:
            raise Exception("Configuration file not found.")
        except KeyError:
            raise Exception("Database path not found in configuration.")
        except json.JSONDecodeError:
            raise Exception("Error decoding the configuration file.")

    def insert_data(self, data: Dict[str, Any]) -> None:
        """
        Insert a dictionary of data into the database.

        :param data: A dictionary containing the data to be inserted.
        :raises: ValueError if the data is not a dictionary.
        """
        if isinstance(data, dict):
            self.database.add(data)
            print(f"Inserted data: {data}")
        else:
            raise ValueError("Data should be a dictionary.")

    def fetch_all_data(self) -> List[Dict[str, Any]]:
        """
        Fetch all records from the database.

        :return: A list of dictionaries representing all records in the database.
        """
        return self.database.getAll()