# -*- coding: utf-8 -*-
import os
import shutil
import unittest

from source.commands import remove_command
from source.src.trash import Trash
from source.commands.bin_command import DFTCommand


class TestRRCommand(unittest.TestCase):
    def setUp(self):
        self.path = os.path.expanduser('~/Desktop/tests_for_srm')
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.trash = Trash('')
        self.RRCommand = remove_command.RRCommand(self.trash)
        self.DFTCommand = DFTCommand(self.trash)
        self.trash_path = self.trash.path_of_trash
        if os.path.exists(os.path.join(self.trash_path, '.DS_Store')):
            os.remove(os.path.join(self.trash_path, '.DS_Store'))

    def test_normal_working(self):
        filepath = []
        dirpath = os.path.join(self.path, 'test')
        if os.path.exists(dirpath):
            pass
        else:os.makedirs(dirpath)
        for index in xrange(10):
            filepath.append(os.path.join(dirpath, "some" + str(index)))
            with open(filepath[index], "w") as fi:
                fi.write('123')
        number_of_files_in_trash = len(os.listdir(self.trash_path))
        os.chdir(dirpath)
        self.RRCommand.execute("some")
        for path in filepath:
            self.assertFalse(os.path.exists(path))
        self.assertTrue(number_of_files_in_trash + 10 == len(os.listdir(self.trash_path)))
        for i in xrange(-10, 0):
            print self.trash.arr_json_files[i]['hash']
            self.DFTCommand.execute([self.trash.arr_json_files[i]['hash']])

    def tearDown(self):
        shutil.rmtree(self.path)

if __name__ == "__main__":
    unittest.main()
