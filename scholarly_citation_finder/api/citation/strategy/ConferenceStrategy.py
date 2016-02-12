#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.apps.core.models import Publication
from scholarly_citation_finder.api.citation.strategy.Strategy import Strategy

class ConferenceStrategy(Strategy):

    ordered = None
    min_year = None

    def __init__(self, ordered=False, min_year=False):
        name = 'conference'
        if ordered:
            name += '-ordered'
        if min_year:
            name += '-minyear'
        super(ConferenceStrategy, self).__init__(name=name)
        self.ordered = ordered
        self.min_year = min_year
        
    def run(self, publication_set, callback):
        conferences = publication_set.get_conferences(ordered=self.ordered)
        self.logger.info('found {} conferences in search set'.format(len(conferences)))
        for conference in conferences:
            conference_publications = self.__find_conference_publications(conference.id)
            callback(conference_publications, 'conference "{}"'.format(conference))

    def __find_conference_publications(self, conference_id, min_year=None):
        query = Publication.objects.using(self.database).filter(conference_id=conference_id)
        if min_year:
            query = query.filter(year__gte=min_year)
        return query