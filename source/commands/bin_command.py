import logging
import os
import shutil

import source.src.serialization
import source.src.user_input
from source.src.dry_run import dry_run

import command_object
import remove_command
from command import Command
from source.src.interactive import interactive

class RecCommand(Command):

    def __init__(self, my_trash):
        super(Command, self).__init__()
        self.dried = my_trash.dried
        self.interactive = my_trash.interactive
        self.trash = my_trash
        self.files_to_return = []

    def execute(self, list_of_files):
        """
        Do this operation
        :param list_of_files:
        :return:
        """
        self.recover(list_of_files, self.trash)
        return self.files_to_return

    def cancel(self, list_of_files):
        """
        Cancel last operation
        :return:
        """
        temp_remove_files_command = remove_command.RFCommand(self.trash)
        temp_remove_dirs_command = remove_command.RDCommand(self.trash)
        self.trash.rootLogger.info('cancel for rec')
        for each_file in list_of_files:
            if os.path.isdir(each_file):
                temp_remove_dirs_command.execute([each_file])
            elif os.path.isfile(each_file) or os.path.islink(each_file):
                temp_remove_files_command.execute([each_file])
        # else:
        #     for each_file in list_of_files:
        #         if os.path.isdir(each_file):
        #             temp_remove_dirs_command.execute([each_file], self.trash)
        #         elif os.path.isfile(each_file) or os.path.islink(each_file):
        #             temp_remove_files_command.execute([each_file], self.trash)

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
        self.files_to_return.append(each_json_file['path'])

    @dry_run
    def soft_recover(self, path_of_file, each_json_file, my_trash):
        """
        Soft recovering
        :param path_of_file:
        :param each_json_file:
        :param my_trash:
        :return:
        """
        answer = source.src.user_input.UserInput()
        my_trash.rootLogger.info('This file is exist. Would you like to replace it?')
        answer.ask_yes_or_no()
        if answer.state == 'yes':
            os.rename(path_of_file, each_json_file['path'])
            my_trash.arr_json_files.remove(each_json_file)
        else:
            pass
        self.files_to_return.append(each_json_file['path'])

    @dry_run
    def simple_recover(self,each_json_file, my_trash):
        """
        Recover of element with no exceptions
        :param each_json_file: dict of file
        :param my_trash: the instance of trash
        :return:
        """
        os.rename(os.path.join(my_trash.path_of_trash, each_json_file['hash']), each_json_file['path'])
        my_trash.arr_json_files.remove(each_json_file)

    @interactive
    def recover(self, list_of_files, my_trash):
        """
        Recover files from trash bin to their locations
        :param list_of_files:
        :param my_trash:
        :return:
        """
        temp_list = []
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
                                logging.info('Recovering ' + each_json_file['name'] + ' from bin')
                            else:
                                self.simple_recover(each_json_file, my_trash)
                                logging.info('Recovering ' + each_json_file['name'] + ' from bin')
                                self.files_to_return.append(each_json_file['path'])
                        except OSError as e:
                            logging.error('Error: ', e)

        source.src.serialization.push_json(my_trash.arr_json_files, my_trash.database)


class DFTCommand(Command):
    def __init__(self, my_trash):
        super(Command, self).__init__()
        self.dried = my_trash.dried
        self.interactive = my_trash.interactive
        self.trash = my_trash
        self.files_to_return = []

    def execute(self, list_of_files):
        """
        Deleting from trash function
        :param list_of_files: Files to delete
        :return:
        """
        self.remove_from_trash(list_of_files, self.trash)
        return self.files_to_return

    def cancel(self, list_of_files):
        """
        Cancel last operation
        :param list_of_files:
        :return:
        """
        self.trash.rootLogger.info('Delete from trash can not be undo')

    @dry_run
    def real_remove_from_trash(self, list_of_files, my_trash):
        """
        Removing prepared files from trash
        :param list_of_files: files to remove
        :param my_trash: the instance of trash
        :return:
        """
        for path in list_of_files:
            for index, each_dict in enumerate(my_trash.arr_json_files):
                if each_dict['hash'] == path:
                    try:
                        shutil.rmtree(os.path.join(my_trash.path_of_trash, str(each_dict['hash'])))
                    except OSError:
                        os.remove(os.path.join(my_trash.path_of_trash, str(each_dict['hash'])))
                    self.files_to_return.append([my_trash.arr_json_files[index]['name']] )
                    my_trash.rootLogger.info('Removing from trash %s' % my_trash.arr_json_files[index]['name'])
                    my_trash.arr_json_files.remove(my_trash.arr_json_files[index])
    @interactive
    def remove_from_trash(self, list_of_files, my_trash):
        """
        Remove a file from trash
        :param list_of_files: list of files to remove
        :return:
        """
        count = 0
        length = len(list_of_files)
        self.real_remove_from_trash(list_of_files, my_trash)

        source.src.serialization.push_json(my_trash.arr_json_files, my_trash.database)
        if length == count:
            my_trash.rootLogger.info('There are no such files')
