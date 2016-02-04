#!/usr/bin/python
# -*- coding: utf-8 -*-
from ..CitationFinder import CitationFinder
from scholarly_citation_finder.apps.core.models import Journal, Publication,\
    PublicationReference

class JournalStrategy(CitationFinder):


    def __init__(self):
        super(JournalStrategy, self).__init__(name='journal_strategy')
        
    def run(self, publication_limit=None, time_limit=None):
        CitationFinder.run(self, publication_limit=publication_limit, time_limit=time_limit)

        citing_papers = PublicationReference.objects.using(self.database_name).filter(reference__in=self.publication_search_set)
        
    
        journals = self.publication_set.get_journals()
        self.logger.info('found {} journals in search set'.format(len(journals)))
        for journal in journals:
            journal_publications = self.__find_journal_publications(journal.id)            
            journal_publications_citing = citing_papers.filter(publication__in=journal_publications)
            self.logger.info('journal "{}": found {} publications, {} citations'.format(journal, len(journal_publications), len(journal_publications_citing)))
            
            for publicationReference in journal_publications_citing:
                if publicationReference not in self.publicationreferences_result_set:
                    self.publicationreferences_result_set.append(publicationReference)
            self.output.write_values(len(journal_publications), len(self.publicationreferences_result_set))
        self.run_done()
        
    def __find_journal_publications(self, journal_id):
        #self.cursor.execute("SELECT publication_id FROM core_publication WHERE journal_id IN "+self._array2sqllist(journal_ids))
        #return self._sqllist2array(self.cursor.fetchall())
        return Publication.objects.using(self.database_name).filter(journal_id=journal_id)
    
    def __find_journals_citation(self, journal_publications):
        
        #self.cursor.execute("SELECT publication_id as num FROM core_publicationreference WHERE publication_id IN "+self._array2sqllist(authors_publications)+" and reference_id IN "+self._array2sqllist(publication_search_set))
        #return self._sqllist2array(self.cursor.fetchall())
        pass
    
#if __name__ == '__main__':
#    s = JournalStrategy()
#    s.set_author('tom müller')
#    s.run()