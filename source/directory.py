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

    def set_state(self, state):
        super(Folder, self).set_state(state)

    def set_type(self, type):
        super(Folder, self).set_type(type)

    def add_path(self, path):
        super(Folder, self).add_path(path)

    def add_size(self, path):
        size = os.path.getsize(path)
        if os.path.isdir(path):
            for item in os.listdir(path):
                subpath = os.path.join(path, item)
                size += Folder.get_size(subpath)
        self.size = size

    def add_number_of_objects(self, path):
        num = 0
        for abs_path, sub_path, files in os.walk(path):
            num += len(files)
        self.num_of_obj = num


f = Folder()
f.make_from_json('qwe', 11, 'dima', 'Folder', '2313', True, 112312, 312)
print f.show_all()
