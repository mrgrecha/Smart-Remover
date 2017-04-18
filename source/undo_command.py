from command import Command


class UndoCommand(Command):
    def execute(self, history, trash):
        try:
            cmd = str(history.pop())
            print cmd
            # trash.append(cmd)
            # print("Undo command \"{0}\"\n".format(cmd.name()))
            # cmd.cancel()

        except IndexError:
            print("ERROR: HISTORY is empty\n")

    def name(self, my_list):
        return "undo"

    def cancel(self):
        pass
