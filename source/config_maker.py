import ConfigParser
import argparse
import json
import os


def main():
    config = ConfigParser.RawConfigParser()
    parser = argparse.ArgumentParser(description='An utility for making configure files')
    parser.add_argument('-p', '--path', help='Input path of trash in config file.')
    parser.add_argument('-db', '--database', help='Input path of database in config file.')
    parser.add_argument('-ms', '--maxsize', help='Input maximal size(memory) of a trash in config file.')
    parser.add_argument('-mn', '--maxnumber', help='Input maximal count of trash files in config file.')
    parser.add_argument('-mt', '--maxtime', help='Input maximal time for storing elements in a trash in config file.')
    parser.add_argument('-dr', '--dryrun', action='store_true', help='Dry run mode on.')
    parser.add_argument('-s', '--silent', action='store_true', help='Silent mode on.')
    parser.add_argument('-po', '--policies', help='Input diffrent policies.')
    parser.add_argument('-l', '--list', action='store_true', help='Show a config settings')
    parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode on.')
    parser.add_argument('-f', '--force', action='store_true', help='Force mode on.')


    args = parser.parse_args()

    json_dict = {}
    file_path = '~'
    if args.list:
        with open(os.path.join(os.path.expanduser(file_path), 'config.cfg'), 'r+') as configfile:
            for line in configfile.readlines():
                print line
    else:
        config.add_section('Section_Custom')
        if args.path:
            config.set('Section_Custom', 'path', args.path)
            json_dict['path'] = args.path
        else:
            config.set('Section_Custom', 'path', '~/.MyTrash')
            json_dict['path'] = '~/.MyTrash'
        if args.database:
            config.set('Section_Custom', 'database', args.database)
            json_dict['database'] = args.database
        else:
            config.set('Section_Custom', 'database', '~/.DB.json')
            json_dict['database'] = '~/.DB.json'
        if args.maxsize:
            config.set('Section_Custom', 'max_size', args.maxsize)
            json_dict['max_size'] = args.maxsize
        else:
            config.set('Section_Custom', 'max_size', 500000000)
            json_dict['max_size'] = 500000000
        if args.maxtime:
            config.set('Section_Custom', 'max_time', args.maxtime)
            json_dict['max_time'] = args.maxtime
        else:
            config.set('Section_Custom', 'max_time', 999999999)
            json_dict['max_time'] = 999999999
        if args.maxnumber:
            config.set('Section_Custom', 'max_num', args.maxnumber)
            json_dict['max_num'] = args.maxnumber
        else:
            config.set('Section_Custom', 'max_num', 1000)
            json_dict['max_num'] = 1000
        if args.dryrun:
            config.set('Section_Custom', 'dry_run', True)
            json_dict['dry_run'] = True
        else:
            config.set('Section_Custom', 'dry_run', 'False')
            json_dict['dry_run'] = 'False'
        if args.silent:
            config.set('Section_Custom', 'silent', True)
            json_dict['silent'] = True
        else:
            config.set('Section_Custom', 'silent', 'False')
            json_dict['silent'] = 'False'
        if args.policies:
            config.set('Section_Custom', 'policies', args.policies)
            json_dict['policies'] = args.policies
        else:
            config.set('Section_Custom', 'policies', 'default')
            json_dict['policies'] = 'default'
        if args.interactive:
            config.set('Section_Custom', 'interactive', args.interactive)
            json_dict['policies'] = args.interactive
        else:
            config.set('Section_Custom', 'interactive', 'False')
            json_dict['interactive'] = 'False'
        if args.force:
            config.set('Section_Custom', 'force', args.force)
            json_dict['force'] = args.force
        else:
            config.set('Section_Custom', 'force', 'False')
            json_dict['force'] = 'False'

        print 'Config is made'

        with open(os.path.join(os.path.expanduser(file_path), 'config.cfg'), 'wb') as configfile:
            config.write(configfile)
        with open(os.path.join(os.path.expanduser(file_path),'config.json'), 'wb') as config_json:
            json.dump(json_dict, config_json, indent=4)

if __name__ == '__main__':
    main()
