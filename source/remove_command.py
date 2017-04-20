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

my_command = command_object.CommandObject()

class RFCommand(Command):

    def __init__(self, my_trash):
        super(Command, self).__init__()
        self.dried = my_trash.dried
        self.interactive = my_trash.interactive

    def name(self, list_of_files):
        return_list = ' '.join([str(item) for item in list_of_files])
        return 'Remove Files' + return_list

    def execute(self, list_of_files, my_trash):
        self.delete_files(list_of_files, my_trash)

    def cancel(self):
        print 'cancel for rfc'

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
        my_command.remove_files(files_to_delete)

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

    def name(self, list_of_args):
        return 'Remove Directories'

    def execute(self, list_of_dirs, my_trash):
        self.delete_dir(list_of_dirs, my_trash)

    def cancel(self):
        print 'cancel for rdc'

    @dry_run
    def real_delete_dir(self, dirs_to_delete, length, my_trash):
        arr_dirs = [directory.Folder() for i in xrange(0, length)]
        for index, each_dir in enumerate(dirs_to_delete):
            directory.Folder.make_objects(arr_dirs[index], each_dir)
            os.rename(each_dir, str(arr_dirs[index].hash))
            shutil.move(str(arr_dirs[index].hash), my_trash.path_of_trash)
            my_trash.arr_json_files.append(arr_dirs[index].__dict__)
        my_command.remove_dirs(dirs_to_delete)

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

    def name(self, list_of_args):
        return 'Remove RegEx'

    def execute(self, regex, my_trash):
        self.delete_for_regex(self.cur_dir, regex, my_trash)

    def cancel(self):
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
                rfc.execute([path], my_trash)
            elif os.path.isdir(path) and re.match(regex, name):
                rdc.execute([path], my_trash)
            elif os.path.isdir(path) and not re.match(regex, name):
                self.delete_for_regex(path, regex, my_trash)

class DFTComand(Command):
    def __int__(self, my_trash):
        self.dried = my_trash.dried
        self.interactive = my_trash.interactive

    def name(self, list_of_args):
        return 'Delete from trash'

    def execute(self, list_of_files, my_trash):
        self.remove_from_trash(list_of_files, my_trash)

    def cancel(self):
        print 'Delete from trash can not be undo'

    @dry_run
    def real_remove_from_trash(self, path, my_trash):
        for index, each_dict in enumerate(my_trash.arr_json_files):
            if each_dict['hash'] == path:
                try:
                    shutil.rmtree(os.path.join(my_trash.path_of_trash, str(each_dict['hash'])))
                except OSError:
                    os.remove(os.path.join(my_trash.path_of_trash, str(each_dict['hash'])))
                my_trash.arr_json_files.remove(my_trash.arr_json_files[index])
                my_command.remove_from_trash(path)

    @interactive
    def remove_from_trash(self, list_of_files, my_trash):
        """
        Remove a file from trash
        :param list_of_files:
        :return:
        """
        count = 0
        length = len(list_of_files)
        for path in list_of_files:
           self.real_remove_from_trash(path, my_trash)
           my_trash.rootLogger.info('Removing from trash %s' % path)

        serialization.push_json(my_trash.arr_json_files, my_trash.database)
        if length == count:
            my_trash.rootLogger.info('There are no such files')

def save_command():
    my_command.save()