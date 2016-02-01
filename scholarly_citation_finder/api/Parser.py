#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2
from psycopg2._psycopg import DataError, ProgrammingError, IntegrityError

from scholarly_citation_finder.settings.development import DATABASES
from Process import Process

class ParserDataError(Exception):
    pass

class ParserRollbackError(Exception):
    pass

class ParserConnectionError(Exception):
    pass

class Parser(Process):
    
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

    def __init__(self, name):
        super(Parser, self).__init__(name)
        self.conn = self.get_database_connection(name)
        self.cursor = self.conn.cursor()
        self.count_publications = 0
        #self.count_citations = 0
        self.logger.info('start -------------------')

    def get_database_connection(self, name='default'):
        db = DATABASES[name]
        return psycopg2.connect(host=db['HOST'],
                                dbname=db['NAME'],
                                user=db['USER'],
                                password=db['PASSWORD'])

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
            self.logger.info('commit')
            self.conn.commit()
        except(IntegrityError) as e:
            self.logger.error(e, exc_info=True)
            self.conn.rollback()
            raise ParserRollbackError               

    def parse_author(self, name):
        '''
        If the author with the given name already exists, the ID of that author is returned.
        Otherwise a new author gets created.
        
        :param name: Name of the author
        :return: ID of the author
        :raise DataError: When the name is too long
        '''
        self.cursor.execute("SELECT id FROM core_author WHERE name = %s LIMIT 1", (name,))
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            if name and len(name) <= 100:
                self.cursor.execute("INSERT INTO core_author (name) VALUES (%s) RETURNING id", (name,))
                return self.cursor.fetchone()[0]
            else:
                raise ParserDataError('Author name is too long')

    def parse_journal(self, name):
        '''
        If the journal with the given name already exists, the ID of that journal is returned.
        Otherwise a new journel gets created.
        
        :param name: Name of the journal
        :return: ID of the journal
        :raise DataError: When the name is too long
        '''
        self.cursor.execute("SELECT id FROM core_journal WHERE name = %s LIMIT 1", (name,))
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            if name and len(name) <= 250:
                self.cursor.execute("INSERT INTO core_journal (name) VALUES (%s) RETURNING id", (name,))
                return self.cursor.fetchone()[0]
            else:
                raise ParserDataError('Journal name is too long')

    def parse_publication(self, type=None, title=None, year=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages_from=None, pages_to=None, series=None, publisher=None, isbn=None, doi=None, abstract=None, copyright=None, conference=None, source=None):
        if title and len(title) <= 250:
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
            self.cursor.execute("INSERT INTO core_publication (type, title, year, date, booktitle, journal_id, volume, number, pages_from, pages_to, series, publisher, isbn, doi, abstract, copyright, conference_id, source) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id", (type, title, year, date, booktitle, journal, volume, number, pages_from, pages_to, series, publisher, isbn, doi, abstract, copyright, conference, source))
            return self.cursor.fetchone()[0]
        else:
            raise ParserDataError('Title does not exists or is too long')

    def parse(self, publication, journal=None, authors=None, keywords=None, urls=None):
        '''
        
        :param publication: Publication dictonary
        :param journal: Journal name
        :param authors: Authors name array
        :param keywords: Keywords array
        :param urls: Url array
        :return: True, if entry was successfully parsed
        :raise ParserRollbackError: When a problems occurred, that required to do a rollback
        '''
        
        self.count_publications += 1
        try:
            
            if journal:
                try:
                    journal = self.parse_journal(journal)
                except(DataError) as e:
                    journal = None
                    self.logger.warn(str(e))

            publication_id = self.parse_publication(journal=journal,
                                                    **publication)
            if authors:
                for author in authors:
                    try:
                        self.cursor.execute("INSERT INTO core_publicationauthoraffilation (publication_id, author_id) VALUES (%s, %s)", (publication_id, self.parse_author(author)))
                    except(DataError) as e:
                        self.logger.warn(str(e))
            if keywords:
                for keyword in keywords:
                    if keyword and len(keyword) <= 100:
                        self.cursor.execute("INSERT INTO core_publicationkeyword (publication_id, name) VALUES (%s, %s)", (publication_id, keyword))
            if urls:
                for url in urls:
                    url_type = None
                    if isinstance(url, dict):
                        url_type = url['type']
                        url = url['value']
                        
                    if url and len(url) <= 200:
                        if url_type and len(url_type) >= 30:
                            url_type = None
                        self.cursor.execute("INSERT INTO core_publicationurl (publication_id, url, type) VALUES (%s, %s, %s)", (publication_id, url, url_type))

            return True
        except(ParserDataError) as e:
            #self.logger.warn(str(e))
            return False
        except(ProgrammingError, DataError) as e:
            self.logger.error(e, exc_info=True)
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
            self.logger.warn(str(e))

        return False
    
    def _check_publication_is_valid(self, entry):
        return 'title' in entry and 'authors' in entry
    
    def parse_publication(self, type=None, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, arxiv_id=None, extractor=None, source=None):
    
        if title and authors:

            self.count_publications += 1
                
            #if date and pages and (booktitle or (journal and volume)):
            self.xml_writer.write_start_tag('publication')
            self.xml_writer.write_element('type', type)
            self.xml_writer.write_element('title', title)
            self.xml_writer.write_element('date', date)
            self.xml_writer.write_element('booktitle', booktitle)
            self.xml_writer.write_element('journal', journal)
            self.xml_writer.write_element('volume', volume)
            self.xml_writer.write_element('pages', pages)
            self.xml_writer.write_element('number', number)
            self.xml_writer.write_element('publisher', publisher)
            self.xml_writer.write_element('abstract', abstract, is_cdata=True)
            self.xml_writer.write_element('doi', doi)
            self.xml_writer.write_element('citeseerx_id', citeseerx_id)
            self.xml_writer.write_element('dblp_id', dblp_id)
            self.xml_writer.write_element('arxiv_id', arxiv_id)
            self.xml_writer.write_element('extractor', extractor)
            self.xml_writer.write_element('source', source)

            for author in authors:
                author = self.check_author_name(author)
                if author:
                    self.xml_writer.write_element('author', author)
                else:
                    self.logger.warn('Not an author name: %s' % author)
            
            self.xml_writer.write_close_tag('publication')
            return True
        else:
            self.logger.warn('No title (%s) or authors' % title)
            #print('no title or authors')
            return False
    """