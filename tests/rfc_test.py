# -*- coding: utf-8 -*-
import os
import shutil
import unittest

from source.commands import remove_command
from source.src.trash import Trash

def test():
    unittest.main()

class TestRFCommand(unittest.TestCase):

    def setUp(self):
        self.path = os.path.expanduser('~/Desktop/tests_for_srm')
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.trash = Trash('')
        self.RFCommand = remove_command.RFCommand(self.trash)
        self.trash_path = self.trash.path_of_trash
        if os.path.exists(os.path.join(self.trash_path, '.DS_Store')):
            os.remove(os.path.join(self.trash_path, '.DS_Store'))

    def test_normal_working_with_empty_file(self):
        filepath = os.path.join(self.path, "test1.txt")
        with open(filepath, "w"):
            pass
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        remove_command.RFCommand.execute(self.RFCommand, [filepath])
        self.assertFalse(os.path.exists(filepath))
        self.assertTrue(number_of_files_in_trash + 1 == len(os.listdir(self.trash_path)))

    def test_normal_working_with_not_empty_file(self):
        filepath = os.path.join(self.path, "test2.txt")
        with open(filepath, "w") as test:
            test.write('testing not empty')
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        remove_command.RFCommand.execute(self.RFCommand, [filepath])
        self.assertFalse(os.path.exists(filepath))
        self.assertTrue(number_of_files_in_trash + 1 == len(os.listdir(self.trash_path)))
    #
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
    def test_no_file(self):
        filepath = os.path.join(self.path, "test3.txt")
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        try:
            remove_command.RFCommand.execute(self.RFCommand, [filepath])
        except:
            pass
        self.assertFalse(os.path.exists(filepath))
        self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)))

    def test_for_some_files(self):
        filepath = os.path.join(self.path, "test4.txt")

        filepath1 = os.path.join(self.path, "test5.txt")
        with open(filepath, "w") as fi:
            fi.write('it is testing')
        with open(filepath1, "w") as fi:
            fi.write('it is too')
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        remove_command.RFCommand.execute(self.RFCommand, [filepath, filepath1])
        self.assertFalse(os.path.exists(filepath))
        self.assertFalse(os.path.exists(filepath1))
        self.assertTrue(number_of_files_in_trash + 2 == len(os.listdir(self.trash_path)))

    def test_for_folder(self):
        dirpath = os.path.join(self.path, 'test')
        os.makedirs(dirpath)
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        try:
            remove_command.RFCommand.execute(self.RFCommand, [dirpath])
        except:
            pass
        self.assertTrue(os.path.exists(dirpath))
        self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)))
        shutil.rmtree(dirpath)

    def tearDown(self):
        shutil.rmtree(self.path)

if __name__ == "__main__":
    test()
