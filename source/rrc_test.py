# -*- coding: utf-8 -*-
import unittest
from trash import Trash
import os
import remove_command
import shutil

class TestRRCommand(unittest.TestCase):
    def setUp(self):
        self.path = os.path.expanduser('~/Desktop/tests_for_srm')
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.trash = Trash('')
        self.RRCcommand = remove_command.RRCommand()
        self.trash_path = self.trash.path_of_trash

    def test_normal_working(self):
        filepath = []
        dirpath = os.path.join(self.path, 'test')
        os.makedirs(dirpath)
        for index in xrange(10):
            filepath.append(os.path.join(dirpath, "dima.txt" + str(index)))
            with open(filepath[index], "w") as fi:
                fi.write('123')
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        remove_command.RRCommand.execute(self.RRCcommand,self.path, 'dim', self.trash)
        for path in filepath:
            self.assertFalse(os.path.exists(path))
        self.assertTrue(number_of_files_in_trash + 10 == len(os.listdir(self.trash_path)))

    def tearDown(self):
        shutil.rmtree(self.path)
if __name__ == "__main__":
    unittest.main()
