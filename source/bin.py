# -*- coding: utf-8 -*-
import trash
import argparse


def main():
    parser = argparse.ArgumentParser(description='Bin utility')
    parser.add_argument('-l', '--list', action='store_true', help='A list of files in trash')
    parser.add_argument('-c', '--clear', action='store_true', help='Clear all files in trash')
    parser.add_argument('--full', action='store_true', help='Full list of files')
    parser.add_argument('-d', '--delete', nargs='+', help='Delete a file/files from bin')
    parser.add_argument('-r', '--recover', nargs='+', help='Recover files from a trash bin')
    parser.add_argument('-a', '--all', action='store_true', help='Recover all elements')
    parser.add_argument('-t', '--test', action='store_true', help='test')

    my_trash = trash.Trash('/Users/Dima/Documents/Python/Lab_2.Smart_RM/python_lab_2/source/config.cfg')

    args = parser.parse_args()

    if args.list:
        my_trash.bin_show()

    if args.clear:
        my_trash.remove_from_trash(my_trash.get_names())

    if args.full:
        my_trash.full_show()

    if args.recover:
        my_trash.recover(args.recover)

    if args.delete:
        my_trash.remove_from_trash(args.delete)

    if args.all:
        my_trash.recover(my_trash.get_names())

    if args.test:
        print my_trash.get_names()


if __name__ == '__main__':
    main()
