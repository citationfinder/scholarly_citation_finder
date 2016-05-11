import logging
import os.path

from scholarly_citation_finder import config
from scholarly_citation_finder.lib.file import create_dir
from scholarly_citation_finder.apps.parser.Parser import Parser

logger = logging.getLogger(__name__)


class Harvester(object):
    '''
    Abstract harvester class.
    '''
    
    COMMIT_AFTER_NUM_PUBLICATIONS = 50000

    def __init__(self, name, database='default'):
        '''
        Create object.
        
        :param name: Harvester name
        :param database: Database name
        '''
        self.name = name
        self.download_dir = create_dir(os.path.join(config.DOWNLOAD_DIR, self.name))
        self.parser = Parser(database=database)

    def start_harevest(self, logger_string=''):
        '''
        Call when start harvesting.
               
        :param logger_string: Optional string that get written into the log, e.g. parameters of the harvest run
        '''
        #self.count_publications = 0
        logger.info('start {} harvester ({})'.format(self.name, logger_string))        
        
    def stop_harvest(self):
        '''
        Call when stop harvesting. Commit all database changes.
        '''
        logger.info('stop parsed {} entries'.format(self.parser.count_publications))
        self.parser.count_publications = 0
        self.parser.commit()

    def check_stop_harvest(self):
        '''
        Check, if the harvester should stop.
        
        :return: True, if the harvester should stop
        '''
        if self.parser.count_publications > 0 and (self.parser.count_publications % self.COMMIT_AFTER_NUM_PUBLICATIONS) == 0:
            self.parser.commit()
        return self.limit and self.parser.count_publications >= self.limit
    
    def set_limit(self, limit):
        '''
        Set the limit of the harvester.
        
        :param limit: Limit of parsed entries.
        '''
        try:
            self.limit = int(limit)
        except(TypeError):
            self.limit = None
