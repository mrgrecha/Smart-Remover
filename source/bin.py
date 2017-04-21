# -*- coding: utf-8 -*-
import trash
import argparse
import bin_command

def main():
    parser = argparse.ArgumentParser(description='Bin utility')
    parser.add_argument('-l', '--list', action='store_true', help='A list of files in trash')
    parser.add_argument('-c', '--clear', action='store_true', help='Clear all files in trash')
    parser.add_argument('--full', action='store_true', help='Full list of files')
    parser.add_argument('-d', '--delete', nargs='+', help='Delete a file/files from bin')
    parser.add_argument('-r', '--recover', nargs='+', help='Recover files from a trash bin')
    parser.add_argument('-a', '--all', action='store_true', help='Recover all elements')
    parser.add_argument('-t', '--test', action='store_true', help='test')
    parser.add_argument('-dr', '--dryrun', action='store_true', help='Dry run mode on')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode on')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode on')

    my_trash = trash.Trash('/Users/Dima/Documents/Python/Lab_2.Smart_RM/python_lab_2/source/config.cfg')
    my_rec_command = bin_command.RecCommand(my_trash)
    my_dft_command = bin_command.DFTCommand(my_trash)
    args = parser.parse_args()
    if args.silent:
        my_trash.go_silent_mode()

    if args.dryrun:
        my_trash.go_dry_run()

    if args.interactive:
        my_trash.go_interactive_mode()

    if args.list:
        my_trash.bin_show()

    if args.clear:
        my_dft_command.execute(my_trash.get_names(), my_trash)

    if args.full:
        my_trash.full_show()

    if args.recover:
        my_rec_command.execute(args.recover, my_trash)

    if args.delete:
        my_dft_command.execute(args.delete, my_trash)

    if args.all:
        my_rec_command.execute(my_trash.get_names(), my_trash)


    bin_command.save_command()

if __name__ == '__main__':
    main()
