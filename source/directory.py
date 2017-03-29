from file_object import FileObject
import os

class Folder(FileObject):
    """Class for folders in Smart RM"""
    def __init__(self):
        super(FileObject).__init__(FileObject)
        self.num_of_obj = 0

    def make_from_json(self, path, time, name, type, hash, state, size, num):
        super(Folder, self).make_from_json(path, time, name, type, hash, state, size)
        self.num_of_obj = num

    def add_number_of_objects(self, num):
        self.num_of_obj = num

    def add_hash(self, hash):
        super(Folder, self).add_hash(hash)

    def add_name(self, name):
        super(Folder, self).add_name(name)

    def add_time_of_life(self, time):
        super(Folder, self).add_time_of_life(time)

    def show_all(self):
        super(Folder, self).show_all()
        print 'Number: ',self.num_of_obj

    def make_from_dict(self, some_dict):
        super(Folder, self).make_from_json(some_dict)
        self.num_of_obj = some_dict['num_of_obj']


f = Folder()
f.make_from_json('qwe', 11, 'dima', 'Folder', '2313', True, 112312, 312)
print f.show_all()
