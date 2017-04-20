from command import Command
from dry_run import dry_run
from interactive import interactive
import os
import user_input
import serialization
import logging


class RecCommand(Command):

    def __init__(self, my_trash):
        super(Command, self).__init__()
        self.dried = my_trash.dried
        self.interactive = my_trash.interactive

    def name(self, my_list):
        """
        Get name of operation
        :param my_list:
        :return:
        """
        return 'Recover Files'

    def execute(self, list_of_files, my_trash):
        """
        Do this operation
        :param list_of_files:
        :param my_trash:
        :return:
        """
        self.recover(list_of_files, my_trash)

    def cancel(self):
        """
        Cancel last operation
        :return:
        """
        print 'cancel for rec'

    @dry_run
    def force_recover(self, path_of_file, each_json_file, my_trash):
        """
        Force recovering
        :param path_of_file:
        :param each_json_file:
        :param my_trash:
        :return:
        """
        os.renames(path_of_file, each_json_file['path'])
        my_trash.arr_json_files.remove(each_json_file)

    @dry_run
    def soft_recover(self, path_of_file, each_json_file, my_trash):
        """
        Soft recovering
        :param path_of_file:
        :param each_json_file:
        :param my_trash:
        :return:
        """
        answer = user_input.UserInput()
        my_trash.rootLogger.info('This file is exist. Would you like to replace it?')
        answer.ask_yes_or_no()
        if answer.state == 'yes':
            os.rename(path_of_file, each_json_file['path'])
            my_trash.arr_json_files.remove(each_json_file)
            logging.info('Recovering ' + each_json_file['name'] + ' from bin')
        else:
            pass

    @interactive
    def recover(self, list_of_files, my_trash):
        """
        Recover files from trash bin to their locations
        :param list_of_files:
        :param my_trash:
        :param force:
        :return:
        """
        for each_file in list_of_files:
            for each_json_file in my_trash.arr_json_files:
                if each_file == each_json_file['hash']:
                    path_of_file = os.path.join(my_trash.path_of_trash, str(each_json_file['hash']))
                    if my_trash.force:
                        try:
                            self.force_recover(path_of_file, each_json_file, my_trash)
                            my_trash.rootLogger.info('Recovering ' + each_json_file['name'] + ' from bin')
                        except OSError as e:
                            my_trash.rootLogger.error('Error: ', e)
                    else:
                        try:
                            if os.path.exists(each_json_file['path']):
                                self.soft_recover(path_of_file, each_json_file, my_trash)
                            else:
                                os.rename(os.path.join(my_trash.path_of_trash, each_json_file['hash']), each_json_file['path'])
                                my_trash.arr_json_files.remove(each_json_file)
                                logging.info('Recovering' + each_json_file['name'] + ' from bin')
                        except OSError as e:
                            logging.error('Error: ', e)

        serialization.push_json(my_trash.arr_json_files, my_trash.database)
