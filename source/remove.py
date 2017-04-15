import argparse
import trash
import os
import undo_command
import remove_command

def main():
    parser = argparse.ArgumentParser(description='Smart remove')
    parser.add_argument('-d', '--directory', nargs='+', help='Remove a directory')
    parser.add_argument('-f', '--files', nargs='+', help='Remove files')
    parser.add_argument('--regular', help='Remove files for a regular expression')
    parser.add_argument('-u', '--undo', action='store_true', help='Undo function')

    my_trash = trash.Trash('/Users/Dima/Documents/Python/Lab_2.Smart_RM/python_lab_2/source/config.cfg')
    my_rfc_command = remove_command.RFCommand()
    my_rdc_command = remove_command.RDCommand()
    my_rrc_command = remove_command.RRComand()
    my_undo_command = undo_command.UndoCommand()
    stack = []
    args = parser.parse_args()
    with open('History.txt', 'r') as my_history:
        history = list(my_history.readlines())
        print history
        if args.files:
            my_rfc_command.execute(args.files, my_trash)
            history.append(my_rfc_command.name(args.files))
            for item in args.files:
                history.append(item)

            #my_trash.delete_files(args.files)

        if args.directory:
            #my_trash.delete_dir(args.directory)
            my_rdc_command.execute(args.directory, my_trash)
            history.append(my_rfc_command.name())
            for item in args.directory:
                history.append(item)

        if args.regular:
            #my_trash.delete_for_regex(os.path.abspath(os.curdir), args.regular)
            my_rrc_command.execute(os.path.abspath(os.curdir), args.regular, my_trash)

        if args.undo:
            my_undo_command.execute(history, stack)

    with open('History.txt', 'w') as my_history:
        for item in history:
             my_history.writelines(str((item) + ' '))
        my_history.writelines('\n')

if __name__ == '__main__':
    main()
