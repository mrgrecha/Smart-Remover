import argparse
import os
from source.commands import undo_command
from source.src import trash


def main():
    parser = argparse.ArgumentParser(description='Undo and Redo mode for Smart RM')
    my_trash = trash.Trash(os.path.join(os.path.expanduser('~/'), 'config.cfg'))
    my_undo_command = undo_command.UndoCommand(my_trash)
    my_undo_command.execute('a')

if __name__ == '__main__':
    main()
