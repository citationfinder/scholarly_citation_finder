#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import json
import csv
import logging
from os.path import os

from scholarly_citation_finder.apps.core.models import PublicationReference
from scholarly_citation_finder.apps.parser.ScfjsonSerializer import ScfjsonSerializer
from .search.CitationExtractor import CitationExtractor
from .search.PublicationSet import PublicationSet

logger = logging.getLogger(__name__)


class EmptyPublicationSetException(Exception):
    pass


class NoCitationsFoundExeception(Exception):
    pass


class CitationFinder:

    def __init__(self, database='default', evaluation=False):
        self.evaluation = evaluation
        self.database = database
        self.publication_set = PublicationSet(database=self.database)
        self.citation_extractor = CitationExtractor(database=self.database)
        self.seralizer = ScfjsonSerializer(database=self.database)
        self.reset()

    def load_stored_citations(self):
        # Get already stored citations
        self.stored_citations = PublicationReference.objects.using(self.database).filter(reference__in=self.publication_set.get())
        
    def reset(self):
        self.publication_set.reset()
        self.citations = []
        self.evaluation_result = []
        
    def run(self, strategies):
        if self.publication_set.is_empty():
            raise EmptyPublicationSetException('publication_search_set is empty')

        self.reset()    
        strategies_name = '+'.join([strategy.name for strategy in strategies])
        
        for strategy in strategies:
            #logger.info('run {}'.format(strategy.name))
            strategy.setup(database=self.database)
            strategy.run(self.publication_set, self.inspect_publications)
            
        return strategies_name

    def inspect_publications(self, publications, string=''):
        # Evaluation only
        if self.evaluation:
            publications_citing = self.stored_citations.filter(publication__in=publications)
    
            # add
            for citation in publications_citing:
                if citation not in self.citations:
                    self.citations.append(citation)
                    self.publication_set.add(citation.publication_id)            
            
            # output for evaluation
            self.evaluation_result.append([len(publications), len(self.citations)])
        # Normally
        else:
            logger.info(string)
            self.citation_extractor.run(publications)
            # TODO: go on
        
    def store(self, path, filename, isi_fieldofstudy=False):
        '''
        
        :param path:
        :param filename:
        :param isi_fieldofstudy:
        :return: File name of the stored output
        :raise IOError: Problem to create or write output file
        :raise NoCitationsFoundExeception: When no citations where found
        '''
        # TODO: go on
        if not self.citations:
            self.citations = self.load_stored_citations()

        if not self.citations:
            raise NoCitationsFoundExeception('No citations found which could be stored')

        filename = os.path.join(path, '{}.json'.format(filename))
        results = []

        for publication in self.publication_set.get():
            results.append(self.seralizer.serialze(publication, self.citations.filter(reference_id=publication.id), isi_fieldofstudy=isi_fieldofstudy))
 
        with codecs.open(filename, 'w+', encoding='utf-8') as output_file: # raises IOError
            output_file.write(json.dumps(results, indent=4))
            return filename
    
    def store_evaluation(self, path, filename):
        '''
        
        :param path: File path
        :param filename: File name (without extension)
        :raise IOError: 
        :return: total number of inspected publications, total number of found citations
        '''
        filename = os.path.join(path, '{}.csv'.format(filename))
        try:
            with open(filename, 'w+') as csvfile:
                num_inspected_publications = 0
                writer = csv.writer(csvfile)
                writer.writerow(['num_inspected_publications', 'num_citations'])
                writer.writerow([0, 0])
                if len(self.evaluation_result) > 0:
                    for result in self.evaluation_result:
                        num_inspected_publications += result[0]
                        writer.writerow([num_inspected_publications, result[1]])
                    # return total number of inspected publications and total number of found citations
                    return num_inspected_publications, self.evaluation_result[-1][1]
                else:
                    return 0, 0
        except(IOError) as e:
            raise e
