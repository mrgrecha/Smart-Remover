import argparse
import serialization
import shutil, os, sys, constants


if serialization.num_of_dicts() == 0:
    arr_json_files = []
else:
    arr_json_files = serialization.load_json()

def recover(list_of_files):
	for each_file in list_of_files:
		for each_json_file in arr_json_files:
			if each_file == each_json_file['name']:
				path_of_file = constants.TRASH +'/' + str(each_json_file['hash'])
				shutil.move(path_of_file, each_json_file['path'])
				arr_json_files.remove(each_json_file)

	with open('DB.txt', 'w') as db:
		serialization.push_json(arr_json_files, db)



def main():
	parser = argparse.ArgumentParser(description='Smart recover utility')
	parser.add_argument('-d', '--directory', nargs='+', help='Recover a directory')
	parser.add_argument('-f', '--files', nargs='+', help='Recover files')

	args = parser.parse_args()

	if args.files:
		recover(args.files)


if __name__ == '__main__':
	main()