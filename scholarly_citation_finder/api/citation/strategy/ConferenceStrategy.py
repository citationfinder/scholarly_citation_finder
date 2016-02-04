#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.apps.core.models import Publication, PublicationReference
from scholarly_citation_finder.api.citation.strategy.Strategy import Strategy

class ConferenceStrategy(Strategy):


    def __init__(self):
        super(ConferenceStrategy, self).__init__(name='conference')
        
    def run(self, publication_set, citation_set):
        citing_papers = PublicationReference.objects.using(self.database).filter(reference__in=publication_set.get())
        
    
        conferences = publication_set.get_conferences()
        self.logger.info('found {} conferences in search set'.format(len(conferences)))
        for conference in conferences:
            conference_publications = self.__find_conference_publications(conference.id)            
            conference_publications_citing = citing_papers.filter(publication__in=conference_publications)
            self.logger.info('conference "{}": found {} publications, {} citations'.format(conference, len(conference_publications), len(conference_publications_citing)))
            
            citation_set.add(conference_publications_citing, len(conference_publications))        
    
    def __find_conference_publications(self, conference_id):
        return Publication.objects.using(self.database).filter(conference_id=conference_id)
