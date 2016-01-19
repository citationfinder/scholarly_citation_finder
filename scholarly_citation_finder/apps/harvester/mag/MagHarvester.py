import os.path
import os.rename
import codecs
import psycopg2


from ....settings.development import DATABASES
from psycopg2._psycopg import ProgrammingError, OperationalError, DataError
from ..Harvester import Harvester
from scholarly_citation_finder.apps.harvester.mag.normalize_files import MagNormalize
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
            return True
        except(ProgrammingError, OperationalError, DataError) as e:
            self.logger.warn('{}: {}'.format(type(e).__name__, str(e)))
            return False
        except(IOError): # by open(<file>)
            self.logger.warn('{}: {}'.format(type(e).__name__, str(e)))
            return False

    def run(self):
        self.logger.info('run -----------------------------')        
        for name, file in MagNormalize.FILES.iteritems():
            csv_file = os.path.join(self.download_dir, '{}_pre.txt'.format(file[:-4]))
            if os.path.isfile(csv_file):
                #self.logger.info('start store {}'.format(csv_file))
                if getattr(self, name)(csv_file):
                    os.rename(csv_file, '~{}'.format(csv_file))
                else:
                    pass # exceptions already get logged before this line
            else:
                self.logger.info('no file {}'.format(csv_file))
        self.logger.info('run done ------------------------')

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
                            columns='id, conference_id', 'short_name', 'name', 'location', 'url', 'year')

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
        
