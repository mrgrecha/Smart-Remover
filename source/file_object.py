
# -*- coding: utf-8 -*-
class FileObject(object):

    def __init__(self):
        self.path = ''
        self.time_of_life = 0
        self.name = ''
        self.type = ''
        self.hash = 0
        self.size = 0
        self.IsInBin = False      #if bin has this file = true. else = false

    def make_from_json(self, path, time, name, type, hash, state, size):
        self.path = path
        self.time_of_life = time
        self.name = name
        self.type = type
        self.hash = hash
        self.IsInBin = state
        self.size = size

    def add_size(self, size):
        self.size = size

    def add_path(self, path):
        self.path = path

    def add_time_of_life(self, time):
        self.time_of_life = time

    def add_name(self, name):
        self.name = name

    def set_state(self, state):
        self.IsInBin = state

    def set_type(self, type):
        self.type = type

    def add_hash(self, hash):
        self.hash = hash

    def show_all(self):
        print 'Name:', self.name
        print 'Path:', self.path
        print 'Time:', self.time_of_life
        print 'Type:', self.type
        print 'IsInBin:', self.state
        print 'Size: ', self.size

    def make_from_dict(self, some_dict):
        self.path = some_dict['path']
        self.time_of_life = some_dict['time_of_life']
        self.name = some_dict['name']
        self.type = some_dict['type']
        self.hash = some_dict['hash']
        self.IsInBin = some_dict['IsInBin']
        self.size = some_dict['size']

        #ini-file ;для читаемости

        #наследовать от файла для см-линка, файла, папки

        #dry-run? и silence

        #системная папка

        #обнаружение циклов?,

        #для удаления по регулярке - как искать?

        #отдельно показать допы?
