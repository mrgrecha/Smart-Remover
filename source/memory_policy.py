import verification
import logging
import os
import shutil
from policy import Policy

class memory_policy(Policy):
    def run(self, trash):
        self.update(trash)


    def update(self, trash):
        max_size_elem = 0
        index = 0
        name = ''
        if verification.check_memory(trash.path_of_trash, trash.max_size):
            pass
        else:
            logging.info('Clear the largest file?')
            if verification.yes_or_no():
                for i, elem in enumerate(trash.arr_json_files):
                    if elem['size'] > max_size_elem:
                        max_size_elem = elem['size']
                        index = i
                        name = str(elem['hash'])
                try:
                    shutil.rmtree(os.path.join(trash.path_of_trash, name))
                except OSError:
                    os.remove(os.path.join(trash.path_of_trash, name))
                trash.arr_json_files.remove(trash.arr_json_files[index])