import source.src.verification
from policy import Policy


class TimePolicy(Policy):
    def run(self, trash):
        return set(self.update(trash))

    def update(self, trash):
        """
               Update info by policy
               :param trash: the instance of trash
               :return:
        """
        list_of_time_files = source.src.verification.check_time(trash.arr_json_files, trash.max_time)
        file_names = []
        for item in list_of_time_files:
            file_names.append(item['hash'])
        return file_names
