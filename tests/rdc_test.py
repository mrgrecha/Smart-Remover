# -*- coding: utf-8 -*-
import os
import shutil
import unittest

from source.commands import remove_command
from source.src.trash import Trash


class TestRDCommand(unittest.TestCase):
    def setUp(self):
        self.path = os.path.expanduser('~/Desktop/tests_for_srm')
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.trash = Trash('')
        self.RDCommand = remove_command.RDCommand(self.trash)
        self.trash_path = self.trash.path_of_trash

    def test_normal_working_with_empty_dir(self):
        dirpath = os.path.join(self.path, 'testdir1')
        os.makedirs(dirpath)
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        remove_command.RDCommand.execute(self.RDCommand, [dirpath])
        self.assertFalse(os.path.exists(dirpath))
        self.assertTrue(number_of_files_in_trash + 1 == len(os.listdir(self.trash_path)))

    def test_normal_working_with_not_empty_dir(self):
        dirpath = os.path.join(self.path, 'testdir2')
        os.makedirs(dirpath)
        filepath = os.path.join(dirpath, '1.txt')
        with open(filepath, "w") as fi:
            fi.write('it is testing')
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        remove_command.RDCommand.execute(self.RDCommand, [dirpath])
        self.assertFalse(os.path.exists(dirpath))
        self.assertTrue(number_of_files_in_trash + 1 == len(os.listdir(self.trash_path)))

    # # def test_normal_working_with_not_permissions_file(self):
    # #     filepath = os.path.join(self.path, "test.txt")
    # #     with open(filepath, "w") as fi:
    # #         fi.write('it is testing')
    # #     os.chmod(filepath, 0o777)
    # #     number_of_files_in_trash = len(os.listdir(self.trash_path))
    # #     #remove_command.RFCommand.execute(self.RFCcommand, [filepath], self.trash)
    # #     self.assertTrue(os.path.exists(filepath))
    # #     self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)))
    #
    def test_no_dir(self):
        dirpath = os.path.join(self.path, 'testdir3')
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        try:
            remove_command.RDCommand.execute(self.RDCommand, [dirpath])
        except:
            pass
        self.assertFalse(os.path.exists(dirpath))
        self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)))

    def test_for_some_dirs(self):
        dirpath = os.path.join(self.path, 'testdir4')
        dirpath1 = os.path.join(self.path, 'testdir5')
        os.makedirs(dirpath)
        os.makedirs(dirpath1)
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        remove_command.RDCommand.execute(self.RDCommand, [dirpath, dirpath1])
        self.assertFalse(os.path.exists(dirpath))
        self.assertFalse(os.path.exists(dirpath1))
        self.assertTrue(number_of_files_in_trash + 2 == len(os.listdir(self.trash_path)))

    def test_for_file(self):
        filepath = os.path.join(self.path, 'test.txt')
        with open(filepath, 'w'):
            pass
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        try:
            remove_command.RDCommand.execute(self.RDCcmmand, [filepath])
        except:
            pass
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)))

    def tearDown(self):
        shutil.rmtree(self.path)

if __name__ == "__main__":
    unittest.main()
