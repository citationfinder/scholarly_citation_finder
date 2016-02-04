#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.apps.core.models import Publication, PublicationReference
from scholarly_citation_finder.api.citation.strategy.Strategy import Strategy

class AuthorStrategy(Strategy):


    def __init__(self, ordered=False):
        name = 'author'
        if ordered:
            name += '_ordered'
        super(AuthorStrategy, self).__init__(name=name)
        self.ordered = ordered
        
    def run(self, publication_set, citation_set):        
        citing_papers = PublicationReference.objects.using(self.database).filter(reference__in=publication_set.get())


        authors = publication_set.get_authors(ordered=self.ordered)
        self.logger.info('found {} author in the search set'.format(len(authors)))
        for author in authors:
            author_publications = self.__find_author_publications(author.id)
            author_publications_citing = citing_papers.filter(publication_id__in=author_publications)
            self.logger.info('author "{}": found {} publications, {} citations'.format(author.id, len(author_publications), len(author_publications_citing)))

            citation_set.add(author_publications_citing)         
    
    def __find_author_publications(self, author_id):
        #self.cursor.execute("SELECT author_id, COUNT(author_id) as num FROM core_publicationauthoraffilation LEFT JOIN publicationreference ON publicationreference.publication_id =  WHERE publication_id IN %s GROUP BY author_id ORDER BY num DESC", (publications_authors,))
        #return self.cursor.fetchall()

        #self.cursor.execute("SELECT publication_id FROM core_publicationauthoraffilation WHERE author_id = %s", (author_id,))
        #return self._sqllist2array(self.cursor.fetchall())
        return Publication.objects.using(self.database).filter(publicationauthoraffilation__author_id=author_id)
    
    #def __find_citations_in_authors_publications(self, publication_search_set, authors_publications):
    #    self.cursor.execute("SELECT publication_id as num FROM core_publicationreference WHERE publication_id IN "+self._array2sqllist(authors_publications)+" and reference_id IN "+self._array2sqllist(publication_search_set))
    #    return self._sqllist2array(self.cursor.fetchall())
