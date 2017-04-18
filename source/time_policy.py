import verification
import shutil
import serialization
import os
import user_input
from policy import Policy


class TimePolicy(Policy):
    def run(self, trash):

        # print ('These files are staying in the bin > %s' %
        #              datetime.datetime.fromtimestamp(trash.max_time).strftime
        # ('%m month %d days %H hours %M minutes %S seconds'))
        #
        # print('These files are staying in the bin > %s' %
        #              datetime.datetime.fromtimestamp(20).strftime('%m month %d days %H hours %M minutes %S seconds'))
        list_of_files = self.update(trash)
        return list_of_files

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
            return list_of_time_files
        elif answer.state == 'no':
            pass
