import os
import codecs
import psycopg2


from ....settings.development import DATABASES
from psycopg2._psycopg import ProgrammingError, OperationalError, DataError
from ..Harvester import Harvester
#from psycopg2._psycopg import DataError, IntegrityError, InternalError
#from ...core.models import Author
#from django.db.utils import DataError

class MagHarvester(Harvester):
    
    def __init__(self):
        super(Harvester, self).__init__('mag')
        self.conn = self.connect_database()

    def connect_database(self):
        db = DATABASES[self.name]
        return psycopg2.connect(host=db['HOST'],
                                dbname=db['NAME'],
                                user=db['USER'],
                                password=db['PASSWORD'])

    def _database_copy(self, filename, table, columns):
        filename = os.path.join(self.path, filename)
        """
        http://initd.org/psycopg/docs/cursor.html
        """
        try:
            self.logger.info('start ---------------------------------')
            self.logger.info(filename)
            cur = self.conn.cursor()
            #cur.copy_from(file=filename,
            #              table=table,
            #              sep='\t',
            #query = "COPY {} ({}) FROM '{}' DELIMITER '\t' HEADER CSV;".format(table, columns, filename)
            #self.logger.info(query)
            #cur.execute(query)
            query = "COPY {} ({}) FROM STDIN DELIMITER '\t' HEADER CSV;".format(table, columns)
            cur.copy_expert(sql=query,
                            file=open(filename, 'r'))
            self.logger.info(cur.statusmessage)
            self.conn.commit()
            self.logger.info('end -----------------------------------')
        except(ProgrammingError, OperationalError, DataError) as e:
            self.logger.warn('{}: {}'.format(type(e).__name__, str(e)))
        except(IOError): # by open(<file>)
            self.logger.warn('{}: {}'.format(type(e).__name__, str(e)))            

    def store_publications(self, filename):
        self._database_copy(filename=filename,
                            table='core_publication',
                            columns='id, title, year, doi, series, journal')

    def store_publicationreferences(self, filename):
        self._database_copy(filename=filename,
                            table='core_publicationreference',
                            columns='publication_id, reference_id')

    def store_publication_authors(self, filename):
        self._database_copy(filename=filename,
                            table='core_publication_authors',
                            columns='publication_id, author_id')

    def store_authors(self, filename):
        self._database_copy(filename,
                            table='core_author',
                            columns='id, name')
