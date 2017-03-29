import os

def check_for_files_and_links(list_of_files):
    """Return a list of only files in list that was given"""
    list = []
    for file in list_of_files:
        if os.path.isfile(file) or os.path.islink(file):
            list.append(file)
        else:
            msg = str(file) + ' is not a file or link'
            raise TypeError(msg)
    return list

def check_for_dir(list_of_dir):
    """Return a list of only directories"""
    list = []
    for dir in list_of_dir:
        if os.path.isdir(dir):
            list.append(dir)
        else:
            msg = str(dir) + ' is not a directory'
            raise TypeError(msg)
    return list

