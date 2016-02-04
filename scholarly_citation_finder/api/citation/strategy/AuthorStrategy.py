#!/usr/bin/python
# -*- coding: utf-8 -*-
from ..CitationFinder import CitationFinder
from scholarly_citation_finder.apps.core.models import Author, Publication, PublicationReference

class AuthorStrategy(CitationFinder):


    def __init__(self):
        super(AuthorStrategy, self).__init__(name='author_strategy')
        
    def run(self, publication_limit=None, time_limit=None):
        super(AuthorStrategy, self).run(publication_limit=publication_limit, time_limit=time_limit)
        
        
        citing_papers = PublicationReference.objects.using(self.database_name).filter(reference__in=self.publication_search_set)


        #CitationFinder.run(self, publication_limit=publication_limit, time_limit=time_limit)
        authors = self.publication_set.get_authors()
        self.logger.info('found {} author in the search set'.format(len(authors)))
        for author in authors:
            author_publications = self.__find_author_publications(author.id)
            author_publications_citing = citing_papers.filter(publication_id__in=author_publications)
            self.logger.info('author "{}": fround {} publications, {} citations'.format(author, len(author_publications), len(author_publications_citing)))

            for publicationReference in author_publications_citing:
                if publicationReference not in self.publicationreferences_result_set:
                    self.publicationreferences_result_set.append(publicationReference)
            self.output.write_values(len(author_publications), len(self.publicationreferences_result_set))
        self.run_done()
            

    
    def __find_author_publications(self, author_id):
        #self.cursor.execute("SELECT author_id, COUNT(author_id) as num FROM core_publicationauthoraffilation LEFT JOIN publicationreference ON publicationreference.publication_id =  WHERE publication_id IN %s GROUP BY author_id ORDER BY num DESC", (publications_authors,))
        #return self.cursor.fetchall()

        #self.cursor.execute("SELECT publication_id FROM core_publicationauthoraffilation WHERE author_id = %s", (author_id,))
        #return self._sqllist2array(self.cursor.fetchall())
        return Publication.objects.using(self.database_name).filter(publicationauthoraffilation__author_id=author_id)
    
    #def __find_citations_in_authors_publications(self, publication_search_set, authors_publications):
    #    self.cursor.execute("SELECT publication_id as num FROM core_publicationreference WHERE publication_id IN "+self._array2sqllist(authors_publications)+" and reference_id IN "+self._array2sqllist(publication_search_set))
    #    return self._sqllist2array(self.cursor.fetchall())
    

#if __name__ == '__main__':
#    s = AuthorStrategy()
#    s.set_author('tom müller')
#    s.run()
