from file_object import FileObject
import os

class Folder(FileObject):
    """Class for folders in Smart RM"""
    def __init__(self):
        super(Folder, self).__init__()
        self.num_of_obj = 0

    def make_from_json(self, path, time, name, type, hash, state, size, num):
        super(Folder, self).make_from_json(path, time, name, type, hash, state, size)
        self.num_of_obj = num
        self.type = 'Directory'


    def make_objects(self, name):
        # self.name = name
        # self.path = os.path.abspath(name)
        # self.time_of_life = os.path.getctime(name)
        # self.hash = self.__hash__() + self.time_of_life.__hash__()
        super(Folder, self).make_object(name)
        self.num_of_obj = self.add_number_of_objects(self.path)
        self.size = self.add_size(self.path)
        self.type = 'Directory'

    def show_all(self):
        super(Folder, self).show_all()
        print 'Number of objects: ', self.num_of_obj

    @staticmethod
    def add_size(path):
        size = os.path.getsize(path)
        if os.path.isdir(path):
            for item in os.listdir(path):
                subpath = os.path.join(path, item)
                size += Folder.add_size(subpath)
        return size

    @staticmethod
    def add_number_of_objects(path):
        num = 0
        for abs_path, sub_path, files in os.walk(path):
            num += len(files)
        return num
