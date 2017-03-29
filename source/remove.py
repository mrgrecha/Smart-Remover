import argparse, sys, os.path, shutil
import verification
import file_object
import serialization
import random

#TO DO: make one func in remove to add files, and other in file of class
#TO DO: make removing without flags for files


#global const:
if serialization.num_of_dicts() == 0:
    arr_json_files = []
else:
    arr_json_files = serialization.load_json()

TRASH = '/Users/Dima/.MyTrash'

def delete_files(list_of_files):
    """Delete a list of files with checking for folders"""

 #TO DO : Add catch of exception if file doesn't exist, problems with '[]' in DB.txt



    with open('DB.txt', 'w') as db:
        try:
            checked_list = verification.check_for_files_and_links(list_of_files)
            n = checked_list.__len__()
            arr_files = [file_object.FileObject() for i in xrange(1, n + 2)]
            index = 0
            for each_file in checked_list:

                arr_files[index].add_name(each_file)
                arr_files[index].add_path(os.path.abspath(each_file))
                arr_files[index].add_size(os.path.getsize(each_file))
                arr_files[index].add_time_of_life(os.path.getctime(each_file))
                if os.path.islink(each_file[index]):
                    arr_files[index].set_type('Link')
                else:
                    arr_files[index].set_type('File')
                #ran = random.randint(0, 2132132)
                arr_files[index].add_hash(arr_files[index].__hash__()  + arr_files[index].time_of_life.__hash__())
                os.rename(each_file, str(arr_files[index].__hash__() + arr_files[index].time_of_life.__hash__()))
                arr_files[index].set_state(True)
                shutil.move(str(arr_files[index].__hash__() + arr_files[index].time_of_life.__hash__()), TRASH) #random for deleting files with the same cache of name that are deleting at the same time
                print 'Removing',arr_files[index].name, 'to trash'
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
            arr_dirs = [file_object.FileObject() for i in xrange(1, n + 2)]
            index = 0
            for each_dir in checked_list_of_dirs:

                arr_dirs[index].add_name(each_dir)
                arr_dirs[index].add_path(os.path.abspath(each_dir))
                arr_dirs[index].add_size(os.path.getsize(each_dir))
                arr_dirs[index].add_time_of_life(os.path.getctime(each_dir))
                arr_dirs[index].set_type('Directory')
                # ran = random.randint(0, 2132132)
                arr_dirs[index].add_hash(arr_dirs[index].__hash__() + arr_dirs[index].time_of_life.__hash__())
                os.rename(each_dir, str(arr_dirs[index].__hash__() + arr_dirs[index].time_of_life.__hash__()))
                arr_dirs[index].set_state(True)
                shutil.move(str(arr_dirs[index].__hash__() + arr_dirs[index].time_of_life.__hash__()),
                            TRASH)  # random for deleting files with the same cache of name that are deleting at the same time
                print 'Removing directory', arr_dirs[index].name, 'to trash'
                index += 1

            for i in xrange(0, n):
                arr_json_files.append(arr_dirs[i].__dict__)

            serialization.push_json(arr_json_files, db)

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


