import os.path

from scholarly_citation_finder.api.Process import Process

class CitationFinder(Process):
        
    def __init__(self, name, database_name='mag'):
        super(CitationFinder, self).__init__(name)
        self.conn = self.get_database_connection(database_name)
        self.cursor = self.conn.cursor()
        self.logger.info('init {} ------------------'.format(name))
        
    def _array2sqllist(self, list):
        #return ','.join([str(i) for i in list])
        return '('+str(list)[1:-1]+')'
    
    def _sqllist2array(self, sqllist):
        #result = '('+','.join([item[0] for item in sqllist])+')'
        return [item[0] for item in sqllist]
    
    def _open_output_file(self, name):
        self.output = open(os.path.join(self.download_dir, '{}.csv'.format(name)), 'w+')
        
    def set_publications(self, publication_ids):
        self.logger.info('set {} publications as search set'.format(len(publication_ids)))
        self.publication_ids = publication_ids
        
    def set_author(self, name):
        '''
        
        :param name: Name of the author
        '''
        
        self.cursor.execute("SELECT id FROM core_author WHERE name LIKE %s LIMIT 1", (name,))
        result = self.cursor.fetchone()
        
        if result:
            id = result[0]
            self._open_output_file(id)
            self.logger.info('search author "{}", found author id: {}'.format(name, id))
            self.cursor.execute("SELECT publication_id FROM core_publicationauthoraffilation WHERE author_id = %s", (id,))
            self.set_publications(self._sqllist2array(self.cursor.fetchall()))
            return True
        else:
            self.logger.info('search author "{}", found nothing'.format(name))
        return False          
    
    def set_journal(self, journal_name):
        # SQL -> get papers and call set_publications
        pass

    def run(self, publication_limit=None, time_limit=None):
        self.logger.info('run with publication_limit={} and time_limit={}'.format(publication_limit, time_limit))
        #raise Exception('Implement run method')
