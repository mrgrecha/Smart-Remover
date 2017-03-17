#!/usr/bin/python
#! -*- coding: utf-8 -*-

import shutil, argparse, sys, os

def main():
    parser = argparse.ArgumentParser(description = 'Smart RM with extra options', epilog = 'Epilog. To be continied...')
    parser.add_argument('-l', '--list', action = 'store_true', help = 'List of removed files')
    parser.add_argument('file', action = 'append', type = str, help = 'Remove this file or directory')
    args = parser.parse_args()
    print args
    # if args.file:
    #     try:
    #         shutil.move(args.file, r'/Users/Dima/.MyTrash')
    #     except Exception as e:
    #         print 'Error: ', e

    # if args.list:
    #     print os.listdir('/Users/Dima/.MyTrash')



if __name__ == '__main__':
    main()