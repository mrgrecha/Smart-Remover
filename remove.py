import argparse, sys, os.path, shutil
import test
import file_object

def delete_files(list_of_files):
    TRASH = '/Users/Dima/.MyTrash'
    checked_list = test.check(list_of_files)
    file1 = file_object.FileObject()

    try:
        for each_file in checked_list:
            file1.add_name(each_file)
            file1.add_path(os.path.abspath(each_file))
            file1.add_time_of_life(os.path.getctime(each_file))
            shutil.move(each_file, TRASH)
            file1.set_type(True)

        file1.show_all()

    except Exception as e:
        print 'Error:', e

def bin_clear():
     files_to_delete = os.listdir('/Users/Dima/.MyTrash')
     print files_to_delete
     for each in files_to_delete:
        delete_path = '/Users/Dima/.MyTrash/' + each
        os.remove(delete_path)

if __name__ == '__main__':
    pass


