import unittest, os

class TrashBinMethods(unittest.TestCase):
    def test_remove_files(self):
        os.system('touch example.txt')
        os.system('echo "QWERTY" >> example.txt')
        if (os.system('srm -f example.txt')) == 0:
            self.assertTrue(True)

    def test_remove_dires(self):
        os.system('mkdir example')
        os.system('touch example/example_1.txt')
        os.system('echo "QWERTY" >> example')
        if (os.system('srm -d example')) == 0:
            self.assertTrue(True)

    def test_remove_regex(self):
        os.system('mkdir example')
        os.system('cd example')
        os.system('touch example/name{1..5}.lol')
        os.system('echo "QWERTY" >> example/name2.lol')
        if (os.system('srm --regular ".lol"')) == 0:
            self.assertTrue(True)
if __name__ == '__main__':
    unittest.main()