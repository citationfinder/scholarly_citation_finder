#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import psycopg2


from scholarly_citation_finder import config
from scholarly_citation_finder.settings.development import DATABASES
from Process import Process
from scholarly_citation_finder.apps.core.models import Author, Journal, Publication
from psycopg2._psycopg import DataError


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

    def stop_harvest(self):
        self.logger.info('stop')
  
    #def parse_publication_reference(self, context=None, type=None, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, arxiv_id=None, extractor=None, source=None):
    #    self.count_citations += 1
    #    
    #    self.xml_writer.write_start_tag('reference')
    #    self.xml_writer.write_element('context', context, is_cdata=True)
    #    self.parse_publication(type, title, authors, date, booktitle, journal, volume, number, pages, publisher, abstract, doi, citeseerx_id, dblp_id, arxiv_id, extractor, source)
    #    self.xml_writer.write_close_tag('reference')

    def check_stop_harvest(self):
        return self.limit and self.count_publications >= self.limit

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
            if len(name) <= 100:
                self.cursor.execute("INSERT INTO core_author (name) VALUES (%s) RETURNING id", (name,))
                return self.cursor.fetchone()[0]
            else:
                raise DataError

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
            if len(name) <= 250:
                self.cursor.execute("INSERT INTO core_journal (name) VALUES (%s) RETURNING id", (name,))
                return self.cursor.fetchone()[0]
            else:
                raise DataError
    def parse_publication(self, entry):
        self.count_publications += 1
        try:
            if 'journal' in entry:
                try:
                    entry['journal'] = self.parse_author(entry['journal'])
                except(DataError) as e:
                    self.logger.warn(e, exc_info=True)                
                    del entry['journal']

            fields = ''
            values = ''
            for field in self.PUBLICATION_ATTRIBUTES:
                if field in entry:
                    fields += ", " + field
                    values += ", '"+entry[field]+"'"

            fields = fields[2:]
            values = values[2:]
            
            print(fields)
            print(values)
            
            query = "INSERT INTO core_publication ("+fields+") VALUES ("+values+") RETURNING id"
            self.logger.info(query)
            self.cursor.execute(query)
            publication_id = self.cursor.fetchone()[0]
                        
            if 'authors' in entry:
                for author in entry['authors']:
                    try:
                        self.cursor.execute("INSERT INTO core_publicationauthoraffilation (publication_id, author_id) VALUES (%s, %s)", (publication_id, self.parse_author(author)))
                    except(DataError) as e:
                        self.logger.warn(e, exc_info=True)
            if 'keywords' in entry:
                for keyword in entry['keywords']:
                    try:
                        if len(keyword) <= 100:
                            self.cursor.execute("INSERT INTO core_publicationurl (publication_id, name) VALUES (%s, %s)", (publication_id, keyword))
                    except(DataError) as e:
                        self.logger.warn(e, exc_info=True)
            if 'urls' in entry:
                for url in entry['urls']:
                    url_type = None
                    if isinstance(url, dict):
                        url_type = url.type
                        url = url.value
                        
                    try:
                        if len(url) <= 200:
                            self.cursor.execute("INSERT INTO core_publicationurl (publication_id, url, type) VALUES (%s, %s, %s)", (publication_id, url, url_type))
                    except(DataError) as e:
                        self.logger.warn(e, exc_info=True)
        except(Exception) as e:
            self.logger.warn(e, exc_info=True)
            return False
        
        return True
    
    
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