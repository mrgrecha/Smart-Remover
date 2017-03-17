# if args.list:
#     print os.listdir('/Users/Dima/.MyTrash')

import os

def full_show():
    for ind, file in enumerate(os.listdir('/Users/Dima/.MyTrash')):
        print("{0}. {1}".format(ind + 1, file))