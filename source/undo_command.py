from command import Command
import remove_command
import bin_command
import serialization

class UndoCommand(Command):
    def __init__(self, my_trash):
        super(Command, self).__init__()
        self.all_operations = serialization.load_json('history.json')

    def execute(self, history, my_trash):
        if len(self.all_operations) >= 1:
            current_operation = self.all_operations[-1]
            self.all_operations.remove(current_operation)
            serialization.push_json(self.all_operations, 'history.json')
            for sub_operation in current_operation:
                if sub_operation == 'remove_files':
                    my_remove_command = remove_command.RFCommand(my_trash)
                    my_remove_command.cancel(current_operation['remove_files'])
                if sub_operation == 'remove_dirs':
                    my_remove_command = remove_command.RDCommand(my_trash)
                    my_remove_command.cancel(current_operation['remove_dirs'])
                if sub_operation == 'recover_items':
                    my_recover_command = bin_command.RecCommand(my_trash)
                    my_recover_command.cancel(current_operation['recover_items'])
                if sub_operation == 'remove_from_trash':
                    my_remove_from_trash_command = bin_command.DFTCommand(my_trash)
                    my_remove_from_trash_command.cancel(current_operation['remove_from_trash'])

        else:
            my_trash.rootLogger.info('No commands. History is empty.')


    def name(self, my_list):
        return "undo"

    def cancel(self, something):
        pass
