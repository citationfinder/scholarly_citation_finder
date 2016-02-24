
#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import json

from scholarly_citation_finder.api.citation.PublicationSet import PublicationSet
from scholarly_citation_finder.apps.core.models import PublicationReference


class EmptyPublicationSetException(Exception):
    pass


class CitationFinder:

    # PublicationReference
    citations = []
    evaluation_result = []

    def __init__(self, database_name='mag', evaluation=False):
        self.evaluation = evaluation
        self.database = database_name
        self.publication_set = PublicationSet(database=self.database)

    def hack(self):
        # <----- remove
        self.citing_papers = PublicationReference.objects.using(self.database).filter(reference__in=self.publication_set.get())
        
    def reset(self):
        self.publication_set.additional_publications_idstring = ''
        self.citations = []
        self.evaluation_result = []
        
    def run(self, strategies):
        if self.publication_set.is_empty():
            raise EmptyPublicationSetException('publication_search_set not set')

        self.reset()    
        strategies_name = '+'.join([strategy.name for strategy in strategies])
        
        for strategy in strategies:
            #self.logger.info('run {}'.format(strategy.name))
            strategy.setup(logger=self.logger, database=self.database)
            strategy.run(self.publication_set, self.inspect_publications)
            
        return strategies_name, self.evaluation_result

    def inspect_publications(self, publications, string=''):
        # <----- remove
        publications_citing = self.citing_papers.filter(publication__in=publications)

        #self.logger.info('{}: found {} publications, {} citations'.format(string, len(publications), len(publications_citing)))
        # add
        for citation in publications_citing:
            if citation not in self.citations:
                self.citations.append(citation)
                self.publication_set.add(citation.publication_id)        
        
        # output
        if self.evaluation:
            self.evaluation_result.append([len(publications), len(self.citations)])
        
    def store(self, filename):
        results = []
        for publication in self.publication_set.get():
            results.append(self.__serialze(publication, self.citations.filter(reference_id=publication.id)))

        with codecs.open(filename, 'w+', encoding='utf-8') as output_file:
            output_file.write(json.dumps(results, indent=4))

    def __serialze(self, publication, citations=None):
        result = {'type': 'article',
                'title': publication.title,
                'journal_name': 'journal of example',
                'year': publication.year,
                'authors': ["A B", "B C"],
                'citations': []}
        if citations:
            for citation in citations:
                result['citations'].append(self.__serialze(citation.publication))
        
        return result
