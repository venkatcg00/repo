import os
import random
import csv
import time
import configparser
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from allowed_values import connect_to_database, fetch_allowed_values, close_database_connection

def get_max_record_id(csv_file_path: str) -> int:
    """
    etch the maximum RECORD_IF from the existing CSV file.

    Parameters:
    csv_file_path (str): The file path of the CSV data file.

    Returns:
    int: The maximum RECORD_ID found in the CSV file, or 0 if the file is empty or does not exist.
    """
    try:
        with open(csv_file_path) as csv_file:
            reader = csv.reader(csv_file)
            lines = list(reader)
            return int(lines[-1][0])
    except (FileNotFoundError, csv.Error()):
        return 0
    

def generate_random_recod(
        record_id: int,
        support_categories: List[str],
        agent_pseudo_names: List[str],
        customer_types: List[str]
) -> list[str]:
    """
    Generate a random record with specified data fields.

    Parameters:
    record_id (int): The unique record ID.
    support_categories (List[str]): List of allowed support_categories.
    agent_pseudo_names (List[str]): List of allowed agent pseudo names.
    customer_types (List[str]): List of allowed customer types.

    Returns:
    List[str]: A list representing the generated record.
    """

    return [
        record_id,
        random.choice(support_categories),
        random.choice(agent_pseudo_names),
        (datetime.now() - timedelta(days = random.randint(0, 1000))).strftime('%m%d%Y%H%M%S'),
        random.choice(["Completed", "Dropped", "Transferred"]),
        random.choice(["Call", "Chat"]),
        random.choice(customer_types),
        random.choice([random.randint(10, 600)]),
        random.choice([random.randint(10, 600)]),
        random.choice(["Resolved", "Pending Resolution", "Pending Customer Update", "Work In Progress", "Transferred to another Queue"]),
        random.choice(["Yes", "No"]),
        random.choice(["Self-Help Option", "Support Team Intervention"]),
        random.choice(["Worst", "Bad", "Neutral", "Good", "Best"])
    ]


def generate_and_update_records(
        support_categories: List[str],
        agent_pseudo_names: List[str],
        customer_types: List[str],
        start_record_id: int,
        num_records: int
) -> List[List[str]]:
    """
    Generate a specified number of new records and optionally update existing records.

    Parameters:
    support_categories (List[str]): List of allowed support categories.
    agent_pseudo_names (List[str]): List of allowed agent pseudo names.
    customer_types (List[str]): List of allowed customer types.
    start_record_id (int): The starting RECORD_ID for the new records.
    num_records (int): The number of new records to generate.

    Returns:
    List[List[str]]: A list containing the new and updated records.
    """
    records  = []

    for i in range(num_records):
        record_id = start_record_id + 1
        new_record = generate_random_recod(record_id, support_categories, agent_pseudo_names, customer_types)

        # Introduce NULL values to some fields
        if random.random() < 0.1:
            key_to_nullify = random.choice(random.randint(1,12))
            new_record[key_to_nullify] = None
        
        records.append(new_record)

        # Introduce updated to data
        if random.random() < 0.25 and record_id > 1:
            update_record_id = random.randint(1, record_id)
            updated_record = generate_random_recod(update_record_id, support_categories, agent_pseudo_names, customer_types)

        records.append(updated_record)

    return records


def write_csv_data(csv_file_path: str, data: List[List[str]]) -> None:
    """
    Write the generated data to a CSV file.

    Parameters:
    csv_file_path (str): The file path where the CSV data should be saved.
    data (List[List[str]]): The data to be written to the CSV file.
    """
    try:
        with open(csv_file_path, 'r+') as csv_file:
            csv_file.write("|".join(data))
    except FileNotFoundError:
        with open(csv_file_path, 'w') as csv_file:
            csv_file.write('TICKET_IDENTIFIER|SUPPORT_CATEGORY|AGENT_NAME|DATE_OF_CALL|CALL_STATUS|CALL_TYPE|TYPE_OF_CUSTOMER|DURATION|WORK_TIME|TICKET_STATUS|RESOLVED_IN_FIRST_CONTACT|RESOLUTION_CATEGORY|RATING')
            csv_file.write("|".join(data))


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
    support_categories: List[str] = fetch_allowed_values(cursor, 'CSD_SUPPORT_AREAS', 'AT&T', 'SUPPORT_AREA_NAME')
    agent_pseudo_names: List[str] = fetch_allowed_values(cursor, 'CSD_AGENTS', 'AT&T', 'PSEUDO_CODE')
    customer_types: List[str] = fetch_allowed_values(cursor, 'CSD_CUSTOMER_TYPES', 'AT&T', 'CUSTOMER_TYPE_NAME')

    # Close the database connection
    close_database_connection(connection, cursor)

    # Get CAV file path and name from config
    csv_file_path: str = config.get('DEFAULT', 'CSV_FILE_PATH')
    csv_file_name: str = config.get('DEFAULT', 'CSV_FILE_NAME')
    full_csv_path: str = os.path.join(csv_file_path, csv_file_name)

    # Fetch the maximum RECORD_ID from the existinf CSV file
    max_record_id: int = get_max_record_id(full_csv_path)

    while True:
        # Generate a random number of records
        num_records: int = random.randint(1, 1000)

        # Generate new and possibly updated records
        records: List[List[str]] = generate_and_update_records(support_categories, agent_pseudo_names, customer_types, max_record_id, num_records)

        # Write the records to the CSV ile
        write_csv_data(full_csv_path, records)

        # Update max_record_id for the next iteration
        max_record_id += len([record for record in records if int(record[0]) > max_record_id])

        # Sleep for a random interval
        time.sleep(random.uniform(1, 50))

if __name__ == "__main__":
    main()