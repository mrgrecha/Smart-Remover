import bin_command
import remove_command
import source.src.serialization
import os
from command import Command


class UndoCommand(Command):
    def __init__(self, my_trash):
        super(Command, self).__init__()
        self.all_operations = source.src.serialization.load_json(os.path.expanduser('~/history.json'))
        self.trash = my_trash

    def execute(self, history):
        if len(self.all_operations) >= 1:
            current_operation = self.all_operations[-1]
            self.all_operations.remove(current_operation)
            source.src.serialization.push_json(self.all_operations, os.path.expanduser('~/history.json'))
            for sub_operation in current_operation:
                if sub_operation == 'remove_files':
                    my_remove_command = remove_command.RFCommand(self.trash)
                    my_remove_command.cancel(current_operation['remove_files'])
                if sub_operation == 'remove_dirs':
                    my_remove_command = remove_command.RDCommand(self.trash)
                    my_remove_command.cancel(current_operation['remove_dirs'])
                if sub_operation == 'recover_items':
                    my_recover_command = bin_command.RecCommand(self.trash)
                    my_recover_command.cancel(current_operation['recover_items'])
                if sub_operation == 'remove_from_trash':
                    my_remove_from_trash_command = bin_command.DFTCommand(self.trash)
                    my_remove_from_trash_command.cancel(current_operation['remove_from_trash'])

        else:
            self.trash.rootLogger.info('No commands. History is empty.')

    def cancel(self, something):
        pass
