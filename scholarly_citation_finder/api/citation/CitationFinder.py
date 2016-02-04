#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections

from scholarly_citation_finder.api.Process import Process
from scholarly_citation_finder.apps.core.models import Author,\
    PublicationAuthorAffilation, Publication
from scholarly_citation_finder.api.citation.EvaluationWriter import EvaluationWriter
from scholarly_citation_finder.api.citation.PublicationSet import PublicationSet

class CitationFinder(Process):
        
    def __init__(self, name, database_name='mag'):
        super(CitationFinder, self).__init__(name)
        self.database_name = database_name
        #self.conn = connections['my_db_alias'].cursor()
        self.cursor = connections[self.database_name].cursor()
        
        self.output = EvaluationWriter(path=self.download_dir)
        
        self.publication_set = PublicationSet()
        self.publicationreferences_result_set = []        
    
    """    
    def _array2sqllist(self, list):
        #return ','.join([str(i) for i in list])
        return '('+str(list)[1:-1]+')'
    
    def _sqllist2array(self, sqllist):
        #result = '('+','.join([item[0] for item in sqllist])+')'
        return [item[0] for item in sqllist]
    """
    
    def set_by_author(self, name=None, id=None):
        try:
            author, length_publication_set = self.publication_set.set_by_author(name, id)
            filename = self.output.open(name=author.id)
            self.logger.info('set {} publications by author {} ({}), file {}'.format(length_publication_set, author.name, author.id, filename))
        except(ObjectDoesNotExist):
            self.logger.info('search author "{}", found nothing'.format(name))            

    def run(self, publication_limit=None, time_limit=None):
        if self.publication_set.is_set():
            self.logger.info('run {} with publication_limit={} and time_limit={}'.format(self.name, publication_limit, time_limit))
        else:
            raise Exception('publication_search_set not set')
        
    
    def run_done(self):
        self.output.close()
        self.logger.info('done')  
