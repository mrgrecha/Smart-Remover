# -*- coding: utf-8 -*-
import os
import datetime
import time
import directory
import logging

YES_TO_ALL = 1

logging.basicConfig(level=logging.DEBUG, filename='log.log')


def check_for_files_and_links(list_of_files):
    """Return a list of only files in list that was given"""
    checked_list = []
    for unchecked_file in list_of_files:
        if not os.path.exists(unchecked_file):
            msg = '%s is not exist' % unchecked_file
            raise SystemError(msg)
        if not os.access(unchecked_file, os.W_OK):
            msg = 'You have not such permissions for %s' % unchecked_file
            raise SystemError(msg)
        if os.path.isfile(unchecked_file) or os.path.islink(unchecked_file):
            checked_list.append(unchecked_file)
        else:
            msg = '%s is not a file or link' % unchecked_file
            raise SystemError(msg)
    return checked_list


def check_for_dir(list_of_dir):
    """Return a list of only directories"""
    checked_list = []
    for unchecked_dir in list_of_dir:
        if not os.path.exists(unchecked_dir):
            msg = '%s is not exist' % unchecked_dir
            raise SystemError(msg)
        if os.path.isdir(unchecked_dir):
            checked_list.append(unchecked_dir)
        else:
            msg = '%s is not a directory' % unchecked_dir
            raise OSError(msg)
        if not os.access(unchecked_dir, os.W_OK):
            msg = 'You have not such permissions for %s' % unchecked_dir
            raise SystemError(msg)
    return checked_list


def check_for_trash_files(database, path_of_trash):
    """
    For files that are named in list_of_files checking if they are in trash bin and in database
    """
    trash_set = set()
    database_set = set()

    for data in database:
        database_set.add(str(data['hash']))
    for path in os.listdir(path_of_trash):
        trash_set.add(path)
    if os.listdir(path_of_trash).count('.DS_Store'):
        trash_set.remove('.DS_Store')
    if trash_set == database_set:
        return True
    elif trash_set > database_set:
        raise ValueError(list(trash_set - database_set))
    elif trash_set < database_set:
        raise StandardError(list(database_set - trash_set))


def check_time(database, times):
    """
    Check database and trash bin for time policy
    :param database:
    :param times:
    :return:
    """
    my_list = []
    logging.info('These files are staying in the bin > %s' %
                 datetime.datetime.fromtimestamp(times).strftime('%m month %d days %H hours %M minutes %S seconds'))
    for index, json_dicts in enumerate(database):
        if time.time() - json_dicts['time_of_life'] >= times:
            logging.info(json_dicts['name'])
            my_list.append(json_dicts)
    return my_list


def check_memory(path_of_trash, size):
    """
    Checker for memory policy
    :param path_of_trash:
    :param size:
    :return:
    """
    if directory.Folder.add_size(path_of_trash) > size:
        logging.info('The size of folder is much than size in config. Please delete files.')
    else:
        return True


def yes_to_all():
    """
    Help function for mode Yes to All
    :return:
    """
    print 'Yes to all? '
    answer = str(raw_input('Yes/No '))
    if answer == 'Yes' or answer == 'yes' or answer == 'Y' or answer == 'y':
        return YES_TO_ALL
    elif answer == 'No' or answer == 'no' or answer == 'N'or answer == 'n':
        return True
    else:
        logging.error('Error. Try again!')
        yes_to_all()


def yes_or_no():
    """
    User input
    if yes - returns True
    if no - returns False
    :return:
    """
    answer = str(raw_input('Yes/No? '))
    if answer == 'Yes' or answer == 'yes' or answer == 'Y':
        return yes_to_all()
    elif answer == 'No' or answer == 'no' or answer == 'N':
        return False
    else:
        logging.error('Error. Try again!')
        yes_or_no()
