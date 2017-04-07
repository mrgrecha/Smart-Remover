import verification, file_object, os, shutil, serialization, directory, pydoc, datetime, singleton, re, ConfigParser

class Trash:
    __metaclass__ = singleton.Singleton

    #TODO add max time to init
    #TODO add checking for parent folders
    #TODO add checking for the same names in dict
    #TODO add checkong for number of files

    def __init__(self, path_of_config):
        config = ConfigParser.RawConfigParser()
        config.read(path_of_config)
        self.path_of_trash = config.get('Section_Custom', 'path')
        self.database = config.get('Section_Custom', 'database')
        self.max_size = config.get('Section_Custom', 'max_size')
        self.max_number = config.get('Section_Custom', 'max_num')
        self.max_list_height = 50
        self.max_time = config.getint('Section_Custom', 'max_time')
        self.arr_json_files = serialization.load_json(self.database)
        self.policy = config.get('Section_Custom', 'policy')



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
                self.arr_json_files.append(arr_files[index].__dict__)
                print 'Removing', arr_files[index].name, 'to trash'
                index += 1


        except TypeError as e:
            print 'Error:', e
        except SystemError as e:
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

    def full_show(self):
        """
        Demonstrating a list of files with full description
        :return:
        """
        if serialization.num_of_dicts() == 0:
            print 'No files in trash'
        full_show_string = ''
        for index, each_file in enumerate(self.arr_json_files):
            full_show_string += '%d %s %s %d %s %d Bytes \n' % (
            index + 1, each_file['name'], each_file['type'], each_file['hash'],
            datetime.datetime.fromtimestamp(each_file['time_of_life']).strftime('%Y-%m-%d %H:%M:%S'), each_file['size'])

        if len(self.arr_json_files) > self.max_list_height:
            pydoc.pager(full_show_string)
        else:
            print full_show_string

    def bin_show(self):
        """
        Demonstrating a list of files in trash bin
        :return:
        """
        if serialization.num_of_dicts() == 0:
            print 'No files in trash'
        for ind, file in enumerate(self.arr_json_files):
            print("{0}. {1}".format(ind + 1, file))

    def remove_from_trash(self, list_of_files):
        """
        Remove a file from trash
        :param list_of_files:
        :return:
        """
        count = 0
        length = len(list_of_files)
        for file in list_of_files:
            for index, each_dict in enumerate(self.arr_json_files):
                if each_dict['name'] == file:
                    try:
                        shutil.rmtree(os.path.join(self.path_of_trash, str(each_dict['hash'])))
                    except OSError:
                        os.remove(os.path.join(self.path_of_trash, str(each_dict['hash'])))
                    self.arr_json_files.remove(self.arr_json_files[index])
                    print 'Removing from trash %s' % each_dict['name']

        serialization.push_json(self.arr_json_files, self.database)

        print length, count
        if length == count:
            print 'There are no such files'

    def delete_for_regex(self, dir, regex):

        """
        Removing for regular expression
        :param regex:
        :return:
         """
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            print name
            if re.search(regex, name) and os.path.isfile(path):
                self.delete_files([path])
            elif os.path.isdir(path) and re.search(regex, name):
                self.delete_dir([path])
            elif os.path.isdir(path) and not re.search(regex, name):
                self.delete_for_regex(path, regex)



    def update(self):
        try:
            verification.check_for_trash_files(self.arr_json_files, self.path_of_trash)
        except ValueError as e:
            print '''Error: Unknown %s
        Delete them ?
        Y - delete them
        N - keep them''' % (e)
            if  verification.yes_or_no():
                    for n in e[0]:
                        path_of_n = os.path.join(self.path_of_trash, n)
                        if os.path.isdir(path_of_n):
                            shutil.rmtree(path_of_n)
                        else:
                            os.remove(path_of_n)

        except StandardError as e:
            for elem in e[0]:
                for index, json_dict in enumerate(self.arr_json_files):
                    if elem == str(json_dict['hash']):
                        self.arr_json_files.remove(self.arr_json_files[index])
        serialization.push_json(self.arr_json_files, self.database)

    def time_update(self):
        list_of_time_files = verification.check_time(self.arr_json_files, self.max_time)
        print list_of_time_files
        print 'Delete them?'
        if verification.yes_or_no():
            for file in list_of_time_files:
                print file
                path_of_file = os.path.join(self.path_of_trash, str(file['hash']))
                if os.path.isdir(path_of_file):
                    shutil.rmtree(path_of_file)
                else:
                    os.remove(path_of_file)
                self.arr_json_files.remove(file)
        serialization.push_json(self.arr_json_files, self.database)

    def memory_update(self):
        max = 0
        index = 0
        name = ''
        if verification.check_memory(self.path_of_trash, self.max_size):
            pass
        else:
            print 'Clear the largest file?'
            if verification.yes_or_no():
                for i, elem in enumerate(self.arr_json_files):
                    if elem['size'] > max:
                        max = elem['size']
                        index = i
                        name = str(elem['hash'])
                try:
                    shutil.rmtree(os.path.join(self.path_of_trash, name))
                except OSError:
                    os.remove(os.path.join(self.path_of_trash, name))
                self.arr_json_files.remove(self.arr_json_files[index])


    def recover(self, list_of_files, force = True):
        """
        Recover files from trash bin to their locations
        :param list_of_files:
        :return:
        """
        for each_file in list_of_files:
            for each_json_file in self.arr_json_files:
                if each_file == each_json_file['name']:
                    path_of_file = self.path_of_trash +  '/' + str(each_json_file['hash'])
                    if force:
                        try:
                            os.renames(path_of_file, each_json_file['path'])
                            self.arr_json_files.remove(each_json_file)
                            print 'Recovering', each_json_file['name'], 'from bin'
                        except Exception as e:
                             print 'Error: ', e
                    else:
                        try:
                            if os.path.exists(each_json_file['path']):
                                print 'This file is exist. Would you like to replace it?'
                                if verification.yes_or_no():
                                    os.rename(path_of_file, each_json_file['path'])
                                    self.arr_json_files.remove(each_json_file)
                                    print 'Recovering', each_json_file['name'], 'from bin'
                                else:
                                    pass

                        except OSError as e:
                            print 'Error: ', e

        serialization.push_json(self.arr_json_files, self.database)
