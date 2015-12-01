import getopt
import sys
import config

from ...Parser import Parser

class Harvester(Parser):
    
    def __init__(self, name):
        super(Harvester, self).__init__(name)
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
            num = self.count_publications / self.split_publications
            if num > 0:
                self.close_output_file()
            self.open_output_file(config.DOWNLOAD_PATH+'harvester/{}/publication-{}.xml'.format(self.name, num))   
        
    def stop_harvest(self):
        self.close_output_file()
        self.logger.info('stop')
    
    def check_stop_harvest(self):
        if self.limit and self.count_publications >= self.limit:
            self.stop_harvest()
            return True
        else:
            return False
        

