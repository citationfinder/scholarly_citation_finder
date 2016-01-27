import os.path
from lxml import etree

from ..Harvester import Harvester


class DblpHarvester(Harvester):
    
    COLLABORATIONS = [
        'article',
        'inproceedings',
        'proceedings',
        'book',
        'incollection',
        'phdthesis',
        'mastersthesis',
        'www'
    ]

    # Furher avaible tags:  address|month|url|cdrom|cite|note|crossref|school|chapter
    FIELD_MAPPING = {
        'title': 'title',
        'author': 'authors',
        'editor': 'authors',
        'year': 'date',
        'booktitle': 'booktitle',
        'journal': 'journal',
        'volume': 'volume',
        'number': 'number',
        #pages
        'series': 'series',
        'publisher': 'publisher',
        'isbn': 'isbn',
        # doi
        # abstract
        'ee': 'urls'
    }
    
    def __init__(self, **kwargs):
        super(DblpHarvester, self).__init__('dblp', **kwargs)
    
    def harvest(self, filename, limit=None):
        if limit:
            self.limit = int(limit)
        else:
            self.limit = None
            
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
    @desc: Read xml chunk. After read, clear and delete chunk to release memory.
            Also, replace html encoding to similar ascii code
    """
    def _fast_iter(self, context):
        result_entry = {}
        
        #read chunk line by line
        #we focus author and title
        for _, elem in context:
            if elem.tag == 'html' or elem.tag == 'body':
                continue
            # title
            elif elem.tag == 'title' and elem.text:
                title = elem.text
                if title.endswith('.'):
                    title = title[:-1]
                result_entry[self.FIELD_MAPPING[elem.tag]] = title
            # author and editor
            elif elem.tag in ('author', 'editor') and elem.text:
                field = self.FIELD_MAPPING['author']
                if field not in result_entry:
                    result_entry[field] = []
                result_entry[field].append(elem.text)
            # pages
            elif elem.tag == 'pages' and elem.text:
                pages = elem.text.split('-')
                result_entry['pages_from'] = pages[0]
                if len(pages) > 1:
                    result_entry['pages_to'] = pages[1]
            # ee
            elif elem.tag == 'ee' and elem.text:
                field = self.FIELD_MAPPING['ee']
                if field not in result_entry:
                    result_entry[field] = []
                result_entry[field].append(elem.text)

                if 'http://dx.doi.org/' in elem.text:
                    result_entry['doi'] = elem.text.replace('http://dx.doi.org/', '')
            # other
            elif elem.tag in self.FIELD_MAPPING and elem.text:
                result_entry[self.FIELD_MAPPING[elem.tag]] = elem.text
            # collaboration
            elif elem.tag in self.COLLABORATIONS:
                self.open_split_file()
                
                result_entry['type'] = elem.tag
                result_entry['dblp_id'] = elem.get('key')

                # store and clear entry afterwards
                self.parse_publication2(result_entry, check_author=False)
                result_entry.clear()
                
                # Check, if break harvest loop
                if self.check_stop_harvest():
                    break
     
            # Clear element
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context
        # clear chunks
