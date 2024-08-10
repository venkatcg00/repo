import xml.etree.ElementTree as ET
import json
from typing import Optional, List, Dict, Any


class XMLDB_library:
    def __init__(self, config_file: str):
        """
        Initialize the XMLDB_library class with the path to the XML file from the config file.

        :param config_file: Path to the configuration file containing the database path.
        """
        self.file_path: str = self.load_config(config_file)
        self.tree: Optional[ET.ElementTree] = None
        self.root: Optional[ET.Element] = None
        self.load_database()

    @staticmethod
    def load_config(config_file: str) -> str:
        """
        Load the database path from the JSON configuration file.

        :param config_file: Path to the configuration file.
        :return: The database file path.
        """
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
                return config['database_path']
        except FileNotFoundError:
            raise Exception("Configuration file not found.")
        except KeyError:
            raise Exception("Database path not found in the configuration.")
        except json.JSONDecodeError:
            raise Exception("Error decofing the file.")
        
    def load_database(self) -> None:
        """
        Load the XML database into memory.
        """
        try:
            self.tree = ET.parse(self.file_path)
            self.root = self.tree.getroot()
            print(f"Loaded XML database from {self.file_path}")
        except FileNotFoundError:
            # Initialize a new XML file with a root element if the file does not exist.
            self.root = ET.Element('database')
            self.tree = ET.ElementTree(self.root)
            self.save_database()
            print(f"Initialized new XML database at {self.file_path}")
            
    def save_database(self) -> None:
        """
        Save the current state of the XML database to file.
        """
        if self.tree is not None:
            self.tree.write(self.file_path, encoding = 'utr-8', xml_declaration=True)

    def insert_data(self, data: Dict[str, Any]) -> None:
        """
        Insert a new record into the XML database.

        :param data: A dictionary of data to insert.
        """
        if self.root is None:
            raise Exception("Database not loaded properly.")
        
        record = ET.Element('record')
        for key, value in data.items():
            element = ET.SubElement(record, key)
            element.text = str(value)
        self.root.append(record)
        self.save_database()
        print("Inserted new record into XML database.")

    def fetch_all_data(self) -> List[Dict[str, str]]:
        """
        Fetch all records from the XML database.

        :return: A list of dictionaries representing the records.
        """
        if self.root is None:
            raise Exception("Database not loaded properly.")
        
        records: List[Dict[str, str]] = []
        for record in self.root.findall('record'):
            record_data = {child.tag: child.text for child in record}
            records.append(record_data)
        return records