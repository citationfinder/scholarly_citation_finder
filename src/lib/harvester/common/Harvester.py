import os.path
import getopt
import sys

import config
from lib import utils
from ...Parser import Parser

class Harvester(Parser):
    
    def __init__(self, name):
        super(Harvester, self).__init__('{}'.format(name))
        utils.create_dir(os.path.join(config.DOWNLOAD_DIR, 'harvester', name))
        self.split_publications = 10000
        self.limit = self.get_arguments(sys.argv[1:])
        self.logger.info('start')
    
    def get_arguments(self, argv):
        try:
            opts, _ = getopt.getopt(argv, "hl:", ["help", "limit="])
        except getopt.GetoptError as e:
            print(str(e))
            print('Usage: -h for help')
            sys.exit(2)
    
        limit = None
        for opt, arg in opts:
            if opt == '-h':
                print('Usage: my-process.py -s <start> -e <end>')
                sys.exit()
            elif opt in ("-l", "--limit"):
                limit = int(arg);
            else:
                raise Exception("unhandled option")
        return limit 
        
    def open_split_file(self):
        if self.count_publications % self.split_publications == 0:
            file_num = self.count_publications / self.split_publications
            if file_num > 0:
                self.close_output_file()
            self.open_output_file(os.path.join(config.DOWNLOAD_DIR, 'harvester', self.name, 'publication-{}.xml'.format(file_num)))   
        
    def stop_harvest(self):
        self.close_output_file()
        self.logger.info('stop')
    
    def check_stop_harvest(self):
        return self.limit and self.count_publications >= self.limit        
