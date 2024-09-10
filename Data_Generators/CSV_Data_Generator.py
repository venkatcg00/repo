import os
import random
import csv
import time
from typing import List, Dict
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

def get_max_record_id(csv_file_path: str) -> int:
    """
    Fetch the maximum TICEKT_IDENTIFIER from the existing CSV file.

    Parameters:
    csv_file_path (str): The file path of the CSV data file.

    Returns:
    int: The maximum TICEKT_IDENTIFIER found in the CSV file, or 0 if the file is empty or does not exist.
    """
    # Check if the file exists and is not empty
    if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
        try:
            with open(csv_file_path, mode = 'r', newline = '') as csv_file:
                reader = csv.DictReader(csv_file, delimiter = '|')
                record_ids = [int(row['TICKET_IDENTIFIER']) for row in reader]
                return max(record_ids)
        except Exception as e:
            return 0
    else:
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
        random.choice(["COMPLETED", "DROPPED", "TRANSFERRED"]),
        random.choice(["CALL", "CHAT"]),
        random.choice(customer_types),
        random.choice([random.randint(10, 600)]),
        random.choice([random.randint(10, 600)]),
        random.choice(["RESOLVED", "PENDING RESOLUTION", "PENDING CUSTOMER UPDATE", "WORK IN PROGRESS", "TRANSFERRED TO ANOTHER QUEUE"]),
        random.choice([1, 0]),
        random.choice(["SELF-HELP OPTION", "SUPPORT TEAM INTERVENTION"]),
        random.choice(["WORST", "BAD", "NEUTRAL", "GOOD", "BEST"])
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
    record_id = start_record_id

    for i in range(num_records):
        record_id = record_id + 1
        new_record = generate_random_recod(record_id, support_categories, agent_pseudo_names, customer_types)

        # Introduce NULL values to some fields
        if random.random() < 0.1:
            key_to_nullify = random.randint(1,12)
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
    header = ["TICKET_IDENTIFIER", "SUPPORT_CATEGORY", "AGENT_NAME", "DATE_OF_CALL", "CALL_STATUS", "CALL_TYPE", "TYPE_OF_CUSTOMER", "DURATION", "WORK_TIME", "TICKET_STATUS", "RESOLVED_IN_FIRST_CONTACT", "RESOLUTION_CATEGORY", "RATING"]
    try:
        
        with open(csv_file_path, 'a', newline = '') as csv_file:
            if os.path.getsize(csv_file_path) == 0:
                writer = csv.writer(csv_file, delimiter = '|')
                writer.writerow(header)
                writer.writerows(data)
            else:
                writer = csv.writer(csv_file, delimiter = '|')
                writer.writerows(data)
    except FileNotFoundError:
        with open(csv_file_path, 'w', newline = '') as csv_file:
            writer = csv.writer(csv_file, delimiter = '|')
            writer.writerow(header)
            writer.writerows(data)


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
    support_categories: List[str] = fetch_allowed_values(cursor, "CSD_SUPPORT_AREAS", "'AT&T'", "SUPPORT_AREA_NAME")
    agent_pseudo_names: List[str] = fetch_allowed_values(cursor, "CSD_AGENTS", "'AT&T'", "PSEUDO_CODE")
    customer_types: List[str] = fetch_allowed_values(cursor, "CSD_CUSTOMER_TYPES", "'AT&T'", "CUSTOMER_TYPE_NAME")

    # Close the database connection
    close_database_connection(connection, cursor)

    # Get CAV file path and name from config
    csv_file_path: str = parameters['CSV_FILE']

    # Fetch the maximum RECORD_ID from the existinf CSV file
    max_record_id: int = get_max_record_id(csv_file_path)

    while True:
        # Generate a random number of records
        num_records: int = random.randint(1, 1000)

        # Generate new and possibly updated records
        records: List[List[str]] = generate_and_update_records(support_categories, agent_pseudo_names, customer_types, max_record_id, num_records)

        # Write the records to the CSV ile
        write_csv_data(csv_file_path, records)

        # Update max_record_id for the next iteration
        max_record_id = get_max_record_id(csv_file_path)

        # Sleep for a random interval
        time.sleep(random.uniform(1, 50))

if __name__ == "__main__":
    main()