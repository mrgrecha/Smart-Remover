# -*- coding: utf-8 -*-
import os
import datetime
import time
import directory
import logging
import my_exceptions

logging.basicConfig(level=logging.DEBUG, filename='log.log')


def check_for_files_and_links(list_of_files):
    """Return a list of only files in list that was given"""
    checked_list = []
    for unchecked_file in list_of_files:
        if not os.path.exists(unchecked_file):
            raise my_exceptions.NotSuchFileError(unchecked_file)

        if not os.access(unchecked_file, os.W_OK):
            raise my_exceptions.PermissionError(unchecked_file)

        if os.path.isfile(unchecked_file) or os.path.islink(unchecked_file):
            checked_list.append(unchecked_file)
        else:
            raise my_exceptions.NotFileError(unchecked_file)
    return checked_list


def check_for_dir(list_of_dir, path_of_trash):
    """Return a list of only directories"""
    checked_list = []
    for unchecked_dir in list_of_dir:

        if not os.path.exists(unchecked_dir):
            raise my_exceptions.NotSuchFileError(unchecked_dir)

        if os.path.abspath(unchecked_dir) == os.path.abspath(path_of_trash):
            raise my_exceptions.RemoveError(unchecked_dir)

        if os.path.isdir(unchecked_dir):
            checked_list.append(unchecked_dir)
        else:
            raise my_exceptions.NotDirectoryError(unchecked_dir)

        if not os.access(unchecked_dir, os.W_OK):
            raise my_exceptions.PermissionError(unchecked_dir)
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
        raise my_exceptions.TrashSetError(list(trash_set - database_set))
    elif trash_set < database_set:
        raise my_exceptions.DatabaseSetError(list(database_set - trash_set))
    else:
        raise my_exceptions.TrashSetError(list(trash_set - database_set))
        raise my_exceptions.DatabaseSetError(list(database_set - trash_set))


def check_time(database, times):
    """
    Check database and trash bin for time policy
    :param database:
    :param times:
    :return:
    """
    my_list = []
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
        return False
    else:
        return True
