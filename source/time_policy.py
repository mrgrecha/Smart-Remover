import verification
import shutil
import serialization
import os
import user_input
from policy import Policy

class time_policy(Policy):
    def run(self, trash):

        # print ('These files are staying in the bin > %s' %
        #              datetime.datetime.fromtimestamp(trash.max_time).strftime('%m month %d days %H hours %M minutes %S seconds'))
        #
        # print('These files are staying in the bin > %s' %
        #              datetime.datetime.fromtimestamp(20).strftime('%m month %d days %H hours %M minutes %S seconds'))
        self.time_update(trash)

    def update(self, trash):
        answer = user_input.UserInput()
        list_of_time_files = verification.check_time(trash.arr_json_files, trash.max_time)
        file_names = []
        for item in list_of_time_files:
            file_names.append(item['name'])
        trash.rootLogger.info(file_names)
        trash.rootLogger.info('Delete them?')
        answer.ask_yes_or_no()
        if answer.state == 'yes':
            for path in list_of_time_files:
                path_of_file = os.path.join(trash.path_of_trash, str(path['hash']))
                if os.path.isdir(path_of_file):
                    shutil.rmtree(path_of_file)
                else:
                    os.remove(path_of_file)
                trash.arr_json_files.remove(path)
        serialization.push_json(trash.arr_json_files, trash.database)