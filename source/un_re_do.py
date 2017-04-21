import argparse
import trash
import os
import undo_command
import remove_command
import command_object


def main():
    parser = argparse.ArgumentParser(description='Undo and Redo mode for Smart RM')
    parser.add_argument('-u', '--undo', action='store_true', help='Undo function')
    my_trash = trash.Trash('/Users/Dima/Documents/Python/Lab_2.Smart_RM/python_lab_2/source/config.cfg')

    args = parser.parse_args()

    if args.undo:
        my_undo_command = undo_command.UndoCommand(my_trash)
        my_undo_command.execute('1', my_trash)

if __name__ == '__main__':
    main()
