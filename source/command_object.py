import serialization

class CommandObject(object):
    def __init__(self):
        self.my_dict = {}
        self.all_operations = serialization.load_json('history.json')

    def remove_files(self, list_of_files):
        self.my_dict['remove_files'] = list_of_files

    def remove_dirs(self, list_of_dirs):
        self.my_dict['remove_dirs'] = list_of_dirs

    def recover_items(self, list_of_items):
        self.my_dict['recover_items'] = list_of_items

    def remove_from_trash(self, list_of_items):
        self.my_dict['remove_from_trash'] = list_of_items

    def save(self):
        self.all_operations.append(self.my_dict)
        serialization.push_json(self.all_operations, 'history.json')