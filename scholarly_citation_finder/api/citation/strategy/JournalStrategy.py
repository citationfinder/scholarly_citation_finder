#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.apps.core.models import Publication
from scholarly_citation_finder.api.citation.strategy.Strategy import Strategy

class JournalStrategy(Strategy):


    def __init__(self, ordered=False, min_year=False):
        name = 'journal'
        if ordered:
            name += '-ordered'
        if min_year:
            name += '-minyear'
        super(JournalStrategy, self).__init__(name=name)
        self.ordered = ordered
        self.min_year = min_year
        
    def run(self, publication_set, _, callback):
        journals = publication_set.get_journals(ordered=self.ordered)
        self.logger.info('found {} journals in search set'.format(len(journals)))
        for journal in journals:
            min_year = publication_set.get_min_year() if self.min_year else None
            callback(self.__find_journal_publications(journal.id, min_year), 'journal "{}" (year>={})'.format(journal.id, min_year))
        
    def __find_journal_publications(self, journal_id, min_year=None):
        query = Publication.objects.using(self.database).filter(journal_id=journal_id)
        if min_year:
            query = query.filter(year__gte=min_year)
        return query
