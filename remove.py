import argparse, sys, os, shutil
import test

def delete_files(list_of_files):
    TRASH = '/Users/Dima/.MyTrash'
    checked_list = test.check(list_of_files)

    try:
        for each_file in checked_list:
            shutil.move(each_file, TRASH)

    except Exception as e:
        print 'Error:', e



if __name__ == '__main__':
    pass