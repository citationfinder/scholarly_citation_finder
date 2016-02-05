#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.apps.core.models import Publication, PublicationReference
from scholarly_citation_finder.api.citation.strategy.Strategy import Strategy

class JournalStrategy(Strategy):


    def __init__(self, ordered=False):
        name = 'journal'
        if ordered:
            name += '-ordered'
        super(JournalStrategy, self).__init__(name=name)
        self.ordered = ordered
        
    def run(self, publication_set, citation_set):
        citing_papers = PublicationReference.objects.using(self.database).filter(reference__in=publication_set.get())
        
    
        journals = publication_set.get_journals(ordered=self.ordered)
        self.logger.info('found {} journals in search set'.format(len(journals)))
        for journal in journals:
            journal_publications = self.__find_journal_publications(journal.id)            
            journal_publications_citing = citing_papers.filter(publication__in=journal_publications)
            self.logger.info('journal "{}": found {} publications, {} citations'.format(journal.id, len(journal_publications), len(journal_publications_citing)))
            
            citation_set.add(journal_publications_citing, len(journal_publications))
        
    def __find_journal_publications(self, journal_id):
        #self.cursor.execute("SELECT publication_id FROM core_publication WHERE journal_id IN "+self._array2sqllist(journal_ids))
        #return self._sqllist2array(self.cursor.fetchall())
        return Publication.objects.using(self.database).filter(journal_id=journal_id)
    
    def __find_journals_citation(self, journal_publications):
        
        #self.cursor.execute("SELECT publication_id as num FROM core_publicationreference WHERE publication_id IN "+self._array2sqllist(authors_publications)+" and reference_id IN "+self._array2sqllist(publication_set))
        #return self._sqllist2array(self.cursor.fetchall())
        pass
