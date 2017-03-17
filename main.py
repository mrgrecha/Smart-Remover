#!/usr/bin/python
#! -*- coding: utf-8 -*-

import shutil, argparse, sys, os
import remove
import show

def main():

    TRASH = '/Users/Dima/.MyTrash'


    parser = argparse.ArgumentParser(description='Smart remove/recover utility' )
    parser.add_argument('-l', '--list', action = 'store_true', help = 'List of files in the bin')
    parser.add_argument('-d', '--delete', nargs='+', help = 'Delete a file/files')
    parser.add_argument('--rec', nargs = '+', help = 'Recover a file/files')

    args = parser.parse_args()


    if args.list:
       show.full_show()

    if args.delete:
       remove.delete_files(args.delete)

    if args.rec:
        print 'recc'


if __name__ == '__main__':
    main()