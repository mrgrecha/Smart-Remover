import json

def num_of_dicts():
    """Returns a number of dicts in file"""
    with open ('DB.txt', 'r') as some_file:
        i = 0
        for each_data in json.load(some_file):
            i += 1
        return i


# def load_json():
#     index = 0
#     try:
#         with open('DB.txt', 'r') as db:
#             arr_json_files = [file_object.FileObject() for i in xrange(0, num_of_dicts())]
#             for each_data in json.load(db):
#                 file_object.FileObject.make_from_dict(arr_json_files[index], each_data)
#                 index += 1
#             return arr_json_files
#     except Exception as e:
#         print e

def load_json():
    """Return a list of dicts in JSON-file"""
    with open('DB.txt', 'r') as db:
        arr_json_files = []
        for each_data in json.load(db):
           arr_json_files.append(each_data)
        return arr_json_files


def push_json(list, file):
    """Push a list of dicts to JSON-file"""
    json.dump(list, file, indent = 4)