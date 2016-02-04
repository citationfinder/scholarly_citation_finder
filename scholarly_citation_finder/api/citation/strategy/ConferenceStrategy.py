#!/usr/bin/python
# -*- coding: utf-8 -*-
from ..CitationFinder import CitationFinder
from scholarly_citation_finder.apps.core.models import Conference, Publication,\
    PublicationReference

class ConferenceStrategy(CitationFinder):


    def __init__(self):
        super(ConferenceStrategy, self).__init__(name='conference_strategy')
        
    def run(self, publication_limit=None, time_limit=None):
        CitationFinder.run(self, publication_limit=publication_limit, time_limit=time_limit)

        citing_papers = PublicationReference.objects.using(self.database_name).filter(reference__in=self.publication_search_set)
        
    
        conferences = self.publication_set.get_conferences()
        self.logger.info('found {} conferences in search set'.format(len(conferences)))
        for conference in conferences:
            conference_publications = self.__find_conference_publications(conference.id)            
            conference_publications_citing = citing_papers.filter(publication__in=conference_publications)
            self.logger.info('conference "{}": found {} publications, {} citations'.format(conference, len(conference_publications), len(conference_publications_citing)))
            
            for publicationReference in conference_publications_citing:
                if publicationReference not in self.publicationreferences_result_set:
                    self.publicationreferences_result_set.append(publicationReference)
            self.output.write_values(len(conference_publications), len(self.publicationreferences_result_set))
        self.run_done()
        
    
    def __find_conference_publications(self, conference_id):
        return Publication.objects.using(self.database_name).filter(conference_id=conference_id)
