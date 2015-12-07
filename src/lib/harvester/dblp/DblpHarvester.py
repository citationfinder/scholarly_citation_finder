import os.path
from lxml import etree

import config
from ..common.Harvester import Harvester

class DblpHarvester(Harvester):
    
    def __init__(self):
        super(DblpHarvester, self).__init__('dblp')
    
    # Available elements are:   article|inproceedings|proceedings|book|incollection|phdthesis|mastersthesis|www
    # Available tags are:       author|editor|title|booktitle|pages|year|address|journal|volume|number|month|url|ee|cdrom|cite|
    #                           publisher|note|crossref|isbn|series|school|chapter
    COLLABORATIONS = [u'article', u'www', u'phdthesis', u'inproceedings', u'incollection', u'proceedings', u'book', u'mastersthesis']
    
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
        booktitle = ''
        journal = ''
        volume = ''
        number = ''
        source = ''
        pages = ''
        doi = ''
    
        #read chunk line by line
        #we focus author and title
        for event, elem in context:
            if elem.tag == 'html' or elem.tag == 'body':
                continue
            elif elem.tag == 'author' and elem.text:
                author_array.append(elem.text)
            elif elem.tag == 'title' and elem.text:
                title = elem.text
            elif elem.tag == 'year' and elem.text:
                date = elem.text
            elif elem.tag == 'booktitle' and elem.text:
                booktitle = elem.text
            elif elem.tag == 'journal' and elem.text:
                journal = elem.text
            elif elem.tag == 'volume' and elem.text:
                volume = elem.text
            elif elem.tag == 'number' and elem.text:
                number = elem.text
            elif elem.tag == 'pages' and elem.text:
                pages = elem.text
            elif elem.tag == 'ee' and elem.text:
                if 'http://dx.doi.org/' in elem.text:
                    doi = elem.text.replace('http://dx.doi.org/', '')
                else: # TODO: used?
                    source = elem.text
    
            elif elem.tag in self.COLLABORATIONS:
                self.open_split_file()
                self.parse_publication(
                    type=elem.tag,
                    title=title,
                    authors=author_array,
                    date=date,
                    booktitle=booktitle,
                    journal=journal,
                    volume=volume,
                    pages=pages,
                    number=number,
                    doi=doi,
                    dblp_id=elem.get('key'),
                    source=source
                )
                del author_array[:]
                
                title = ''
                date = ''
                booktitle = ''
                journal = ''
                volume = ''
                number = ''
                source = ''
                pages = ''
                doi = ''
                
                # Check, if break harvest loop
                if self.check_stop_harvest():
                    break
     
            # Clear element
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context
        #clear chunks