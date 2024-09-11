import os
import random
import time
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from typing import List, Dict
from allowed_values import connect_to_database, fetch_allowed_values, close_database_connection


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


def get_max_record_id(xml_file_path: str) -> int:
    """
    Fetch the maximum SUPPORT_IDENTIFIER from the existing XML file.

    Parameters:
    xml_file_path (str): The file path of the XML data file.

    Returns:
    int: The maximum SUPPORT_IDENTIFIER found in the XML file, or 0 if the file is empty or does not exist.
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        if root:
            return max(int(record.find('SUPPORT_IDENTIFIER').text) for record in root.findall('RECORDS') if record.find('SUPPORT_IDENTIFIER').text is not None) # type: ignore
    except (FileNotFoundError, ET.ParseError):
        return 0
    return 0


def generate_random_record(
        record_id: int,
        support_categories: List[str],
        agent_psuedo_names: List[str],
        customer_types: List[str]
) -> ET.Element:
    """
    Generate a random record with specified data fields.

    Parameters:
    record_id (int): The unique SUPPORT_IDENTIFIER.
    support_categories (List[str]): List of allowed support categories.
    agent_pseudo_names (List[str]): List of allowed agent pseudo names.
    customer_types (List[str]): List of allowed customer types.

    Returns:
    ET.Elememt: An XML Element representing the generated record.
    """

    record = ET.Element("RECORD")
    ET.SubElement(record, "SUPPORT_IDENTIFIER").text = str(record_id)
    ET.SubElement(record, "CONTACT_REGARDING").text = random.choice(support_categories)
    ET.SubElement(record, "AGENT_CODE").text = random.choice(agent_psuedo_names)
    ET.SubElement(record, "DATE_OF_INTERACTION").text = (datetime.now() - timedelta(days = random.randint(0,1000))).strftime("%Y%m%d%H%M%S")
    ET.SubElement(record, "STATUS_OF_INTERACTION").text  = random.choice(["INTERACTION COMPLETED", "CUSTOMER DROPPED", "TRANSFERRED"])
    ET.SubElement(record, "TYPE_OF_INTERACTION").text = random.choice(["CALL", "CHAT"])
    ET.SubElement(record, "CUSTOMER_TYPE").text = random.choice(customer_types)
    ET.SubElement(record, "CONTACT_DURATION").text = str(timedelta(seconds = random.randint(10,600)))
    ET.SubElement(record, "AFTER_CONTACT_WORK_TIME").text  = str(timedelta(seconds = random.randint(10,600)))
    ET.SubElement(record, "INCIDENT_STATUS").text = random.choice(["RESOLVED", "PENDING RESOLUTION", "PENDING CUSTOMER UPDATE", "WORK IN PROGRESS", "TRANSFERRED TO ANOTHER QUEUE"])
    ET.SubElement(record, "FIRST_CONTACT_SOLVE").text  = random.choice(["TRUE", "FALSE"])
    ET.SubElement(record, "SUPPORT_RATING").text = str(random.choice([random.randint(1, 5)]))
    ET.SubElement(record, "TIME_STAMP").text = str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    return record

def generate_and_update_records(
        support_categories: List[str],
        agent_pseudo_names: List[str],
        customer_types: List[str],
        start_record_id: int,
        num_records: int
) -> List[ET.Element]:
    """
    Generate a specified number of new records and optionally update existing records.

    Parameters:
    support_categories (List[str]): List of allowed support categories.
    agent_pseudo_names (List[str]): List of allowed agent pseudo names.
    customer_types (List[str]): List of allowed customer types.
    start_record_id (int): The startinf SUPPORT_IDENTIFIER for the new records.
    num_records (int): The number of new records to generate.

    Returns:
    List[ET.Element]: A list containing the new and updated records.
    """
    records: List[ET.Element] = []
    record_id = start_record_id

    for i in range(num_records):
        record_id: int = record_id + 1
        new_record: ET.Element = generate_random_record(record_id, support_categories, agent_pseudo_names, customer_types)

        # Introduce NULL calues to some fiedls
        if random.random() < 0.1:
            key_to_nullify: str = random.choice(["CONTACT_REGARDING", "AGENT_CODE", "DATE_OF_INTERACTION", "STATUS_OF_INTERACTION","TYPE_OF_INTERACTION", "CUSTOMER_TYPE", "CONTACT_DURATION", "AFTER_CONTACT_WORK_TIME", "INCIDENT_STATUS", "FIRST_CONTACT_SOLVE", "SUPPORT_RATING"])
            new_record.find(key_to_nullify).text = None # type: ignore # type: ignore

        records.append(new_record)

        # Introduce updated to existing records
        if random.random() < 0.25 and record_id > 1:
            update_record_id: int = random.randint(1, record_id)
            update_record: ET.Element = generate_random_record(update_record_id, support_categories, agent_pseudo_names, customer_types)
            records.append(update_record)

    return records
    
def write_xml_data(xml_file_path: str, data: List[ET.Element]) -> None:
    """
    Write the generated data to an XML file.

    Parameters:
    xml_file_path (str): The file path where the XML data should be saved.
    data (list[Et.Element]): The data to be written to the XML file.
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except (FileNotFoundError, ET.ParseError):
        root = ET.Element("RECORDS")

    for record in data:
        root.append(record)
    
    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding = 'utf-8', xml_declaration = True)


def main() -> None:
    # Get the directory where the current Python script is located
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the parent directory
    project_directory = os.path.dirname(current_directory)

    # Construct the path to the parameter file
    parameter_file_path = os.path.join(project_directory, 'Application_Setup', 'Setup_parameters.txt')
    
    parameters = get_parameters(parameter_file_path)

    # MySQL database configuration
    db_config = {
        'user' : parameters['DB_USER'],
        'password' : parameters['DB_PASSWORD'],
        'host' : parameters['DB_HOST'],
        'database' : parameters['DB_NAME']
    }

    # Connect to the database
    connection, cursor = connect_to_database(db_config)

    # Fetch allowed values from the database
    support_categories: List[str] = fetch_allowed_values(cursor, "CSD_SUPPORT_AREAS", "'UBER'", "SUPPORT_AREA_NAME")
    agent_pseudo_names: List[str] = fetch_allowed_values(cursor, "CSD_AGENTS", "'UBER'", "PSEUDO_CODE")
    customer_types: List[str] = fetch_allowed_values(cursor, "CSD_CUSTOMER_TYPES", "'UBER'", "CUSTOMER_TYPE_NAME")

    # Close the database connection
    close_database_connection(connection, cursor)

    # Get XML file path and name from config
    xml_file_path: str = parameters['XML_FILE']

    # Fetch the maximum SUPPORT_IDENTIFIER from the existing XML file
    max_record_id: int = get_max_record_id(xml_file_path)

    while True:
        # Generate a random number of records
        num_records: int = random.randint(1, 1000)

        # Generate new and possibly updated records
        records: List[ET.Element] = generate_and_update_records(support_categories, agent_pseudo_names, customer_types, max_record_id, num_records)

        # Write the records to the XML file
        write_xml_data(xml_file_path, records)

        # Update the max_record_id for the next iteration
        max_record_id: int = get_max_record_id(xml_file_path)

        # Sleep for a random interval
        time.sleep(random.uniform(1, 50))

if __name__ == "__main__":
    main()