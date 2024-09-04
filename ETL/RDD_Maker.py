from pyspark.sql import SparkSession
from pyspark.rdd import RDD
import xml.etree.ElementTree as ET
import json

class FileLoader:
    def __init__(self, spark: SparkSession) -> None:
        self.spark = spark
    
    def load_xml(self, file_path: str) -> RDD:
        """
        Load XML file into a Pyspark RDD.

        Parameters:
        file_path (str): Path to the XML file.
        
        Returns:
        RDD: Pyspark RDD containing the parsed XML data.
        """
        def parse_xml(line: str):
            root = ET.fromstring(line)
            return {child.tag: child.text for child in root}
        
        # Load the file as text and parse each line as XML
        rdd = self.spark.sparkContext.textfile(file_path).map(parse_xml)
        return rdd
    

    def load_json(self, file_path: str) -> RDD:
        """
        Load JSON file into a PySpark RDD.

        Parameters:
        file_path (str): Path to the JSON file.

        Returns:
        RDD: PySpark RDD containing JSON data.
        """
        # Load the file as text and parse each line as JSON
        rdd = self.spark.sparkContext.textFile(file_path).map(json.loads)
        return rdd
    
    def load_csv(self, file_path: str, delimiter: str = '|') -> RDD:
        """
        Load CSV file into a PySPark RDD

        Parameters:
        file_path (str): Path to the CSV file.
        delimieter (str): Delimiter used in the CSV file (default is '|').

        Returns:
        RDD: PySpark RDD containing CSV data.
        """
        # Load the file as text and split each line by delimiter
        rdd = self.spark.sparkContext.textFile(file_path).map(lambda line: line.split(delimiter))
        return rdd