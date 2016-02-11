#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.apps.core.models import Publication
from scholarly_citation_finder.api.citation.strategy.Strategy import Strategy

class ConferenceStrategy(Strategy):


    def __init__(self, ordered=False):
        name = 'conference'
        if ordered:
            name += '-ordered'
        super(ConferenceStrategy, self).__init__(name=name)
        self.ordered = ordered
        
    def run(self, publication_set, _, callback):
        conferences = publication_set.get_conferences(ordered=self.ordered)
        self.logger.info('found {} conferences in search set'.format(len(conferences)))
        for conference in conferences:
            conference_publications = self.__find_conference_publications(conference.id)
            callback(conference_publications, 'conference "{}"'.format(conference))

    def __find_conference_publications(self, conference_id):
        return Publication.objects.using(self.database).filter(conference_id=conference_id)
