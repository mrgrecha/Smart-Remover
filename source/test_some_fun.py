import os, sys
import stat
import verification
import trash

#os.chmod('/Users/Dima/.MyTrash', stat.ST_MODE)
#print os.access('/Users/Dima/.MyTrash', os.W_OK)

#print verification.check_for_removing('111')

# print os.listdir(path)
# file_list = os.listdir(path)
# for files_or_dirs in file_list:
#     if os.path.isdir(files_or_dirs):
#         print 'Dir ', files_or_dirs
#         print os.path.join(os.path.abspath(path), files_or_dirs)
#         self.delete_for_regex(os.path.join(os.path.abspath(path), files_or_dirs), regex)
#     elif os.path.isfile(files_or_dirs) or os.path.islink(files_or_dirs):
#         print 'File ', files_or_dirs

print os.path.getctime('rr')