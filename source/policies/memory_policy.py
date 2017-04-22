import logging
import os
import shutil

import source.src.verification

import source.src.user_input
from policy import Policy


class MemoryPolicy(Policy):
    def run(self, trash):
        self.update(trash)

    def update(self, trash):
        """
               Update info by policy
               :param trash: the instance of trash
               :return:
               """
        max_size_elem = 0
        index = 0
        name = ''
        path = ''
        answer = source.src.user_input.UserInput()
        if source.src.verification.check_memory(trash.path_of_trash, trash.max_size):
            pass
        else:
            logging.error('Clear the largest file?')
            answer.ask_yes_or_no()
            if answer.state == 'yes':
                for i, elem in enumerate(trash.arr_json_files):
                    if elem['size'] > max_size_elem:
                        max_size_elem = elem['size']
                        index = i
                        path = str(elem['hash'])
                        name = elem['name']

                try:
                    shutil.rmtree(os.path.join(trash.path_of_trash, path))
                except OSError:
                    os.remove(os.path.join(trash.path_of_trash, path))
                logging.info('Removing ' + name + ' ' + str(max_size_elem) + ' bytes')
                trash.arr_json_files.remove(trash.arr_json_files[index])
                self.update(trash)

            elif answer.state == 'no':
                pass
