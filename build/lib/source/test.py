import os.path

def check(list_of_files):
    list = []
    for file in list_of_files:
        if os.path.isfile(file):
            list.append(file)
    return list
