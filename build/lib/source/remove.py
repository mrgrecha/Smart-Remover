import argparse, sys, os.path, shutil
import test
import file_object
import json

def delete_files(list_of_files):
    """Delete a list of files with checking for folders"""
    TRASH = '/Users/Dima/.MyTrash'
    temp = open('python_lab_2/database/DB.txt', 'w')
    checked_list = test.check(list_of_files)
    n = checked_list.__len__()
    # file_name = 'File', index
    arr_files = [file_object.FileObject() for i in xrange(1, n + 2)]
    index = 0
    try:
        for each_file in checked_list:
            index += 1
            arr_files[index].add_name(each_file)
            arr_files[index].add_path(os.path.abspath(each_file))
            arr_files[index].add_time_of_life(os.path.getctime(each_file))
            shutil.move(each_file, TRASH)
            arr_files[index].set_type(True)

        for i in xrange(n + 1):
            json.dump(arr_files[i].__dict__,temp)

    except Exception as e:
        print 'Error:', e

def bin_clear():
     """Full clearing of trash"""
     files_to_delete = os.listdir('/Users/Dima/.MyTrash')
     print files_to_delete
     for each in files_to_delete:
        delete_path = '/Users/Dima/.MyTrash/' + each
        os.remove(delete_path)

def main():
    parser = argparse.ArgumentParser(description='Smart remove' )
    parser.add_argument('-d', '--directory', nargs='+', help = 'Remove a directory')
    parser.add_argument('-f', '--files', nargs='+', help = 'Remove files')
    parser.add_argument('--regular', help = 'Remove files for a regular expression')

    args = parser.parse_args()
    if args.files:
        delete_files(args.files)

if __name__ == '__main__':
    main()


