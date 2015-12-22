import os.path
import getopt
import sys
import time

from search_for_citations import config
from ... import utils
from ...Parser import Parser


def get_arguments():
    argv = sys.argv[1:]
    try:
        opts, _ = getopt.getopt(argv, 'hl:f:', ['help', 'limit=', 'from='])
    except getopt.GetoptError as e:
        print(str(e))
        print('Usage: -h for help')
        sys.exit(2)
    
    limit = None
    _from = None
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: my-process.py -l 2 -f 2015-12-15')
            sys.exit()
        elif opt in ('-l', '--limit'):
            limit = int(arg)
        elif opt in ('-f', '--from'):
            _from = arg.lstrip()
        else:
            raise Exception('unhandled option')
    return (limit, _from)


class Harvester(Parser):
    
    def __init__(self, name, limit=None):
        super(Harvester, self).__init__('{}'.format(name))
        utils.create_dir(os.path.join(config.DOWNLOAD_DIR, 'harvester', name))
        self.split_publications = 10000
        self.limit = limit
        self.start_time = int(time.time())
        self.logger.info('start at {}'.format(self.start_time))
        
    def open_split_file(self):
        if self.count_publications % self.split_publications == 0:
            file_num = self.count_publications / self.split_publications
            if file_num > 0:
                self.close_output_file()
            self.open_output_file(os.path.join(config.DOWNLOAD_DIR, 'harvester', self.name, '{}-{}.xml'.format(self.start_time, file_num)))
        
    def stop_harvest(self):
        self.close_output_file()
        self.logger.info('stop')
    
    def check_stop_harvest(self):
        return self.limit and self.count_publications >= self.limit
