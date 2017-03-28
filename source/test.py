import os.path

def check(list_of_files):
    """Return a list of only files in list that was given"""
    list = []
    for file in list_of_files:
        if os.path.isfile(file):
            list.append(file)
    return list
