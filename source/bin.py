import os, argparse
import file_object

def bin_show():
	for ind, file in enumerate(os.listdir('/Users/Dima/.MyTrash')):
		print("{0}. {1}".format(ind + 1, file))

def update():
	files_in_trash = os.listdir('/Users/Dima/.MyTrash')
	n = files_in_trash.__len__()
	index = 0
	for files in files_in_trash:
		arr_of_files = [file_object.FileObject() for i in xrange(n)]
		arr_of_files[index].add_name(files)
		index += 1

def main():
	parser = argparse.ArgumentParser(description='Bin utility')
	parser.add_argument('-l', '--list', action = 'store_true', help = 'A list of files in trash')
	parser.add_argument('-c', '--clear', action = 'store_true', help = 'Clear all files in trash')
	parser.add_argument('--full', action = 'store_true', help = 'Full list of files')

if __name__ == '__main__':
	main()