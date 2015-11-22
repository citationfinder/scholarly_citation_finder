#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import logging
from config import LOG_PATH

class Parser(object):
    
    def __init__(self, name):
        self.name = name
        self.init_logger(name)
        self.count_publications = 0
        
    def init_logger(self, name):
        logging.basicConfig(
            filename=LOG_PATH+name+'.log',
            level=logging.DEBUG,
            format='[%(asctime)s] %(levelname)s [%(module)s] %(message)s'
        )
        self.logger = logging.getLogger()      
    
    def _write_element(self, element, value):
        if value:
            self.output.write("\t<%s>%s</%s>\n" % (element, value, element))

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
        try:
            self.output = codecs.open(filename, 'w+', 'utf-8')
        except(IOError) as e:
            raise IOError('Path to file {} not found: {}'.format(filename, e))                  
    
    def close_output_file(self):
        self.output.close()
    
    def parse_publication(self, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, extractor=None, source=None):
    
        if title and authors:

            self.count_publications += 1
                
            #if date and pages and (booktitle or (journal and volume)):
            self.output.write("<publication>\n")
            self._write_element('title', title)
            self._write_element('date', date)
            self._write_element('booktitle', booktitle)            
            self._write_element('journal', journal)
            self._write_element('volume', volume)
            self._write_element('pages', pages)
            self._write_element('number', number)
            self._write_element('publisher', publisher)
            self._write_element('abstract', abstract)
            self._write_element('doi', doi)
            self._write_element('citeseerx_id', citeseerx_id)
            self._write_element('dblp_id', dblp_id)
            self._write_element('extractor', extractor)
            self._write_element('source', source)

            for author in authors:
                author = self.check_author_name(author)
                if author:
                    self._write_element('author', author)
                else:
                    self.logger.warn("Not an author name: %s" % author)
            
            self.output.write("</publication>\n")
            return True
        else:
            self.logger.warn("No title (%s) or authors" % title)
            #print('no title or authors')
            return False