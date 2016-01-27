import getopt
import sys

from ..Parser import Parser


def get_arguments(argv):
    try:
        opts, _ = getopt.getopt(argv, 'hl:f:u:', ['help', 'limit=', 'from=', 'until='])
    except getopt.GetoptError as e:
        print(str(e))
        print('Usage: -h for help')
        sys.exit(2)
    
    kwargs = {}
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: my-process.py -l 2 -f 2015-12-15 -u 2015-12-24')
            sys.exit()
        elif opt in ('-l', '--limit'):
            kwargs['limit'] = int(arg)
        elif opt in ('-f', '--from'):
            kwargs['_from'] = arg.lstrip()
        elif opt in ('-u', '--until'):
            kwargs['until'] = arg.lstrip()
        else:
            raise Exception('unhandled option')
    return kwargs


class Harvester(Parser):
    
    def __init__(self, name):
        super(Harvester, self).__init__(name)
        self.logger.info('start {} harvester'.format(name))
        
    def stop_harvest(self):
        self.logger.info('stop')
    
    def check_stop_harvest(self):
        return self.limit and self.count_publications >= self.limit
