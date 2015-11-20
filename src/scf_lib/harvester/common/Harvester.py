#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import getopt
import logging
import sys



def check_author_name(name):
    # block: n.n., S., Jr., A.
    if ' ' in name:
        # block: University, Università, Universität, Université
        if not any(extension in name for extension in ('Universit', 'et al.')):
            return True
    return False


class Harvester:
    
    PREFIX = ''
    LOG_PATH = '../log/'
    DOWNLOAD_PATH = '../downloads/'
    
    def __init__(self):
        self.init_logger()
        self.count_publications = 0
        self.split_publications = 10000
        self.limit = self.get_arguments(sys.argv[1:])
        self.logger.info('start')
    
    def init_logger(self):
        logging.basicConfig(
            filename=self.LOG_PATH+self.PREFIX+'_harvester.log',
            level=logging.DEBUG,
            format='[%(asctime)s] %(levelname)s [%(module)s] %(message)s'
        )
        self.logger = logging.getLogger()
        
    def get_arguments(self, argv):
        try:
            opts, args = getopt.getopt(argv, "hl:", ["help", "limit="])
        except getopt.GetoptError as e:
            print(str(e))
            print('Usage: -h for help')
            sys.exit(2)    
    
        limit = None
        for opt, arg in opts:
            if opt == '-h':
                print('Usage: my-process.py -s <start> -e <end>')
                sys.exit()
            elif opt in ("-l", "--limit"):
                limit = int(arg);
            else:
                raise Exception("unhandled option")
        return limit 
        
    def stop_harvest(self):
        self.f.close()
        self.logger.info('stop')
        
    def _write_element(self, element, value):
        if value:
            self.f.write("\t<%s>%s</%s>\n" % (element, value, element))
        
    def parse_publication(self, title=None, authors=None, date=None, booktitle=None, journal=None, volume=None, number=None, pages=None, publisher=None, abstract=None, doi=None, citeseerx_id=None, dblp_id=None, extractor=None, source=None):
    
        if title and authors:

            if self.count_publications % self.split_publications == 0:
                filename = self.DOWNLOAD_PATH+'harvester/{}/publication-{}.xml'.format(self.PREFIX, self.count_publications / self.split_publications)
                self.f = codecs.open(filename, 'w+', 'utf-8')               
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
                    self.logger.warn("Not an author name: %s" % author)
            
            self.f.write("</publication>\n")
            return True
        else:
            self.logger.warn("No title (%s) or authors" % title)
            #print('no title or authors')
            return False
