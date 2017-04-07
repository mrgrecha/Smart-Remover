import os

def check_for_files_and_links(list_of_files):
    """Return a list of only files in list that was given"""
    list = []
    for file in list_of_files:
        if not os.path.exists(file):
            msg = '%s is not exist' % file
            raise SystemError(msg)
        if os.path.isfile(file) or os.path.islink(file):
            list.append(file)
        else:
            msg = '%s is not a file or link' % file
            raise TypeError(msg)
        if not os.access(file, os.W_OK):
            msg = 'You have not such permissions for %s' % file
            raise SystemError(msg)

    return list

def check_for_dir(list_of_dir):
    """Return a list of only directories"""
    list = []
    for dir in list_of_dir:
        if not os.path.exists(dir):
            msg = '%s is not exist' % dir
            raise SystemError(msg)
        if os.path.isdir(dir):
            list.append(dir)
        else:
            msg = '%s is not a directory'%dir
            raise TypeError(msg)
        if not os.access(dir, os.W_OK):
            msg = 'You have not such permissions for %s' % dir
            raise SystemError(msg)
    return list

def check_for_trash_files(datebase, path_of_trash):
    """
    For files that are named in list_of_files checking if they are in trash bin and in database
    """
    trash_set = set()
    datebase_set = set()

    for data in datebase:
        datebase_set.add(str(data['hash']))
    for file in os.listdir(path_of_trash):
        trash_set.add(file)
    trash_set.remove('.DS_Store')
    if trash_set == datebase_set:
        return True
    elif trash_set > datebase_set:
        raise ValueError(list(trash_set - datebase_set))
    elif trash_set < datebase_set:
        raise StandardError(list(datebase_set - trash_set))

def yes_or_no():
    answer = str(raw_input('Y/N?'))
    if answer == 'Y' or answer =='y':
        return True
    elif answer == 'N' or answer == 'n':
        return False
    else:
        print 'Error. Try again!'
        yes_or_no()


