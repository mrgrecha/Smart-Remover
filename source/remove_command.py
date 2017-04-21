from command import Command
from dry_run import dry_run
from interactive import interactive
import file_object
import os
import sys
import shutil
import verification
import serialization
import logging
import directory
import re
import command_object
import my_exceptions
import bin_command

my_command = command_object.CommandObject()

class RFCommand(Command):

    def __init__(self, my_trash):
        super(Command, self).__init__()
        self.dried = my_trash.dried
        self.interactive = my_trash.interactive
        self.trash = my_trash

    def execute(self, list_of_files):
        self.delete_files(list_of_files, self.trash)

    def cancel(self, list_of_files):
        print 'Cancel for rfc'
        temp_recover_command = bin_command.RecCommand(self.trash)
        temp_recover_command.execute(list_of_files)
        print 'OK'

    @dry_run
    def real_delete(self, files_to_delete, length, my_trash):
        arr_files = [file_object.FileObject() for i in xrange(0, length)]
        for index, each_file in enumerate(files_to_delete):
            if os.path.islink(each_file):
                arr_files[index].set_type('Link')
            else:
                arr_files[index].set_type('File')
            arr_files[index].make_object(each_file)
            os.rename(each_file, str(arr_files[index].hash))
            shutil.move(arr_files[index].hash, my_trash.path_of_trash)
            my_trash.arr_json_files.append(arr_files[index].__dict__)
        my_command.remove_files([arr_files[ind].hash for ind in xrange(0, length)])

    @interactive
    def delete_files(self, list_of_files, my_trash):
        """Delete a list of files with checking for folders"""
        try:
            checked_list = verification.check_for_files_and_links(list_of_files)
            length = len(checked_list)
            self.real_delete(checked_list, length, my_trash)
            for removing_file in checked_list:
                my_trash.rootLogger.info('Removing ' + removing_file + ' to trash')

        except my_exceptions.NotSuchFileError as e:
            logging.error('Error:' + str(e))
            sys.exit(1)

        except my_exceptions.PermissionError as e:
            logging.error('Error:' + str(e))
            sys.exit(2)

        except my_exceptions.NotFileError as e:
            logging.error('Error:' + str(e))
            sys.exit(3)

        serialization.push_json(my_trash.arr_json_files, my_trash.database)


class RDCommand(Command):

    def __init__(self, my_trash):
        super(Command, self).__init__()
        self.dried = my_trash.dried
        self.interactive = my_trash.interactive
        self.trash = my_trash

    def name(self, list_of_args):
        return 'Remove Directories'

    def execute(self, list_of_dirs):
        self.delete_dir(list_of_dirs, self.trash)

    def cancel(self, list_of_files):
        print 'Cancel for rdc'
        temp_recover_command = bin_command.RecCommand(self.trash)
        temp_recover_command.execute(list_of_files)
        print 'OK'

    @dry_run
    def real_delete_dir(self, dirs_to_delete, length, my_trash):
        arr_dirs = [directory.Folder() for i in xrange(0, length)]
        for index, each_dir in enumerate(dirs_to_delete):
            directory.Folder.make_objects(arr_dirs[index], each_dir)
            os.rename(each_dir, str(arr_dirs[index].hash))
            shutil.move(str(arr_dirs[index].hash), my_trash.path_of_trash)
            my_trash.arr_json_files.append(arr_dirs[index].__dict__)
        my_command.remove_dirs([arr_dirs[ind].hash for ind in xrange(0, length)])

    @interactive
    def delete_dir(self, list_of_dirs, my_trash):
        """
        Delete a list of directories with checking
        :param list_of_dirs:
        :return:
        """
        try:
            checked_list_of_dirs = verification.check_for_dir(list_of_dirs, my_trash.path_of_trash)
            length = len(checked_list_of_dirs)
            self.real_delete_dir(checked_list_of_dirs, length, my_trash)
            for each_dir in checked_list_of_dirs:
                my_trash.rootLogger.info('Removing directory ' + each_dir + ' to trash')

        except my_exceptions.NotSuchFileError as e:
            logging.error('Error:' + str(e))
            sys.exit(1)

        except my_exceptions.PermissionError as e:
            logging.error('Error:' + str(e))
            sys.exit(2)

        except my_exceptions.NotFileError as e:
            logging.error('Error:' + str(e))
            sys.exit(3)

        except my_exceptions.RemoveError as e:
            logging.error('Error:' + str(e) + '. It is a trash folder.')
            sys.exit(4)

        serialization.push_json(my_trash.arr_json_files, my_trash.database)

class RRCommand(Command):

    def __init__(self, my_trash):
        super(Command, self).__init__()
        self.cur_dir = os.path.curdir
        self.dried = my_trash.dried
        self.interactive = my_trash.interactive
        self.trash = my_trash

    def execute(self, regex):
        self.delete_for_regex(self.cur_dir, regex, self.trash)

    def cancel(self, list_of_something):
        pass


    def delete_for_regex(self, cur_dir, regex, my_trash):

        """
        Removing for regular expression
        :param regex:
        :param cur_dir: current directory from which starts removing
        :return:
         """
        rfc = RFCommand(my_trash)
        rdc = RDCommand(my_trash)
        for name in os.listdir(cur_dir):
            path = os.path.join(cur_dir, name)
            if re.search(regex, name) and os.path.isfile(path):
                rfc.execute([path])
            elif os.path.isdir(path) and re.match(regex, name):
                rdc.execute([path])
            elif os.path.isdir(path) and not re.match(regex, name):
                self.delete_for_regex(path, regex)

def save_command():
    my_command.save()