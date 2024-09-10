from pyspark.sql import SparkSession
import xml.etree.ElementTree as ET
import json

class File_to_DF:
    def __init__(self, app_name = 'File to DF'):
        # Initialize Spark session in the constructor
        self.spark = SparkSession.builder.appName(app_name).getOrCreate()

    def read_csv_as_DF(self, file_path, delimiter = '|', header=True):
        """
        Reads a CSV file and converts it to Pyspark DF.

        Parameters:
        file_path (str): Path to the CSV file.
        delimiter (str): Delimiter used in the CSV file (default is '|').
        header (bool): Whether the CSV file has a header (defualt is True).

        Returns:
        DF: Pyspark DF object.
        """
        # Read the CSV file with the given options
        df = self.spark.read.option("header", header).option("delimiter", delimiter).csv(file_path)

        return df
    

    def parse_xml(self, file_path):
        """
        Parses an XML file and returns a list of dictionaries representing each record.

        Parameters:
        xml_file (str): Path to the XML file.

        Returns:
        list: A list of dictionaries, where each dictionary is a record.
        """
        tree = ET.parse(file_path)
        root = tree.getroot()
        records = []

        for record in root.findall('RECORD'):
            record_dict = {}
            for column in record:
                record_dict[column.tag] = column.text
            
            records.append(record_dict)
        
        return records
    

    def read_xml_as_DF(self, file_path):
        """
        Reads an XML file, converts it to a list of dictionaries, and then converts it to a PySpark DF.

        Parameters:
        file_path (str): Path to the XML file.

        Returns:
        DF: PySpark DF object.
        """
        # Parse the XML file into a list of dictionaries
        parsed_data = self.parse_xml(file_path)

        # Convert the parsed data to Spark Dataframe
        df = self.spark.createDataFrame(parsed_data)

        return df
    

    def read_json_as_DF(self, file_path):
        """
        Reads a JSON file (expected to be in list of dictionaries format) and converts it to a PySpark DF.

        Parameters:
        file_path (str): Path to the XML file.

        Returns:
        DF: PySpark DF object.
        """

        # Convert the JSON data (list of dictionaries) to a Spark Dataframe
        df = self.spark.read.json(file_path)

        return df
    

    def stop_spark(self):
        """
        Stops the Spark session
        """
        self.spark.stop()