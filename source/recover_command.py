from command import Command
from dry_run import dry_run
import file_object
import os
import shutil
import verification
import serialization
import logging
import directory
import re

class RecCommand(Command):

    def name(self):
        return 'Recover Files'

    def execute(self, list_of_files, my_trash):
        self.dried = my_trash.dried
        self.recover(list_of_files, my_trash)

    def cancel(self):
        print 'cancel for rec'

    @dry_run
    def force_recover(self, path_of_file, each_json_file, my_trash):
        os.renames(path_of_file, each_json_file['path'])
        my_trash.arr_json_files.remove(each_json_file)

    @dry_run
    def soft_recover(self, path_of_file, each_json_file, my_trash):
        my_trash.rootLogger.info('This file is exist. Would you like to replace it?')
        if verification.yes_or_no():
            os.rename(path_of_file, each_json_file['path'])
            my_trash.arr_json_files.remove(each_json_file)

    def recover(self, list_of_files, my_trash, force=True):
        """
        Recover files from trash bin to their locations
        :param list_of_files:
        :param force:
        :return:
        """
        for each_file in list_of_files:
            for each_json_file in my_trash.arr_json_files:
                if each_file == each_json_file['name'] or each_file == each_json_file['hash']:
                    path_of_file = my_trash.path_of_trash+'/'+str(each_json_file['hash'])
                    if force:
                        try:
                            self.force_recover(path_of_file, each_json_file, my_trash)
                            my_trash.rootLogger.info('Recovering ' + each_json_file['name'] + ' from bin')
                        except OSError as e:
                            my_trash.rootLogger.error('Error: ', e)
                    else:
                        try:
                            if os.path.exists(each_json_file['path']):
                                self.soft_recover(path_of_file, each_json_file, my_trash)
                                my_trash.rootLogger.info('Recovering ' + each_json_file['name'] + ' from bin')

                        except OSError as e:
                            logging.error('Error: ', e)

        serialization.push_json(my_trash.arr_json_files, my_trash.database)