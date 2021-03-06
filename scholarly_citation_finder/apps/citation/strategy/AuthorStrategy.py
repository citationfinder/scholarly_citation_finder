#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from scholarly_citation_finder.apps.core.models import Publication
from .Strategy import Strategy

logger = logging.getLogger(__name__)


class AuthorStrategy(Strategy):
    '''
    Author search strategy.
    '''

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
        '''
        @see parent method
        '''
        authors = publication_set.get_authors(ordered=self.ordered, plus_additionals=True)
        logger.info('found {} author in the search set'.format(len(authors)))
        
        self._run_for_author(publication_set, callback, authors)
        
        if self.recursive:
            authors_level2 = []
            for author in publication_set.get_authors(ordered=self.ordered, only_additionals=True):
                if author not in authors:
                    authors_level2.append(author)
                    
            self._run_for_author(publication_set, callback, authors_level2)

    def _run_for_author(self, publication_set, callback, authors):
        logger.info('authors: {}'.format(len(authors)))
        for author in authors:
            min_year = publication_set.get_min_year() if self.min_year else None
            callback(self.__find_author_publications(author.id, min_year), 'author "{} (year>={})"'.format(author.id, min_year))

    def __find_author_publications(self, author_id, min_year=None):
        query = Publication.objects.using(self.database).filter(publicationauthoraffilation__author_id=author_id)
        if min_year:
            query = query.filter(year__gte=min_year)
        return query
