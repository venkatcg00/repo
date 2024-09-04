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
        