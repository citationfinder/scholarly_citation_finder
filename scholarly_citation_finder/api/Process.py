#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
import os.path
import logging


from scholarly_citation_finder import config
from scholarly_citation_finder.settings.development import DATABASES
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

    def get_database_connection(self, name='default'):
        '''
        Returns a psycopg2 for the given database by using the Django settings
        file.
        
        :param name: Name of the database
        '''
        db = DATABASES[name]
        return psycopg2.connect(host=db['HOST'],
                                dbname=db['NAME'],
                                user=db['USER'],
                                password=db['PASSWORD'])
