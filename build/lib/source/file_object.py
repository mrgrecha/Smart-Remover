class FileObject(object):

    def __init__(self):
        self.path = ''
        self.time_of_life = 0
        self.name = ''
        self.type = ''
        self.state = False      #if bin has this file = true. else = false

    def add_path(self, path):
        self.path = path

    def add_time_of_life(self, time):
        self.time_of_life = time

    def add_name(self, name):
        self.name = name

    def set_state(self, state):
        self.state = state

    def set_type(self, type):
        self.type = type


    def show_all(self):
        print 'Name:', self.name
        print 'Path:', self.path
        print 'Time:', self.time_of_life
        print 'Type:', self.type
        print 'State:', self.state

        #ini-file ;для читаемости

        #наследовать от файла для см-линка, файла, папки

        #dry-run? и silence

        #системная папка

        #обнаружение циклов?,

        #для удаления по регулярке - как искать?

        #отдельно показать допы?
