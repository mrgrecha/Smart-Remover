import argparse
import os
import commands.remove_command as remove_command
from source.src import trash


def main():
    parser = argparse.ArgumentParser(description='Smart remove')
    parser.add_argument('-d', '--directory', nargs='+', help='Remove a directory')
    parser.add_argument('-f', '--files', nargs='+', help='Remove files')
    parser.add_argument('--regular', help='Remove files for a regular expression')
    parser.add_argument('-dr', '--dryrun', action='store_true', help='Dry run mode on')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode on')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode on')

    my_trash = trash.Trash(os.path.expanduser('~/config.cfg'))
    args = parser.parse_args()

    if args.silent:
        my_trash.go_silent_mode()

    if args.dryrun:
        my_trash.go_dry_run()

    if args.interactive:
        my_trash.go_interactive_mode()

    if args.files:
        my_rfc_command = remove_command.RFCommand(my_trash)
        my_rfc_command.execute(args.files)

    if args.directory:
        my_rdc_command = remove_command.RDCommand(my_trash)
        my_rdc_command.execute(args.directory)

    if args.regular:
        my_rrc_command = remove_command.RRCommand(my_trash)
        my_rrc_command.execute(args.regular)
        my_rrc_command.real_regex()


    remove_command.save_command()
if __name__ == '__main__':
    main()
