import argparse
import trash
import os

#TODO: make one func in remove to add files, and other in file of class
#TODO: make removing without flags for files




 #TODO : Add catch of exception if file doesn't exist, problems with '[]' in DB.json




def main():
    parser = argparse.ArgumentParser(description='Smart remove' )
    parser.add_argument('-d', '--directory', nargs='+', help = 'Remove a directory')
    parser.add_argument('-f', '--files', nargs='+', help = 'Remove files')
    parser.add_argument('--regular', help = 'Remove files for a regular expression')

    my_trash = trash.Trash('/Users/Dima/Documents/Python/Lab_2.Smart_RM/python_lab_2/source/config.cfg')

    args = parser.parse_args()

    if args.files:
        my_trash.delete_files(args.files)

    if args.directory:
        my_trash.delete_dir(args.directory)

    if args.regular:
        my_trash.delete_for_regex(os.path.abspath(os.curdir), args.regular)


if __name__ == '__main__':
    main()


