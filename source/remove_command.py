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

class RFCommand(Command):

    def name(self, list_of_files):
        return_list = ' '.join([str(item) for item in list_of_files])
        return 'Remove Files' + return_list

    def execute(self, list_of_files, my_trash):
        self.dried = my_trash.dried
        self.delete_files(list_of_files, my_trash)

    def cancel(self):
        print 'cancel for rfc'

    @dry_run
    def real_delete(self, files_to_delete, length, my_trash):
        arr_files = [file_object.FileObject() for i in xrange(0, length + 1)]
        index = 0
        for each_file in files_to_delete:
            if os.path.islink(each_file[index]):
                arr_files[index].set_type('Link')
            else:
                arr_files[index].set_type('File')
            arr_files[index].make_object(each_file)
            os.rename(each_file, str(arr_files[index].hash))
            shutil.move(arr_files[index].hash, my_trash.path_of_trash)
            my_trash.arr_json_files.append(arr_files[index].__dict__)
            index += 1

    def delete_files(self, list_of_files, my_trash):
        """Delete a list of files with checking for folders"""
        try:
            checked_list = verification.check_for_files_and_links(list_of_files)
            length = len(checked_list)
            self.real_delete(checked_list, length, my_trash)
            for removing_file in checked_list:
                my_trash.rootLogger.info('Removing ' + removing_file + ' to trash')

        except SystemError as e:
            logging.error('Error:' + str(e))

        serialization.push_json(my_trash.arr_json_files, my_trash.database)


class RDCommand(Command):
    def name(self):
        return 'Remove Directories'

    def execute(self, list_of_dirs, my_trash):
        self.dried = my_trash.dried
        self.delete_dir(list_of_dirs, my_trash)

    def cancel(self):
        print 'cancel for rdc'

    @dry_run
    def real_delete_dir(self, dirs_to_delete, length, my_trash):
        arr_dirs = [directory.Folder() for i in xrange(0, length + 1)]
        index = 0
        for each_dir in dirs_to_delete:
            directory.Folder.make_objects(arr_dirs[index], each_dir)
            os.rename(each_dir, str(arr_dirs[index].hash))
            shutil.move(str(arr_dirs[index].hash), my_trash.path_of_trash)
            my_trash.arr_json_files.append(arr_dirs[index].__dict__)
            index += 1

    def delete_dir(self, list_of_dirs, my_trash):
        """
        Delete a list of directories with checking
        :param list_of_dirs:
        :return:
        """
        try:
            checked_list_of_dirs = verification.check_for_dir(list_of_dirs)
            length = len(checked_list_of_dirs)
            self.real_delete_dir(checked_list_of_dirs, length, my_trash)
            for each_dir in checked_list_of_dirs:
                my_trash.rootLogger.info('Removing directory ' + each_dir + ' to trash')

        except SystemError as e:
            my_trash.rootLogger.error('Error:' + str(e))
        except OSError as e:
            my_trash.rootLogger.error('Error:' + str(e) + 'can not delete a parent folder')
        serialization.push_json(my_trash.arr_json_files, my_trash.database)

class RRComand(Command):

    def name(self):
        return 'Remove RegEx'

    def execute(self, cur_dir, regex, my_trash):
        self.dried = my_trash.dried
        self.delete_for_regex(cur_dir, regex, my_trash)

    def cancel(self):
        pass

    def delete_for_regex(self, cur_dir, regex, my_trash):

        """
        Removing for regular expression
        :param regex:
        :param cur_dir: current directory from which starts removing
        :return:
         """
        rfc = RFCommand()
        rdc = RDCommand()
        for name in os.listdir(cur_dir):
            path = os.path.join(cur_dir, name)
            if re.search(regex, name) and os.path.isfile(path):
                rfc.execute([path], my_trash)
            elif os.path.isdir(path) and re.search(regex, name):
                rdc.execute([path], my_trash)
            elif os.path.isdir(path) and not re.search(regex, name):
                self.delete_for_regex(path, regex)

class DFTComand(Command):

    def name(self):
        return 'Delete from trash'

    def execute(self, list_of_files, my_trash):
        self.dried = my_trash.dried
        self.remove_from_trash(list_of_files, my_trash)

    def cancel(self):
        print 'Delete from trash can not be undo'

    @dry_run
    def real_remove_from_trash(self, path, my_trash):
        for index, each_dict in enumerate(my_trash.arr_json_files):
            if each_dict['name'] == path or each_dict['hash'] == path:
                try:
                    shutil.rmtree(os.path.join(my_trash.path_of_trash, str(each_dict['hash'])))
                except OSError:
                    os.remove(os.path.join(my_trash.path_of_trash, str(each_dict['hash'])))
                my_trash.arr_json_files.remove(my_trash.arr_json_files[index])

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

        print length, count
        if length == count:
            my_trash.rootLogger.info('There are no such files')