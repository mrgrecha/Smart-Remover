import argparse, sys, os.path, shutil
import test
import file_object
import serialization

#global const:
if serialization.num_of_dicts() == 0:
    arr_json_files = []
else:
    arr_json_files = serialization.load_json()

TRASH = '/Users/Dima/.MyTrash'

def delete_files(list_of_files):
    """Delete a list of files with checking for folders"""



    checked_list = test.check(list_of_files)
    n = checked_list.__len__()
    arr_files = [file_object.FileObject() for i in xrange(1, n + 2)]
    index = 0

    with open('DB.txt', 'w') as db:
        try:
            for each_file in checked_list:

                arr_files[index].add_name(each_file)
                arr_files[index].add_path(os.path.abspath(each_file))
                arr_files[index].add_time_of_life(os.path.getctime(each_file))
                arr_files[index].add_hash(arr_files[index].__hash__()  + arr_files[index].time_of_life.__hash__())
                os.rename(each_file, str(arr_files[index].hash + arr_files[index].time_of_life.__hash__()))
                arr_files[index].set_state(True)
                shutil.move(str(arr_files[index].hash + arr_files[index].time_of_life.__hash__()), TRASH)
                index += 1

            for i in xrange(0, n):
                arr_json_files.append(arr_files[i].__dict__)

            serialization.push_json(arr_json_files, db)

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

    if args.directory:
        print arr_json_files




if __name__ == '__main__':
    main()


