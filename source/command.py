class Command(object):

    def __init__(self, my_trash):
        pass

    def execute(self, my_list, my_trash):
        raise NotImplementedError()

    def cancel(self):
        raise NotImplementedError()

    def name(self, list_of_args):
        raise NotImplementedError()
