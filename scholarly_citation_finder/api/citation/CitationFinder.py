#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections

from scholarly_citation_finder.api.Process import Process
from scholarly_citation_finder.api.citation.PublicationSet import PublicationSet
from scholarly_citation_finder.api.citation.CitationSet import CitationSet
from scholarly_citation_finder.lib.file import create_dir
from scholarly_citation_finder.apps.core.models import PublicationReference

class CitationFinder(Process):
        
    def __init__(self, database_name='mag'):
        super(CitationFinder, self).__init__('citationfinder')
        self.database = database_name
        
        # init
        self.cursor = connections[self.database].cursor()
        self.publication_set = PublicationSet(database=self.database)
        self.citation_set = CitationSet(self.publication_set)

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
            self.logger.info('set {} publications by author {}'.format(length_publication_set, author.id))
        except(ObjectDoesNotExist):
            self.logger.info('search author "{}", found nothing'.format(name))            

    def run(self, strategy):
        self.citing_papers = PublicationReference.objects.using(self.database).filter(reference__in=self.publication_set.get())
        
        if self.publication_set.is_set():
            strategy.setup(logger=self.logger,
                           database=self.database)
            output_path = create_dir(os.path.join(self.download_dir, strategy.name))
            output_filename = self.citation_set.open(filename=os.path.join(output_path, '{}.csv'.format(self.publication_set.name)))      
            self.logger.info('run strategy: {}; file: {}'.format(strategy.name, output_filename))            
            strategy.run(self.publication_set, self.citation_set, self.inspect_publications)
            self.citation_set.close()
            self.logger.info('done')  
        else:
            raise Exception('publication_search_set not set')
        
    def inspect_publications(self, publications, string=''):
        publications_citing = self.citing_papers.filter(publication__in=publications)

        self.logger.info('{}: found {} publications, {} citations'.format(string, len(publications), len(publications_citing)))
        self.citation_set.add(publications_citing, len(publications))        
