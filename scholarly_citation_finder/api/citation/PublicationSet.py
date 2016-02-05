#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Min

from scholarly_citation_finder.apps.core.models import Author, Publication, PublicationReference,\
    Conference, Journal, FieldOfStudy


class PublicationSet:
    
    publications = None
    name = None
    publications_idstring = ''
    
    min_year = None

    def __init__(self, database='mag'):
        self.database = database

    def is_set(self):
        return self.publications is not None
    
    def set(self, publications, name):
        self.publications = publications
        self.name = name
        self.publications_idstring = ','.join([str(publication.id) for publication in self.publications])
        return len(self.publications)

    def set_by_author(self, name=None, id=None):
        '''
        
        :param name: Name of the author
        :param id: ID of the author
        :return: Author, if author was found in database otherwise False
        '''
        try:
            query = Author.objects.using(self.database)
            if id:
                author = query.get(id=id)
            else:
                author = query.get(name=name)
                
            #author_publication = PublicationAuthorAffilation.objects.using(self.database).filter(author=author)
            #Publication.objects.using(self.database).filter()
            num_publications = self.set(publications=Publication.objects.using(self.database).filter(publicationauthoraffilation__author=author),
                                        name=author.id)
            return (author, num_publications)
        except(ObjectDoesNotExist) as e:
            raise e
            
        """    
        self.cursor.execute("SELECT id FROM core_author WHERE name LIKE %s LIMIT 1", (name,))
        result = self.cursor.fetchone()
        
        if result:
            id = result[0]
            self._open_output_file(id)
            self.logger.info('search author "{}", found author id: {}'.format(name, id))
            self.cursor.execute("SELECT publication_id FROM core_publicationauthoraffilation WHERE author_id = %s", (id,))
            self.set_publication_search_set(self._sqllist2array(self.cursor.fetchall()))
            return True
        else:
            self.logger.info('search author "{}", found nothing'.format(name))
        return False     
        """    

    def set_by_journal(self, name=None, id=None):
        pass

    def get(self):
        return self.publications

    def get_min_year(self):
        return self.min_year if self.min_year else self.publications.aggregate(Min('year'))['year__min']

    def get_authors(self, ordered=False):
        '''
        Find all authors (precise author IDs) of the given publication search set.
        
        :param publications_ids:
        :return: Array of author IDs ordered descending by frequency
        '''
        if ordered:
            return list(Author.objects.using(self.database).raw("SELECT author_id AS id FROM core_publicationauthoraffilation WHERE publication_id IN ("+self.publications_idstring+") GROUP BY author_id ORDER BY COUNT(author_id) DESC"))
        else:
            return Author.objects.using(self.database).filter(publicationauthoraffilation__publication__in=self.publications).distinct()
        
    def get_conferences(self, ordered=False):
        if ordered:
            return list(Conference.objects.using(self.database).raw("SELECT conference_id AS id FROM core_publication WHERE conference_id IS NOT NULL AND id IN ("+self.publications_idstring+") GROUP BY conference_id ORDER BY COUNT(conference_id) DESC"))
        else:
            return Conference.objects.using(self.database).filter(publication__in=self.publications).distinct()

    def get_journals(self, ordered=False):
        '''
        Find all journals (precise journal IDs) of the given publication search set.
        
        :param publications_ids:
        :return: Array of journal IDs ordered descending by frequency
        '''
        if ordered:
            return list(Journal.objects.using(self.database).raw("SELECT journal_id AS id FROM core_publication WHERE journal_id IS NOT NULL AND id IN ("+self.publications_idstring+") GROUP BY journal_id ORDER BY COUNT(journal_id) DESC"))
        else:
            return Journal.objects.using(self.database).filter(publication__in=self.publications).distinct()
    
    def get_fieldofstudies(self, ordered=False):
        if ordered:
            return list(FieldOfStudy.objects.using(self.database).raw("SELECT fieldofstudy_id AS id FROM core_publicationkeyword WHERE publication_id IN ("+self.publications_idstring+") GROUP BY fieldofstudy_id ORDER BY COUNT(fieldofstudy_id) DESC"))
        else:
            return FieldOfStudy.objects.using(self.database).filter(publicationkeyword__publication__in=self.publications).distinct()
    
