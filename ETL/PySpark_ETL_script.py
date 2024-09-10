from DF_Maker import File_to_DF
from typing import Dict
import os


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

# Initialize the File to DF class
file_DF_reader = File_to_DF()

# Get the directory where the current Python script is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Navigate to the parent directory
project_directory = os.path.dirname(current_directory)

# Construct the path to the parameter file
parameter_file_path = os.path.join(project_directory, 'Application_Setup', 'Setup_parameters.txt')

parameters = get_parameters(parameter_file_path)

# Convert CSV to DF
csv_DF = file_DF_reader.read_csv_as_DF(parameters['CSV_FILE'])
print('CSV DF: ', csv_DF)

# Convert JSON to DF
json_DF = file_DF_reader.read_json_as_DF(parameters['JSON_FILE'])
print('JSON DF: ', csv_DF)

# Convert XML to DF
xml_DF = file_DF_reader.read_xml_as_DF(parameters['XML_FILE'])
print('XML DF: ', csv_DF)