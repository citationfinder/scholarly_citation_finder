from lxml import etree
from io import BytesIO


class CiteseerParser:
    '''
    Parser to the CiteSeerExtractor output.
    '''
    
    def __init__(self, name=''):
        '''
        Create object.
        
        :param name: Parser name
        '''
        self.name = name

    def parse(self, xml):
        '''
        Parse output
        
        :param xml: XML
        '''
        context = etree.iterparse(BytesIO(xml), html=False)
        return self.fast_iter(context)

    def _escape_text(self, text):
        # TODO: .replace('&', '&amp;') destroys other symbols like "&lt;", which are already escaped
        return text.replace('<', '&lt;').replace('>', '&gt;')

    def fast_iter(self, context):
        results = []
        
        publication = {}
        journal_name = None
        authors = []
        
        for _, elem in context:
            if elem.tag == 'author':
                authors.append(self._escape_text(elem.text))
            elif elem.tag == 'title' and elem.text:
                publication['title'] = self._escape_text(elem.text)
            elif elem.tag == 'date' and elem.text:
                publication['date'] = self._escape_text(elem.text)            
            elif elem.tag == 'booktitle' and elem.text:
                publication['booktitle'] = self._escape_text(elem.text)
            elif elem.tag == 'journal' and elem.text:
                journal_name = self._escape_text(elem.text)
            elif elem.tag == 'volume' and elem.text:
                publication['volume'] = self._escape_text(elem.text)
            elif elem.tag == 'pages' and elem.text:
                publication['pages'] = self._escape_text(elem.text)
            #elif elem.tag == 'context' and elem.text:
            #    publication['context'] = self._escape_text(elem.text)                        

            # citation
            elif elem.tag == 'reference':
                
                if 'title' in publication:
                    publication['source'] = self.name
    
                    results.append({'reference': {
                                        'publication_id': '',
                                        'source_id': '',
                                        'context': ''
                                    },
                                   'publication': publication.copy(),
                                   'journal_name': journal_name,
                                   'authors': authors })

                publication.clear()
                journal_name = None
                authors = []

            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context
        #print(results)
        return results
