import source.src.serialization
import os

class CommandObject(object):
    def __init__(self):
        self.my_dict = {}
        if not os.path.exists(os.path.expanduser('~/history.json')):
            with open(os.path.expanduser('~/history.json'), 'w') as fi:
                pass
        self.all_operations = source.src.serialization.load_json(os.path.expanduser('~/history.json'))
        self.check_for_empty_dicts()
        self.index = len(self.all_operations)

    def check_for_empty_dicts(self):
        """
        Checks for dict that was empty
        :return:
        """
        for item in self.all_operations:
            if len(item) == 1:
                self.all_operations.remove(item)

    def remove_files(self, list_of_files):
        """
        Append files that were removed in history of operations
        :param list_of_files: files to remove
        :return:
        """
        self.my_dict['remove_files'] = list_of_files

    def remove_dirs(self, list_of_dirs):
        """
        Append dirs that were removed in history of operations
        :param list_of_dirs:
        :return:
        """
        self.my_dict['remove_dirs'] = list_of_dirs

    def recover_items(self, list_of_items):
        """
        Append files or dirs that were recovered in history of operations
        """
        self.my_dict['recover_items'] = list_of_items

    def remove_from_trash(self, list_of_items):
        """
        Append files that were removed from trash in history of operations
        :param list_of_items:
        :return:
        """
        self.my_dict['remove_from_trash'] = list_of_items

    def save(self):
        """
        Save all changes
        :return:
        """
        self.my_dict['index'] = self.index
        self.all_operations.append(self.my_dict)
        source.src.serialization.push_json(self.all_operations, os.path.expanduser('~/history.json'))
