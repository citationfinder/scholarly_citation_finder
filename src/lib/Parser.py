#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path
import logging

import config
from .XmlFileWriter import XmlFileWriter


class Parser(object):
    
    MAIN_TAG = 'sfc'

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
        self.count_citations = 0
        self.output = XmlFileWriter()
        
    def init_logger(self, name):
        logging.basicConfig(
            filename=os.path.join(config.LOG_DIR, name + '.log'),
            level=logging.DEBUG,
            format='[%(asctime)s] %(levelname)s [%(module)s] %(message)s'
        )
        self.logger = logging.getLogger()

    def check_author_name(self, name):
        # Milena Mihail, et al.
        name = name.strip().replace(', et al.', '')
        # block: n.n., S., Jr., A.
        if ' ' in name:
            # block: University, Università, Universität, Université
            if not any(extension in name for extension in ('Universit', 'et al.')):
                return name
        return False
    
    def open_output_file(self, filename):
        self.logger.debug('open output file: {}'.format(filename))
        self.output.open(filename)
        self.output.write_declaration()
        self.output.write_start_tag(self.MAIN_TAG)
    
    def close_output_file(self):
        self.output.write_close_tag(self.MAIN_TAG)
        self.output.close()
    
    def parse_citation(self, context=None, type=None, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, arxiv_id=None, extractor=None, source=None):
        self.count_citations += 1
        
        self.output.write_start_tag('citation')
        self.output.write_element('context', context, is_cdata=True)
        self.parse_publication(type, title, authors, date, booktitle, journal, volume, number, pages, publisher, abstract, doi, citeseerx_id, dblp_id, arxiv_id, extractor, source)
        self.output.write_close_tag('citation')

    def _check_publication_is_valid(self, entry):
        return 'title' in entry and 'authors' in entry

    def _parse_publication_urls(self, urls):
        for url in urls:
            if isinstance(url, dict):
                self.output._write_line('<%s type="%s">%s</%s>' % ('url', url['type'], url['value'], 'url'))
            else:
                self.output.write_element('url', url)

    def parse_publication2(self, entry, check_author=True):
        if not self._check_publication_is_valid(entry):
            #self.logger.warn("No title or authors")
            return False
        
        self.count_publications += 1
        self.output.write_start_tag('publication')
        for field in self.PUBLICATION_ATTRIBUTES:
            if field in entry:
                self.output.write_element(field, entry[field])
        if 'authors' in entry:
            for author in entry['authors']:
                if check_author:
                    author_parsed = self.check_author_name(author)
                    if author:
                        self.output.write_element('author', author_parsed)
                    else:
                        self.logger.warn('Not an author name: %s' % author)
                else:
                    self.output.write_element('author', author)
        if 'urls' in entry:
            self._parse_publication_urls(entry['urls'])
        
        self.output.write_close_tag('publication')
        return True

    def parse_publication(self, type=None, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, arxiv_id=None, extractor=None, source=None):
    
        if title and authors:

            self.count_publications += 1
                
            #if date and pages and (booktitle or (journal and volume)):
            self.output.write_start_tag('publication')
            self.output.write_element('type', type)
            self.output.write_element('title', title)
            self.output.write_element('date', date)
            self.output.write_element('booktitle', booktitle)
            self.output.write_element('journal', journal)
            self.output.write_element('volume', volume)
            self.output.write_element('pages', pages)
            self.output.write_element('number', number)
            self.output.write_element('publisher', publisher)
            self.output.write_element('abstract', abstract, is_cdata=True)
            self.output.write_element('doi', doi)
            self.output.write_element('citeseerx_id', citeseerx_id)
            self.output.write_element('dblp_id', dblp_id)
            self.output.write_element('arxiv_id', arxiv_id)
            self.output.write_element('extractor', extractor)
            self.output.write_element('source', source)

            for author in authors:
                author = self.check_author_name(author)
                if author:
                    self.output.write_element('author', author)
                else:
                    self.logger.warn('Not an author name: %s' % author)
            
            self.output.write_close_tag('publication')
            return True
        else:
            self.logger.warn('No title (%s) or authors' % title)
            #print('no title or authors')
            return False
