#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import logging
logging.basicConfig(
    filename='../log/harvester.log',
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s] %(message)s'
)
logger = logging.getLogger()

def check_author_name(name):
    # block: n.n., S., Jr., A.
    if ' ' in name:
        # block: University, Università, Universität, Université
        if not any(extension in name for extension in ('Universit', 'et al.')):
            return True
    return False

class Harvester:
    
    PREFIX = ''
    
    def __init__(self):
        logger.info('start')
        self.count_publications = 0
        self.split_publications = 10000
        
    def stop_harvest(self):
        self.f.close()
        logger.info('stop')
        
    def _write_element(self, element, value):
        if value:
            self.f.write("\t<%s>%s</%s>\n" % (element, value, element))
        
    def parse_publication(self, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, extractor=None, source=None):
    
        if title and authors:

            if self.count_publications % self.split_publications == 0:
                filename = '../downloads/harvester/{}/publication-{}.xml'.format(self.PREFIX, self.count_publications / self.split_publications)
                self.f = codecs.open(filename, 'w+', 'utf8')               
                #self.f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
                
            self.count_publications += 1
                
            #if date and pages and (booktitle or (journal and volume)):
            self.f.write("<publication>\n")
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
                if check_author_name(author):
                    self._write_element('author', author)
                else:
                    logger.warn("Not an author name: %s" % author)
            
            self.f.write("</publication>\n")
            return True
        else:
            logger.warn("No title (%s) or authors" % title)
            #print('no title or authors')
            return False
