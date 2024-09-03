import random
import time
import json
import configparser
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from allowed_values import connect_to_database, fetch_allowed_values, close_database_connection

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
    support_categories (List[str]): List of allowed support categories.
    agent_psuedo_names (List[str]): List of allowed agent names.
    customer_types (List[str]): List of allowed customer types.

    Returns:
    Dict[str, Optional[Any]]: A dictionary representing the generated record.
    """

    interaction_duration: int = random.choice([random.randint(10, 600), None])

    return {
        "RECORD_ID": record_id,
        "INTERACTION_ID": random.choice([record_id,random.randint(1, record_id)]),
        "SUPPORT_CATEGORY": random.choice(support_categories),
        "AGENT_PSUEDO_NAME": random.choice(agent_psuedo_names),
        "CONTACT_DATE": (datetime.now() - timedelta(days=random.randint(0, 1000))).strftime("%d%m%Y %H:%M:%S"),
        "INTERACTION_STATUS": random.choice(["Completed", "Dropped", "Transferred"]),
        "INTERACTION_TYPE": random.choice(["Call", "Chat"]),
        "TYPE_OF_CUSTOMER": random.choice(customer_types),
        "INTERACTION_DURATION": interaction_duration,
        "TOTAL_TIME": (interaction_duration + random.choice([random.randint(10, 600), None])),
        "STATUS_OF_CUSTOMER_INCIDENT": random.choice(["Resolved", "Pending Resolution", "Pending Customer Update", "Work In Progress", "Transferred to another Queue"]),
        "RESOLVED_IN_FIRST_CONTACT": random.choice(["Yes", "No"]),
        "SOLUTION_TYPE": random.choice(["Self-Help Option", "Support Team Intervention"]),
        "RATING": random.choice([random.randint(1, 10), None])
    }


def generate_data_records(
        support_categories: List[str],
        agent_psuedo_names: List[str],
        customer_types: List[str],
        initial_record_id: int = 1
) -> List[Dict[str, Optional[Any]]]:
    """
    Generate a list of data records with random content.

    Parameters:
    support_categories (List[str]): List of allowed support categories.
    agent_psuedo_name (List[str]): List of allowed psuedo names.
    customer_types (List[str]): List of allowed customer types.
    initial_record_id (int): The starting record ID for data generation.

    Returns:
    List[Dict[str, Optional[Any]]]: A list of generated data records.
    """
    data: List[Dict[str, Optional[Any]]] = []
    record_id = initial_record_id

    for _ in range(random.randint(5, 20)):
        record = generate_random_record(record_id, support_categories, agent_psuedo_names, customer_types)

        # Introduce NULL values to some fields (up to 10% of data)
        if random.random() < 0.1:
            key_to_nullify = random.choice(list(record.keys()))
            record[key_to_nullify] = None

        data.append(record)

        # Introduce updates to existinf records (up to 25% of total data)
        if random.random() < 0.25 and record_id > 1:
            update_record_id = random.randint(1, record_id)
            update_record = generate_random_record(update_record_id, support_categories, agent_psuedo_names, customer_types)
            data.append(update_record)

        record_id += 1

    return data


def write_json_data(json_file_path: str, data: List[Dict[str, Optional[Any]]]) -> None:
    """
    Write the generated data to a JSON file.

    Parameters:
    json_file_path (str): The file path where the JSON data should be saved.
    data (List[Dict[str, Optional[Any]]]): The data to be written to the JSON file.
    """
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main() -> None:
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read("path")

    db_config = {
        'user': config.get('DEFAULT', 'DB_USER'),
        'password': config.get('DEFAULT', 'DB_PASS'),
        'host' : 'localhost',
        'database' : config.get('DEFAULT', 'DB_NAME')
    }

    # Connect to the database
    connecton, cursor = connect_to_database(db_config)

    # Fetch allowed values values from the database
    support_categories = fetch_allowed_values(cursor, 'CSD_SUPPORT_AREAS', 'AMAZON', 'SUPPORT_AREA_NAME')
    agent_psuedo_names = fetch_allowed_values(cursor, 'CSD_AGENTS', 'AMAZON', 'PSUEDO_CODE')
    customer_types = fetch_allowed_values(cursor, 'CSD_CUSTOMER_TYPES', 'AMAZON', 'CUSTOMER_TYPE_NAME')

    # Close the database connection
    close_database_connection(connecton, cursor)

    # Generate random data records
    data = generate_data_records(support_categories, agent_psuedo_names, customer_types)

    # Write the data to a JSON file
    json_file_path = config.get('DEFAULT','JSON_FILE_PATH')
    write_json_data(json_file_path, data)

if __name__ == "__main__":
    main()