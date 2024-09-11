import os
import random
import time
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
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


def get_max_record_id(json_file_path: str) -> List[int]:
    """
    Fetch the maximum RECORD_ID and INCIDENT_ID from the existing JSON file.

    Parameters:
    json_file_path (str): The file path of the JSON data file.

    Returns:
    List(int): The list of maximum RECORD_ID and INTERACTION_ID found in the JSON file, or 0 if the file is empty or does not exist.
    """
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            if data:
                return [max(int(record["RECORD_ID"]) for record in data if int(record["RECORD_ID"]) is not None),
                max(int(record["INTERACTION_ID"]) for record in data if int(record["INTERACTION_ID"]) is not None)]
    except (FileNotFoundError, json.JSONDecodeError):
        return [0, 0]
    return [0, 0]


def generate_random_record(
        record_id: int,
        interaction_id: int,
        support_categories: List[str],
        agent_pseudo_names: List[str],
        customer_types: List[str]
) -> Dict[str, Optional[Any]]:
    """
    Generate a random record with specified data fields.

    Parameters:
    record_id (int): The unique record ID.
    interaction_id (int): The unique identifier of a support incident.
    support_categories (List[str]): List of allowed support_categories.
    agent_pseudo_names (List[str]): List of allowed agent pseudo names.
    customer_types (List[str]): List of allowed customer types.

    Returns:
    Dict[str, Optional[Any]]: A dictionary representing the generated record.
    """

    interaction_duration: int = random.choice([random.randint(10, 600)])

    return {
        "RECORD_ID" : record_id,
        "INTERACTION_ID" : interaction_id,
        "SUPPORT_CATEGORY" : random.choice(support_categories),
        "AGENT_PSEUDO_NAME" : random.choice(agent_pseudo_names),
        "CONTACT_DATE" : (datetime.now() - timedelta(days = random.randint(0, 1000))).strftime('%d/%m/%Y %H:%M:%S'),
        "INTERACTION_STATUS" : random.choice(["COMPLETED", "DROPPED", "TRANSFERRED"]),
        "INTERACTION_TYPE" : random.choice(["CALL", "CHAT"]),
        "TYPE_OF_CUSTOMER" : random.choice(customer_types),
        "INTERACTION_DURATION" : int(interaction_duration),
        "TOTAL_TIME" : int(interaction_duration + random.choice([random.randint(10, 600)])),
        "STATUS_OF_CUSTOMER_INCIDENT" : random.choice(["RESOLVED", "PENDING RESOLUTION", "PENDING CUSTOMER UPDATE", "WORK IN PROGRESS", "TRANSFERRED TO ANOTHER QUEUE"]),
        "RESOLVED_IN_FIRST_CONTACT" : random.choice(["YES", "NO"]),
        "SOLUTION_TYPE" : random.choice(["SELF-HELP OPTION", "SUPPORT TEAM INTERVENTION"]),
        "RATING" : random.choice([random.randint(1, 10)])
    }


def generate_and_update_records(
        support_categories: List[str],
        agent_pseudo_names: List[str],
        customer_types: List[str],
        start_record_id: int,
        start_interaction_id: int,
        num_records: int
) -> List[Dict[str, Optional[Any]]]:
    """
    Generate a specified number of new records and optionally update existing records.

    Parameters:
    support_categories (List[str]): List of allowed support categories.
    agent_pseudo_names (List[str]): List of allowed agent pseudo names.
    customer_types (List[str]): List of allowed customer types.
    start_record_id (int): The starting RECORD_ID for the new records.
    start_interaction_id (int): The starting INTERACTION_ID for the new records.
    num_records (int): The number of new records to generate.

    Returns:
    List[Dict[str, Optional[Any]]]: A list containing the new and updated records.
    """
    records = []
    record_id = start_record_id
    interaction_id = start_interaction_id

    for i in range(num_records):
        record_id = record_id + 1
        interaction_id = interaction_id + 1
        new_record = generate_random_record(record_id, interaction_id, support_categories, agent_pseudo_names, customer_types)

        # Introduce NULL values to some fields (up to 10% of data)
        if random.random() < 0.1:
            key_to_nullify = random.choice(["SUPPORT_CATEGORY", "AGENT_PSEUDO_NAME", "CONTACT_DATE", "INTERACTION_STATUS", "INTERACTION_TYPE", "TYPE_OF_CUSTOMER", "INTERACTION_DURATION", "TOTAL_TIME", "STATUS_OF_CUSTOMER_INCIDENT", "SOLUTION_TYPE", "RATING"])
            new_record[key_to_nullify] = None
        
        records.append(new_record)

        # Introduce updtes to existinf records (up to 25% of data)
        if random.random() < 0.25 and record_id > 1:
            update_interaction_id = random.randint(1, record_id)
            record_id = record_id + 1
            update_record = generate_random_record(record_id,update_interaction_id, support_categories, agent_pseudo_names, customer_types)
            records.append(update_record)

    return records

def write_json_data(json_file_path: str, data: List[Dict[str, Optional[Any]]]) -> None:
    """
    Write the generated data to a JSON file.

    Parameters:
    json_file_path (str): The file path where the JSON data should be saved.
    data (List[Dict[str, Optional[Any]]]): The data to be written to the JSON file.
    """
    
    try:
        if os.stat(json_file_path).st_size != 0:
            with open(json_file_path, 'r') as json_file:
                existing_data = json.load(json_file)
                for element in data:
                    existing_data.append(element)
        else:
            existing_data = data
    except FileNotFoundError or json.JSONDecodeError:
        existing_data = data

    # Write data to the json file.
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent = 4)


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
    support_categories: List[str] = fetch_allowed_values(cursor, "CSD_SUPPORT_AREAS", "'AMAZON'", "SUPPORT_AREA_NAME")
    agent_pseudo_names: List[str] = fetch_allowed_values(cursor, "CSD_AGENTS", "'AMAZON'", "PSEUDO_CODE")
    customer_types: List[str] = fetch_allowed_values(cursor, "CSD_CUSTOMER_TYPES", "'AMAZON'", "CUSTOMER_TYPE_NAME")

    # Close the database connection
    close_database_connection(connection, cursor)

    # Get JSON file path and name from config
    json_file_path: str = parameters['JSON_FILE']

    # Fetch the maximum RECORD_ID from the existinf JSON file
    max_ids: list = get_max_record_id(json_file_path)
    max_record_id = max_ids[0]
    max_interaction_id = max_ids[1]

    while True:
        # Generate a random number of records
        num_records: int = random.randint(1, 1000)

        # Generate new and possibly updated records
        records: List[Dict[str, Optional[Any]]] = generate_and_update_records(support_categories, agent_pseudo_names, customer_types, max_record_id, max_interaction_id, num_records)

        # Write the records to the JSON ile
        write_json_data(json_file_path, records)

        # Update max_record_id for the next iteration
        max_ids: list = get_max_record_id(json_file_path)
        max_record_id = max_ids[0]
        max_interaction_id = max_ids[1]

        # Sleep for a random interval
        time.sleep(random.uniform(1, 50))

if __name__ == "__main__":
    main()