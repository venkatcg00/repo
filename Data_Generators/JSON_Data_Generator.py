import os
import random
import time
import json
import configparser
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from allowed_values import connect_to_database, fetch_allowed_values, close_database_connection

def get_max_record_id(json_file_path: str) -> int:
    """
    Fetch the maximum RECORD_IF from the existing JSON file.

    Parameters:
    json_file_path (str): The file path of the JSON data file.

    Returns:
    int: The maximum RECORD_ID found in the JSON file, or 0 if the file is empty or does not exist.
    """
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            if data:
                return max(int(record["RECORD_ID"]) for record in data if record["RECORD_ID"] is not None)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0
    return 0


def generate_random_record(
        record_id: int,
        support_categories: List[str],
        agent_psuedo_names: List[str],
        customer_types: List[str]
) -> Dict[str, Optional[Any]]:
    """
    Generate a random record with specified data fields.

    Parameters:
    record_id (int): The unique record ID.
    support_categories (List[str]): List of allowed support_categories.
    agent_psuedo_names (List[str]): List of allowed agent psuedo names.
    customer_types (List[str]): List of allowed customer types.

    Returns:
    Dict[str, Optional[Any]]: A dictionary representing the generated record.
    """

    interaction_duration: int = random.choice([random.randint(10, 600)])

    return {
        "RECORD_ID" : record_id,
        "INTERACTION_ID" : random.choice([record_id, random.randint(1, record_id)]),
        "SUPPORT_CATEGORY" : random.choice(support_categories),
        "AGENT_PSUEDO_NAME" : random.choice(agent_psuedo_names),
        "CONTACT_DATE" : (datetime.now() - timedelta(days = random.randint(0, 1000))).strftime('%d%m%Y %H:%M:%S'),
        "INTERACTION_STATUS" : random.choice(["Completed", "Dropped", "Transferred"]),
        "INTERACTION_TYPE" : random.choice(["Call", "Chat"]),
        "TYPE_OF_CUSTOMER" : random.choice(customer_types),
        "INTERACTION_DURATION" : int(interaction_duration),
        "TOTAL_TIME" : int(interaction_duration + random.choice([random.randint(10, 600)])),
        "STATUS_OF_CUSTOMER_INCIDENT" : random.choice(["Resolved", "Pending Resolution", "Pending Customer Update", "Work In Progress", "Transferred to another Queue"]),
        "RESOLVED_IN_FIRST_CONTACT" : random.choice(["Yes", "No"]),
        "SOLUTION_TYPE" : random.choice(["Self-Help Option", "Support Team Intervention"]),
        "RATING" : random.choice([random.randint(1, 10)])
    }


def generate_and_update_records(
        support_categories: List[str],
        agent_psuedo_names: List[str],
        customer_types: List[str],
        start_record_id: int,
        num_records: int
) -> List[Dict[str, Optional[Any]]]:
    """
    Generate a specified number of new records and optionally update existing records.

    Parameters:
    support_categories (List[str]): List of allowed support categories.
    agent_psuedo_names (List[str]): List of allowed agent psuedo names.
    customer_types (List[str]): List of allowed customer types.
    start_record_id (int): The starting RECORD_ID for the new records.
    num_records (int): The number of new records to generate.

    Returns:
    List[Dict[str, Optional[Any]]]: A list containing the new and updated records.
    """
    records = []

    for i in range(num_records):
        record_id = start_record_id + 1
        new_record = generate_random_record(record_id, support_categories, agent_psuedo_names, customer_types)

        # Introduce NULL values to some fields (up to 10% of data)
        if random.random() < 0.1:
            key_to_nullify = random.choice(["SUPPORT_CATEGORY", "AGENT_PSUEDO_NAME", "CONTACT_DATE", "INTERACTION_STATUS", "INTERACTION_TYPE", "TYPE_OF_CUSTOMER", "INTERACTION_DURATION", "TOTAL_TIME", "STATUS_OF_CUSTOMER_INCIDENT", "SOLUTION_TYPE", "RATING"])
            new_record[key_to_nullify] = None
        
        records.append(new_record)

        # Introduce updtes to existinf records (up to 25% of data)
        if random.random() < 0.25 and record_id > 1:
            update_record_id = random.randint(1, record_id)
            update_record = generate_random_record(update_record_id, support_categories, agent_psuedo_names, customer_types)

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
        with open(json_file_path, 'r+') as json_file:
            existing_data = json.load(json_file)
            existing_data.extend(data)
            json_file.seek(0)
            json.dump(existing_data, json_file, indent = 4)
    except FileNotFoundError:
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent = 4)


def main() -> None:
    # Get the directory where the current Python script is located
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the parent directory
    project_directory = os.path.dirname(current_directory)

    # Construct the path to the parameter file
    cfg_file_path = os.path.join(project_directory, 'Setup', 'Initial_setup_parameters.cfg')
    
    config = configparser.ConfigParser()
    config.read(cfg_file_path)

    # MySQL database configuration
    db_config = {
        'user' : config.get('DEFAULT', 'DB_USER'),
        'password' : config.get('DEFAULT', 'DB_PASS'),
        'host' : 'localhost',
        'database' : config.get('DEFAULT', 'DB_NAME')
    }

    # Connect to the database
    connection, cursor = connect_to_database(db_config)

    # Fetch allowed values from the database
    support_categories = fetch_allowed_values(cursor, 'CSD_SUPPORT_AREAS', 'AMAZON', 'SUPPORT_AREA_NAME')
    agent_psuedo_names = fetch_allowed_values(cursor, 'CSD_AGENTS', 'AMAZON', 'PSUEDO_CODE')
    customer_types = fetch_allowed_values(cursor, 'CSD_CUSTOMER_TYPES', 'AMAZON', 'CUSTOMER_TYPE_NAME')

    # Close the database connection
    close_database_connection(connection, cursor)

    # Get JSON file path and name from config
    json_file_path: str = config.get('DEFAULT', 'JSON_FILE_PATH')
    json_file_name: str = config.get('DEFAULT', 'JSON_FILE_NAME')
    full_json_path: str = f"{json_file_path}/{json_file_name}"

    # Fetch the maximum RECORD_ID from the existinf JSON file
    max_record_id: int = get_max_record_id(full_json_path)

    while True:
        # Generate a random number of records
        num_records: int = random.randint(1, 1000)

        # Generate new and possibly updated records
        records: List[Dict[str, Optional[Any]]] = generate_and_update_records(support_categories, agent_psuedo_names, customer_types, max_record_id, num_records)

        # Write the records to the JSON ile
        write_json_data(full_json_path, records)

        # Update max_record_id for the next iteration
        max_record_id += len([record for record in records if record["RECORD_ID"] > max_record_id])

        # Sleep for a random interval (ledd than 50 seconds)
        time.sleep(random.uniform(1, 50))

if __name__ == "__main__":
    main()