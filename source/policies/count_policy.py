import os
from policy import Policy


class CountPolicy(Policy):
    def run(self, trash):
        return set(self.update(trash))

    def update(self, trash):
        """
        Update info by policy
        :param trash: the instance of trash
        :return:
        """
        if len(os.listdir(trash.path_of_trash)) <= trash.max_number:
            return []
        else:
            return os.listdir(trash.path_of_trash)