# -*- coding: utf-8 -*-
import unittest
from trash import Trash
import os
import remove_command


class TestDFTommand(unittest.TestCase):

    def setUp(self):
        self.path = os.path.expanduser('~/Desktop/tests_for_srm')
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.trash = Trash('')
        self.RFCcommand = remove_command.RFCommand()
        self.DFTcommand = remove_command.DFTComand()
        self.RDCcommand = remove_command.RDCommand()
        self.trash_path = self.trash.path_of_trash

    def test_normal_working_with_not_empty_file(self):
        filepath = os.path.join(self.path, "test.txt")
        with open(filepath, "w") as fi:
            fi.write('3asfsdaf')
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        remove_command.RFCommand.execute(self.RFCcommand, [filepath], self.trash)
        self.assertTrue(number_of_files_in_trash + 1 == len(os.listdir(self.trash_path)))
        remove_command.DFTComand.execute(self.DFTcommand, [filepath], self.trash)
        if os.path.exists(os.path.join(self.trash_path, '.DS_Store')):
            self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)) - 1)
        else:
            self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)))

    def test_no_file(self):
        filepath = os.path.join(self.path, "test123.txt")
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        remove_command.DFTComand.execute(self.DFTcommand, [filepath], self.trash)
        self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)))

    def test_for_dir(self):
        dirpath = os.path.join(self.path, '123')
        os.makedirs(dirpath)
        filepath1 = os.path.join(dirpath, 'test1.txt')
        filepath2 = os.path.join(dirpath, 'test2.txt')
        with open(filepath1, 'w') as fi:
            fi.write('dima')
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        remove_command.RDCommand.execute(self.RDCcommand, [dirpath], self.trash)
        self.assertTrue(number_of_files_in_trash + 1 == len(os.listdir(self.trash_path)))
        remove_command.DFTComand.execute(self.DFTcommand, '123', self.trash)
        if os.path.exists(os.path.join(self.trash_path, '.DS_Store')):
            self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)) - 1)
        else:
            self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)))

if __name__ == "__main__":
    unittest.main()
