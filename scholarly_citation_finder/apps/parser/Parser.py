#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from django.db import connections
from django.db.utils import IntegrityError, DataError, ProgrammingError

from .AuthorParser import AuthorParser
from .Exceptions import ParserRollbackError, ParserDataError
from scholarly_citation_finder.lib.string import normalize_string

logger = logging.getLogger(__name__)


class Parser:

    PUBLICATION_ATTRIBUTES = [
        'type',
        'title',
        'date',
        'booktitle'
        #'journal',
        'volume',
        'number',
        'pages_from',
        'pages_to',
        'series',
        'publisher',
        'isbn',
        'doi',
        'abstract',
        'copyright'
    ]

    def __init__(self, database):
        self.conn = connections[database]
        self.cursor = self.conn.cursor()
        self.count_publications = 0
        self.author_parser = AuthorParser(database=database)

    def commit(self):
        '''
        :raise ParserRollbackError When a problems occurred, that required to do a rollback
        '''
        try:
            logger.info('commit')
            self.conn.commit()
        except(IntegrityError) as e:
            logger.error(e, exc_info=True)
            self.conn.rollback()
            raise ParserRollbackError(e)

    def parse_author(self, name):
        '''
        If the author with the given name already exists, the ID of that author is returned.
        Otherwise a new author gets created.
        
        :param name: Name of the author
        :return: ID of the author
        :raise ParserDataError: When the name is too long
        '''
        name = normalize_string(name)
        self.cursor.execute("SELECT id FROM core_author WHERE name LIKE %s LIMIT 1", [name])
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            if name and len(name) <= 100:
                self.cursor.execute("INSERT INTO core_author (name) VALUES (%s) RETURNING id", [name])
                return self.cursor.fetchone()[0]
            else:
                raise ParserDataError('Author name is too long')

    def parse_journal(self, name):
        '''
        If the journal with the given name already exists, the ID of that journal is returned.
        Otherwise a new journel gets created.
        
        :param name: Name of the journal
        :return: ID of the journal
        :raise ParserDataError: When the name is too long
        '''
        name = normalize_string(name)
        self.cursor.execute("SELECT id FROM core_journal WHERE name LIKE %s LIMIT 1", [name])
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            if name and len(name) <= 250:
                self.cursor.execute("INSERT INTO core_journal (name) VALUES (%s) RETURNING id", [name])
                return self.cursor.fetchone()[0]
            else:
                raise ParserDataError('Journal name is too long')

    def parse_conference(self, short_name):
        short_name = normalize_string(short_name)
        self.cursor.execute("SELECT id FROM core_conference WHERE short_name LIKE %s LIMIT 1", [short_name])
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            if short_name and len(short_name) <= 20:
                self.cursor.execute("INSERT INTO core_conference (short_name) VALUES (%s) RETURNING id", [short_name])
                return self.cursor.fetchone()[0]
            else:
                raise ParserDataError('Conference short name is too long: %s' % short_name)        

    def parse_publication(self, type=None, title=None, year=None, date=None, booktitle=None, journal_id=None, volume=None, number=None, pages_from=None, pages_to=None, series=None, publisher=None, isbn=None, doi=None, abstract=None, copyright=None, conference_id=None, source=None):
        if title and len(title) <= 250:
            title = normalize_string(title)
            
            self.cursor.execute("SELECT id FROM core_publication WHERE title LIKE %s LIMIT 1", [title])
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                if date and len(date) > 50:
                    date = None
                if booktitle and len(booktitle) > 200:
                    booktitle = None
                if volume and len(volume) > 20:
                    volume = None
                if number and len(number) > 20:
                    number = None
                if pages_from and len(pages_from) > 5:
                    pages_from = None
                if pages_to and len(pages_to) > 5:
                    pages_to = None
                if series and len(series) > 200:
                    series = None
                if publisher and len(publisher) > 150:
                    publisher = None
                if isbn and len(isbn) > 50:
                    isbn = None
                if doi and len(doi) > 50:
                    doi = None
                self.cursor.execute("INSERT INTO core_publication (type, title, year, date, booktitle, journal_id, volume, number, pages_from, pages_to, series, publisher, isbn, doi, abstract, copyright, conference_id, source) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id", [type, title, year, date, booktitle, journal_id, volume, number, pages_from, pages_to, series, publisher, isbn, doi, abstract, copyright, conference_id, source])
                return self.cursor.fetchone()[0]
        else:
            raise ParserDataError('Title does not exists or is too long')

    def parse_reference(self, publication_id, reference_id, context=None, source_id=None):
        if publication_id and reference_id:
            self.cursor.execute("INSERT INTO core_publicationreference (publication_id, reference_id, context, source_id) VALUES (%s, %s, %s, %s)", [publication_id, reference_id, context, source_id])
        else:
            raise ParserDataError('publication_id or reference_id does not exists')

    def parse(self, publication, conference_short_name=None, journal_name=None, authors=None, keywords=None, urls=None, reference=None):
        '''
        
        :param publication: Publication dictionary
        :param conference_short_name: Conference short name
        :param journal_name: Journal name
        :param authors: Authors name array
        :param keywords: Keywords array
        :param urls: URL array
        :param reference: Reference dictionary
        :return: Publication ID, if entry was successfully parsed; False otherwise
        :raise ParserRollbackError: When a problems occurred, that required to do a rollback
        '''
        
        self.count_publications += 1
        try:
            
            conference_id = None
            journal_id = None

            # conference
            if conference_short_name:
                try:
                    conference_id = self.parse_conference(conference_short_name)
                except(ParserDataError) as e:
                    logger.warn(str(e))
                del conference_short_name
            # journal
            if journal_name:
                try:
                    journal_id = self.parse_journal(journal_name)
                except(ParserDataError) as e:
                    logger.warn(str(e))
                del journal_name
            # publication
            publication_id = self.parse_publication(conference_id=conference_id,
                                                    journal_id=journal_id,
                                                    **publication)
            # authors
            if authors:
                for author in authors:
                    try:
                        self.cursor.execute("INSERT INTO core_publicationauthoraffilation (publication_id, author_id) VALUES (%s, %s)", [publication_id, self.author_parser.parse(author)])
                    except(ParserDataError, DataError) as e:
                        logger.warn(str(e))
                del authors
            # keywords
            if keywords:
                for keyword in keywords:
                    if keyword and len(keyword) <= 100:
                        keyword = normalize_string(keyword)
                        self.cursor.execute("INSERT INTO core_publicationkeyword (publication_id, name) VALUES (%s, %s)", [publication_id, keyword])
                del keywords
            # urls
            if urls:
                for url in urls:
                    url_type = None
                    if isinstance(url, dict):
                        url_type = url['type']
                        url = url['value']
                        
                    if url and len(url) <= 200:
                        if url_type and len(url_type) >= 30:
                            url_type = None
                        self.cursor.execute("INSERT INTO core_publicationurl (publication_id, url, type) VALUES (%s, %s, %s)", [publication_id, url, url_type])
                del urls
            # reference
            if reference:
                try:
                    self.parse_reference(reference_id=publication_id, **reference)
                except(ParserDataError) as e:
                    logger.warn(str(e))
                del reference

            return publication_id
        except(ParserDataError) as e:
            #logger.warn(str(e))
            return False
        except(ProgrammingError, DataError) as e:
            logger.error(e, exc_info=True)
            self.conn.rollback()
            raise ParserRollbackError(str(e))
