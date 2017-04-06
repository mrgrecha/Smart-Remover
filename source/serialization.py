import json

def num_of_dicts():
    """Returns a number of dicts in file"""
    with open ('DB.txt', 'r') as some_file:
        i = 0
        for each_data in json.load(some_file):
            i += 1
        return i




def load_json(file):
    """Return a list of dicts in JSON-file"""
    with open(file, 'r') as db:
        arr_json_files = []
        for each_data in json.load(db):
           arr_json_files.append(each_data)
        return arr_json_files


def push_json(list, file):
    """Push a list of dicts to JSON-file"""
    with open(file,'w') as db:
        json.dump(list, db, indent = 4)