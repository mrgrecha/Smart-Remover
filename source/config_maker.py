import ConfigParser, argparse, json

config = ConfigParser.RawConfigParser()
parser = argparse.ArgumentParser(description='An utility for making configure files')
parser.add_argument('-d', '--default', action = 'store_true', help = 'Make a default config. Has only DateBase and path of trash bin')
parser.add_argument('-c', '--custom', action = 'store_true', help = 'Make a custom config with user input.')

args = parser.parse_args()

if args.default:
    json_dict = {}
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
    config.set('Section_Custom', 'policy', 'default')
    json_dict['policy'] = 'default'
    print 'Default config is made'

if args.custom:
    json_dict = {}
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
    policy = raw_input('Enter a policy for your trash bin (Number, Memory, Time, Combo, Default, Force): ')
    config.set('Section_Custom', 'policy', policy)
    json_dict['policy'] = policy
    print 'Custom config is made'

with open('config.cfg', 'wb') as configfile:
    config.write(configfile)
with open('config.json', 'wb') as config_json:
    json.dump(json_dict, config_json, indent=4)