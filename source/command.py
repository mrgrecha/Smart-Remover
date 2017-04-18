class Command(object):

    def execute(self, my_list, my_trash):
        raise NotImplementedError()

    def cancel(self):
        raise NotImplementedError()

    def name(self, my_list):
        raise NotImplementedError()
