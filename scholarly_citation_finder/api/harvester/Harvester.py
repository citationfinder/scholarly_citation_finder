import logging
import os.path

from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir
from scholarly_citation_finder.api.Parser import Parser

logger = logging.getLogger(__name__)


class Harvester(object):
    
    COMMIT_AFTER_NUM_PUBLICATIONS = 100000

    def __init__(self, name, database='default'):
        self.name = name
        self.download_dir = create_dir(os.path.join(config.DOWNLOAD_DIR, self.name))
        self.parser = Parser(database=database)

    def start_harevest(self, logger_string=''):
        '''        
        :param logger_string: Optional string that get written into the log, e.g. parameters of the harvest run
        '''
        #self.count_publications = 0
        logger.info('start {} harvester ({})'.format(self.name, logger_string))        
        
    def stop_harvest(self):
        logger.info('stop parsed {} entries'.format(self.parser.count_publications))
        self.parser.commit()
    
    def check_stop_harvest(self):
        if self.parser.count_publications > 0 and (self.parser.count_publications % self.COMMIT_AFTER_NUM_PUBLICATIONS) == 0:
            self.parser.commit()
        return self.limit and self.parser.count_publications >= self.limit
    
    def set_limit(self, limit):
        try:
            self.limit = int(limit)
        except(TypeError):
            self.limit = None
