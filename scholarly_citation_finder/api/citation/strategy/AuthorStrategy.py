#!/usr/bin/python
# -*- coding: utf-8 -*-
from scholarly_citation_finder.apps.core.models import Publication
from scholarly_citation_finder.api.citation.strategy.Strategy import Strategy
from scholarly_citation_finder.api.citation.PublicationSet import PublicationSet

class AuthorStrategy(Strategy):

    ordered = None
    min_year = None
    recursive = None

    def __init__(self, ordered=False, recursive=False, min_year=False):
        name = 'author'
        if ordered:
            name += '-ordered'
        if min_year:
            name += '-minyear'
        if recursive:
            name += '-recursive'            
        super(AuthorStrategy, self).__init__(name=name)
        self.ordered = ordered
        self.min_year = min_year
        self.recursive = recursive
        
    def run(self, publication_set, callback):
        authors = publication_set.get_authors(ordered=self.ordered)
        self.logger.info('found {} author in the search set'.format(len(authors)))
        
        self._run_for_author(publication_set, callback, authors)
        
        if self.recursive:
            authors_level2 = []
            for author in publication_set.get_authors(ordered=self.ordered, only_additionals=True):
                if author not in authors:
                    authors_level2.append(author)
                    
            self._run_for_author(publication_set, callback, authors_level2)

    def _run_for_author(self, publication_set, callback, authors):
        self.logger.info('authors: {}'.format(len(authors)))
        for author in authors:
            min_year = publication_set.get_min_year() if self.min_year else None
            callback(self.__find_author_publications(author.id, min_year), 'author "{} (year>={})"'.format(author.id, min_year))

    def __find_author_publications(self, author_id, min_year=None):
        #self.cursor.execute("SELECT author_id, COUNT(author_id) as num FROM core_publicationauthoraffilation LEFT JOIN publicationreference ON publicationreference.publication_id =  WHERE publication_id IN %s GROUP BY author_id ORDER BY num DESC", (publications_authors,))
        #return self.cursor.fetchall()

        #self.cursor.execute("SELECT publication_id FROM core_publicationauthoraffilation WHERE author_id = %s", (author_id,))
        #return self._sqllist2array(self.cursor.fetchall())
        query = Publication.objects.using(self.database).filter(publicationauthoraffilation__author_id=author_id)
        if min_year:
            query = query.filter(year__gte=min_year)
        return query