import os, datetime, time, directory
import logging
logging.basicConfig(level=logging.DEBUG, filename = 'log.log')
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
            raise SystemError(msg)
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
            raise SError(msg)
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

def check_time(datebase, times):
    my_list = []
    logging.info('These files are staying in the bin > %s' % datetime.datetime.fromtimestamp(times).strftime('%m month %d days %H hours %M minutes %S seconds'))
    for index, json_dicts in enumerate(datebase):
        if time.time() - json_dicts['time_of_life'] >= times:
            logging.info(json_dicts['name'])
            my_list.append(json_dicts)
    return my_list


def check_memory(path_of_trash, size):
    if directory.Folder.add_size(path_of_trash) > size:
        logging.info('The size of folder is much than size in config. Please delete files.')
    else:
        return True


def yes_or_no():
    answer = str(raw_input('Y/N?'))
    if answer == 'Y' or answer =='y':
        return True
    elif answer == 'N' or answer == 'n':
        return False
    else:
        logging.error('Error. Try again!')
        yes_or_no()


