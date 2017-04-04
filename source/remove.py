import argparse, sys, os.path, shutil
import verification
import file_object
import serialization
import directory, trash
import random

#TO DO: make one func in remove to add files, and other in file of class
#TO DO: make removing without flags for files




 #TO DO : Add catch of exception if file doesn't exist, problems with '[]' in DB.txt


my_trash = trash.Trash('/Users/Dima/.MyTrash','DB.txt', 1000, 300)


def main():
    parser = argparse.ArgumentParser(description='Smart remove' )
    parser.add_argument('-d', '--directory', nargs='+', help = 'Remove a directory')
    parser.add_argument('-f', '--files', nargs='+', help = 'Remove files')
    parser.add_argument('--regular', help = 'Remove files for a regular expression')

    args = parser.parse_args()
    if args.files:
        my_trash.delete_files(args.files)

    if args.directory:
        my_trash.delete_dir(args.directory)




if __name__ == '__main__':
    main()


