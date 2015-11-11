from lxml import etree
from unidecode import unidecode
from search_for_citations.models import Publication

import os.path
import logging
logger = logging.getLogger()

class DblpHarvester:
    
    # Available elements are:   article|inproceedings|proceedings|book|incollection|phdthesis|mastersthesis|www
    # Available tags are:       author|editor|title|booktitle|pages|year|address|journal|volume|number|month|url|ee|cdrom|cite|
    #                           publisher|note|crossref|isbn|series|school|chapter
    COLLABORATIONS = [u'www', u'phdthesis', u'inproceedings', u'incollection', u'proceedings', u'book', u'mastersthesis', u'article']
    
    def harvest(self, filename):
        if os.path.isfile(filename):
            logger.debug('Start')
            context = etree.iterparse(filename, load_dtd=True, html=True)
            self.fast_iter(context)
            logger.debug('End')
        else:
            raise IOError
            

    """
    @see: https://github.com/Ajeo/dblp-to-csv/blob/master/parser.py

    @func: fast_iter
    @param context : iterparsed (chunk of xml) data
    @param func : handler
    @desc: Read xml chunk. After read, clear and delete chunk to release memory.
            Also, replace html encoding to similar ascii code
    """
    def fast_iter(self, context, *args, **kwargs):
        #xml categories
        title = ''
        author_array = []
        #abstract = ''
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
                publication = Publication(
                    type=elem.tag,
                    title=title,
                    date=date,
                    journal=journal,
                    volume=volume,
                    number=number,
                    pages=pages,
                    source=source,
                    dblp_id=elem.get('key'))
                publication.save()
                
                for author in author_array:
                    publication.authors.create(last_name=author)
                    
                del author_array[:]
     
            # Clear element
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context
        #clear chunks