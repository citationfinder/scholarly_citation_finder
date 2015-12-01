import os.path
from lxml import etree
#from unidecode import unidecode
#from core.models import Publication

import config
from ..common.Harvester import Harvester

#import logging
#logger = logging.getLogger()

DOWNLOAD_PATH = 'downloads/'

class DblpHarvester(Harvester):
    
    def __init__(self):
        super(DblpHarvester, self).__init__('dblp')
    
    # Available elements are:   article|inproceedings|proceedings|book|incollection|phdthesis|mastersthesis|www
    # Available tags are:       author|editor|title|booktitle|pages|year|address|journal|volume|number|month|url|ee|cdrom|cite|
    #                           publisher|note|crossref|isbn|series|school|chapter
    COLLABORATIONS = [u'www', u'phdthesis', u'inproceedings', u'incollection', u'proceedings', u'book', u'mastersthesis', u'article']
    
    def harvest(self, filename):
        if os.path.isfile(filename):
            context = etree.iterparse(filename, load_dtd=True, html=True)
            self._fast_iter(context)
            self.stop_harvest()
        else:
            raise IOError('File {} not found'.format(filename))
            

    """
    @see: https://github.com/Ajeo/dblp-to-csv/blob/master/parser.py

    @func: fast_iter
    @param context : iterparsed (chunk of xml) data
    @param func : handler
    @desc: Read xml chunk. After read, clear and delete chunk to release memory.
            Also, replace html encoding to similar ascii code
    """
    def _fast_iter(self, context, *args, **kwargs):
        title = ''
        author_array = []
        date = ''
        journal = ''
        volume = ''
        number = ''
        source = ''
        pages = ''
    
        #read chunk line by line
        #we focus author and title
        for event, elem in context:
            if elem.tag == 'html' or elem.tag == 'body':
                continue
            
            if elem.tag == 'author':
                author_array.append(elem.text)
    
            elif elem.tag == 'title':
                if elem.text:
                    title = elem.text
            elif elem.tag == 'year':
                if elem.text:
                    date = elem.text
                    
            elif elem.tag == 'journal':
                if elem.text:
                    journal = elem.text

            elif elem.tag == 'volume':
                if elem.text:
                    volume = elem.text

            elif elem.tag == 'number':
                if elem.text:
                    number = elem.text

            elif elem.tag == 'pages':
                if elem.text:
                    pages = elem.text

            elif elem.tag == 'ee':
                if elem.text:
                    source = elem.text
    
            elif elem.tag in self.COLLABORATIONS:
                self.open_split_file()
                self.parse_publication(
                    title=title,
                    authors=author_array,
                    date=date,
                    journal=journal,
                    volume=volume,
                    pages=pages,
                    number=number,
                    dblp_id=elem.get('key'),
                    source=source
                )
                del author_array[:]
                
                # Check, if break harvest loop
                if self.check_stop_harvest():
                    break
     
            # Clear element
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context
        #clear chunks
        
if __name__ == '__main__':
    harvester = DblpHarvester()
    harvester.harvest(DOWNLOAD_PATH+'dblp/dblp.xml')