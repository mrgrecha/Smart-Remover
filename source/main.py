#!/usr/bin/python
#! -*- coding: utf-8 -*-

import shutil, argparse, sys, os
import remove
import bin
import file_object

def eze():
    print '123'

def main():

    TRASH = '/Users/Dima/.MyTrash'


    parser = argparse.ArgumentParser(description='Smart remove/recover utility' )
    parser.add_argument('-l', '--list', action = 'store_true', help = 'List of files in the bin')
    parser.add_argument('-d', '--delete', nargs='+', help = 'Delete a file/files')
    parser.add_argument('--rec', nargs = '+', help = 'Recover a file/files')
    parser.add_argument('-c', '--clear', action='store_true', help='Clear files in the bin')

    args = parser.parse_args()


    if args.clear:
        remove.bin_clear()

    if args.list:
       bin.bin_show()

    if args.delete:
        remove.delete_files(args.delete)

    if args.rec:
        print 'recc'


if __name__ == '__main__':
    main()