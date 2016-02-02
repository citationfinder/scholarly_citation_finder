#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections

from scholarly_citation_finder.api.Process import Process
from scholarly_citation_finder.apps.core.models import Author,\
    PublicationAuthorAffilation, Publication
from scholarly_citation_finder.api.citation.EvaluationWriter import EvaluationWriter

class CitationFinder(Process):
        
    def __init__(self, name, database_name='mag'):
        super(CitationFinder, self).__init__(name)
        self.database_name = database_name
        #self.conn = connections['my_db_alias'].cursor()
        self.cursor = connections[self.database_name].cursor()
        
        self.output = EvaluationWriter(path=self.download_dir)
        
        self.publication_search_set = None
        self.publicationreferences_result_set = []        
        
    def _array2sqllist(self, list):
        #return ','.join([str(i) for i in list])
        return '('+str(list)[1:-1]+')'
    
    def _sqllist2array(self, sqllist):
        #result = '('+','.join([item[0] for item in sqllist])+')'
        return [item[0] for item in sqllist]
    
    def set_publication_search_set(self, publication_search_set):
        self.logger.info('set {} publications as search set'.format(len(publication_search_set)))
        self.publication_search_set = publication_search_set
        
    def set_author(self, name):
        '''
        
        :param name: Name of the author
        '''
        try:
            author = Author.objects.using(self.database_name).get(name=name)
            self.logger.warn(self.output.open(name=author.id))
            #author_publication = PublicationAuthorAffilation.objects.using(self.database_name).filter(author=author)
            #Publication.objects.using(self.database_name).filter()
            self.set_publication_search_set(Publication.objects.using(self.database_name).filter(publicationauthoraffilation__author=author))
            return True
        except(ObjectDoesNotExist):
            self.logger.info('search author "{}", found nothing'.format(name))
        return False 
        
        
        """    
        self.cursor.execute("SELECT id FROM core_author WHERE name LIKE %s LIMIT 1", (name,))
        result = self.cursor.fetchone()
        
        if result:
            id = result[0]
            self._open_output_file(id)
            self.logger.info('search author "{}", found author id: {}'.format(name, id))
            self.cursor.execute("SELECT publication_id FROM core_publicationauthoraffilation WHERE author_id = %s", (id,))
            self.set_publication_search_set(self._sqllist2array(self.cursor.fetchall()))
            return True
        else:
            self.logger.info('search author "{}", found nothing'.format(name))
        return False     
        """     
    
    def set_journal(self, journal_name):
        # SQL -> get papers and call set_publication_search_set
        pass
    
    #def __get_references(self):
    #    

    def run(self, publication_limit=None, time_limit=None):
        if self.publication_search_set:
            self.logger.info('run {} with publication_limit={} and time_limit={}'.format(self.name, publication_limit, time_limit))
        else:
            raise Exception('publication_search_set not set')
        #raise Exception('Implement run method')
        
    
    def run_done(self):
        self.output.close()
        self.logger.info('done')  
