# -*- coding: utf-8 -*-
import trash
import argparse
import remove_command
import recover_command
import undo_command

def main():
    parser = argparse.ArgumentParser(description='Bin utility')
    parser.add_argument('-l', '--list', action='store_true', help='A list of files in trash')
    parser.add_argument('-c', '--clear', action='store_true', help='Clear all files in trash')
    parser.add_argument('--full', action='store_true', help='Full list of files')
    parser.add_argument('-d', '--delete', nargs='+', help='Delete a file/files from bin')
    parser.add_argument('-r', '--recover', nargs='+', help='Recover files from a trash bin')
    parser.add_argument('-a', '--all', action='store_true', help='Recover all elements')
    parser.add_argument('-t', '--test', action='store_true', help='test')
    parser.add_argument('-u', '--undo', action='store_true', help='Undo last operatin')

    my_trash = trash.Trash('/Users/Dima/Documents/Python/Lab_2.Smart_RM/python_lab_2/source/config.cfg')
    my_rec_command = recover_command.RecCommand()
    my_dft_command = remove_command.DFTComand()
    my_undo_command = undo_command.UndoCommand()
    history = []
    stack = []
    args = parser.parse_args()
    with open('History.txt', 'rw') as my_history:
        history.append(my_history.readlines())
        if args.list:
            my_trash.bin_show()

        if args.clear:
            my_dft_command.execut(my_trash.get_names(), my_trash)

        if args.full:
            my_trash.full_show()

        if args.recover:
            my_rec_command.execute(args.recover, my_trash)

        if args.delete:
            my_dft_command.execute(args.delete, my_trash)

        if args.all:
            my_rec_command.execute(my_trash.get_names(), my_trash)

        if args.undo:
            my_undo_command.execute(history, stack)
            print history
            # for item in history:
            #     my_history.write(item)

        if args.test:
            print my_trash.get_names()


if __name__ == '__main__':
    main()
