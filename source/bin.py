import os, argparse
import file_object
import serialization, shutil
import trash

def main():
	parser = argparse.ArgumentParser(description='Bin utility')
	parser.add_argument('-l', '--list', action = 'store_true', help = 'A list of files in trash')
	parser.add_argument('-c', '--clear', action = 'store_true', help = 'Clear all files in trash')
	parser.add_argument('--full', action = 'store_true', help = 'Full list of files')
	parser.add_argument('-d', '--delete',nargs='+', help = 'Delete a file/files from bin')
	parser.add_argument('-r', '--recover', nargs = '+', help = 'Recover files from a trash bin')

	parser.add_argument('-t', '--test', action = 'store_true', help = 'test')

	my_trash = trash.Trash('/Users/Dima/Documents/Python/Lab_2.Smart_RM/python_lab_2/source/config.cfg')
	args = parser.parse_args()

	if args.list:
		my_trash.bin_show()

	if args.clear:
		my_trash.remove_from_trash(os.listdir(my_trash.path_of_trash))

	if args.full:
		my_trash.full_show()

	if args.recover:
		my_trash.recover(args.recover)

	if args.delete:
	 	my_trash.remove_from_trash(args.delete)

	if args.test:
		my_trash.memory_update()


if __name__ == '__main__':
	main()