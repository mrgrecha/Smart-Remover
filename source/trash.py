# -*- coding: utf-8 -*-
import verification
import file_object
import os
import shutil
import serialization
import directory
import pydoc
import datetime
import singleton
import re
import ConfigParser
import logging
from dry_run import dry_run


class Trash:
    __metaclass__ = singleton.Singleton
    # TODO add checking for parent folders +
    # TODO add checking for the same names in dict
    # TODO Undo
    # TODO check codes for recover
    # TODO dry run
    # TODO policy
    # TODO yes to all
    # TODO tests
    # TODO refactor code + 1.20 / 11
    # TODO color terminal
    # TODO checks
    # TODO add default setting if config does not exist

    def __init__(self, path_of_config):
        config = ConfigParser.RawConfigParser()
        config.read(path_of_config)
        self.path_of_trash = config.get('Section_Custom', 'path')
        self.database = config.get('Section_Custom', 'database')
        self.max_size = config.get('Section_Custom', 'max_size')
        self.max_number = config.get('Section_Custom', 'max_num')
        self.max_list_height = 50
        self.max_time = config.getint('Section_Custom', 'max_time')
        self.arr_json_files = serialization.load_json(self.database)
        self.policy_for_trash = config.get('Section_Custom', 'policy_for_trash')
        self.silent = config.getboolean('Section_Custom', 'silent')
        self.dried = config.getboolean('Section_Custom', 'dry_run')
        self.rootLogger = logging.getLogger()
        self.set_logger()
        self.update()
        self.check_policy()

    def check_policy(self):
        if self.policy_for_trash == 'time':
            self.time_update()
        elif self.policy_for_trash == 'memory':
            self.memory_update()
        elif self.policy_for_trash == 'combo':
            self.time_update()
            self.memory_update()
        elif self.path_of_trash == 'default':
            pass

    def set_logger(self):
        if self.silent:
            silentHandler = logging.StreamHandler()
            silentHandler.setLevel(logging.CRITICAL)
            self.rootLogger.addHandler(silentHandler)
        else:
            logFormatter = logging.Formatter("%(asctime)s[%(threadName)-12.12s][%(levelname)-5.5s] %(message)s")
            #
            # fileHandler = logging.FileHandler(filename='log.log')
            # fileHandler.setFormatter(logFormatter)
            # fileHandler.setLevel(logging.DEBUG)
            # self.rootLogger.addHandler(fileHandler)

            consoleHandler = logging.StreamHandler()
            consoleHandler.setLevel(logging.INFO)
            self.rootLogger.addHandler(consoleHandler)

    @dry_run
    def real_delete(self, files_to_delete, length):
        arr_files = [file_object.FileObject() for i in xrange(0, length + 1)]
        index = 0
        for each_file in files_to_delete:
            if os.path.islink(each_file[index]):
                arr_files[index].set_type('Link')
            else:
                arr_files[index].set_type('File')
            arr_files[index].make_object(each_file)
            os.rename(each_file, str(arr_files[index].hash))
            shutil.move(arr_files[index].hash, self.path_of_trash)
            self.arr_json_files.append(arr_files[index].__dict__)
            index += 1

    def delete_files(self, list_of_files):
        """Delete a list of files with checking for folders"""
        try:
            checked_list = verification.check_for_files_and_links(list_of_files)
            length = len(checked_list)
            self.real_delete(checked_list, length)
            for removing_file in checked_list:
                self.rootLogger.info('Removing ' + removing_file + ' to trash')

        except SystemError as e:
            logging.error('Error:' + str(e))

        serialization.push_json(self.arr_json_files, self.database)

    @dry_run
    def real_delete_dir(self, dirs_to_delete, length):
        arr_dirs = [directory.Folder() for i in xrange(0, length + 1)]
        index = 0
        for each_dir in dirs_to_delete:
            directory.Folder.make_objects(arr_dirs[index], each_dir)
            os.rename(each_dir, str(arr_dirs[index].hash))
            shutil.move(str(arr_dirs[index].hash), self.path_of_trash)
            self.arr_json_files.append(arr_dirs[index].__dict__)
            index += 1

    def delete_dir(self, list_of_dirs):
        """
        Delete a list of directories with checking
        :param list_of_dirs:
        :return:
        """
        try:
            checked_list_of_dirs = verification.check_for_dir(list_of_dirs)
            length = len(checked_list_of_dirs)
            self.real_delete_dir(checked_list_of_dirs, length)
            for each_dir in checked_list_of_dirs:
                self.rootLogger.info('Removing directory ' + each_dir + ' to trash')

        except SystemError as e:
            self.rootLogger.error('Error:' + str(e))
        except OSError as e:
            self.rootLogger.error('Error:' + str(e) + 'can not delete a parent folder')
        serialization.push_json(self.arr_json_files, self.database)

    def full_show(self):
        """
        Demonstrating a list of files with full description
        :return:
        """
        if serialization.num_of_dicts() == 0:
            logging.info('No files in trash')
        full_show_string = ''
        for index, each_file in enumerate(self.arr_json_files):
            full_show_string += '%d %s %s %s %s %d Bytes \n' % (
            index + 1, each_file['name'], each_file['type'], each_file['hash'],
            datetime.datetime.fromtimestamp(each_file['time_of_life']).strftime('%Y-%m-%d %H:%M:%S'), each_file['size'])

        if len(self.arr_json_files) > self.max_list_height:
            pydoc.pager(full_show_string)
        else:
            logging.info(full_show_string)

    def bin_show(self):
        """
        Demonstrating a list of files in trash bin
        :return:
        """
        if serialization.num_of_dicts() == 0:
            logging.info('No files in trash')
        for ind, json_file in enumerate(self.arr_json_files):
            logging.info("{0}. {1}".format(ind + 1, json_file))

    @dry_run
    def real_remove_from_trash(self, path):
        for index, each_dict in enumerate(self.arr_json_files):
            if each_dict['name'] == path:
                try:
                    shutil.rmtree(os.path.join(self.path_of_trash, str(each_dict['hash'])))
                except OSError:
                    os.remove(os.path.join(self.path_of_trash, str(each_dict['hash'])))
                self.arr_json_files.remove(self.arr_json_files[index])

    def remove_from_trash(self, list_of_files):
        """
        Remove a file from trash
        :param list_of_files:
        :return:
        """
        count = 0
        length = len(list_of_files)
        for path in list_of_files:
           self.real_remove_from_trash(path)
           self.rootLogger.info('Removing from trash %s' % path)

        serialization.push_json(self.arr_json_files, self.database)

        print length, count
        if length == count:
            self.rootLogger.info('There are no such files')

    def delete_for_regex(self, cur_dir, regex):

        """
        Removing for regular expression
        :param regex:
        :param cur_dir: current directory from which starts removing
        :return:
         """
        for name in os.listdir(cur_dir):
            path = os.path.join(cur_dir, name)
            if re.search(regex, name) and os.path.isfile(path):
                self.delete_files([path])
            elif os.path.isdir(path) and re.search(regex, name):
                self.delete_dir([path])
            elif os.path.isdir(path) and not re.search(regex, name):
                self.delete_for_regex(path, regex)

    def update(self):
        try:
            verification.check_for_trash_files(self.arr_json_files, self.path_of_trash)
        except ValueError as e:
            self.rootLogger.error('''Error: Unknown %s
        Delete them ?
        Y - delete them
        N - keep them''' % (e))
            if verification.yes_or_no():
                    for n in e[0]:
                        path_of_n = os.path.join(self.path_of_trash, n)
                        if os.path.isdir(path_of_n):
                            shutil.rmtree(path_of_n)
                        else:
                            os.remove(path_of_n)

        except StandardError as e:
            for elem in e[0]:
                for index, json_dict in enumerate(self.arr_json_files):
                    if elem == str(json_dict['hash']):
                        self.arr_json_files.remove(self.arr_json_files[index])
        serialization.push_json(self.arr_json_files, self.database)

    def time_update(self):
        list_of_time_files = verification.check_time(self.arr_json_files, self.max_time)
        self.rootLogger.info(list_of_time_files)
        self.rootLogger.info('Delete them?')
        if verification.yes_or_no():
            for path in list_of_time_files:
                path_of_file = os.path.join(self.path_of_trash, str(path['hash']))
                if os.path.isdir(path_of_file):
                    shutil.rmtree(path_of_file)
                else:
                    os.remove(path_of_file)
                self.arr_json_files.remove(path)
        serialization.push_json(self.arr_json_files, self.database)

    def memory_update(self):
        max_size_elem = 0
        index = 0
        name = ''
        if verification.check_memory(self.path_of_trash, self.max_size):
            pass
        else:
            logging.info('Clear the largest file?')
            if verification.yes_or_no():
                for i, elem in enumerate(self.arr_json_files):
                    if elem['size'] > max_size_elem:
                        max_size_elem = elem['size']
                        index = i
                        name = str(elem['hash'])
                try:
                    shutil.rmtree(os.path.join(self.path_of_trash, name))
                except OSError:
                    os.remove(os.path.join(self.path_of_trash, name))
                self.arr_json_files.remove(self.arr_json_files[index])
    @dry_run
    def force_recover(self, path_of_file, each_json_file):
        os.renames(path_of_file, each_json_file['path'])
        self.arr_json_files.remove(each_json_file)

    def soft_recover(self, path_of_file, each_json_file):
        self.rootLogger.info('This file is exist. Would you like to replace it?')
        if verification.yes_or_no():
            os.rename(path_of_file, each_json_file['path'])
            self.arr_json_files.remove(each_json_file)

    def recover(self, list_of_files, force=True):
        """
        Recover files from trash bin to their locations
        :param list_of_files:
        :param force:
        :return:
        """
        for each_file in list_of_files:
            for each_json_file in self.arr_json_files:
                if each_file == each_json_file['name']:
                    path_of_file = self.path_of_trash+'/'+str(each_json_file['hash'])
                    if force:
                        try:
                            self.force_recover(path_of_file, each_json_file)
                            self.rootLogger.info('Recovering ' + each_json_file['name'] + ' from bin')
                        except OSError as e:
                            self.rootLogger.error('Error: ', e)
                    else:
                        try:
                            if os.path.exists(each_json_file['path']):
                                self.soft_recover(path_of_file, each_json_file)
                                self.rootLogger.info('Recovering ' + each_json_file['name'] + ' from bin')

                        except OSError as e:
                            logging.error('Error: ', e)

        serialization.push_json(self.arr_json_files, self.database)

    def get_names(self):
        """

        :return: list of names of files in Database
        """
        list_of_names = []
        for items in self.arr_json_files:
            list_of_names.append(items['name'])
        return list_of_names
