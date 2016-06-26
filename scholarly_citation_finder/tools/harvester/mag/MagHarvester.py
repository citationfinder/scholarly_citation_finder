#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import psycopg2
import logging
from psycopg2._psycopg import ProgrammingError, OperationalError, DataError,\
    InternalError

from scholarly_citation_finder import config
from scholarly_citation_finder.settings.development import DATABASES
from .MagNormalize import MagNormalize, get_pre_name

logging.basicConfig(filename=os.path.join(config.LOG_DIR, 'mag.log'),
                            level=logging.INFO,
                            format='[%(asctime)s] %(levelname)s [%(module)s] %(message)s')
logger = logging.getLogger(__name__)


class MagHarvester:
    '''
    Harvester of the MAG graph.
    '''
    
    def __init__(self):
        '''
        Create object.
        '''
        self.name = 'mag'
        self.download_dir = os.path.join(config.DOWNLOAD_DIR, self.name)
        self.conn = self.connect_database()

    def connect_database(self):
        '''
        Connect to database.
        
        :return: Database connection
        '''
        db = DATABASES[self.name]
        return psycopg2.connect(host=db['HOST'],
                                dbname=db['NAME'],
                                user=db['USER'],
                                password=db['PASSWORD'])

    def _database_copy(self, filename, table, columns):
        '''
        Copy normalized CSV file into database
        
        @see: http://initd.org/psycopg/docs/cursor.html
        :param filename: Name of the CSV file
        :param table: Database table name
        :param columns: Table columns
        :return: If copy was successful
        '''
        try:
            logger.info('harvest {} ++++++++'.format(filename))
            cur = self.conn.cursor()
            #cur.copy_from(file=filename,
            #              table=table,
            #              sep='\t',
            #query = "COPY {} ({}) FROM '{}' DELIMITER '\t' HEADER CSV;".format(table, columns, filename)
            #self.logger.info(query)
            #cur.execute(query)
            
            # Workaround: Some strings contain a ", but that is the default quote
            # character of the PostgreSQL copy function. That is why we specify
            # the quote character to \b (Backspace), because this should never
            # be in a string.
            query = "COPY {} ({}) FROM STDIN DELIMITER E'\t' QUOTE E'\b' HEADER CSV;".format(table, columns)
            logger.info(query)
            cur.copy_expert(sql=query,
                            file=open(filename, 'r'))
            logger.info(cur.statusmessage)
            self.conn.commit()
            logger.info('end harvest ++++++++++')
            return True
        except(DataError, InternalError, ProgrammingError, OperationalError) as e: # by psycopg2
            self.conn.rollback()
            logger.warn(e, exc_info=True)
        except(IOError) as e: # by open(<file>)
            logger.warn(e, exc_info=True)
        return False

    def run(self, files=None):
        if files is None:
            files = MagNormalize.FILES
        logger.info('run -----------------------------')        
        for name, file in files.iteritems():
            file_pre = get_pre_name(file)
            csv_file = os.path.join(self.download_dir, file_pre)
            if os.path.isfile(csv_file) and hasattr(self, name):
                logger.info('start store {}'.format(csv_file))
                if getattr(self, name)(csv_file):
                    os.rename(csv_file, os.path.join(self.download_dir, '~{}'.format(file_pre)))
                else:
                    pass # exceptions already get logged before this line
            elif not hasattr(self, name):
                logger.info('no attribute {}'.format(name))                
            else:
                logger.info('no file {}'.format(csv_file))
        logger.info('run done ------------------------')

    def affiliations(self, filename):
        return self._database_copy(filename=filename,
                            table='core_affilation',
                            columns='id, name')

    def authors(self, filename):
        return self._database_copy(filename,
                            table='core_author',
                            columns='id, name')
        
    def conferences(self, filename):
        return self._database_copy(filename,
                            table='core_conference',
                            columns='id, short_name, name')
        
    def conference_instances(self, filename):
        return self._database_copy(filename,
                            table='core_Conferenceinstance',
                            columns='id, conference_id, short_name, name, location, url, year')

    def fields_of_study(self, filename):
        return self._database_copy(filename,
                            table='core_fieldOfStudy',
                            columns='id, name')

    def journals(self, filename):
        return self._database_copy(filename,
                            table='core_journal',
                            columns='id, name')

    def papers(self, filename):
        return self._database_copy(filename=filename,
                            table='core_publication',
                            columns='id, title, year, date, doi, series, journal_id, conference_id')

    def paper_author_affiliations(self, filename):
        return self._database_copy(filename=filename,
                            table='core_publicationauthoraffilation',
                            columns='publication_id, author_id, affilation_id')
        
    def paper_keywords(self, filename):
        return self._database_copy(filename=filename,
                            table='core_publicationkeyword',
                            columns='publication_id, name, fieldofstudy_id')      

    def paper_references(self, filename):
        return self._database_copy(filename=filename,
                            table='core_publicationreference',
                            columns='publication_id, reference_id')
        
    def paper_urls(self, filename):
        return self._database_copy(filename=filename,
                            table='core_publicationurl',
                            columns='publication_id, url')
        
#if __name__ == '__main__':
#    a = MagHarvester()
#    a.run()