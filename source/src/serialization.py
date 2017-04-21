import json
import logging


def load_json(path):
    """Return a list of dicts in JSON-file"""
    try:
        with open(path, 'r') as db:
            arr_json_files = []
            for each_data in json.load(db):
                arr_json_files.append(each_data)
            return arr_json_files
    except Exception as e:
        logging.error('Error with database. Database is cleared.' + str(e))
        return []


def push_json(list_of_json, path):
    """Push a list of dicts to JSON-file"""
    with open(path, 'w') as db:
        json.dump(list_of_json, db, indent=4)
