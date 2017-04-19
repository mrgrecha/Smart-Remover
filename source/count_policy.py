import os
from policy import Policy


class CountPolicy(Policy):
    def run(self, trash):
        return self.update(trash)

    def update(self, trash):
        if len(os.listdir(trash.path_of_trash)) <= trash.max_count:
            pass
        else:
            return os.listdir(trash.path_of_trash)