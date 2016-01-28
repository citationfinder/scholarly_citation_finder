import getopt
import sys

from ..Parser import Parser
from psycopg2._psycopg import IntegrityError
from scholarly_citation_finder.api.Parser import ParserRollbackError


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
    
    COMMIT_AFTER_NUM_PUBLICATIONS = 200000

    def __init__(self, name):
        super(Harvester, self).__init__(name)
        
    def start_harevest(self):
        self.count_publications = 0
        self.logger.info('start {} harvester'.format(self.name))        
        
    def stop_harvest(self):
        self.logger.info('stop parsed {} entries'.format(self.count_publications))
        self.commit()
    
    def check_stop_harvest(self):
        if (self.count_publications % self.COMMIT_AFTER_NUM_PUBLICATIONS) == 0:
            self.commit()
        return self.limit and self.count_publications >= self.limit
