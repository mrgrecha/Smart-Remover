# -*- coding: utf-8 -*-
import verification
import os
import shutil
import serialization
import pydoc
import datetime
import singleton
import ConfigParser
import logging
import termcolor
import memory_policy
import time_policy

class Trash(object):
    __metaclass__ = singleton.Singleton
    # TODO add checking for parent folders +/-
    # TODO add checking for the same names in dict +/-
    # TODO Undo
    # TODO policy +/-
    # TODO yes to all
    # TODO tests
    # TODO checks
    # TODO maybe add removing for index
    # TODO add check for sets when there both exceptions

    def __init__(self, path_of_config):
        if os.path.exists(path_of_config):
            config = ConfigParser.RawConfigParser()
            config.read(path_of_config)
            self.path_of_trash = config.get('Section_Custom', 'path')
            self.database = config.get('Section_Custom', 'database')
            self.max_size = config.getint('Section_Custom', 'max_size')
            self.max_number = config.getint('Section_Custom', 'max_num')
            self.max_list_height = 50
            self.max_time = config.getint('Section_Custom', 'max_time')
            self.arr_json_files = serialization.load_json(self.database)
            self.policy_for_trash = config.get('Section_Custom', 'policy_for_trash')
            self.silent = config.getboolean('Section_Custom', 'silent')
            self.dried = config.getboolean('Section_Custom', 'dry_run')
        else:
            self.path_of_trash = '/Users/Dima/.MyTrash'
            self.database = 'DB.json'
            self.max_size = 500000000
            self.max_number = 1000
            self.max_list_height = 50
            self.max_time = 1000
            self.arr_json_files = serialization.load_json(self.database)
            self.policy_for_trash = 'default'
            self.silent = False
            self.dried = False
        self.rootLogger = logging.getLogger()
        self.set_logger()
        self.update()
        self.check_policy()


    def check_policy(self):
        time_policy_instance = time_policy.time_policy()
        memory_policy_instance = memory_policy.memory_policy()
        if self.policy_for_trash == 'time':
            time_policy_instance.run(self)
        elif self.policy_for_trash == 'memory':
            memory_policy_instance.run(self)
        elif self.policy_for_trash == 'combo':
            time_policy_instance.run(self)
            memory_policy_instance.run(self)
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
            index + 1, termcolor.colored(each_file['name'], 'red'), termcolor.colored(each_file['type'], 'green'), termcolor.colored(each_file['hash'], 'yellow'),
            termcolor.colored(datetime.datetime.fromtimestamp(each_file['time_of_life']).strftime('%Y-%m-%d %H:%M:%S'), 'blue'), each_file['size'])

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


    def get_names(self):
        """

        :return: list of names of files in Database
        """
        list_of_names = []
        for items in self.arr_json_files:
            list_of_names.append(items['name'])
        return list_of_names
