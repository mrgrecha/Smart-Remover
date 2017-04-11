import ConfigParser
import argparse
import json
import logging


def main():
    config = ConfigParser.RawConfigParser()
    parser = argparse.ArgumentParser(description='An utility for making configure files')
    parser.add_argument('-d', '--default', action='store_true', help='Make a default config.')
    parser.add_argument('-c', '--custom', action='store_true', help='Make a custom config with user input.')

    args = parser.parse_args()
    json_dict = {}

    if args.default:
        config.add_section('Section_Custom')
        config.set('Section_Custom', 'path', '/Users/Dima/.MyTrash')
        json_dict['path'] = '/Users/Dima/.MyTrash'
        config.set('Section_Custom', 'database', 'DB.json')
        json_dict['database'] = 'DB.json'
        config.set('Section_Custom', 'max_size', 500000000)
        json_dict['max_size'] = 500000000
        config.set('Section_Custom', 'max_num', 1000)
        json_dict['max_num'] = 1000
        config.set('Section_Custom', 'max_time', 999999999)
        json_dict['max_time'] = 999999999
        config.set('Section_Custom', 'policy_for_program', 'soft')
        json_dict['policy_for_program'] = 'soft'
        config.set('Section_Custom', 'policy_for_trash', 'default')
        json_dict['policy_for_trash'] = 'default'
        config.set('Section_Custom', 'silent', 'False')
        json_dict['silent'] = 'False'
        config.set('Section_Custom', 'dry_run', 'False')
        json_dict['dry_run'] = 'False'
        logging.info('Default config is made')

    if args.custom:
        config.add_section('Section_Custom')
        path = raw_input('Enter a path of trash bin: ')
        config.set('Section_Custom', 'path',  path)
        json_dict['path'] = path
        database = raw_input('Enter a path of database: ')
        config.set('Section_Custom', 'database', database)
        json_dict['database'] = database
        max_size = raw_input('Enter a max size of trash bin: ')
        config.set('Section_Custom', 'max_size', max_size)
        json_dict['max_size'] = max_size
        max_time = raw_input('Enter a maximal time for items in trash bin: ')
        config.set('Section_Custom', 'max_time', max_time)
        json_dict['max_time'] = max_time
        max_num = raw_input('Enter a maximal number of trash bin files: ')
        config.set('Section_Custom', 'max_num', max_num)
        json_dict['max_num'] = max_num
        policy_for_trash = raw_input('Enter a policy for your trash bin (Number, Memory, Time, Combo, Default): ')
        config.set('Section_Custom', 'policy_for_trash', policy_for_trash)
        json_dict['policy_for_trash'] = policy_for_trash
        policy_for_program = raw_input('Enter a policy for your trash bin (soft, force): ')
        config.set('Section_Custom', 'policy_for_program', policy_for_program)
        json_dict['policy_for_program'] = policy_for_program
        silent = raw_input('Enter True if you want to activate silent mode, False if you want print logs: ')
        config.set('Section_Custom', 'silent', silent)
        json_dict['silent'] = silent
        dry_run = raw_input('Enter True if you want to activate dry run mode: ')
        config.set('Section_Custom', 'dry_run', dry_run)
        json_dict['dry_run'] = dry_run
        logging.info('Custom config is made')

    with open('config.cfg', 'wb') as configfile:
        config.write(configfile)
    with open('config.json', 'wb') as config_json:
        json.dump(json_dict, config_json, indent=4)

if __name__ == '__main__':
    main()
