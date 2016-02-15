from lxml import etree
from io import BytesIO


class TeiParser:
    
    def __init__(self, name=''):
        self.name = name

    def parse(self, xml, callback_biblstruct):
        context = etree.iterparse(BytesIO(xml), html=True)
        self.fast_iter(context, callback_biblstruct)
      
    def fast_iter(self, context, callback_biblstruct):
        publication = {}
        journal_name = None
        authors = []
        tmp_author_name = ''
        
        for _, elem in context:
            if elem.tag == 'forename':
                tmp_author_name += elem.text
            elif elem.tag == 'surname':
                tmp_author_name = elem.text + ',' + tmp_author_name
            elif elem.tag == 'author':
                authors.append(tmp_author_name)
                tmp_author_name = ''
            elif elem.tag == 'title' and 'level' in elem.attrib:
                # @see http://www.tei-c.org/release/doc/tei-p5-doc/de/html/ref-title.html
                if elem.attrib['level'] == 'a':
                    publication['title'] = elem.text
                elif elem.attrib['level'] == 'j':
                    journal_name = elem.text
                elif elem.attrib['level'] == 'b':
                    publication['booktitle'] = elem.text
            elif elem.tag == 'biblscope' and 'unit' in elem.attrib:
                if elem.attrib['unit'] == 'volume':
                    publication['volume'] = elem.text
                elif elem.attrib['unit'] == 'issue':
                    publication['number'] = elem.text
                elif elem.attrib['unit'] == 'page':
                    publication['pages_from'] = elem.attrib.get('from')
                    publication['pages_to'] = elem.attrib.get('to')
            elif elem.tag == 'date' and 'when' in elem.attrib:
                if 'type' in elem.attrib and elem.attrib['type'] == 'published':
                    publication['date'] = elem.attrib['when']
            elif elem.tag == 'publisher':
                publication['publisher'] = elem.text

            # citation
            elif elem.tag == 'biblstruct':
                publication['source'] = self.name
                
                callback_biblstruct(
                    context=elem.attrib.get('xml:id'),
                    publication=publication,
                    journal_name=journal_name,
                    authors=authors,
                )
                
                publication.clear()
                journal_name = None
                authors = []
                tmp_author_name = ''

            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context
