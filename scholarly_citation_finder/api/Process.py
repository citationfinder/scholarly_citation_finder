import os.path
import logging


from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir

class Process(object):
    
    def __init__(self, name):
        self.name = name
        self.download_dir = create_dir(os.path.join(config.DOWNLOAD_DIR, self.name))
        self.logger = self.init_logger()
        
    def init_logger(self):
        logging.basicConfig(filename=os.path.join(config.LOG_DIR, '{}.log'.format(self.name)),
                            level=logging.INFO,
                            format='[%(asctime)s] %(levelname)s [%(module)s] %(message)s')
        return logging.getLogger()  