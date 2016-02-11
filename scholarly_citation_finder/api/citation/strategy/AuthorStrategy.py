#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.apps.core.models import Publication
from scholarly_citation_finder.api.citation.strategy.Strategy import Strategy
from scholarly_citation_finder.api.citation.PublicationSet import PublicationSet

class AuthorStrategy(Strategy):

    ordered = None
    recursive = None

    def __init__(self, ordered=False, recursive=False):
        name = 'author'
        if ordered:
            name += '-ordered'
        if recursive:
            name += '-recursive'            
        super(AuthorStrategy, self).__init__(name=name)
        self.ordered = ordered
        self.recursive = recursive
        
    def run(self, publication_set, _, callback):
        authors = publication_set.get_authors(ordered=self.ordered)
        self.logger.info('found {} author in the search set'.format(len(authors)))
        
        self._run_for_author(publication_set, callback, authors)
        
        if self.recursive:
            
            #citation_set_publications = PublicationSet()
            #citation_set_publications.publications_idstring = ','.join([str(citation.publication_id) for citation in citation_set.get()])
            #self.logger.warn(citation_set_publications.publications_idstring)
            authors_level2 = []
            for author in publication_set.get_authors(ordered=True, only_additionals=True):
                if author not in authors:
                    authors_level2.append(author)
                    
            self._run_for_author(publication_set, callback, authors_level2)

    def _run_for_author(self, publication_set, callback, authors):
        self.logger.info('authors: {}'.format(len(authors)))
        for author in authors:
            author_publications = self.__find_author_publications(author.id)
            callback(author_publications, 'author "{}"'.format(author.id))

    def __find_author_publications(self, author_id):
        #self.cursor.execute("SELECT author_id, COUNT(author_id) as num FROM core_publicationauthoraffilation LEFT JOIN publicationreference ON publicationreference.publication_id =  WHERE publication_id IN %s GROUP BY author_id ORDER BY num DESC", (publications_authors,))
        #return self.cursor.fetchall()

        #self.cursor.execute("SELECT publication_id FROM core_publicationauthoraffilation WHERE author_id = %s", (author_id,))
        #return self._sqllist2array(self.cursor.fetchall())
        return Publication.objects.using(self.database).filter(publicationauthoraffilation__author_id=author_id)
    
    #def __find_citations_in_authors_publications(self, publication_search_set, authors_publications):
    #    self.cursor.execute("SELECT publication_id as num FROM core_publicationreference WHERE publication_id IN "+self._array2sqllist(authors_publications)+" and reference_id IN "+self._array2sqllist(publication_search_set))
    #    return self._sqllist2array(self.cursor.fetchall())
