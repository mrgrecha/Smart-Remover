class Command(object):

    def __init__(self, my_trash):
        pass

    def execute(self, list_of_files):
        raise NotImplementedError()

    def cancel(self, list_of_files):
        raise NotImplementedError()

