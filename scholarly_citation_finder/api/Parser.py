#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from django.db import connections
from django.db.utils import IntegrityError, DataError, ProgrammingError

logger = logging.getLogger(__name__)


class ParserDataError(Exception):
    pass


class ParserRollbackError(Exception):
    pass


class ParserConnectionError(Exception):
    pass


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
        #self.count_citations = 0

    #def parse_publication_reference(self, context=None, type=None, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, arxiv_id=None, extractor=None, source=None):
    #    self.count_citations += 1
    #    
    #    self.xml_writer.write_start_tag('reference')
    #    self.xml_writer.write_element('context', context, is_cdata=True)
    #    self.parse_publication(type, title, authors, date, booktitle, journal, volume, number, pages, publisher, abstract, doi, citeseerx_id, dblp_id, arxiv_id, extractor, source)
    #    self.xml_writer.write_close_tag('reference')

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
            raise ParserRollbackError

    def __normalize_string(self, value):
        return value.strip().lower()

    def parse_author(self, name):
        '''
        If the author with the given name already exists, the ID of that author is returned.
        Otherwise a new author gets created.
        
        :param name: Name of the author
        :return: ID of the author
        :raise ParserDataError: When the name is too long
        '''
        self.cursor.execute("SELECT id FROM core_author WHERE name = %s LIMIT 1", [name])
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            if name and len(name) <= 100:
                name = self.__normalize_string(name)
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
        self.cursor.execute("SELECT id FROM core_journal WHERE name = %s LIMIT 1", [name])
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            if name and len(name) <= 250:
                name = self.__normalize_string(name)
                self.cursor.execute("INSERT INTO core_journal (name) VALUES (%s) RETURNING id", [name])
                return self.cursor.fetchone()[0]
            else:
                raise ParserDataError('Journal name is too long')

    def parse_conference(self, short_name):
        self.cursor.execute("SELECT id FROM core_conference WHERE short_name = %s LIMIT 1", [short_name])
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            if short_name and len(short_name) <= 20:
                short_name = self.__normalize_string(short_name)
                self.cursor.execute("INSERT INTO core_conference (short_name) VALUES (%s) RETURNING id", [short_name])
                return self.cursor.fetchone()[0]
            else:
                raise ParserDataError('Conference short name is too long')        

    def parse_publication(self, type=None, title=None, year=None, date=None, booktitle=None, journal_id=None, volume=None, number=None, pages_from=None, pages_to=None, series=None, publisher=None, isbn=None, doi=None, abstract=None, copyright=None, conference_id=None, source=None):
        if title and len(title) <= 250:
            title = self.__normalize_string(title)
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

    def parse(self, publication, conference_short_name=None, journal_name=None, authors=None, keywords=None, urls=None):
        '''
        
        :param publication: Publication dictonary
        :param conference_short_name: Conference short name
        :param journal_name: Journal name
        :param authors: Authors name array
        :param keywords: Keywords array
        :param urls: Url array
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
                except(DataError) as e:
                    logger.warn(str(e))
                del conference_short_name
            # journal
            if journal_name:
                try:
                    journal_id = self.parse_journal(journal_name)
                except(DataError) as e:
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
                        self.cursor.execute("INSERT INTO core_publicationauthoraffilation (publication_id, author_id) VALUES (%s, %s)", [publication_id, self.parse_author(author)])
                    except(ParserDataError) as e:
                        logger.warn(str(e))
                del authors
            # keywords
            if keywords:
                for keyword in keywords:
                    if keyword and len(keyword) <= 100:
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
            return publication_id
        except(ParserDataError) as e:
            #logger.warn(str(e))
            return False
        except(ProgrammingError, DataError) as e:
            logger.error(e, exc_info=True)
            self.conn.rollback()
            raise ParserRollbackError(str(e))
    
    """
        def check_author_name(self, name):
        try:
            # Milena Mihail, et al.
            name = name.strip().replace(', et al.', '')
            # block: n.n., S., Jr., A.
            if ' ' in name:
                # block: University, Università, Universität, Université
                if not any(extension in name for extension in ('Universit', 'et al.')):
                    return name
        except(AttributeError) as e:
            logger.warn(str(e))

        return False
    
    def _check_publication_is_valid(self, entry):
        return 'title' in entry and 'authors' in entry
    """
