import verification, file_object, os, shutil, serialization, directory

class Trash:
    def __init__(self, path_of_trash, database, max_size, max_number):
        self.path_of_trash = path_of_trash
        self.arr_json_files = serialization.load_json()
        self.database = database
        self.max_size = max_size
        self.max_number = max_number

    def delete_files(self, list_of_files):
        """Delete a list of files with checking for folders"""
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
                shutil.move(str(arr_files[index].hash), self.path_of_trash)
                print 'Removing', arr_files[index].name, 'to trash'
                index += 1
            for i in xrange(0, n):
                self.arr_json_files.append(arr_files[i].__dict__)

        except TypeError as e:
            print 'Error:', e
        except Exception as e:
            print 'Error:', e

        serialization.push_json(self.arr_json_files, self.database)

    def delete_dir(self, list_of_dirs):
        """
        Delete a list of directories with chechiing
        :param list_of_dirs:
        :return:
        """
        with open('DB.txt', 'w') as db:
            try:
                checked_list_of_dirs = verification.check_for_dir(list_of_dirs)
                n = checked_list_of_dirs.__len__()
                arr_dirs = [directory.Folder() for i in xrange(0, n + 1)]
                index = 0
                for each_dir in checked_list_of_dirs:
                    directory.Folder.make_objects(arr_dirs[index], each_dir)
                    os.rename(each_dir, str(arr_dirs[index].hash))
                    shutil.move(str(arr_dirs[index].hash), self.path_of_trash)
                    print 'Removing directory', arr_dirs[index].name, 'to trash'
                    index += 1

                for i in xrange(0, n):
                    self.arr_json_files.append(arr_dirs[i].__dict__)


            except TypeError as e:
                print e
            except Exception as e:
                print 'Error:', e

        serialization.push_json(self.arr_json_files, self.database)