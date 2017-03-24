class FileObject(object):

    def __init__(self):
        self.path = ''
        self.time_of_life = 0
        self.name = ''
        self.state = False      #if bin has this file = true. else = false

    def add_path(self, path):
        self.path = path

    def add_time_of_life(self, time):
        self.time_of_life = time

    def add_name(self, name):
        self.name = name

    def set_type(self, state):
        self.state = state

    def show_all(self):
        print 'Name:', self.name
        print 'Path:', self.path
        print 'Time:', self.time_of_life
        print 'State:', self.state