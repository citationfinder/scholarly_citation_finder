#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from django.db.models import Min

from scholarly_citation_finder.apps.core.models import Author, Publication, Conference, Journal, FieldOfStudy

logger = logging.getLogger(__name__)


class EmptyIdstringException(Exception):
    pass


class PublicationSet:
    '''
    Set of publications.
    '''

    def __init__(self, database='default'):
        '''
        Create object.
        
        :param database: Database name
        '''
        self.database = database
        
        self.publications = []
        self.publications_idstring = ''
        self.additional_publications_idstring = ''
        self.min_year = None

    def __len__(self):
        '''
        Get length of the set.
        '''
        return len(self.publications)

    def is_empty(self):
        '''
        Check, if set is empty.
        '''
        return not self.publications
    
    def reset(self):
        '''
        Reset set.
        '''
        self.additional_publications_idstring = ''
    
    def set(self, publications):
        '''
        Set the set ;-)

        :param publications: List of publications
        '''
        self.publications = publications
        self.publications_idstring = ','.join([str(publication.id) for publication in self.publications])
        return len(self.publications)

    def set_by_author(self, name=None, id=None):
        '''
        Create set by author.
        
        :param name: Name of the author
        :param id: ID of the author
        :return: Author ID, number of publications
        :raise: ObjectDoesNotExist
        :raise: MultipleObjectsReturned
        '''
        query = Author.objects.using(self.database)
        if id:
            author = query.get(id=id)
        else:
            author = query.get(name=name)
                
        #author_publication = PublicationAuthorAffilation.objects.using(self.database).filter(author=author)
        #Publication.objects.using(self.database).filter()
        num_publications = self.set(Publication.objects.using(self.database).filter(publicationauthoraffilation__author=author))
        return author.id, num_publications

    def set_by_conference(self, name=None, id=None):
        '''
        Create set by conference.
        
        :param name:
        :param id:
        :return: Conference ID, number of publications
        :raise: ObjectDoesNotExist
        :raise: MultipleObjectsReturned
        '''
        query = Conference.objects.using(self.database)
        if id:
            conference = query.get(id=id)
        else:
            conference = query.get(name=name)
        num_publications = self.set(Publication.objects.using(self.database).filter(conference=conference))
        return conference.id, num_publications

    def set_by_journal(self, name=None, id=None):
        '''
        Create set by joural.
        
        :param name:
        :param id:
        :return: Journal ID, number of publications
        :raise: ObjectDoesNotExist
        :raise: MultipleObjectsReturned
        '''
        query = Journal.objects.using(self.database)
        if id:
            journal = query.get(id=id)
        else:
            journal = query.get(name=name)
        num_publications = self.set(Publication.objects.using(self.database).filter(journal=journal))
        return journal.id, num_publications
    
    def add(self, publication_id):
        '''
        Add a additional publication.
        
        :param publication_id: Publication ID
        '''
        if not self.publications.filter(id=publication_id):
            #self.additional_publications.append(publication)
            self.additional_publications_idstring += ',' + str(publication_id)

    def get(self):
        '''
        Get the set.
        '''
        return self.publications

    def get_min_year(self):
        '''
        Get the minimum publication year.
        '''
        return self.min_year if self.min_year else self.publications.aggregate(Min('year'))['year__min']

    def get_authors(self, ordered=False, only_additionals=False, plus_additionals=False):
        '''
        Find all authors (precise author IDs) of the given publication search set.
        
        :param ordered: Descending order 
        :param only_additionals: Only use additional publications
        :param plus_additionals: Include additional publications
        :return: Array of author IDs ordered descending by frequency
        '''
        if ordered:
            try:
                return list(Author.objects.using(self.database).raw("SELECT author_id AS id FROM core_publicationauthoraffilation WHERE publication_id IN ("+self.__get_idstring(only_additionals=only_additionals, plus_additionals=plus_additionals)+") GROUP BY author_id ORDER BY COUNT(author_id) DESC"))
            except(EmptyIdstringException):
                return []
        else:
            return Author.objects.using(self.database).filter(publicationauthoraffilation__publication__in=self.publications).distinct()
        
    def get_conferences(self, ordered=False, plus_additionals=False):
        '''
        Get all conferences in set.
        
        :param ordered: Descending order 
        :param plus_additionals: Include additional publications
        '''
        if ordered:
            return list(Conference.objects.using(self.database).raw("SELECT conference_id AS id FROM core_publication WHERE conference_id IS NOT NULL AND id IN ("+self.__get_idstring(plus_additionals=plus_additionals)+") GROUP BY conference_id ORDER BY COUNT(conference_id) DESC"))
        else:
            return Conference.objects.using(self.database).filter(publication__in=self.publications).distinct()

    def get_journals(self, ordered=False, plus_additionals=False):
        '''
        Find all journals (precise journal IDs) of the given publication search set.
        
        :param ordered: Descending order 
        :param plus_additionals: Include additional publications
        :return: Array of journal IDs ordered descending by frequency
        '''
        if ordered:
            return list(Journal.objects.using(self.database).raw("SELECT journal_id AS id FROM core_publication WHERE journal_id IS NOT NULL AND id IN ("+self.__get_idstring(plus_additionals=plus_additionals)+") GROUP BY journal_id ORDER BY COUNT(journal_id) DESC"))
        else:
            return Journal.objects.using(self.database).filter(publication__in=self.publications).distinct()
    
    def get_fieldofstudies(self, ordered=False, plus_additionals=False):
        '''
        Get all field of studies. 
        
        :param ordered: Descending order 
        :param plus_additionals: Include additional publications
        '''
        if ordered:
            query = "SELECT fieldofstudy_id AS id FROM core_publicationkeyword WHERE publication_id IN ("+self.__get_idstring(plus_additionals=plus_additionals)+") GROUP BY fieldofstudy_id ORDER BY COUNT(fieldofstudy_id) DESC"
            return list(FieldOfStudy.objects.using(self.database).raw(query))
        else:
            return FieldOfStudy.objects.using(self.database).filter(publicationkeyword__publication__in=self.publications).distinct()
    
    def __get_idstring(self, only_additionals=False, plus_additionals=False):
            if plus_additionals:
                idstring = self.publications_idstring + self.additional_publications_idstring
            elif only_additionals:
                idstring = self.additional_publications_idstring[1:]
            else:
                idstring = self.publications_idstring
            
            if idstring:
                return idstring
            else:
                raise EmptyIdstringException('ID-String is empty')
