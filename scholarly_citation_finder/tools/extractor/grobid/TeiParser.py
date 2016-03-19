import logging
from lxml import etree
from io import BytesIO

logger = logging.getLogger(__name__)


class TeiParserNoDocumentTitle(Exception):
    pass


class TeiParserNoReferences(Exception):
    pass


class TeiParser:
    
    ELEMENT_TEIHEADER = 'teiheader'
    ELEMENT_BODY = 'body'
    ELEMENT_BIBLSTRUCT = 'biblstruct'

    def __init__(self, name=''):
        self.name = name
        
    def parse_document(self, xml):
        '''
        
        :param xml:
        :return: Document meta object, References list
        :raise TeiParserNoReferences: Document has no references
        :raise TeiParserNoDocumentTitle: Document has no title
        '''
        try:
            result = self.__parse(xml, end_element=self.ELEMENT_TEIHEADER)
            return result[0], result[1:]
        except(IndexError) as e:
            raise TeiParserNoReferences()
        except(TeiParserNoDocumentTitle) as e:
            raise e

    """
    def parse_header(self, xml):
        '''
        <TEI>
            <teiHeader>
                ...
                
        :param xml:
        :raise TeiParserNoDocumentTitle
        '''
        try:
            results = self.__parse(xml, end_element=self.ELEMENT_TEIHEADER) 
            return results[0]
        except(TeiParserNoDocumentTitle) as e:
            raise e
    """

    def parse_references(self, xml):
        '''
        <TEI>
            <text>
                <back>
                    <div type="references">
                        <listBibl>
                            ...
        
        :param xml:
        '''
        return self.__parse(xml, end_element=self.ELEMENT_BIBLSTRUCT)
    
    def __parse(self, xml, end_element):
        '''
        
        :param xml:
        :param end_element:
        :raise TeiParserNoDocumentTitle: 
        '''
        results = []
        context = etree.iterparse(BytesIO(xml), html=True)
        
        publication = {}
        journal_name = None
        conference_instance_name = None
        authors = []
        tmp_author_name = None
        keywords = []
        
        for _, elem in context:
            if elem.tag == 'html':  # skipped add html (html=True option)
                continue
            # Extract teiHeader / biblstruct
            elif end_element in (self.ELEMENT_TEIHEADER, self.ELEMENT_BIBLSTRUCT):
                if elem.tag == 'forename':
                    if tmp_author_name is None:
                        tmp_author_name = elem.text
                    else:
                        tmp_author_name += ' '+elem.text
                elif elem.tag == 'surname':
                    if tmp_author_name is None:
                        tmp_author_name = elem.text
                    else:
                        tmp_author_name = elem.text + ',' + tmp_author_name
                elif elem.tag == 'author':
                    authors.append(tmp_author_name)
                    tmp_author_name = None
                elif elem.tag == 'title' and elem.text and 'level' in elem.attrib:
                    level = elem.attrib.get('level')
                    # @see http://www.tei-c.org/release/doc/tei-p5-doc/de/html/ref-title.html
                    if elem.attrib.get('type') == 'main' and 'title' not in publication:
                        #if elem.attrib.get('level') in ('a', 'm'):
                        publication['title'] = elem.text
                    elif level == 'j':
                        journal_name = elem.text
                    elif level == 'b':
                        publication['booktitle'] = elem.text
                    elif level == 'm':
                        conference_instance_name = elem.text
                    else:
                        logger.warn('Unknown title with level %s: %s' % (level, elem.text))
                    # else: 's', 'u'
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
                        publication['year'] = elem.attrib['when']
                elif elem.tag == 'publisher':
                    publication['publisher'] = elem.text
                elif elem.tag == 'note':
                    publication['copyright'] = elem.text
                elif elem.tag == 'term' and elem.text:
                    keywords.append(elem.text)
                # citation ('biblstruct') or document header ('teiheader')
                elif elem.tag == end_element:
                    if 'title' in publication:
                        publication['source'] = self.name

                        results.append({'reference': {
                                            'publication_id': '',
                                            'source_id': '',
                                            'context': elem.attrib.get('xml:id')
                                        },
                                       'publication': publication.copy(),
                                       'journal_name': journal_name,
                                       'conference_instance_name': conference_instance_name,
                                       'authors': authors,
                                       'keywords': keywords})
                    else:
                        if end_element == self.ELEMENT_TEIHEADER:
                            raise TeiParserNoDocumentTitle('No document title detected')
                        else:
                            logger.info('skip, no title found')                            
                    # TODO: improve (idea: header read, move on to references)   
                    if end_element == self.ELEMENT_TEIHEADER:
                        end_element = self.ELEMENT_BODY
                    
                    publication.clear()
                    journal_name = None
                    conference_instance_name = None
                    authors = []
                    tmp_author_name = ''
                    keywords = []
            # Skip text body
            elif elem.tag == end_element:
                end_element = self.ELEMENT_BIBLSTRUCT

            # Clear
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context
        return results
