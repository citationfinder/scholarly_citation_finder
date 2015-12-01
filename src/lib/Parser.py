#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from config import LOG_PATH
from .XmlFileWriter import XmlFileWriter

class Parser(object):
    
    MAIN_TAG = 'sfc'    

    def __init__(self, name):
        self.name = name
        self.init_logger(name)
        self.count_publications = 0
        self.count_citations = 0
        self.output = XmlFileWriter()
        
    def init_logger(self, name):
        logging.basicConfig(
            filename=LOG_PATH+name+'.log',
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
        self.output.open(filename)
        self.output.write_declaration()
        self.output.write_start_tag(self.MAIN_TAG)
    
    def close_output_file(self):
        self.output.write_close_tag(self.MAIN_TAG)
        self.output.close()
    
    def parse_citation(self, context=None, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, extractor=None, source=None):
        self.count_citations += 1
        
        self.output.write_start_tag('citation')
        self.output.write_element('context', context)
        self.parse_publication(title, authors, date, booktitle, journal, volume, number, pages, publisher, abstract, doi, citeseerx_id, dblp_id, extractor, source)
        self.output.write_end_tag('citation')

    def parse_publication(self, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, extractor=None, source=None):
    
        if title and authors:

            self.count_publications += 1
                
            #if date and pages and (booktitle or (journal and volume)):
            self.output.write_start_tag('publication')
            self.output.write_element('title', title)
            self.output.write_element('date', date)
            self.output.write_element('booktitle', booktitle)            
            self.output.write_element('journal', journal)
            self.output.write_element('volume', volume)
            self.output.write_element('pages', pages)
            self.output.write_element('number', number)
            self.output.write_element('publisher', publisher)
            self.output.write_element('abstract', abstract)
            self.output.write_element('doi', doi)
            self.output.write_element('citeseerx_id', citeseerx_id)
            self.output.write_element('dblp_id', dblp_id)
            self.output.write_element('extractor', extractor)
            self.output.write_element('source', source)

            for author in authors:
                author = self.check_author_name(author)
                if author:
                    self.output.write_element('author', author)
                else:
                    self.logger.warn("Not an author name: %s" % author)
            
            self.output.write_close_tag("publication")
            return True
        else:
            self.logger.warn("No title (%s) or authors" % title)
            #print('no title or authors')
            return False