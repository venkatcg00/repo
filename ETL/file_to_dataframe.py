import pandas as pd
import json
import xml.etree.ElementTree as ET

def read_csv(file_path):
    return pd.read_csv(file_path, delimiter = '|')


def read_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return pd.json_normalize(data)

def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []
    for record in root.findall('RECORD'):
        record_data = {}
        for child in record:
            record_data[child.tag] = child.text
        data.append(record_data)
    return pd.DataFrame(data)