import argparse, sys, os.path, shutil
import verification
import file_object
import serialization
import directory
import random

#TO DO: make one func in remove to add files, and other in file of class
#TO DO: make removing without flags for files


#global const:
if serialization.num_of_dicts() == 0:
    arr_json_files = []
else:
    arr_json_files = serialization.load_json()

TRASH = '/Users/Dima/.MyTrash'



 #TO DO : Add catch of exception if file doesn't exist, problems with '[]' in DB.txt



def delete_files(list_of_files):
    """Delete a list of files with checking for folders"""
    with open('DB.txt', 'w') as db:
        try:
            checked_list = verification.check_for_files_and_links(list_of_files)
            n = checked_list.__len__()
            arr_files = [file_object.FileObject() for i in xrange(0, n + 1)]
            index = 0
            for each_file in checked_list:
                if os.path.islink(each_file[index]):
                    arr_files[index].set_type('Link')
                else:
                    arr_files[index].set_type('File')
                arr_files[index].make_object(each_file)
                os.rename(each_file, str(arr_files[index].hash))
                shutil.move(str(arr_files[index].hash), TRASH)
                print 'Removing', arr_files[index].name, 'to trash'
                index += 1
            for i in xrange(0, n):
                arr_json_files.append(arr_files[i].__dict__)

        except TypeError as e:
            print 'Error:',e
        except Exception as e:
            print 'Error:', e

        finally:
            serialization.push_json(arr_json_files, db)


def delete_dir(list_of_dirs):

    with open('DB.txt', 'w') as db:
        try:
            checked_list_of_dirs = verification.check_for_dir(list_of_dirs)
            n = checked_list_of_dirs.__len__()
            arr_dirs = [directory.Folder() for i in xrange(0, n + 1)]
            index = 0
            for each_dir in checked_list_of_dirs:
                directory.Folder.make_objects(arr_dirs[index], each_dir)
                os.rename(each_dir, str(arr_dirs[index].hash))
                shutil.move(str(arr_dirs[index].hash), TRASH)
                print 'Removing directory', arr_dirs[index].name, 'to trash'
                index += 1

            for i in xrange(0, n):
                arr_json_files.append(arr_dirs[i].__dict__)


        except TypeError as e:
            print e
        except Exception as e:
            print 'Error:', e
        finally:
            serialization.push_json(arr_json_files, db)

def bin_clear():
     """Full clearing of trash"""
     files_to_delete = os.listdir('/Users/Dima/.MyTrash')
     print files_to_delete
     for each in files_to_delete:
        delete_path = '/Users/Dima/.MyTrash/' + each
        os.remove(delete_path)
     print 'Clearing a bin'

def main():
    parser = argparse.ArgumentParser(description='Smart remove' )
    parser.add_argument('-d', '--directory', nargs='+', help = 'Remove a directory')
    parser.add_argument('-f', '--files', nargs='+', help = 'Remove files')
    parser.add_argument('--regular', help = 'Remove files for a regular expression')

    args = parser.parse_args()
    if args.files:
        delete_files(args.files)

    if args.directory:
        delete_dir(args.directory)




if __name__ == '__main__':
    main()


