import os

def check_for_files_and_links(list_of_files):
    """Return a list of only files in list that was given"""
    list = []
    for file in list_of_files:
        if os.path.isfile(file) or os.path.islink(file):
            list.append(file)
        else:
            msg = str(file) + ' is not a file or link'
            raise TypeError(msg)
        if not os.access(file, os.W_OK):
            msg = 'You have not such permissions for ' + str(file)
            raise SystemError(msg)
    return list

def check_for_dir(list_of_dir):
    """Return a list of only directories"""
    list = []
    for dir in list_of_dir:
        if os.path.isdir(dir):
            list.append(dir)
        else:
            msg = str(dir) + ' is not a directory'
            raise TypeError(msg)
    return list

def check_for_removing(path): #TO DO: refactor it

     x = False
    # for abs_path, subfolders, files in os.walk(path):
    #     for abs in abs_path:
    #         if os.access(abs, os.W_OK):
    #             for subs in subfolders:
    #                 if os.access(subs, os.W_OK):
    #                     for file in files:
    #                         if os.access(file, os.W_OK):
    #                             x = True
    # return x

def yes_or_no():
    answer = str(raw_input('Y/N ?'))
    if answer == 'Y' or answer =='y':
        return True
    elif answer == 'N' or answer == 'n':
        return False
    else:
        print 'Error. Try again!'
        yes_or_no()


