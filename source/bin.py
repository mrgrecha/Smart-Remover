import os, argparse
import file_object
import serialization
import datetime
import pydoc
import constants

if serialization.num_of_dicts() == 0:
    arr_json_files = []
else:
    arr_json_files = serialization.load_json()

def bin_show():
	if serialization.num_of_dicts() == 0:
		print 'No files in trash'
	for ind, file in enumerate(os.listdir('/Users/Dima/.MyTrash')):
		print("{0}. {1}".format(ind + 1, file))

def update(): #to do automatic update, maybe do it in another file
	files_in_trash = os.listdir('/Users/Dima/.MyTrash')
	n = files_in_trash.__len__()
	index = 0
	for files in files_in_trash:
		arr_of_files = [file_object.FileObject() for i in xrange(n)]
		arr_of_files[index].add_name(files)
		index += 1

def full_show():
	if serialization.num_of_dicts() == 0:
		print 'No files in trash'
	full_show_string = ''
	for index, each_file in enumerate(arr_json_files):
		full_show_string +=	'%d %s %s %d %s %d Bytes \n' % (index + 1, each_file['name'],each_file['type'], each_file['hash'],datetime.datetime.fromtimestamp(each_file['time_of_life']).strftime('%Y-%m-%d %H:%M:%S'),each_file['size'])

	if len(arr_json_files) >  constants.MAX_LIST_HEIGHT:
		pydoc.pager(full_show_string)
	else:
		print full_show_string




def clear():
	with open('DB.txt', 'w') as db:
		files_in_trash = os.listdir('/Users/Dima/.MyTrash')
		for files in files_in_trash:
			os.remove(files)

		arr_json_files = []
		print 'Clearing a bin'
		# for file in arr_json_files:
		# 	arr_json_files.remove(file)


		serialization.push_json(arr_json_files, db)
		print 'Clearing a bin from files'

def delete(list): #to do: delete from bin and delete from DataBase full dict
	pass
	# with open('DB.txt', 'w') as db:
	# 	for delete_elem in list:
	# 		arr_json_files.remove(arr_json_files[])
	# 		os.remove('/Users/Dima/.MyTrash/' + delete_elem)
	# 	serialization.push_json(arr_json_files, db)


def main():
	parser = argparse.ArgumentParser(description='Bin utility')
	parser.add_argument('-l', '--list', action = 'store_true', help = 'A list of files in trash')
	parser.add_argument('-c', '--clear', action = 'store_true', help = 'Clear all files in trash')
	parser.add_argument('--full', action = 'store_true', help = 'Full list of files')
	parser.add_argument('-d', '--delete',nargs='+', help = 'Delete a file/files from bin')

	args = parser.parse_args()

	if args.list:
		bin_show()

	if args.clear:
		clear()

	if args.full:
		full_show()

	if args.delete:
		delete(args.delete)


if __name__ == '__main__':
	main()