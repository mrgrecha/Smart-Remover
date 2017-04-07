import os, argparse
import file_object
import serialization, shutil
import trash


def update(): #TODO: automatic update, maybe do it in another file
	files_in_trash = os.listdir('/Users/Dima/.MyTrash')
	n = files_in_trash.__len__()
	index = 0
	for files in files_in_trash:
		arr_of_files = [file_object.FileObject() for i in xrange(n)]
		arr_of_files[index].add_name(files)
		index += 1






def clear():
	with open('DB.txt', 'w') as db:
		files_in_trash = os.listdir('/Users/Dima/.MyTrash/')
		for files in files_in_trash:
			if os.path.isdir(files):
				shutil.rmtree(files)
			else:
				os.remove(files)
		arr_json_files = []
		print 'Clearing a bin'
		serialization.push_json(arr_json_files, db)
		print 'Clearing a bin from files'




def main():
	parser = argparse.ArgumentParser(description='Bin utility')
	parser.add_argument('-l', '--list', action = 'store_true', help = 'A list of files in trash')
	parser.add_argument('-c', '--clear', action = 'store_true', help = 'Clear all files in trash')
	parser.add_argument('--full', action = 'store_true', help = 'Full list of files')
	parser.add_argument('-d', '--delete',nargs='+', help = 'Delete a file/files from bin')
	parser.add_argument('-r', '--recover', nargs = '+', help = 'Recover files from a trash bin')

	parser.add_argument('-t', '--test', action = 'store_true', help = 'test')

	my_trash = trash.Trash('/Users/Dima/.MyTrash', 'DB.txt', 1000, 300)
	args = parser.parse_args()

	if args.list:
		my_trash.bin_show()

	if args.clear:
		clear()

	if args.full:
		my_trash.full_show()

	if args.recover:
		my_trash.recover(args.recover)

	if args.delete:
	 	my_trash.remove_from_trash(args.delete)

	if args.test:
		my_trash.update()


if __name__ == '__main__':
	main()