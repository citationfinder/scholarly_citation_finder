#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import logging
import time

from scholarly_citation_finder import config
from ..core.models import Author, Journal, Publication
from django.db.utils import DataError

class Parser(object):
    
    PUBLICATION_ATTRIBUTES = [
        'type',
        'title',
        'date',
        'booktitle'
        'journal',
        'volume',
        'number',
        'pages_from',
        'pages_to',
        'series',
        'publisher',
        'isbn',
        'doi',
        'abstract',
        'copyright',
        'citeseerx_id',
        'dblp_id',
        'arxiv_id',
        'extractor'
    ]

    def __init__(self, name):
        self.name = name
        self.init_logger(name)
        self.count_publications = 0
        #self.count_citations = 0
        self.logger.info('start -------------------')

    def stop_harvest(self):
        self.logger.info('stop')
  
    def init_logger(self, name):
        logging.basicConfig(filename=os.path.join(config.LOG_DIR, name + '.log'),
                            level=logging.INFO,
                            format='[%(asctime)s] %(levelname)s [%(module)s] %(message)s')
        self.logger = logging.getLogger()
    
    #def parse_publication_reference(self, context=None, type=None, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, arxiv_id=None, extractor=None, source=None):
    #    self.count_citations += 1
    #    
    #    self.xml_writer.write_start_tag('reference')
    #    self.xml_writer.write_element('context', context, is_cdata=True)
    #    self.parse_publication(type, title, authors, date, booktitle, journal, volume, number, pages, publisher, abstract, doi, citeseerx_id, dblp_id, arxiv_id, extractor, source)
    #    self.xml_writer.write_close_tag('reference')

    #def _parse_publication_urls(self, urls):
    #    for url in urls:
    #        if isinstance(url, dict):
    #            self.xml_writer._write_line('<%s type="%s">%s</%s>' % ('url', url['type'], url['value'], 'url'))
    #        else:
    #            self.xml_writer.write_element('url', url)

    def check_stop_harvest(self):
        return self.limit and self.count_publications >= self.limit

    def parse_author(self, name):
        try:
            author = Author.objects.using(self.name).get(name=name)
        except(Author.DoesNotExist):
            author = Author(name=name)
            author.save()
        return author
    
    def parse_journal(self, name):
        try:
            journal = Journal.objects.using(self.name).get(name=name)
        except(Journal.DoesNotExist):
            journal = Journal(name=name)
            journal.save()
        return journal        

    def parse_publication(self, entry, check_author=True):
        self.count_publications += 1
        try:
            publication = Publication()
            
            for field in self.PUBLICATION_ATTRIBUTES:
                if field in entry:
                    setattr(publication, field, entry[field])
            
            publication.save(using=self.name)     
            
            if 'authors' in entry:
                for author in entry['authors']:
                    publication.authors.add(self.parse_author(author))
            #if 'keywords' in entry:
            #    for keyword in entry['keywords']:
            #        publication.ke
            #        self.xml_writer.write_element('keyword', keyword)
            if 'urls' in entry:
                for url in entry['urls']:
                    if isinstance(url, dict):
                        url_value = url.value
                        url_type = url.type
                    else:
                        url_value = url
                        url_type = ''
                    publication.publicationurl_set.create(url=url_value, type=url_type)
        except(DataError) as e:
            self.logger.warn(str(e))
        
        return True