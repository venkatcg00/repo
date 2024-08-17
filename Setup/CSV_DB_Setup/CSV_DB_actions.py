import csv
import json
import os
from typing import Dict, Any, List

class CSV_DB_Library:
    def __init__(self, config_file: str = 'csv_config.json') -> None:
        """
        Initialize the CSV_DB_Library with a configuration file specifying the CDV file path.
        """
        self.csv_path: str = self.load_config(config_file)

        # Check if the CSV file exists; if not, create it with headers
        if not os.path.exists(self.csv_path):
            self.create_csv_with_headers()

        @staticmethod
        def load_config(config_file: str) -> str:
            """
            Load the CSV file path from a configuration JSON file.

            :param config_file: The path to the configuration file.
            :return: The CSV file path specified in the configuration file.
            :raises: Exception if the configuration file is not found or is incorrectly formatted.
            """
            try:
                with open(config_file, 'r') as file:
                    config = json.load(file)
                    return config['csv_path']
            except FileNotFoundError:
                raise Exception("Configuration file not found.")
            except KeyError:
                raise Exception("CSV path not found in the configuration file.")
            except json.JSONDecodeError:
                raise Exception("Error decoding the configuration file.")
            
    def create_csv_with_headers(self) -> None:
        """
        Create a CSV file with headers if does not exist.

        :raises: ValueError if headers connot be determined.
        """
        headers = self.determine_headers()
        with open(self.csv_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

    def determine_headers(self) -> List[str]:
        """
        Determine the headers for the CSV file.

        :return: A list of headers for the CSV file.
        :raises: ValueError if the headers cannot be determined.
        """
        # You can set default headers or infer them from your data structure
        # For simplicity, we'll use a predefined list of headers
        headers = []
        return headers
    
    def insert_data(self, data: Dict[str, Any]) -> None:
        """
        Insert a dictionary of data into the CSV file.

        :param data: A dictionary containing the data to be inserted.
        :raises: ValueError if the data is not a dicitonary.
        """
        if isinstance(data, dict):
            headers = self.determine_headers()
            with open(self.csv_path, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writerow(data)
            print(f"Inserted data: {data}")
        else:
            raise ValueError("Data should be a dictionary.")
        
    def fetch_all_data(self) -> list[Dict[str, Any]]:
        """
        Fetch all records from the CSV file.

        :return: A list of dictionaries representing all records in the CSV file.
        """
        with open(self.csv_apth, 'r', new_line='') as file:
            reader = csv.DictReader(file)
            return list(reader)