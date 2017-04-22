# -*- coding: utf-8 -*-
import os
import shutil
import unittest
from source.commands import remove_command
from source.src.trash import Trash
from source.commands import bin_command


class TestDryRun(unittest.TestCase):

    def setUp(self):
        self.path = os.path.expanduser('~/Desktop/tests_for_srm')
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.trash = Trash('')
        self.trash.go_dry_run()
        self.DFTCommand = bin_command.DFTCommand(self.trash)
        self.RFCommand = remove_command.RFCommand(self.trash)
        self.RDCommand = remove_command.RDCommand(self.trash)
        self.Rec = bin_command.RecCommand(self.trash)
        self.trash_path = self.trash.path_of_trash
        if os.path.exists(os.path.join(self.trash_path, '.DS_Store')):
            os.remove(os.path.join(self.trash_path, '.DS_Store'))

    def test_normal_working_with_empty_file(self):
        filepath = os.path.join(self.path, "test1.txt")
        with open(filepath, "w"):
            pass
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        self.RFCommand.execute([filepath])
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(number_of_files_in_trash  == len(os.listdir(self.trash_path)))

        if len(self.trash.arr_json_files) >= 1:
            self.DFTCommand.execute([self.trash.arr_json_files[-1]['hash']])
            self.assertTrue(number_of_files_in_trash  == len(os.listdir(self.trash_path)))
            self.assertTrue(os.path.exists(filepath))

    def test_normal_working_with_not_empty_file(self):
        filepath = os.path.join(self.path, "test1")
        os.mkdir(filepath)
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        self.RDCommand.execute([filepath])
        self.assertTrue(os.path.exists(filepath))
        self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)))

        if len(self.trash.arr_json_files) >= 1:
            self.Rec.execute([self.trash.arr_json_files[-1]['hash']])
            self.assertTrue(number_of_files_in_trash == len(os.listdir(self.trash_path)))
            self.assertTrue(os.path.exists(filepath))


    def tearDown(self):
        shutil.rmtree(self.path)

if __name__ == "__main__":
    unittest.main()
