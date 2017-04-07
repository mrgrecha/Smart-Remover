import ConfigParser, argparse

config = ConfigParser.RawConfigParser()
parser = argparse.ArgumentParser(description='An utility for making configure files')
parser.add_argument('-d', '--default', action = 'store_true', help = 'Make a default config. Has only DateBase and path of trash bin')
parser.add_argument('-c', '--custom', action = 'store_true', help = 'Make a custom config with user input.')

args = parser.parse_args()

if args.default:
    config.add_section('Section_Custom')
    config.set('Section_Custom', 'path', '/Users/Dima/.MyTrash')
    config.set('Section_Custom', 'database', 'DB.txt')
    config.set('Section_Custom', 'max_size', 500000000)
    config.set('Section_Custom', 'max_num', 1000)
    config.set('Section_Custom', 'max_time', 999999999)
    config.set('Section_Custom', 'policy', 'default')
    print 'Default config is made'

if args.custom:
    config.add_section('Section_Custom')
    path = raw_input('Enter a path of trash bin: ')
    config.set('Section_Custom', 'path',  path)
    database = raw_input('Enter a path of database: ')
    config.set('Section_Custom', 'database', database)
    max_size = raw_input('Enter a max size of trash bin: ')
    config.set('Section_Custom', 'max_size', max_size)
    max_time = raw_input('Enter a maximal time for items in trash bin: ')
    config.set('Section_Custom', 'max_time', max_time)
    max_num = raw_input('Enter a maximal number of trash bin files: ')
    config.set('Section_Custom', 'max_num', max_num)
    policy = raw_input('Enter a policy for your trash bin (Number, Memory, Time, Combo, Default): ')
    config.set('Section_Custom', 'policy', policy)
    print 'Custom config is made'

with open('config.cfg', 'wb') as configfile:
    config.write(configfile)